import os.path
from typing import Tuple, List

import bioc

from medtext_base.core import BioCProcessor
from bert_deid.model.transformer import Transformer
from bioc import BioCPassage, BioCSentence


class BioCDeidBert(BioCProcessor):
    def __init__(self, repl: str = 'X', model_path: str = '~/.radtext/bert_deid_model'):
        super(BioCDeidBert, self).__init__('deid:bert')
        self.deid_model = Transformer(os.path.expanduser(model_path))
        self.repl = repl
        if len(repl) != 1:
            raise ValueError('The replacement repl cannot have one char: %s' % repl)

    def deidentify(self, text: str, offset: int) -> Tuple[str, List[bioc.BioCAnnotation]]:
        """
        Replace PHI with replacement repl.
        """
        preds = self.deid_model.predict(text)
        anns = []
        for i, pred in enumerate(preds):
            ann = bioc.BioCAnnotation()
            ann.id = 'A%d' % i

            # prob = pred[0]
            label = pred[1]
            start, stop = pred[2:]

            ann.add_location(bioc.BioCLocation(start + offset, stop - start))
            ann.text = text[start:stop]
            ann.infons['source_concept'] = label
            ann.infons['nlp_system'] = self.nlp_system
            ann.infons['nlp_date_time'] = self.nlp_date_time
            anns.append(ann)

        for ann in anns:
            loc = ann.total_span
            text = text[:loc.offset - offset] + self.repl * loc.length + text[loc.end - offset:]
        return text, anns

    def process_passage(self, passage: BioCPassage, docid: str = None) -> BioCPassage:
        text, anns = self.deidentify(passage.text, passage.offset)
        passage.annotations += anns
        passage.text = text

        for sentence in passage.sentences:
            self.process_sentence(sentence, docid)

        return passage

    def process_sentence(self, sentence: BioCSentence, docid: str = None) -> BioCSentence:
        text, anns = self.deidentify(sentence.text, sentence.offset)
        sentence.annotations += anns
        sentence.text = text
        return sentence
