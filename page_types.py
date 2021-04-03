"""
If a ballot  has all the same races on a page as another ballot, the they have the same page type
Usage: python3 page_types.py <directory name> <number of Batches in directory>
Example : python3 page_types.py 'June ICC ABS/' 242
"""
import csv
import sys

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
    maxBatchNo = sys.argv[2]
    get_page_types(directory, maxBatchNo)

if __name__ == "__main__":
    main()
