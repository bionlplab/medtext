import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple

class InputFeatures(object):
    def __init__(self, text, input_ids, attention_mask, ent1, label, **kwargs):
        self.text = text
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.concept = ent1
        self.label = label

        if 'mask_pos' in kwargs:
            self.mask_pos = kwargs['mask_pos']

def from_answer_to_dicts(answers: List, tokenizer) -> Tuple[Dict, Dict, Dict]:
    from_answer_to_index = {}

    for answer in answers:
        from_answer_to_index[answer] = tokenizer.encode(answer, add_special_tokens=False)[0]
    
    from_index_to_answer = {from_answer_to_index[word]: word for word in from_answer_to_index}
    ground_truth_dict = {idx:list(from_index_to_answer.keys()).index(idx) for idx in from_index_to_answer}

    return from_answer_to_index, from_index_to_answer, ground_truth_dict

def convert_examples_to_features(df, tokenizer, max_input_length, use_prompt: bool, **kwargs):

    '''
    Convert examples to features 
    '''
    pad_id = tokenizer.pad_token_id
    cls_id = tokenizer.cls_token_id
    sep_id = tokenizer.sep_token_id
    msk_id = tokenizer.mask_token_id

    if use_prompt:
        features = []
        for _, row in df.iterrows():
            text = str(row.text).replace(f"{row.concept}", f"<E>{row.concept}</E>")
            prompt = f"<E>{str(row.concept)}</E> is [MASK]."
            text_token_ids = tokenizer.encode(text, add_special_tokens=False)
            prompt_token_ids = tokenizer.encode(prompt, add_special_tokens=False)
            
            avail_len = max_input_length - 3 - len(prompt_token_ids)
            input_ids = [cls_id] + text_token_ids[-avail_len:] + [sep_id] + prompt_token_ids + [sep_id]
            
            pad_len = max_input_length - len(input_ids)
            if pad_len > 0:
                input_ids += [pad_id] * pad_len
            
            mask_pos = input_ids.index(msk_id)
            features.append(InputFeatures(text=text,
                                        input_ids=input_ids,
                                        attention_mask=torch.where(torch.tensor(input_ids) != pad_id, torch.tensor(1), torch.tensor(0)).tolist(),
                                        ent1=row.concept,
                                        mask_pos=mask_pos,
                                        label=None))
            
    assert len(features) == len(df)
    return features

def convert_features_to_dataset(features):
    '''
    df = load_formated_dataframe([path])
    features = convert_examples_to_features(df , tokenizer, input_max_length, use_prompt)
    '''
    input_ids = torch.tensor([f.input_ids for f in features])
    attention_mask = torch.tensor([f.attention_mask for f in features])
    mask_pos = torch.tensor([f.mask_pos for f in features])

    return input_ids, attention_mask, mask_pos

    