import os
import sys
folder_path = os.getcwd()
sys.path.append(folder_path)

from src.exception import CustomException
from src.logger import logging

import PyPDF2
import docx

folder = os.path.join(folder_path,'UPLOAD_FOLDER')

def gen_para_file(file_name):
    file_name = os.path.join(folder,file_name)
    file_extension = os.path.splitext(file_name)[1]
    if (file_extension=='.pdf'):
        return gen_para_pdf(file_name)
    elif (file_extension == '.doc' or file_extension=='.docx'):
        return gen_para_doc(file_name)
    elif (file_extension=='.txt'):
        return gen_para_txt(file_name)
    logging.info("Paragraph of {} is generated.".format(file_name))

def gen_para_pdf(file_name):
    try :
        with open(file_name, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            paragraphs=[]
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                text = page.extract_text()
                paragraph = text.split('.\n')
                for para in paragraph:
                    paragraphs.append(para)
            return paragraphs
    except Exception as e:
        logging.info("PDF File not found.")
        paragraph=[]
        return paragraph

def gen_para_doc(file_name):
    try:
        doc = docx.Document(file_name)
        text = []
        for paragraph in doc.paragraphs:
            if (paragraph) :
                p_text = paragraph.text
                if len(p_text):
                    text.append(p_text)
        return text
    except Exception as e:
        logging.info("Doc File not found.")
        paragraph=[]
        return paragraph
    

def gen_para_txt(file_name):
    try:
        paragraphs=[]
        with open(file_name, 'r') as file:
            text = file.read()
            paragraph = str(text).split('.\n')
            for para in paragraph:
                if (para):
                    paragraphs.append(para)
        return paragraphs
    except Exception as e:
        logging.info("File not found.")
        paragraph=[]
        return paragraph

