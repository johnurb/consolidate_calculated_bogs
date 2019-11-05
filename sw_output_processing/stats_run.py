import os
import csv
import json
from time import sleep
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import re
import random


class ShadowBank:
    def __init__(self, info):
        self.data = {
            "bank_details": {
                "name": info["name"],
                "num_pages": info["num_pages"],
                "master_text": {
                    "raw_text": re.sub(' +', ' ', info["master_string"]),
                    "bog_index": 0,
                    "total_words": 0,
                    "avg_sentence_length": 0,
                    "number_sw_chunks": 1
                },
                "refined_text": {
                    "raw_text": re.sub(' +', ' ', info["refined_master_string"]),
                    "bog_index": 0,
                    "total_words": 0,
                    "avg_sentence_length": 0,
                    "number_sw_chunks": 1
                }
            }
        }
    
    def average_chunked_metrics(self):
        self.data["bank_details"]["master_text"]["bog_index"] /= self.data["bank_details"]["master_text"]["number_sw_chunks"]
        self.data["bank_details"]["master_text"]["total_words"] /= self.data["bank_details"]["master_text"]["number_sw_chunks"]
        self.data["bank_details"]["master_text"]["avg_sentence_length"] /= self.data["bank_details"]["master_text"]["number_sw_chunks"]

        self.data["bank_details"]["refined_text"]["bog_index"] /= self.data["bank_details"]["refined_text"]["number_sw_chunks"]
        self.data["bank_details"]["refined_text"]["total_words"] /= self.data["bank_details"]["refined_text"]["number_sw_chunks"]
        self.data["bank_details"]["refined_text"]["avg_sentence_length"] /= self.data["bank_details"]["refined_text"]["number_sw_chunks"]

        
def make_cloud():
    jsons_directory = 'bank_jsons'
    json_files = os.listdir(jsons_directory)
    for json_file in json_files:
        json_filepath = os.path.join(jsons_directory, json_file)
        with open(json_filepath, 'r') as fin:
            data = json.load(fin)
            
        bank_name = data['name']
        master_text = data['master_string']
        refined_text = data['refined_master_string']

        if len(master_text) < 10:
            pass
        else:
            # output wordcloud for master text
            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        stopwords = stopwords, 
                        min_font_size = 10).generate(master_text) 
                            
            plt.figure(figsize = (8, 8), facecolor = None) 
            plt.imshow(wordcloud) 
            plt.axis("off") 
            plt.title(bank_name + ' ' + ('Master Text'))
            out_dir = 'clouds'
            file_name = bank_name.replace(' ','_') + '_master.png'
            out_path = os.path.join(out_dir, file_name)
            plt.savefig(out_path, dpi=1000)
            plt.close('all')

        if len(refined_text) < 10:
            pass
        else:
            # output wordcloud for refined text
            stopwords = set(STOPWORDS)
            wordcloud = WordCloud(width = 800, height = 800, 
                        background_color ='white', 
                        stopwords = stopwords, 
                        min_font_size = 10).generate(refined_text) 
                            
            plt.figure(figsize = (8, 8), facecolor = None) 
            plt.imshow(wordcloud) 
            plt.axis("off") 
            plt.title(bank_name + ' ' + ('Refined Text'))
            out_dir = 'clouds'
            file_name = bank_name.replace(' ','_') + '_refined.png'
            out_path = os.path.join(out_dir, file_name)
            plt.savefig(out_path, dpi=1000)
            plt.close('all')


def process_sw4stats_file():
    file_name = 'sw4stats.txt'
    with open(file_name, 'r') as fin:
        file_contents = fin.readlines()

    bank_details = []
    for i, line in enumerate(file_contents):
        if i == 0 or line == '':
            pass
        else:
            split_line = line.replace('__', '_').split(':')[1].strip().split()[1:-5]
            del split_line[1]
            if 'Clipboard' in split_line:
                pass
            else:
                narrowed_line = split_line[0:6]
                del narrowed_line[3:5]
                bank_file_name = narrowed_line[0]
                bank_total_words = narrowed_line[1]
                bank_average_sentence_length = narrowed_line[2]
                bank_bog_index = narrowed_line[3]
                
                desired_bank_data = bank_file_name + ' ' + bank_total_words + ' ' + bank_average_sentence_length + ' ' + bank_bog_index
                bank_details.append(desired_bank_data.strip())
    
    return bank_details
    

