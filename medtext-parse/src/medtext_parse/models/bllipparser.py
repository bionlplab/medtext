import logging
import os
import string
from pathlib import Path
from typing import Union, List

from bioc import BioCSentence, BioCPassage, BioCAnnotation
from bllipparser import RerankingParser

from medtext_commons.core import BioCProcessor
from medtext_commons.base_utils import is_ner


DEFAULT_BLLLIP_MODEL = str(Path.home() / '.medtext/bllipparser/BLLIP-GENIA-PubMed')


def is_punct(text) -> bool:
    for c in text:
        if c not in string.punctuation:
            return False
    return True


def singleton(cls, *args, **kw):
 instances = {}
 def _singleton(*args, **kw):
    if cls not in instances:
         instances[cls] = cls(*args, **kw)
    return instances[cls]
 return _singleton


@singleton
class BllipParser:
    def __init__(self, model_dir: str=DEFAULT_BLLLIP_MODEL):
        self.model_dir = os.path.expanduser(model_dir)
        print('loading model %s ...' % self.model_dir)
        self.rrp = RerankingParser.from_unified_model_dir(self.model_dir)

    def parse(self, s: Union[None, str]):
        """Parse the sentence text using Reranking parser.

        Args:
            s: one sentence

        Returns:
            ScoredParse: parse tree, ScoredParse object in RerankingParser; None if failed

        Raises:
            ValueError
        """
        if s is None or (isinstance(s, str) and len(s.strip()) == 0):
            raise ValueError('Cannot parse empty sentence: {}'.format(s))
        nbest = self.rrp.parse(str(s))
        return nbest[0].ptb_parse


class BioCParserBllip(BioCProcessor):
    def __init__(self, model_dir: str=DEFAULT_BLLLIP_MODEL, only_ner: bool=True):
        """
        :param model_dir: Bllip parser model path
        :param only_ner: Parse the sentences with NER annotations.
        """
        super(BioCParserBllip, self).__init__('parse:bllip')
        self.parser = BllipParser(model_dir=model_dir)
        self.only_ner = only_ner

    def has_ner(self, sentence: BioCSentence, annotations: List[BioCAnnotation]) -> bool:
        """
        :return: True if the sentence contains named entities
        """
        named_entities = [ann for ann in annotations if is_ner(ann)]
        sen_anns = [ann for ann in named_entities if ann.total_span in sentence.total_span]
        return len(sen_anns) > 0

    def process_passage(self, passage: BioCPassage, docid: str = None) -> BioCPassage:
        for sentence in passage.sentences:
            if self.only_ner and self.has_ner(sentence, passage.annotations):
                self.process_sentence(sentence, docid)
        return passage

    def process_sentence(self, sentence: BioCSentence, docid: str = None) -> BioCSentence:
        sentence.infons['parse_tree'] = None
        try:
            text = sentence.text
            # print(text)
            if not is_punct(text):
                sentence.infons['nlp_system'] = self.nlp_system
                sentence.infons['nlp_date_time'] = self.nlp_date_time
                sentence.infons['parse_tree'] = str(self.parser.parse(text))
        except Exception as e:
            logging.exception('%s:%s: Cannot parse sentence: %s. %s', docid, sentence.offset, sentence.text, e)
        return sentence
