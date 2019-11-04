import os
import csv
import json
from time import sleep
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import re


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
                    "number_sw_chunks": 0
                },
                "refined_text": {
                    "raw_text": re.sub(' +', ' ', info["refined_master_string"]),
                    "bog_index": 0,
                    "total_words": 0,
                    "avg_sentence_length": 0,
                    "number_sw_chunks": 0
                }

            }
        }


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
    

def objectify_sw4_lines(sw4lines):
    for line in sw4lines:
        line_parts = line.split()
        
        bank_name = line_parts[0].replace('.docx', '')
        bank_total_words = float(line_parts[1])
        bank_average_sentence_length = float(line_parts[2])
        bank_bog_index = float(line_parts[3])

        print(bank_name, bank_total_words, bank_average_sentence_length, bank_bog_index)


def output_to_csv(banks, chunked_instances):    
    with open('banks.csv', 'a') as fout:
        writer = csv.writer(fout)
        header = ['Bank Name', 'Total Words', 'Average Sentence Length', 'Bog Index', 'Number Of Pages', 'Number of StyleWriter Chunks']
        writer.writerow(header)
        for bank in banks:
            cur_bank = bank
            bank_name = cur_bank.name
            total_words = cur_bank.total_words / cur_bank.number_stylewriter_chunks
            average_sentence = cur_bank.average_sentence_length / cur_bank.number_stylewriter_chunks
            bog_index = int(cur_bank.data["bank_details"]["bog_index"]) / cur_bank.number_stylewriter_chunks
            num_pages = int(cur_bank.data["bank_details"]["num_pages"]) / cur_bank.number_stylewriter_chunks
            number_stylewriter_chunks = cur_bank.number_stylewriter_chunks

            out_string = [bank_name, total_words, average_sentence, bog_index, num_pages, number_stylewriter_chunks]
          
            for item in chunked_instances:
                item_details = item.get_details()
                if item_details[0] == bank_name:
                    out_string = [bank_name, item_details[1], item_details[2], item_details[3], num_pages, item_details[4]]

            writer.writerow(out_string)







def main():
    json_directory = 'bank_jsons'
    json_files = sorted(os.listdir(json_directory))
   
    bank_objects = []
    #for json_file in json_files:
    #    json_filepath = os.path.join(json_directory, json_file)
    #    with open(json_filepath, 'r') as fin:
    #        data = json.load(fin)
    #        bank_objects.append(ShadowBank(data))

    sw4_lines = process_sw4stats_file()
    sw4_objects = objectify_sw4_lines(sw4_lines)
    
    


main()

