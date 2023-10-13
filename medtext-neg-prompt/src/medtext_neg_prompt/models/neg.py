import tqdm
from bioc import BioCPassage
from medtext_neg_prompt.models.constants import POSITIVE
from medtext_commons.core import BioCProcessor
from medtext_neg_prompt.models.constants import UNCERTAINTY, NEGATION
from medtext_neg_prompt.models.negation_model import NegationModel

class BioCNeg(BioCProcessor):
    def __init__(self, verbose=False):
        super(BioCNeg, self).__init__('neg:negbio')
        self.verbose = verbose
        self.negation_model = NegationModel()

    def process_passage(self, passage: BioCPassage, docid: str = None) -> BioCPassage:

        text = passage.text
        for ann in tqdm.tqdm(passage.annotations, disable=not self.verbose):
            ann.infons[POSITIVE] = True
            if 'nlp_system' in ann.infons:
                ann.infons['nlp_system'] += ';' + self.nlp_system
            else:
                ann.infons['nlp_system'] = self.nlp_system
            if 'nlp_date_time' in ann.infons:
                ann.infons['nlp_date_time'] += ';' + self.nlp_date_time
            else:
                ann.infons['nlp_date_time'] = self.nlp_date_time

            # Assertion detection
            ann_text = ann.text
            negationResponse = self.negation_model.predict(text, ann_text)

            if negationResponse == 'N':
                ann.infons[NEGATION] = True
            elif negationResponse == 'U':
                ann.infons[UNCERTAINTY] = True
            elif negationResponse == 'P':
                ann.infons[POSITIVE] = True
            else:
                raise RuntimeError('Invalid negation response.')
        
        return passage
