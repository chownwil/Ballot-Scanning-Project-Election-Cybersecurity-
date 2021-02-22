from PIL import Image
import numpy as np
import pandas as pd


page_df = pd.read_csv('pages.csv')
page_df.head()

df_dict = {}
page_layout_bubbles = {'Zachary B. Thoma and Dan Hauser': [7, 3],
                       'David R. Couch': [9],
                       'Kathleen A. Fairchild': [7],
                       'Nicole Chase': [7],
                       'Michael Caldwell': [5],
                       'Natalie Zall': [8],
                       'Sarie Toste Zachary B. Thoma and Dan Hauser': [7, 7, 3],
                       'Sherry Dalziel': [7],
                       'Kerry Gail Watty': [3],
                       'Sarie Toste (left)': [7],
                       'Emil Feierabend and Jerry Hansen': [3, 8],
                       #'Sarie Toste and Dan Hauser': [7, 3],
                       #'Sarie Toste (right)': [7],
                       #'Erin Maureen Taylor': [7],
                       'Sarie Toste and David R. Couch': [7, 9],
                       #'Tim Hooven': [8],
                       #'Tom Chapman': [7],
                       'Dan Hauser': [3],
                       'John Ash': [4],
                       #'Gaye Gerdts': [3]
                       }

for i in page_layout_bubbles:
  df_dict[i] = pd.read_csv('Page Types/' + i + '/labels.csv')

col_names = ['JPG', 'Race', 'Bubble', 'Label']

labels_df = pd.DataFrame(columns = col_names)

count = 0

bad = set()
file1 = open('unparsed_ballots.txt', 'r') 
Lines = file1.readlines()
for line in Lines: 
  bad.add(line)

for _, row in page_df.iterrows():
    pl = row['PageType']
    if (pl in df_dict) and (str(row['JPGNumber']) + '\n' not in bad):
        for i in range(len(page_layout_bubbles[pl])):
            for j in range(page_layout_bubbles[pl][i]):
                new_row = {
                    'JPG': row['JPGNumber'],
                    'Race': i,
                    'Bubble': j,
                    'Label': df_dict[pl][df_dict[pl]['JPGNumber'] == row['JPGNumber']]['Race ' + str(i) + ' Bubble ' +str(j)].to_numpy()[0]
                }
                labels_df = labels_df.append(new_row, ignore_index=True)
    count += 1
    if (count % 1000 == 0):
      print('Completed: ', count, ' bubbles')
labels_df.to_csv('y.csv', index=False)

