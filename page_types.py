"""
If a ballot  has all the same races on a page as another ballot, the they have the same page type
Usage: python3 page_types.py <'directory name'>
Example : python3 page_types.py 'June ICC ABS/'

------------------------------------------
PAGE TYPES AND PAGE TYPE KEYS EXPLANATION:
------------------------------------------
The csv file pueblo_page_type_keys.csv contains 16 comma-separated rows that list the race layout of 
    each page type. A race layout is determined by the order in which races appear on a results file; 
    a list of all races can be found in races.csv
The csv file pueblo_page_types.csv contains 2 columns, one with a results file name, and the other
    with a numerical index corresponding to the row number (INDEXING FROM ZERO) in pueblo_page_type_keys.csv
"""
import csv
import sys
import os

def get_pages(directory):
    loc = directory.find('data') - 1
    prefix = directory[0:loc]
    pageTypes = []
    batches = os.listdir(directory)
    ptOut = open(prefix + '_page_types.csv', mode = 'w')
    pt_writer = csv.writer(ptOut)
    keyOut = open(prefix + '_page_type_keys.csv', mode = 'w')
    for batch in batches:
        if batch[0:5] != 'Batch':
            print(batch)
            continue
        results = os.listdir(directory + '/' + batch + '/')
        for result in results:
            if 'results.csv' not in result:
                print('Bad result file: ', result)
                continue

            try:
                with open(directory + '/' + batch + '/' + result, mode='r') as inp:
                    data = csv.reader(inp)
                    races = [row[0] for row in data]
                    races = races[1:]
                index = -1
                try:
                    index = pageTypes.index(races)
                except ValueError:
                    index = len(pageTypes)
                    pageTypes.append(races)
                    print(races)
                    for i in races:
                        keyOut.write(str(i) + ', ')
                    keyOut.write('\n')
                pt_writer.writerow([result, index])
            except FileNotFoundError:
                print('File not found: ', result)
    keyOut.close()
    ptOut.close()

            #pt_writer.writerow([result, index]), where index is the row_num from the keys csv

#old version
def get_page_types(directory, maxBatchNo):
    maxBatchNo = int(maxBatchNo)
    pageTypes = []
    with open(directory + 'pageTypes.csv', mode='w') as valOutp:
        valWriter = csv.writer(valOutp)
        suffix = '_results.csv'
        with open(directory + 'pageTypesKey.txt', mode='w') as keyOutp:
            for batch_num in range(1, maxBatchNo):
                openIt = 1
                ballot_num = 1
                while openIt:
                    middle = 'Batch' + str(batch_num).zfill(3) + '/Results/' + str(ballot_num).zfill(6)
                    filename = directory + middle + suffix
                    try:
                        with open(filename, mode='r') as inp:
                            results = csv.reader(inp)
                            races = [row[0] for row in results]
                            races = races[1:]
                        index = -1
                        try:
                            index = pageTypes.index(races)
                        except ValueError:
                            index = len(pageTypes)
                            pageTypes.append(races)
                            for i in races:
                                keyOutp.write(str(i) + ', ')
                            keyOutp.write('\n')
                        valWriter.writerow([batch_num, ballot_num, index])
                    except FileNotFoundError:
                        #print(f'Batch {batch_num}, ballot {ballot_num} not found')
                        openIt = 0
                    ballot_num += 1


def main():
    directory = sys.argv[1]
    print(directory)
    get_pages(directory)

if __name__ == "__main__":
    main()
