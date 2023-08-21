import json
import os
import tempfile
import warnings
from pathlib import Path

import bioc
from bioc import BioCSentence, BioCPassage, BioCCollection, BioCDocument
from transformers import HfArgumentParser, TrainingArguments

from robust_deid.ner_datasets import DatasetCreator
from robust_deid.sequence_tagging import SequenceTagger
from robust_deid.sequence_tagging.arguments import (
    ModelArguments,
    DataTrainingArguments,
    EvaluationArguments,
)
from robust_deid.deid import TextDeid
from typing import List, Iterable, Dict, Union, Tuple

from medtext_commons.core import BioCProcessor


NOTE_ID_KEY = 'note_id'
METADATA_KEY = 'meta'
# TOKENS_KEY = 'tokens'
# NOTATION = 'BILOU'
PREDICTIONS_KEY = 'predictions'
TEXT_KEY = 'text'


class TextDatasetCreator(DatasetCreator):
    def create_from_memory(
            self,
            notes: List[Dict],
            mode: str = 'predict',
            notation: str = 'BIO',
            token_text_key: str = 'text',
            metadata_key: str = 'meta',
            note_id_key: str = 'note_id',
            label_key: str = 'labels',
            span_text_key: str = 'spans'
    ) -> Iterable[Dict[str, Union[List[Dict[str, Union[str, int]]], List[str]]]]:
        for note in notes:
            note_text = note[token_text_key]
            note_id = note[metadata_key][note_id_key]
            # Skip to next note if empty string
            if not note_text:
                continue

            if mode == 'train':
                note_spans = note[span_text_key]
            elif mode == 'predict':
                note_spans = None
            else:
                raise ValueError("Invalid mode - can only be train/predict")
            sent_tokens = [sent_tok for sent_tok in self._dataset.get_tokens(
                text=note_text,
                spans=note_spans,
                notation=notation
            )]
            for _, ner_sentence in self._sentence_dataset.get_sentences(
                    sent_tokens=sent_tokens,
                    token_text_key=token_text_key,
                    label_key=label_key
            ):
                current_sent_info = ner_sentence['current_sent_info']
                note_sent_info_store = {'start': current_sent_info[0]['start'],
                                        'end': current_sent_info[-1]['end'],
                                        'note_id': note_id}
                ner_sentence['note_sent_info'] = note_sent_info_store
                yield ner_sentence


