import numpy as np
import pandas as pd
import torch
from transformers import (
    BertConfig,
    BertTokenizer,
    BertForMaskedLM
)
import medtext_neg_prompt.models.negation_model_utils as negation_model_utils

MODEL_CLASSES = {"bert_prompt": (BertConfig, BertForMaskedLM, BertTokenizer)}
LABEL_OF_INTEREST = ['P', 'N', 'U']
PRETRAINED_MODEL_DIR = 'medtext-neg-prompt/src/medtext_neg_prompt/models/negation_detection_model_checkpoint'

class NegationModel():
    def __init__(self):
        self.device =  torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.config_class, self.model_class, self.tokenizer_class = MODEL_CLASSES['bert_prompt']
        self.config = self.config_class.from_pretrained(PRETRAINED_MODEL_DIR)
        self.tokenizer = self.tokenizer_class.from_pretrained(PRETRAINED_MODEL_DIR)
        self.model = self.model_class(self.config).from_pretrained(PRETRAINED_MODEL_DIR)
        self.model.to(self.device)
        self.model.eval()

    def load_formated_dataframe(self, input_text, target_disease) -> pd.DataFrame:
        '''
        Format preprocessed source data into dataframe
        '''
        dfs = []
        dfs.append({'text': input_text, 'concept': target_disease})
        df = pd.DataFrame(dfs)

        return df

    def predict(self, text, ann_text):
        df = self.load_formated_dataframe(text, ann_text)
        eval_features= negation_model_utils.convert_examples_to_features(df, self.tokenizer, max_input_length=512, use_prompt=True)
        input_ids, attention_mask, mask_pos = negation_model_utils.convert_features_to_dataset(eval_features)
        inputs = {'input_ids': input_ids.to(self.device), 'attention_mask': attention_mask.to(self.device)}
        outputs = self.model(**inputs)
        logits = outputs.logits

        _, from_index_to_answer, _ = negation_model_utils.from_answer_to_dicts(['P', 'N', 'U'], self.tokenizer)
        mask_pos_formatted = mask_pos.unsqueeze(-1).repeat(1, self.tokenizer.vocab_size).unsqueeze(1) 
        logits = torch.gather(logits, 1, mask_pos_formatted.to(self.device)) 
        logits = logits[:, :, list(from_index_to_answer.keys())].squeeze(1)
        pred_softmax = torch.nn.Softmax(1)(logits).cpu().detach().numpy()

        return LABEL_OF_INTEREST[np.argmax(pred_softmax, axis=1)[0]]
            
