import os
import csv
from tqdm import tqdm

#Return chunks and a bool for adjudicated given input text
def adjudicated(text):
    adjud = False
    chunks = text.split('\n')
    #if text was adjudicated, then one of the chunks will contain an element in bad:
    bad = ['adjudicated', 'over-vote', 'notcounted', 'overvote']
    for chunk in chunks:
        chunk = chunk.lower().replace(' ', '').replace(',', '')
        for i in bad:
            if i in chunk:
                adjud = True
    
    return chunks, adjud

#Function for extracting results from adjudicated ballots
def extract_adjudicated(chunks, races, names):
    data= {}
    first_race = -1
    for i, chunk in enumerate(chunks):
        chunk = chunk.lower().replace(' ', '')
        if ('ballotid:' in chunk):
            loc = chunk.find('ballotid:') + 9
            data['BallotID'] = int(chunk[loc:])
            first_race = i+1
            break
    race_chunks = chunks[first_race:(len(chunks) - 1)]
    isOverVote = 0
    decrement = 0
    for i in range(len(race_chunks)):
        line = race_chunks[i - decrement].lower().replace(' ', '').replace(',', '')
        if line == 'over-vote':
            isOverVote = 1
        elif line in races:
            race = line
            isOverVote = 0
        elif line in names:
            if races == 'Bad Data':
                print('Parsing error for line: ', line)
            if isOverVote and (races[race] in data):
                data[races[race]] *= 1000
                data[races[race]] += names[line]
            else: 
                #normal, non-overvote race
                data[races[race]] = names[line]
        elif line.split('(notcounted)')[0] in names:
            line = line.split('(notcounted)')[0]
            if isOverVote and (races[race] in data):
                #not counted and overvote
                data[races[race]] *= 1000
                data[races[race]] += -1 * names[line]
            else: 
                #if first of multi-vote lines
                data[races[race]] = -1 * names[line]
        elif 'adjudicated' in line:
            break
        else:
            
            print('Parsing failed for line: ', line, ' in chunks:')
            print(chunks)
            val = input('Enter user input [race/name/adj_name/other]: ')
            if val == 'race':
                races[line] = len(races)
                decrement += 1
            elif val == 'name':
                names[line] = len(names)
                decrement += 1
            elif val == 'adj_name':
                name = input('Correct name: ')
                names[name] = len(names)
            else:
                print('Edge case that was not considered')
                print('Line: ', line)
            
    return data

#Function for extracting results from un-adjudicated ballots
def extract_normal(chunks, races, names):
    data = {}
    first_race = -1
    for i, chunk in enumerate(chunks):
        chunk = chunk.lower().replace(' ', '')
        if ('ballotid:' in chunk):
            loc = chunk.find('ballotid:') + 9
            data['BallotID'] = int(chunk[loc:])
            first_race = i+1
            break
    
    chunks = chunks[first_race:(len(chunks) - 1)]
    for i in range(int(len(chunks) / 2)):
        race = chunks[i * 2]
        race = race.lower().replace(' ', '').replace(',', '')
        name = chunks[i * 2 + 1]
        name = name.lower().replace(' ', '').replace(',', '')
        if race not in races:
            races[race] = len(races)
        if name not in names:
            names[name] = len(names)
        data[races[race]] = names[name]
    return data

#main function
def main():

    #change directory name and csv names depending on which dataset
    races_csv = 'June ICC ABS_races.csv' #pueblo_races.csv
    names_csv = 'June ICC ABS_names.csv' #pueblo_names.csv
    text_dir = 'June ICC ABS text' #Pueblo_text
    data_dir = 'June ICC ABS data' #Pueblo_data

    image_texts = os.listdir(text_dir)
    with open(races_csv, mode='r') as inp:
        reader = csv.reader(inp)
        races = {rows[0]:int(rows[1]) for rows in reader}

    with open(names_csv, mode='r') as inp:
        reader = csv.reader(inp)
        names = {rows[0]:int(rows[1]) for rows in reader}

    
    for text_file in tqdm(image_texts):
        batch = text_file[0:8]
        #if batch != 'Batch047':
         #   continue
        with open(text_dir + '/' + text_file, 'r') as file:
            text = file.read()
        chunks, adjud = adjudicated(text)

        data = {}
        if adjud:
            print('>>>>>>>>ADJUDICATED BALLOT<<<<<<<<<<<<')
            data = extract_adjudicated(chunks, races, names)
        else:
            data = extract_normal(chunks, races, names)
        
        if not os.path.exists(data_dir + '/' + batch):
            os.makedirs(data_dir + '/' + batch)
        f = open(data_dir + '/' + batch + '/' + text_file[8:-4] + '_results.csv', 'w')
        for i in data.keys():
            f.write(str(i) + ', ' + str(data[i]) + '\n')
        f.close()

    w = open(races_csv, 'w')
    for key, val in races.items():
        w.write(str(key) + ', ' + str(val) + '\n')
    w.close()

    w = open(names_csv, 'w')
    for key, val in names.items():
        w.write(str(key) + ', ' + str(val) + '\n')
    w.close()


if __name__ == '__main__':
    main()