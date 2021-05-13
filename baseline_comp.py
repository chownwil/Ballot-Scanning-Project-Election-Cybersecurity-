import os
import pandas as pd
import csv
import re

#comparing the machine results in Pueblo_data 
#with our labels in labels_all.csv

name_mapping = {
    0: 1,
    1: 1,
    2: 0,
    3: 1,
    4: 1,
    5: -1,
    6: 0,
    7: 1,
    8: 0,
    9: 0,
    10: 1,
    11: 0,
    12: 1,
    13: 0,
    14: 0,
    15: 0,
    16: 4,
    17: 2,
    18: -2,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 2,
    24: 1,
    25: 1,
    26: 3,
    27: 2,
    28: 20,
    29: 6,
    30: 3,
    31: -2,
    32: 2,
    33: 4,
    34: -2,
    35: 17,
    36: 18,
    37: 9,
    38: 3,
    39: 12,
    40: 7,
    41: 10,
    42: 14,
    43: 16,
    44: 17,
    45: 8,
    46: -2,
    47: -2,
    48: 5,
    49: 11,
    50: 13,
    51: -2,
    52: -2,
    53: -2,
    54: 19,
    55: -2,
    56: -2,
    57: -2,
    58: -2,
    59: -2,
    60: -2,
    61: -2,
    62: -2,
    63: -2,
    64: -2,
    65: -2,
    66: -2,
    67: -2,
    68: -2,
    69: -2,
    70: -2,
    71: -2,
    72: -2,
    73: -2,
    74: -2,
    75: -2,
    76: -2,
    77: -2,
    78: -2,
    79: -2,
    80: -2,
    81: -2,
    82: -2,
    83: -2,
    84: -2,
    85: -2,
    86: -2,
    87: -2,
    88: -2,
    89: -2,
    90: -2,
    91: -2,
    92: -2,
    93: -2,
    94: -2,
    95: -2,
    96: -2,
    97: -2,
    98: -2,
    99: -2,
    100: -2,
    101: -2,
    102: -2,
    103: -2,
    104: -2,
    105: -2,
    106: -2,
    107: -2,
    108: -2,
    109: -2,
    110: -2,
    111: -2,
    112: -2,
    113: -2,
    114: -2,
    115: -2,
    116: -2,
    117: -2,
    118: -2,
    119: -2,
    120: -2,
    121: -2,
    122: -2,
    123: -2,
    124: -2,
    125: -2,
    126: -2,
    127: -2,
    128: -2,
    139: -2,
    130: -2,
    131: -2,
    132: -2,
    133: -2,
    134: -2,
    135: -2,
}

num_bubbles = {
    0: 21,
    1: 5,
    2: 3,
    3: 1,
    4: 2,
    5: 0,
    6: 1,
    7: 0,
    8: 1,
    9: 1,
    10: 1,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1,
    16: 1,
    17: 1,
    18: 1,
    19: 1,
    20: 1,
    21: 1,
    22: 1,
    23: 1,
    24: 1,
    25: 1,
    26: 1,
    27: 1, 
    28: 1,
    29: 1,
    30: 1,
    31: 1
}


def data_file_info(label_path):
    batch = label_path[8:11]
    race = re.search('[0-9]+', label_path[21:]).group()
    bubble = re.search('[0-9]+', label_path[23:]).group()
    result_file = '_' + label_path[:18] + '_results.csv'
    return batch, race, bubble, result_file

