#USAGE: python3 label_mover.py file_path
#file path example: bubbles_2/00101/00001/labels.csv
import os
import shutil
import sys
import pandas as pd

def get_new_path(file_path):
    root = 'Pueblo_labels/'
    project = ('ICC 101/' if (file_path[12] == '1') else 'ICC 201/')
    if not os.path.isdir(root + project):
        os.mkdir(root + project)
    batch = file_path[16:21]
    if not os.path.isdir(root + project + batch):
        os.mkdir(root + project + batch)
    labels = '/labels.csv'
    return root + project + batch + labels

def combine_all_labels():
    combined_df = pd.read_csv('labels_00001.csv')
    dirs = os.listdir('Pueblo_labels/')
    for dir in dirs:
        batch_dirs = os.listdir('Pueblo_labels/' + dir)
        for b_dir in batch_dirs:
            file = 'Pueblo_labels/' + dir + '/' + b_dir + '/labels.csv'
            if file != 'Pueblo_labels/ICC 101/00001/labels.csv':
                temp_df = pd.read_csv(file)
                combined_df = pd.concat([combined_df, temp_df])
    combined_df.to_csv( "labels_all.csv", index=False)
    """
    for dir in dirs:
        batch_dirs = os.listdir('Pueblo_labels/' + dir)
        for b_dir in batch_dirs:
            file = 'Pueblo_labels/' + dir + '/' + b_dir + '/labels.csv'
            print(file)
            f = open(file)
            for line in f:
                fout.write(line)
            f.close()
    fout.close()
    """
    
def main():
    #new_path = get_new_path(sys.argv[1])
    #shutil.copy(sys.argv[1], new_path)

    dirs = os.listdir('bubbles_2/00101')
    for dir in dirs:
        if os.path.exists('bubbles_2/00101/' + dir + '/labels.csv'):
            print("Found labels for batch ", dir)
            new_path = get_new_path('bubbles_2/00101/' + dir)
            if os.path.exists(new_path):
                print('Labels already copied')
            else:
                shutil.copy('bubbles_2/00101/' + dir + '/labels.csv', new_path)

    dirs = os.listdir('bubbles/00101')
    for dir in dirs:
        if os.path.exists('bubbles/00101/' + dir + '/labels.csv'):
            print("Found labels for batch ", dir)
            new_path = get_new_path('bubbles_2/00101/' + dir)
            if os.path.exists(new_path):
                print('Labels already copied')
            else:
                shutil.copy('bubbles/00101/' + dir + '/labels.csv', new_path)

    dirs = os.listdir('bubbles_2/00201')
    for dir in dirs:
        if os.path.exists('bubbles_2/00201/' + dir + '/labels.csv'):
            print('found ICC 201 labels')
            print("Found labels for batch ", dir)
            new_path = get_new_path('bubbles_2/00201/' + dir)
            if os.path.exists(new_path):
                print('Labels already copied')
            else:
                shutil.copy('bubbles_2/00201/' + dir + '/labels.csv', new_path)
    
    combine_all_labels()

if __name__ == '__main__':
    main()