# QRCode Hidden Tool

QRコードを隠す（塗りつぶす）ツール

![image](./docs/qr_hidden_img.jpg)

# Env

- Python3.9.13

# Preparation

```bash
git clone https://github.com/ijiwarunahello/qrcode_hidden.git
git submodule update -i
python -m venv .venv
pip install -r requirements.txt
```

# Quick use

1. `./input/`フォルダに処理したい画像を入れる
1. プログラム実行（`python qrcode_hidden.py`）
1. 処理された画像が`./output/`に保存される

## Usage

```bash
❯ python qrcode_hidden.py -h
usage: qrcode_hidden.py [-h] [--input_dir INPUT_DIR] [--output-dir OUTPUT_DIR] [--fill-color FILL_COLOR] [--detect-prototxt DETECT_PROTOTXT] [--detect-caffemodel DETECT_CAFFEMODEL] [--sr-prototxt SR_PROTOTXT] [--sr-caffemodel SR_CAFFEMODEL]

optional arguments:
  -h, --help            show this help message and exit
  --input_dir INPUT_DIR, -i INPUT_DIR
                        Input QR Code image dir
  --output-dir OUTPUT_DIR, -o OUTPUT_DIR
                        Hidden QR output dir
  --fill-color FILL_COLOR, -c FILL_COLOR
                        Fill color (Based on Color Names)
  --detect-prototxt DETECT_PROTOTXT
                        WeChatQRCode detect.prototxt file path
  --detect-caffemodel DETECT_CAFFEMODEL
                        WeChatQRCode detect.caffemodel file path
  --sr-prototxt SR_PROTOTXT
                        WeChatQRCode sr.prototxt file path
  --sr-caffemodel SR_CAFFEMODEL
                        WeChatQRCode sr.caffemodel file path
```

| argument | type | value | detail |
| :--- | :--- | :--- | :--- |
| `--input_dir, -i` | Optional | `./input` | 入力画像のフォルダ |
| `--output_dir, -o` | Optional | `./output` | 出力先フォルダ |
| `--fill-color, -c` | Optional | `white` | 塗りつぶす色名（カラーコードに準拠） |
| `--detect-prototxt` | Optional | `./opencv_3rdparty/detect.prototxt` | 検出器モデルのアーキテクチャファイル（WeChatQRCode用） |
| `--detect-caffemodel` | Optional | `./opencv_3rdparty/detect.caffemodel` | 検出器モデルの重みファイル（WeChatQRCode用） |
| `--sr-prototxt` | Optional | `./opencv_3rdparty/sr.prototxt` | 超解像モデルのアーキテクチャファイル（WeChatQRCode用） |
| `--sr-caffemodel` | Optional | `./opencv_3rdparty/sr.caffemodel` | 超解像モデルの重みファイル（WeChatQRCode用） |

# Other

## QRコードを差し替える

```bash
python qrcode_replace.py <入力画像> <差し替えたい情報>
```

例) [あるURL](https://www.hinatazaka46.com/s/official/artist/10)が開くQRコードに差し替えたい場合

```bash
python qrcode_replace.py input_image.jpg "https://www.hinatazaka46.com/s/official/artist/10"
```

| before | after |
| :--- | :--- |
| ![before](./docs/before.jpeg) | ![after](./docs/after.jpg) |

※自分のアカウントのQRコードです

### Usage

```bash
❯ python qrcode_replace.py -h
usage: qrcode_replace.py [-h] [--swap-qrcode-img SWAP_QRCODE_IMG] [--detect-prototxt DETECT_PROTOTXT] [--detect-caffemodel DETECT_CAFFEMODEL] [--sr-prototxt SR_PROTOTXT] [--sr-caffemodel SR_CAFFEMODEL] input_img embed_qr_data

positional arguments:
  input_img             Input image with QR Code
  embed_qr_data         Embedded data in QR Code

optional arguments:
  -h, --help            show this help message and exit
  --swap-qrcode-img SWAP_QRCODE_IMG
                        Swap QRCode image file
  --detect-prototxt DETECT_PROTOTXT
                        WeChatQRCode detect.prototxt file path
  --detect-caffemodel DETECT_CAFFEMODEL
                        WeChatQRCode detect.caffemodel file path
  --sr-prototxt SR_PROTOTXT
                        WeChatQRCode sr.prototxt file path
  --sr-caffemodel SR_CAFFEMODEL
                        WeChatQRCode sr.caffemodel file path
```