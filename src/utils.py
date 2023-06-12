# any functionalities used in entire project
import os
import sys
import numpy as np
import pandas as pd
import torch

from src.logger import logging
from src.exception import CustomException


class BART:
    def __init__(self):
        logging.info("Initialising BART.")
        from transformers import BartForConditionalGeneration, BartTokenizer

        model_name="facebook/bart-base"

        self.tokenizer=BartTokenizer.from_pretrained(model_name)
        self.model=BartForConditionalGeneration.from_pretrained(model_name)
    
    def summarize(self,text, max_length=500):
        words = text.split(' ')
        words =set(words)
        max_len = min(len(words),1024)
        logging.info('Total words :{}'.format(max_len))
        inputs = self.tokenizer.batch_encode_plus([text], max_length=max_len, return_tensors='pt', truncation=True)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']
        logging.info("Words encoded. Now generating summary...")
        summary_ids = self.model.generate(input_ids, attention_mask=attention_mask, min_length=max_length//2, max_length=max_length)
        summary = self.tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)

        return summary

class Embeddings:
    def __init__(self):
        logging.info("Initialising BERT transformer.")
        try :
            from transformers import BertTokenizer,BertModel
            self.model = BertModel.from_pretrained("bert-base-uncased")
            self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        except Exception as e:
            raise CustomException(e,sys)
        
    def tokenize_sentences(self,text):
        try :
            token=self.tokenizer.tokenize(text)
            token = self.tokenizer.convert_tokens_to_ids(token)
            return token
        except Exception as e:
            raise CustomException(e,sys)

    def embeddings(self,text):
        try :
            token = self.tokenize_sentences(text)
            with torch.no_grad():
                output = self.model(torch.tensor(token).unsqueeze(0))
                return output[1][0].tolist()
        except Exception as e:
            raise CustomException(e,sys)
        