def complete_bank_object_information(bank_objects, sw4lines):
    for bank in bank_objects:
        cur_bank = bank
        for cur_line in sw4lines:
            line = cur_line.split()
            bank_line_name = line[0].replace('.docx', '')

            if bank_line_name.endswith('refined'):
                if bank_line_name[0].isdigit() and bank_line_name[1] == '_':
                    bank_name = bank_line_name[2:].replace('_', ' ').replace('refined', '').strip()
                    if cur_bank.data['bank_details']['name'] == bank_name:
                        
                        cur_bank.data['bank_details']['refined_text']['bog_index'] += float(line[3])
                        cur_bank.data['bank_details']['refined_text']['total_words'] += int(line[1])
                        cur_bank.data['bank_details']['refined_text']['avg_sentence_length'] += float(line[2])
                        cur_bank.data['bank_details']['refined_text']['number_sw_chunks'] += 1
                
                else:
                    bank_name = bank_line_name.replace('_', ' ').replace('refined', '').strip()
                    if cur_bank.data['bank_details']['name'] == bank_name:
                       
                        cur_bank.data['bank_details']['refined_text']['bog_index'] = float(line[3])
                        cur_bank.data['bank_details']['refined_text']['total_words'] = int(line[1])
                        cur_bank.data['bank_details']['refined_text']['avg_sentence_length'] = float(line[2])
                
            else:
                if bank_line_name[0].isdigit() and bank_line_name[1] == '_':
                    bank_name = bank_line_name[2:].replace('_', ' ').replace('all', '').strip()
                    if cur_bank.data['bank_details']['name'] == bank_name:
                        
                        cur_bank.data['bank_details']['master_text']['bog_index'] += float(line[3])
                        cur_bank.data['bank_details']['master_text']['total_words'] += int(line[1])
                        cur_bank.data['bank_details']['master_text']['avg_sentence_length'] += float(line[2])
                        cur_bank.data['bank_details']['master_text']['number_sw_chunks'] += 1
                
                else:
                    bank_name = bank_line_name.replace('_', ' ').replace('all', '').strip()
                    if cur_bank.data['bank_details']['name'] == bank_name:
                        
                        cur_bank.data['bank_details']['master_text']['bog_index'] = float(line[3])
                        cur_bank.data['bank_details']['master_text']['total_words'] = int(line[1])
                        cur_bank.data['bank_details']['master_text']['avg_sentence_length'] = float(line[2])


def output_to_csv(banks):    
    with open('banks.csv', 'a') as fout:
        writer = csv.writer(fout)
        header = [
            'Bank Name', 'Number of Website Pages', 'Total Words(Master Text)', 'Average Sentence Length(Master Text)', 'Bog Index(Master Text)', 'Number of StyleWriter Chunks(Master Text)',
            'Total Words(Refined Text)', 'Average Sentence Length(Refined Text)', 'Bog Index(Refined Text)', 'Number of StyleWriter Chunks(Refined Text)'
        ]
        writer.writerow(header)

        for bank in banks:
            bank_name = bank.data['bank_details']['name']
            bank_num_pages = bank.data['bank_details']['num_pages']

            master_total_words = bank.data['bank_details']['master_text']['total_words']
            master_avg_sent_len = bank.data['bank_details']['master_text']['avg_sentence_length']
            master_bog_index = bank.data['bank_details']['master_text']['bog_index']
            master_num_sw_chunks = bank.data['bank_details']['master_text']['number_sw_chunks']

            refined_total_words = bank.data['bank_details']['refined_text']['total_words']
            refined_avg_sent_len = bank.data['bank_details']['refined_text']['avg_sentence_length']
            refined_bog_index = bank.data['bank_details']['refined_text']['bog_index']
            refined_num_sw_chunks = bank.data['bank_details']['refined_text']['number_sw_chunks']

            out_string = [
                bank_name, bank_num_pages, 
                master_total_words, master_avg_sent_len, master_bog_index, master_num_sw_chunks,
                refined_total_words, refined_avg_sent_len, refined_bog_index, refined_num_sw_chunks
            ]

            writer.writerow(out_string)


def output_consolidated_text_files():
    json_directory = 'bank_jsons'
    json_files = sorted(os.listdir(json_directory))
    
    out_dir = 'consolidated_texts'

    for json_file in json_files:
        json_filepath = os.path.join(json_directory, json_file)
        with open(json_filepath, 'r') as fin:
            data = json.load(fin)
            bank_name = data['name']
            master_text = data['master_string']
            refined_text = data['refined_master_string']
        
        # output all text file
        outfile_name = bank_name.replace(' ', '_') + 'all_text.txt'
        outfile_path = os.path.join(out_dir, outfile_name)
        with open(outfile_path, 'w') as fout:
            fout.write(master_text)

        # output refined text file
        outfile_name = bank_name.replace(' ', '_') + 'refined_text.txt'
        outfile_path = os.path.join(out_dir, outfile_name)
        with open(outfile_path, 'w') as fout:
            fout.write(refined_text)


def main():
    json_directory = 'bank_jsons'
    json_files = sorted(os.listdir(json_directory))
   
    bank_objects = []
    for json_file in json_files:
        json_filepath = os.path.join(json_directory, json_file)
        with open(json_filepath, 'r') as fin:
            data = json.load(fin)
            bank_objects.append(ShadowBank(data))

    sw4_lines = process_sw4stats_file()
    complete_bank_object_information(bank_objects, sw4_lines)
    for bank in bank_objects:
        bank.average_chunked_metrics()
    
    output_to_csv(bank_objects)
    

#main()
#make_cloud()
output_consolidated_text_files()

