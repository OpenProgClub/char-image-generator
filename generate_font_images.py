from utils.characters import Characters
from utils.font_info import FontInfo
from utils.utils import get_datetime_prefix

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

import os
import traceback


def code_to_filename(code, font_name, ext='.png'):
    hexstr = hex(code)[2:]
    return hexstr + '_' + str(code) + '_' + font_name + ext


class ImageGenerator:
    def __init__(self, font_path, size=(110, 110), ratio=.8):
        self.font_path = font_path
        self.size = size
        self.ratio = ratio
        self.font_size = int(size[0] * ratio)
        self.font = ImageFont.truetype(
            font_path, self.font_size, encoding='unic')

        family_name, font_name = self.font.getname()
        font_full_name = family_name + '-' + font_name
        self.font_full_name = font_full_name.replace(' ', '-')

    def generate_image(self, code, savedir='.'):
        image = Image.new('L', self.size, color=255)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), chr(code), font=self.font, fill=0)

        # check something is drawn
        img_cv = np.asarray(image)
        assert not np.all(img_cv == 255)

        img_center = self.centering_image(img_cv)

        savefile = code_to_filename(code, self.font_full_name)
        cv2.imwrite(os.path.join(savedir, savefile), img_center)

    def centering_image(self, img):
        img_flip = 255 - img
        _, img_thr = cv2.threshold(img_flip, 1, 255, cv2.THRESH_BINARY)
        contours = cv2.findContours(
                img_thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = cv2.boundingRect(contours[0])
        crop = img[y: y + h, x: x + w]

        ho, wo = img.shape[0], img.shape[1]

        # upper left xy of cropped image
        yc = int((ho - h) // 2)
        xc = int((wo - w) // 2)

        img_new = np.ones(img.shape) * 255
        img_new[yc: yc + h, xc: xc + w] = crop

        return img_new


if __name__ == '__main__':
    savedir = '../data/font_images'
    font_dir = '../data/fonts'

    image_size = 28, 28  # Output picture size
    char_ratio = .8  # Character size ratio

    #char_types = ['hiragana_basic']
    char_types = ['hiragana_basic',  'katakana_basic',
                  'alphabets', 'digits', 'kanji_joyo']
    use_codes = Characters.combine_codes(char_types)
    print('Number of codes: ' + str(len(use_codes)))

    font_files = os.listdir(font_dir)
    all_covered = []  # Store font paths that covered all
    load_failed = []  # Store font paths that failed to load
    for font_file in font_files:
        _, ext = os.path.splitext(font_file)
        if ext.lower() not in ['.ttf', '.otf', '.ttc']:
            continue

        font_path = os.path.join(font_dir, font_file)
        try:
            font_info = FontInfo(font_path)
            ig = ImageGenerator(
                    font_path, size=image_size, ratio=char_ratio)
        except:
            print('Could not load font: ' + font_path)
            load_failed.append(font_path)
            continue

        for c in use_codes:
            is_fail = False
            if not font_info.is_char_exist(chr(c)):
                print('Not exists: ' + chr(c) + ' in ' + font_path)
                is_fail = True
                continue
            try:
                ig.generate_image(c, savedir=savedir)
            except:
                print('Error in generating image: ' + chr(c) + ' ' + font_path)
                print(traceback.format_exc())
                is_fail = True
                continue
        if not is_fail:
            print('All char is covered: ' + font_path)
            all_covered.append(font_path + ',' + ig.font_full_name)
    print('Done. Number of all covered font is ' + str(len(all_covered)))

    pref = get_datetime_prefix()
    with open(pref + '_all_covered_fonts.txt', 'w') as f:
        f.write('\n'.join(all_covered))

    with open(pref + '_char_list.txt', 'w') as f:
        f.write('\n'.join(char_types))
        f.write('\n')
        char_list = [chr(i) for i in use_codes]
        f.write(''.join(char_list))
