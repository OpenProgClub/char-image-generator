import subprocess
import os

# NOTE: ImageMagick is required

if __name__ == '__main__':
    filename = '2017-04-20-10-41-09_all_covered_fonts.txt'
    savedir = '../data/font_summary_images'

    if not os.path.exists(savedir):
        os.mkdir(savedir)

    with open(filename, 'r') as f:
        lines = f.read().split('\n')

    for line in lines:
        _,  font_name = line.split(',')
        save_path = os.path.join(savedir, font_name + '.png')
        imgs = os.path.join('../data/font_images', '*' + font_name + '*.png')
        command = [
                'montage',
                '-mode',
                'concatenate', '-tile', '60x40',
                imgs, save_path]

        print(' '.join(command))
        subprocess.call(command)
