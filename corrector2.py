import pandas as pd


"""
results_df = pd.read_csv('labels_all.csv')
for index, row in results_df.iterrows():
    path = row['path']
    if path[21:24] == '5_1':
        new = list(path)
        new[21] = '6'
        results_df.at[index, 'path'] = ''.join(new)
results_df.to_csv('labels_all.csv', index=False)
"""

