#!/usr/bin/python3
# coding: utf-8

import pytesseract
import os
import argparse
try:
    import Image, ImageOps, ImageEnhance, imread
except ImportError:
    from PIL import Image, ImageOps, ImageEnhance

def solve_captcha(path):

    """
    Convert a captcha image into a text,
    using PyTesseract Python-wrapper for Tesseract

    Arguments:
        path (str):
            path to the image to be processed
    Return:
        'textualized' image

    """
    image = Image.open(path).convert('RGB')
    image = ImageOps.autocontrast(image)

    filename = "{}.png".format(os.getpid())
    image.save(filename)

    captchatext = str(pytesseract.image_to_string(Image.open(filename)))
    return captchatext


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--image", required=True, help="path to input image to be OCR'd")
    args = vars(argparser.parse_args())
    path = args["image"]
    print('-- Resolving')
    captcha_text = solve_captcha(path)
    print('-- Result: {}'.format(captcha_text))