class BioCRobustDeid(BioCProcessor):
    def __init__(self, model_config: str = None, repl: str = 'X'):
        super(BioCRobustDeid, self).__init__('deid:robust')
        self.repl = repl
        if len(repl) != 1:
            raise ValueError('The replacement repl cannot have more than one '
                             'char: %s' % repl)

        if model_config is None:
            model_config = os.path.join(os.path.dirname(__file__),
                                        'predict_i2b2_medtext.json')

        with open(model_config) as fp:
            config = json.load(fp)
        self.NOTATION = config['notation']
        self.TOKENS_KEY = config['text_column_name']

        # Create the dataset creator object
        self.dataset_creator = TextDatasetCreator(
            sentencizer='en_core_sci_sm',
            tokenizer='clinical',
            max_tokens=128,
            max_prev_sentence_token=32,
            max_next_sentence_token=32,
            default_chunk_size=32,
            ignore_label='NA'
        )

        parser = HfArgumentParser((
            ModelArguments,
            DataTrainingArguments,
            EvaluationArguments,
            TrainingArguments
        ))
        # If we pass only one argument to the script and it's the path
        # to a json file, let's parse it to get our arguments.
        model_args, data_args, evaluation_args, training_args \
            = parser.parse_json_file(json_file=model_config)

        self.data_args = data_args
        self.training_args = training_args

        # Initialize the sequence tagger
        self.sequence_tagger = SequenceTagger(
            task_name=data_args.task_name,
            notation=data_args.notation,
            ner_types=data_args.ner_types,
            model_name_or_path=model_args.model_name_or_path,
            config_name=model_args.config_name,
            tokenizer_name=model_args.tokenizer_name,
            post_process=model_args.post_process,
            cache_dir=model_args.cache_dir,
            model_revision=model_args.model_revision,
            use_auth_token=model_args.use_auth_token,
            threshold=model_args.threshold,
            do_lower_case=data_args.do_lower_case,
            fp16=training_args.fp16,
            seed=training_args.seed,
            local_rank=training_args.local_rank
        )

        # Load the required functions of the sequence tagger
        self.sequence_tagger.load()

        # Initialize the text deid object
        self.text_deid = TextDeid(notation=self.NOTATION, span_constraint='super_strict')

    def process_sentence(self, sentence: BioCSentence, docid: str = None) \
            -> BioCSentence:
        warnings.warn('Should call process_passage for batch process')
        entity_positions = self.deidentify_text(sentence.text)
        deid_text, anns = self.create_annotations(
            sentence.text, sentence.offset, entity_positions)
        sentence.annotations += anns
        sentence.text = deid_text
        return sentence

    def create_annotations(self, text, offset, entity_positions):
        deid_text = text
        anns = []
        for i, (positions, tag) in enumerate(entity_positions):
            start_pos, end_pos = positions
            ann = bioc.BioCAnnotation()
            ann.id = 'A%d' % i
            ann.add_location(bioc.BioCLocation(offset + start_pos,
                                               end_pos - start_pos))
            ann.text = text[start_pos: end_pos]
            ann.infons['source_concept'] = tag
            ann.infons['nlp_system'] = self.nlp_system
            ann.infons['nlp_date_time'] = self.nlp_date_time
            anns.append(ann)
            deid_tag = self.repl * (end_pos - start_pos)
            deid_text = deid_text[:start_pos] + deid_tag + deid_text[end_pos:]
        return deid_text, anns

    def process_collection(self, collection: BioCCollection) -> BioCCollection:
        if len(collection.documents) == 0:
            return collection

        # batch process for documents
        note_batch = []
        for doc in collection.documents:
            note_batch.append({
                'text': doc.passages[0].text,
                'meta': {NOTE_ID_KEY: doc.id}
            })
        entity_positions_batch = self.deidentify_batch(note_batch)
        for doc in collection.documents:
            if doc.id not in entity_positions_batch:
                print('%s: Cannot deidentify text: %s'
                      % (doc.id, doc.passages[0].text))
            entity_positions = entity_positions_batch[doc.id]
            deid_text, anns = self.create_annotations(
                doc.passages[0].text, doc.passages[0].offset,
                entity_positions)
            doc.passages[0].annotations += anns
            doc.passages[0].text = deid_text
        return collection

    def process_document(self, doc: BioCDocument) -> BioCDocument:
        if len(doc.passages) == 0:
            return doc

        # batch process for passages
        note_batch = []
        for passage in doc.passages:
            note_batch.append({
                'text': passage.text,
                'meta': {NOTE_ID_KEY: passage.offset}
            })
        entity_positions_batch = self.deidentify_batch(note_batch)
        for passage in doc.passages:
            if passage.offset not in entity_positions_batch:
                print('%s:%s Cannot deidentify text: %s'
                      % (doc.id, passage.offset, passage.text))
            entity_positions = entity_positions_batch[doc.id]
            deid_text, anns = self.create_annotations(
                passage.text, passage.offset, entity_positions)
            passage.annotations += anns
            passage.text = deid_text
        return doc

    def process_passage(self, passage: BioCPassage, docid: str = None) \
            -> BioCPassage:
        # if passage.text:
        #     entity_positions = self.deidentify_text(passage.text)
        #     deid_text, anns = self.create_annotations(
        #         passage.text, passage.offset, entity_positions)
        #     passage.annotations += anns
        #     passage.text = deid_text
        if len(passage.sentences) == 0:
            return passage

        # batch process for sentences
        note_batch = []
        for sentence in passage.sentences:
            note_batch.append({
                'text': sentence.text,
                'meta': {NOTE_ID_KEY: sentence.offset}
            })
        entity_positions_batch = self.deidentify_batch(note_batch)
        for sentence in passage.sentences:
            if sentence.offset not in entity_positions_batch:
                print('%s:%s Cannot deidentify sentence: %s'
                      % (docid, sentence.offset, sentence.text))
            entity_positions = entity_positions_batch[sentence.offset]
            deid_text, anns = self.create_annotations(
                sentence.text, sentence.offset, entity_positions)
            sentence.annotations += anns
            sentence.text = deid_text
        return passage

    def deidentify_text(self, text, id = 0) -> List:
        note_batch = [{
            'text': text,
            'meta': {NOTE_ID_KEY: id}
        }]
        entity_positions_batch = self.deidentify_batch(note_batch)
        if len(entity_positions_batch) != 1:
            raise Exception
        return entity_positions_batch[id]

    def deidentify_batch(self, note_batch: List[Dict]) -> Dict:
        ner_notes = self.dataset_creator.create_from_memory(
            notes=note_batch,
            mode='predict',
            notation=self.NOTATION,
            token_text_key='text',
            metadata_key=METADATA_KEY,
            note_id_key=NOTE_ID_KEY,
            label_key='label',
            span_text_key='spans'
        )

        # Write to file
        ner_fd, ner_path = tempfile.mkstemp(suffix='-ner_notes.jsonl')
        with os.fdopen(ner_fd, 'w') as file:
            for ner_sentence in ner_notes:
                file.write(json.dumps(ner_sentence) + '\n')
        print('ner', ner_path)

        # Set the required data and predictions of the sequence tagger
        # Can also use data_args.test_file instead of ner_dataset_file
        # (make sure it matches ner_dataset_file)
        self.sequence_tagger.set_predict(
            test_file=ner_path,
            max_test_samples=self.data_args.max_predict_samples,
            preprocessing_num_workers=self.data_args.preprocessing_num_workers,
            overwrite_cache=self.data_args.overwrite_cache
        )

        # Initialize the huggingface trainer
        self.sequence_tagger.setup_trainer(training_args=self.training_args)

        # Store predictions in the specified file
        predictions = self.sequence_tagger.predict()

        prediction_map = {}
        for pred in predictions:
            prediction_map[pred[NOTE_ID_KEY]] = pred

        # Go through note predictions and de identify the note accordingly
        entity_position_batch = {}
        for deid_note in note_batch:
            note_id = deid_note[METADATA_KEY][NOTE_ID_KEY]
            note = prediction_map[note_id]
            # Get predictions
            predictions = self.text_deid.decode(
                tokens=note[self.TOKENS_KEY],
                predictions=note[PREDICTIONS_KEY])
            # Get entities and their positions
            entity_positions = self.text_deid.get_predicted_entities_positions(
                tokens=note[self.TOKENS_KEY],
                predictions=predictions,
                suffix=False
            )
            entity_position_batch[note_id] = entity_positions
        return entity_position_batch


