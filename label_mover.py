#USAGE: python3 label_mover.py file_path
#file path example: bubbles_2/00101/00001/labels.csv
import os
import shutil
import sys

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

def main():
    new_path = get_new_path(sys.argv[1])
    shutil.copy(sys.argv[1], new_path)

if __name__ == '__main__':
    main()