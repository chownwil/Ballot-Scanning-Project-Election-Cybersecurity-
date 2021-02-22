from PIL import Image
#run 'pip install pytesseract' in terminal if you haven't installed pytesseract
import pytesseract

import cv2
import csv
from tqdm.contrib.discord import tqdm, trange

MAX_BATCH_NUM = 242

race_id = 0

name_id = 3

races = {}
names = {
    'blankcontest': 0,
    'no': 1,
    'yes': 2
}

bot_token = 'ODEzMjU0NDQ0OTgwMzcxNDg3.YDMoOQ.gQQN-YoSY58Iyy7GZI3OzCbriXM'
bot_channel = '765292807740850180'

image_name = ''
for batch_num in tqdm(range(MAX_BATCH_NUM), token=bot_token, channel_id=bot_channel):
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