import os
import json
from time import sleep
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 


class Bank:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.total_words = 0
        self.average_sentence_length = 0
        self.bog_index = 0
        self.number_stylewriter_chunks = 1
        

def make_cloud(bank_name, bank_text):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(bank_text) 
                     
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.title(bank_name)
    out_dir = 'clouds'
    file_name = bank_name.replace(' ','_') + '.png'
    out_path = os.path.join(out_dir, file_name)
    plt.savefig(out_path, dpi=1000)
    plt.close('all')


def bank_details():
    jsons_directory = 'jsons'
    json_files = os.listdir(jsons_directory)

    bank_objects = []
    for file in json_files:
        file_path = os.path.join(jsons_directory, file)
        with open(file_path, 'r') as fin:
            file_string = fin.read()
            bank_parts = file_string.split(',')

            bank_name = bank_parts[0].split(':')[1].replace('"', '').strip()
            bank_text = bank_parts[1].split(':')[1].replace('"', '').replace('\\n', '. ').replace('..', '.').strip()
            bank_text_fixed = ' '.join(bank_text.split()).strip().replace(' . ', '')
            bank_num_pages = bank_parts[2].split(':')[1].replace('}', '').replace('"', '').strip()

            bank_object = {
                "bank_details" : {
                    "name" : bank_name,
                    "complete_text" : bank_text_fixed,
                    "num_pages" : bank_num_pages,
                    "average_sentence_length": 0,
                    "bog_index": 0,
                    "number_stylewriter_chunks": 1
                }
            }

            #if len(bank_text_fixed) > 10:
            #    make_cloud(bank_name, bank_text_fixed)
            
            new_bank = Bank(bank_name, bank_object)

            bank_objects.append(new_bank)

    return bank_objects

    