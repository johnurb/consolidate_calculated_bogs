import os
import csv
import json
from fix_jsons import bank_details
from time import sleep


class ChunkedBank():
    def __init__(self, name, total_words, avg_sentence_length, bog_index):
        self.name = name
        self.total_words = float(total_words)
        self.avg_sentence_length = float(avg_sentence_length)
        self.bog_index = float(bog_index)
        self.number_chunks = 1

    def get_details(self):
        avg_total_words = self.total_words / self.number_chunks
        avg_avg_sentence_length = self.avg_sentence_length / self.number_chunks
        avg_bog_index = self.bog_index / self.number_chunks
        return([self.name.replace('_', ' ').replace('.docx', ''), int(avg_total_words) , int(avg_avg_sentence_length), int(avg_bog_index), self.number_chunks])
    

def get_multi_chunk():
    file_name = 'sw4stats.txt'
    with open(file_name, 'r') as fin:
        file_contents = fin.readlines()

    bank_details = []
    for i, line in enumerate(file_contents):
        if i == 0 or line == '':
            pass
        else:
            split_line = line.split(':')[1].strip().split()[1:-5]
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
    
    bank_details = list(set(bank_details))
    chunked_banks = []
    for item in bank_details:
        item_components = item.split()
        if (item_components[0][0].isdigit() and item_components[0][1] == '_') or (item_components[0][0].isdigit() and item_components[0][1].isdigit() and item_components[0][2] == '_'):
            chunked_banks.append(item_components)

    chunked_instances = []
    seen_chunks = []
    for item in chunked_banks:
        bank_label = item[0].split('_', 1)
        bank_name = bank_label[1]

        if bank_name in seen_chunks:
            for instance in chunked_instances:
                if instance.name == bank_name:
                    instance.total_words += float(item[1])
                    instance.avg_sentence_length += float(item[2])
                    instance.bog_index += float(item[3])
                    instance.number_chunks += 1

        else:
            new_chunked_bank = ChunkedBank(bank_name, item[1], item[2], item[3])
            chunked_instances.append(new_chunked_bank)
            seen_chunks.append(bank_name)

    
    
    return chunked_instances
    
def process_stylewriter_output():
    banks = bank_details()
    
    file_name = 'sw4stats.txt'
    with open(file_name, 'r') as fin:
        file_contents = fin.readlines()

    for bank in banks:
        cur_bank = bank

        for i, line in enumerate(file_contents):
            if i == 0:
                pass
            else:
                if 'Clipboard' in line:
                    pass
                else:
                    sentence = line.split(':', 1)
                    remove_colon = ' '.join(sentence)
                    sentence_parts = remove_colon.split()
                    
                    if sentence_parts[5].replace('_', ' ').replace('.docx', '') == bank.name:
                        cur_bank.total_words = float(sentence_parts[7])
                        cur_bank.average_sentence_length = float(sentence_parts[8])
                        cur_bank.bog_index = float(sentence_parts[11])
                        cur_bank.data["bank_details"]["average_sentence_length"] = float(sentence_parts[8])
                        cur_bank.data["bank_details"]["bog_index"] = float(sentence_parts[11])
                    
                    else:
                        pass
    
    return banks


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
    chunked_banks = get_multi_chunk()
    banks = process_stylewriter_output()
    output_to_csv(banks, chunked_banks)


main()

