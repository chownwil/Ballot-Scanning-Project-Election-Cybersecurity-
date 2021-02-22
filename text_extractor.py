from PIL import Image
import pytesseract
import cv2
import csv
from tqdm import trange
from tqdm.contrib.discord import tdrange
import sys
import json

MAX_BATCH_NUM = 242

race_id = 0
name_id = 3
races = {}
names = {
    'blankcontest': 0,
    'no': 1,
    'yes': 2
}
image_name = ''

sys.argv
args = {}

discord_progress = 0
if (len(sys.argv) == 2):
    if (sys.argv[1] == 'discord'):
        discord_progress = 1
        with open('./config.json', 'r') as cjson:
            config = json.load(cjson)
        args['token'] = config["token"]
        args['channel_id'] = '765292807740850180'

def run_tqdm(discord_progress):
    if discord_progress:
        return tdrange(MAX_BATCH_NUM, **args)
    else:
        return trange(MAX_BATCH_NUM)

#extract results
for batch_num in run_tqdm(discord_progress):
    image_name = 'June ICC ABS/Batch' + str(batch_num + 1).zfill(3)
    image_name += '/Images/00760_00' + str(batch_num + 1).zfill(3) + '_'
    image_num = 1
    openIt = 1
    while(openIt):
        try: 
            img = Image.open(image_name + str(image_num).zfill(6) + '.tif')
            img.seek(2)
            text = pytesseract.image_to_string(img)
            text = text.replace('\n\n','\n')
            chunks = text.split('\n')
            offset = chunks[2].find('Ballot ID: ') + 11
            if (offset == 10):
                offset = chunks[2].find('BallotID: ') + 10
            if (offset == 9):
                ballotID = -1
                print("Did not find ballot ID for: Batch ", batch_num, ", Image ", image_num)
            else:
                ballotID = int(chunks[2][offset:])
            chunks = chunks[3:(len(chunks) - 1)]
            data = {
                'BallotID': ballotID
            }
            for i in range(int(len(chunks) / 2)):
                race = chunks[i * 2]
                race = race.lower().replace(" ", "")
                name = chunks[i * 2 + 1]
                name = name.lower().replace(" ", "")
                if race not in races:
                    races[race] = race_id
                    race_id += 1
                if name not in names:
                    names[name] = name_id
                    name_id += 1
                data[races[race]] = names[name]
            f = open('June ICC ABS/Batch' + str(batch_num + 1).zfill(3) + '/Results/' + str(image_num).zfill(6) + '_results.csv', 'w')
            for i in data.keys():
                f.write(str(i) + ', ' + str(data[i]) + '\n')
            f.close()
            image_num += 1
        except FileNotFoundError:
            openIt  = 0
w = open("races.csv", "w")
for key, val in races.items():
    w.write(str(key) + ', ' + str(val) + '\n')
w.close()

w = open("names.csv", "w")
for key, val in names.items():
    w.write(str(key) + ', ' + str(val) + '\n')
w.close()