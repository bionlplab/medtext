import numpy as np
import pandas as pd
import torch
from transformers import (
    BertConfig,
    BertTokenizer,
    BertForMaskedLM
)
import medtext_neg.models.prompt.negation_model_utils as negation_model_utils

MODEL_CLASSES = {"bert_prompt": (BertConfig, BertForMaskedLM, BertTokenizer)}
LABEL_OF_INTEREST = ['P', 'N', 'U', 'H', 'C', 'O']


def load_formatted_dataframe(input_text, target_disease) -> pd.DataFrame:
    """
    Format preprocessed source data into dataframe
    """
    dfs = [{'text': input_text, 'concept': target_disease}]
    df = pd.DataFrame(dfs)

    return df


class NegationModel:
    def __init__(self, pretrained_model_dir):
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.config_class, self.model_class, self.tokenizer_class = MODEL_CLASSES['bert_prompt']
        self.config = self.config_class.from_pretrained(pretrained_model_dir)
        self.tokenizer = self.tokenizer_class.from_pretrained(pretrained_model_dir)
        self.model = self.model_class(self.config).from_pretrained(pretrained_model_dir)
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text, ann_text):
        df = load_formatted_dataframe(text, ann_text)
        eval_features= negation_model_utils.convert_examples_to_features(df, self.tokenizer, max_input_length=512)
        input_ids, attention_mask, mask_pos = negation_model_utils.convert_features_to_dataset(eval_features)
        inputs = {'input_ids': input_ids.to(self.device), 'attention_mask': attention_mask.to(self.device)}
        outputs = self.model(**inputs)
        logits = outputs.logits

        _, from_index_to_answer, _ = negation_model_utils.from_answer_to_dicts(['P', 'N', 'U', 'H', 'C', 'O'], self.tokenizer)
        mask_pos_formatted = mask_pos.unsqueeze(-1).repeat(1, self.tokenizer.vocab_size).unsqueeze(1) 
        logits = torch.gather(logits, 1, mask_pos_formatted.to(self.device)) 
        logits = logits[:, :, list(from_index_to_answer.keys())].squeeze(1)
        pred_softmax = torch.nn.Softmax(1)(logits).cpu().detach().numpy()

        return LABEL_OF_INTEREST[np.argmax(pred_softmax, axis=1)[0]]
            
