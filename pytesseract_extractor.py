import os
from PIL import Image
import pytesseract
from tqdm import tqdm

#extract text from every ballot scan for every batch in the provided directory pathname
def extract(pathname, done_dir = 'Pueblo_text/'):
    batches = os.listdir(pathname)
    done = os.listdir(done_dir)
    for batch in tqdm(batches):
        if 'Batch' not in batch:
            continue
        images = os.listdir(pathname + batch + '/Images/')
        for image in images:
            if '.pdf' in image:
                print('pdf scan: ', image, '. Likely redacted?')
                continue
            if (batch + '_' + image[0:18] + '.txt') in done:
                done.remove(batch + '_' + image[0:18] + '.txt')
                continue
            image_name = pathname + batch + '/Images/' + image
            img = Image.open(image_name)
            img.seek(2)
            text = pytesseract.image_to_string(img)
            text = text.replace('\n\n', '\n')
            tf = open(done_dir + batch + '_' + image[0:18] + '.txt', 'w')
            tf.write(text)
            tf.close()

def main():
    #change pathnames as necessary
    
    #Pueblo:
    """
    pathname1 = 'Pueblo/Project ICC 101/'
    pathname2 = 'Pueblo/Project ICC 201/'
    extract(pathname1)
    extract(pathname2)
    """
    #June ICC ABS:
    pathname = 'June ICC ABS/'
    done_dir = 'June ICC ABS text/'
    extract(pathname, done_dir)


if __name__ == "__main__":
    main()