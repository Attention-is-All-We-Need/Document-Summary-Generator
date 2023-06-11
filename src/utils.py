# any functionalities used in entire project
import os
import sys
import numpy as np
import pandas as pd
import torch

from logger import logging
from exception import CustomException


    
class Embeddings:
    def __init__(self):
        logging.info("Initialising transformers.")
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

