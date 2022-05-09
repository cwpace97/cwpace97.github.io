import sys
import glob
import math
from PIL import Image

def compress_image(img, desired_width):
    w, h = img.size
    resize_factor = w/desired_width
    new_w = math.ceil(w/resize_factor)
    new_h = math.ceil(h/resize_factor)
    img = img.resize((new_w, new_h))

    return img

def main(argv):
    path_to_astro = r'E:\FINAL OUTPUTS'
    path_to_web_dir = r'C:\Users\cwpac\OneDrive\Documents\Website\cwpace97.github.io\images\photos'
    try:
        pic_list = glob.glob(f'{path_to_astro}/*.jpg')
        print(pic_list)
    except:
        print('Failed to grab photo directory, make sure hard drive is plugged in!')

    #handle pictures
    for pic in pic_list:
        pic_name = pic.split("\\")[-1]
        img = Image.open(pic)
        img_compress = compress_image(img, 720)

        #save images
        img.save(path_to_web_dir +'\\full size\\'+pic_name, "JPEG")
        img_compress.save(path_to_web_dir +'\\compressed\\'+"CMPR_"+pic_name, "JPEG")

    #handle videos?
    

if __name__ == "__main__":
    main(sys.argv[1:])