def main():
    labels = pd.read_csv('labels_all.csv')
    labels['sort_batch'] = labels['path'].str[6:11].str.extract('(\d+)', expand=False).astype(int)
    labels['sort_ballot'] = labels['path'].str[13:19].str.extract('(\d+)', expand=False).astype(int)
    labels['sort_race'] = labels['path'].str[21:].str.extract('(\d+)', expand=False).astype(int)
    labels['sort_bubble'] = labels['path'].str[23:].str.extract('(\d+)', expand=False).astype(int)
    labels = labels.sort_values(by=['sort_batch', 'sort_ballot', 'sort_race', 'sort_bubble'])
    print(labels.head())

    races_reader = csv.reader(open('pueblo_races.csv', 'r'))
    races_dict = {}
    for row in races_reader:
        k, v = row
        races_dict[k] = int(v)

    names_reader = csv.reader(open('pueblo_names.csv', 'r'))
    names_dict = {}
    for row in names_reader:
        k, v = row
        names_dict[k] = int(v)

    count_total = 0
    count_correct = 0
    bad_unmarked = 0
    bad_marked = 0
    other_problem = 0
    for index, row in labels.iterrows():
        batch, race, bubble, result_file = data_file_info(row['path'])
        if row['result'] == 0:
            with open('Pueblo_data/Batch' + batch + '/' + result_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                vote = -1  
                for csv_row in csvreader:
                    #print(result_file)
                    #print('row: ', csv_row)
                    csv_race = int(csv_row[0])
                    csv_name = int(csv_row[1])
                    #print('csv race: ', csv_race)
                    #print('csv_name: ', csv_name)
                    if int(race) == csv_race:
                        vote = csv_name
                    #print('Race: ', race)
                    #print('Vote: ', vote)
                if vote == -1:
                    print('PROBLEM')
                    print(row)
                    return
                elif vote < -1: #caused an overvote and kick, but for different bubble. This bubble is correct
                    count_total += 1
                    count_correct += 1
                elif name_mapping[vote] == -1: #no votes for this one; correct by default
                    count_total += 1
                    count_correct += 1
                elif name_mapping[vote] == -2 and num_bubbles[int(race)] == int(bubble): #write in and last bubble; incorrect
                    count_total += 1
                elif int(name_mapping[vote]) == int(bubble): #machine incorrectly counts bubble as a vote
                    
                    bad_unmarked += 1
                    count_total += 1
                else: #machine correctly did not count this bubble as a vote
                    count_total += 1
                    count_correct += 1
        elif (row['result'] >= 1) and (row['result']) <= 3:
            with open('Pueblo_data/Batch' + batch + '/' + result_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                vote = -1        
                for csv_row in csvreader:
                    csv_race = int(csv_row[0])
                    csv_name = int(csv_row[1])
                    if int(race) == csv_race:
                        vote = csv_name
                if vote == -1:
                    print('PROBLEM')
                    return
                elif vote < -1: #caused an overvote and kick, but for different bubble. This one is correct.
                    count_total += 1
                    count_correct += 1
                elif name_mapping[vote] == -1: #no votes for this one; incorrect by default
                    count_total += 1
                elif name_mapping[vote] == -2 and num_bubbles[int(race)] == int(bubble): #write in and last bubble; correct
                    count_total += 1
                    count_correct += 1
                elif int(name_mapping[vote]) == int(bubble): #machine correctly counts bubble as a vote
                    count_total += 1
                    count_correct += 1
                else: #machine incorrectly did not count this bubble as a vote
                    other_problem += 1
        elif row['result'] == 4:
            with open('Pueblo_data/Batch' + batch + '/' + result_file, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                vote = -1   
                for csv_row in csvreader:
                    csv_race = int(csv_row[0])
                    csv_name = int(csv_row[1])
                    if int(race) == csv_race:
                        vote = csv_name
                if vote == -1:
                    print('PROBLEM')
                    return
                elif vote < -1: #caused an overvote and kick; this bubble is incorrect
                    count_total += 1
                elif name_mapping[vote] == -1: #no votes for this one; incorrect by default
                    count_total += 1
                elif name_mapping[vote] == -2 and num_bubbles[int(race)] == int(bubble): #write in and last bubble; incorrect
                    count_total += 1
                elif int(name_mapping[vote]) == int(bubble): #machine incorrectly counts bubble as a vote
                    count_total += 1
                else: #machine correctly did not count this bubble as a vote
                    count_total += 1
                    count_correct += 1
        else:
            pass

    print('Accuracy: ', count_correct / count_total)
    print('Correct: ', count_correct)
    print('Total:', count_total)
    print('False votes: ', bad_unmarked)
    print('Missed votes: ', bad_marked)
    print('Other Problem: ', other_problem)


if __name__ == '__main__':
    main()