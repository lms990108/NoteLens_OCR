from fastapi import APIRouter, File, UploadFile
from typing import List
import os

from service.ocrService import OCRService

# OCR 서비스 인스턴스화
ocr_service = OCRService()

ocr_router = APIRouter()

@ocr_router.post("/ocr", response_model=List[str])
async def process_image(file: UploadFile = File(...)):
    # 임시 저장할 파일 경로
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # OCR 실행
    texts = ocr_service.perform_ocr(temp_file_path)
    
    # 임시 파일 삭제
    os.remove(temp_file_path)
    
    # 인식된 텍스트 리스트 반환
    return texts
