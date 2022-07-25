import cv2
import numpy as np
from webcolors import name_to_rgb

import argparse
import datetime
import os
import pathlib
import sys


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("--input_dir", "-i", help="Input QR Code image dir", type=pathlib.Path, default="./input")
    parse.add_argument("--output-dir", "-o", help="Hidden QR output dir", type=pathlib.Path, default="./output")
    parse.add_argument("--fill-color", "-c", help="Fill color (Based on Color Names)", default="white")

    # init
    args = parse.parse_args()
    input_dir_path = args.input_dir
    output_dir_path = args.output_dir
    rgb = list(name_to_rgb(args.fill_color))
    rgb[0], rgb[2] = rgb[2], rgb[0]
    bgr = rgb
    output_dir_name = datetime.datetime.today().strftime("%Y%m%d_%H%M%S_exported")
    output_path = output_dir_path / output_dir_name

    # check exists directory
    if not input_dir_path.exists():
        print("please check input dir path.")
        sys.exit(0)
    if not output_dir_path.exists():
        # create output directory
        os.makedirs(output_dir_path.absolute())
    if not output_path.exists():
        os.makedirs(output_path.absolute())

    # get jpg/png image
    qr_images = [p for p in input_dir_path.iterdir() if p.suffix in [".jpg", ".png"]]

    # read qr code
    qr = cv2.QRCodeDetector()
    for qr_image in qr_images:
        img = cv2.imread(str(qr_image.absolute()), cv2.IMREAD_COLOR)
        data, points, straight_qrcode = qr.detectAndDecode(img)

        # fill qr code
        points = points.astype(int)
        img = cv2.fillPoly(img, [points], tuple(bgr))
        cv2.imwrite(f"{str(output_path.absolute())}/{qr_image.name}", img)
