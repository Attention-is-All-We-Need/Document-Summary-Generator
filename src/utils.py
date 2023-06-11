# any functionalities used in entire project
import os
import sys
import numpy as np
import pandas as pd
import torch

from logger import logging
from exception import CustomException


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
        inputs = self.tokenizer.batch_encode_plus([text], max_length=max_len, return_tensors='pt', truncation=True)
        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        summary_ids = self.model.generate(input_ids, attention_mask=attention_mask, min_length=max_length//2, max_length=max_length)
        summary = self.tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)

        return summary

class Embeddings:
    def __init__(self):
        logging.info("Initialising BERT transformer.")
        try :
            from transformers import AlbertTokenizer,AlbertModel
            self.model = AlbertModel.from_pretrained("albert-base-v2")
            self.tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
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
        