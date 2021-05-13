
import pandas as pd
import numpy as np
from pathlib import Path


affected_page_types = [0,1,3,4,5,8,9,10,11,15]

page_types_df = pd.read_csv('pueblo_page_types.csv')
for index, row in page_types_df.iterrows():
    if int(row['page_type']) in affected_page_types:
        file_path_array = row['file'].split('_')
        file_path = Path("bubbles_2/" + file_path_array[1] + "/" + file_path_array[2] + "/")
        if (file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + "_0_5_1_1.jpg")).exists():
            Path(file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + 
                "_0_5_1_1.jpg")).rename(file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + "_0_6_1_1.jpg"))
            print('bing1')
        elif (file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + "_0_5_1_0.jpg")).exists():
            Path(file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + 
                "_0_5_1_0.jpg")).rename(file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + "_0_6_1_0.jpg"))
            print('bing2')



                "_0_5_1_0.jpg")).rename(file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + "_0_6_1_0.jpg"))
            print('bing2')



                "_0_5_1_0.jpg")).rename(file_path/(file_path_array[1] + "_" + file_path_array[2] + "_" + file_path_array[3] + "_0_6_1_0.jpg"))
            print('bing2')



