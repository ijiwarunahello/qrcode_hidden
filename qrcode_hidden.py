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
    parse.add_argument("--detect-prototxt", help="WeChatQRCode detect.prototxt file path", type=pathlib.Path, default="./opencv_3rdparty/detect.prototxt")
    parse.add_argument("--detect-caffemodel", help="WeChatQRCode detect.caffemodel file path", type=pathlib.Path, default="./opencv_3rdparty/detect.caffemodel")
    parse.add_argument("--sr-prototxt", help="WeChatQRCode sr.prototxt file path", type=pathlib.Path, default="./opencv_3rdparty/sr.prototxt")
    parse.add_argument("--sr-caffemodel", help="WeChatQRCode sr.caffemodel file path", type=pathlib.Path, default="./opencv_3rdparty/sr.caffemodel")

    # init
    args = parse.parse_args()
    input_dir_path = args.input_dir
    output_dir_path = args.output_dir
    rgb = list(name_to_rgb(args.fill_color))
    rgb[0], rgb[2] = rgb[2], rgb[0]
    bgr = rgb

    # check exists directory
    if not input_dir_path.exists():
        print("please check input dir path.")
        sys.exit(0)
    if not output_dir_path.exists():
        # create output directory
        os.makedirs(output_dir_path.absolute())

    # get jpg/png image
    qr_images = [p for p in input_dir_path.iterdir() if p.suffix in [".jpg", ".png"]]

    # read qr code
    qr = cv2.QRCodeDetector()
    qr_w = cv2.wechat_qrcode.WeChatQRCode(
        str(args.detect_prototxt.absolute()),
        str(args.detect_caffemodel.absolute()),
        str(args.sr_prototxt.absolute()),
        str(args.sr_caffemodel.absolute())
    )
    for qr_image in qr_images:
        try:
            img = cv2.imread(str(qr_image.absolute()))
            data, points, straight_qrcode = qr.detectAndDecode(img)

            if data == "":
                print("detect failed. use WeChatQRCode")
                # not detected, use WeChatQRCode
                data, points = qr_w.detectAndDecode(img)
                if data == "":
                    print("WeChatQRCode detect failed.")
                else:
                    points = points[0]

            # fill qr code
            points = points.astype(int)
            img = cv2.fillPoly(img, [points], tuple(bgr))
            cv2.imwrite(f"{str(output_dir_path.absolute())}/{qr_image.name}", img)

        except Exception as e:
            print(f"qr hidden failed: {e}, img_name: {qr_image}")
