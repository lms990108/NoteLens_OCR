from paddleocr import PaddleOCR
from PIL import Image

class OCRService:
    def __init__(self):
        # 한국어 OCR을 위한 PaddleOCR 초기화
        self.ocr = PaddleOCR(use_angle_cls=True, lang='korean')

    def perform_ocr(self, image_path):
        # 이미지에서 텍스트 인식
        result = self.ocr.ocr(image_path, cls=True)
        # 결과 처리
        extracted_texts = []
        for line in result:
            for word in line:
                extracted_texts.append(word[1][0])  # 텍스트 정보만 추출
        return extracted_texts
