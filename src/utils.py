# any functionalities used in entire project
import os
import sys
import numpy as np
import pandas as pd
import torch
from transformers import pipeline
from src.logger import logging
from src.exception import CustomException


class LED:
    def __init__(self):
        pass
    def summarize(self, text, max_length=500):
        hf_name = 'pszemraj/led-base-book-summary'
        summarizer = pipeline(
            "summarization",
            hf_name,
            device=0 if torch.cuda.is_available() else -1,
        )

        result = summarizer(
            text,
            min_length = 8,
            max_length = max_length,
            no_repeat_ngram_size=3,
            encoder_no_repeat_ngram_size=3,
            repetition_penalty=3.5,
            num_beams=4,
            do_sample=False,
            early_stopping=True,
        )

        return result[0]['summary_text']

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
        
