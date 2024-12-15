
import cv2
import pytesseract
from PIL import Image
import numpy as np


# 设置Tesseract的路径
pytesseract.pytesseract.tesseract_cmd = r'E:\test\ocr文本识别系统\Tesseract-OCR\tesseract.exe'


def load_image(image_path):
    # 使用 PIL 加载图像
    img = Image.open(image_path)
    return np.array(img)  # 转换为 NumPy 数组


def preprocess_image(image_path):
    # 读取图像
    img = load_image(image_path)
    if img is None:
        raise ValueError(f"Image not found or unable to open: {image_path}")
    # 转为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二值化（阈值处理）
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # 去噪
    denoise = cv2.fastNlMeansDenoising(binary, h=30)

    return denoise


def ocr_image(image):
    # 使用Pytesseract进行OCR识别
    text = pytesseract.image_to_string(image, lang='chi_sim+eng')
    return text


def ocr(image_path):
    # 预处理图像
    processed_image = preprocess_image(image_path)
    # 使用OCR识别文字
    recognized_text = ocr_image(processed_image)
    return recognized_text
