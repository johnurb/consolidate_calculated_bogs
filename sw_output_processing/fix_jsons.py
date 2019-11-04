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
