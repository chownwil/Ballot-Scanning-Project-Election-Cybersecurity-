#from os import lseek
import os
from PIL import Image
import pytesseract
from tqdm import tqdm

def extract(pathname):
    batches = os.listdir(pathname)
    for batch in tqdm(batches):
        images = os.listdir(pathname + batch + '/Images/')
        for image in images:
            image_name = pathname + batch + '/Images/' + image
            img = Image.open(image_name)
            img.seek(2)
            text = pytesseract.image_to_string(img)
            text = text.replace('\n\n', '\n')
            tf = open('Pueblo_text/' + batch + '_' + image[0:18] + '.txt', 'w')
            tf.write(text)
            tf.close()

def main():
    #change pathnames as necessary
    pathname1 = 'Pueblo/Project ICC 101/'
    pathname2 = 'Pueblo/Project ICC 201/'
    extract(pathname1)
    extract(pathname2)

if __name__ == "__main__":
    main()