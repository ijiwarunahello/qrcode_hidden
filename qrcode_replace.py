import qrcode
from PIL import Image, ImageOps
import cv2

import argparse
import pathlib
from urllib.parse import urlparse

DUMMY_QRCODE_NAME = "dummy_qrcode.png"


if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument("input_img", help="Input image with QR Code", type=pathlib.Path)
    parse.add_argument("embed_qr_data", help="Embedded data in QR Code")
    parse.add_argument("--swap-qrcode-img", help="Swap QRCode image file", type=pathlib.Path, default=DUMMY_QRCODE_NAME)
    parse.add_argument("--detect-prototxt", help="WeChatQRCode detect.prototxt file path", type=pathlib.Path, default="./opencv_3rdparty/detect.prototxt")
    parse.add_argument("--detect-caffemodel", help="WeChatQRCode detect.caffemodel file path", type=pathlib.Path, default="./opencv_3rdparty/detect.caffemodel")
    parse.add_argument("--sr-prototxt", help="WeChatQRCode sr.prototxt file path", type=pathlib.Path, default="./opencv_3rdparty/sr.prototxt")
    parse.add_argument("--sr-caffemodel", help="WeChatQRCode sr.caffemodel file path", type=pathlib.Path, default="./opencv_3rdparty/sr.caffemodel")

    # init
    args = parse.parse_args()
    input_img = args.input_img
    qr = cv2.wechat_qrcode.WeChatQRCode(
        str(args.detect_prototxt.absolute()),
        str(args.detect_caffemodel.absolute()),
        str(args.sr_prototxt.absolute()),
        str(args.sr_caffemodel.absolute())
    )
    embed_data = args.embed_qr_data

    # generate qr code
    image_qr = qrcode.make(embed_data)

    try:
        # detect qr code
        img = cv2.imread(str(input_img.absolute()))
        data, points = qr.detectAndDecode(img)

        if data == "":
            print("detection failed.")
        else:
            points = points[0]
        points = points.astype(int)

        # resize dummy qr
        qr_w = points[1][0] - points[0][0]
        qr_h = points[2][1] - points[1][1]
        image_qr = image_qr.get_image().resize((qr_w, qr_h))

        # swap qrcode
        base_img = Image.open(str(input_img.absolute()))
        base_img = ImageOps.exif_transpose(base_img)
        pos = (points[0][0], points[0][1])
        base_img.paste(image_qr, pos)
        base_img.save("qr_replaced.jpg")
    except Exception as e:
        print(e)