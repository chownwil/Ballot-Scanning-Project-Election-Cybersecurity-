import pandas as pd

races_df = pd.read_csv('pueblo_races.csv')

page_types_df = pd.read_csv('pueblo_page_type_keys.csv')

num_bubbles = {}

for index, row in page_types_df.iterrows():
    for i in row:
        if i not in num_bubbles:

