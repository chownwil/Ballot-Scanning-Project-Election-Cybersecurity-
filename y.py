#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image
import numpy as np
import pandas as pd
import torch


# JPG_number    Race_number    bubble_number    label
# 1.            0.             0              0
# 1             0              1.             2

# In[65]:


page_df = pd.read_csv("pages.csv")
page_df.head()


# In[66]:


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
                       'Sarie Toste and Dan Hauser': [7, 3],
                       'Sarie Toste (right)': [7],
                       'Erin Maureen Taylor': [7],
                       'Sarie Toste and David R. Couch': [7, 9],
                       'Tim Hooven': [8],
                       'Tom Chapman': [7],
                       'Dan Hauser': [3],
                       'John Ash': [4],
                       'Gaye Gerdts': [3]
                       }


# In[12]:


for i in page_layout_bubbles:
    df_dict[i] = pd.read_csv('Page Types/' + i + '/labels.csv')

col_names = ["JPG", "Race", "Bubble", "Label"]

labels_df = pd.DataFrame(columns = col_names)


# In[67]:


df_dict['John Ash'].head()


# In[68]:


for i in page_layout_bubbles:
    df_dict[i] = pd.read_csv('Page Types/' + i + '/labels.csv')

col_names = ["JPG", "Race", "Bubble", "Label"]

labels_df = pd.DataFrame(columns = col_names)

for _, row in page_df.iterrows():
    pl = row['PageType']
    print(pl)
    if (pl in df_dict):
        for i in range(len(page_layout_bubbles[pl])):
            for j in range(page_layout_bubbles[pl][i]):
                labels_df.append(row['JPGNumber'], i, j, df_dict[pl][df_dict[pl]['JPGNumber'] == row['JPGNumber']]['Race ' + str(i) +' Bubble ' + str(j)][0])


# In[8]:


page_df = pd.read_csv("pages.csv")
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
                       'Sarie Toste and Dan Hauser': [7, 3],
                       'Sarie Toste (right)': [7],
                       'Erin Maureen Taylor': [7],
                       'Sarie Toste and David R. Couch': [7, 9],
                       'Tim Hooven': [8],
                       'Tom Chapman': [7],
                       'Dan Hauser': [3],
                       'John Ash': [4],
                       'Gaye Gerdts': [3]
                       }

for i in page_layout_bubbles:
    df_dict[i] = pd.read_csv('Page Types/' + i + '/labels.csv')

col_names = ["JPG", "Race", "Bubble", "Label"]

labels_df = pd.DataFrame(columns = col_names)
for _, row in page_df.iterrows():
    pl = row['PageType']
    df = df_dict[pl]
    bing = np.array(df[df['JPGNumber'] == row['JPGNumber']])
    print(bing)
    input("hsdjfhjs")
    if (pl in df_dict):
        for i in range(0, len(page_layout_bubbles[pl])):
            for j in range(0, page_layout_bubbles[pl][i]):
                print(bing[i * page_layout_bubbles[pl][i] + page_layout_bubbles[pl][i] + str(j)])
                val = bing['Race ' + str(i) + ' Bubble ' + str(j)][0]
                new_row = {'JPG':row['JPGNumber'], 'Race':i, 'Bubble':j, 'Label':val}
                #print(new_row)
                labels_df = labels_df.append(new_row, ignore_index=True)


# In[70]:


check = labels_df


# In[62]:


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
                       'Sarie Toste and Dan Hauser': [7, 3],
                       'Sarie Toste (right)': [7],
                       'Erin Maureen Taylor': [7],
                       'Sarie Toste and David R. Couch': [7, 9],
                       'Tim Hooven': [8],
                       'Tom Chapman': [7],
                       'Dan Hauser': [3],
                       'John Ash': [4],
                       'Gaye Gerdts': [3]
                       }

for i in page_layout_bubbles:
  df_dict[i] = pd.read_csv('Page Types/' + i + '/labels.csv')

col_names = ['JPG', 'Race', 'Bubble', 'Label']

labels_df = pd.DataFrame(columns = col_names)

for _, row in page_df.iterrows():
    pl = row['PageType']
    if (pl in df_dict):
        for i in range(len(page_layout_bubbles[pl])):
            for j in range(page_layout_bubbles[pl][i]):
                new_row = {
                    'JPG': row['JPGNumber'],
                    'Race': i,
                    'Bubble': j,
                    'Label': df_dict[pl][df_dict[pl]['JPGNumber'] == row['JPGNumber']]['Race ' + str(i) + ' Bubble ' +str(j)][0]
                }
                labels_df = labels_df.append(new_row, ignore_index=True)


# In[12]:


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
                       'Sarie Toste and Dan Hauser': [7, 3],
                       'Sarie Toste (right)': [7],
                       'Erin Maureen Taylor': [7],
                       'Sarie Toste and David R. Couch': [7, 9],
                       'Tim Hooven': [8],
                       'Tom Chapman': [7],
                       'Dan Hauser': [3],
                       'John Ash': [4],
                       'Gaye Gerdts': [3]
                       }

for i in page_layout_bubbles:
    df_dict[i] = pd.read_csv('Page Types/' + i + '/labels.csv')

col_names = ['JPG', 'Race', 'Bubble', 'Label']

labels_df = pd.DataFrame(columns = col_names)
check = 0
for _, row in page_df.iterrows():
    pl = row['PageType']
    if (pl in df_dict):
        for i in range(len(page_layout_bubbles[pl])):
            for j in range(page_layout_bubbles[pl][i]):
                new_row = {
                    'JPG': row['JPGNumber'],
                    'Race': i,
                    'Bubble': j,
                    'Label': df_dict[pl][df_dict[pl]['JPGNumber'] == row['JPGNumber']]['Race ' + str(i) + ' Bubble ' +str(j)].to_numpy()[0]
                }
                labels_df = labels_df.append(new_row, ignore_index=True)
                check += 1
                if check % 1000 == 0:
                    print(check)
                    print(labels_df.tail())
labels_df.to_csv('y.csv')


# In[16]:





# In[35]:


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
    if (pl in df_dict) and ((str(row['JPGNumber'])+ '\n') not in bad):
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


# In[36]:


len(labels_df)


# In[ ]:




