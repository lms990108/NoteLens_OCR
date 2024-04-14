from fastapi import APIRouter, File, UploadFile, HTTPException
import requests
from typing import List
import os
from io import BytesIO

from ..service.ocrService import OCRService

# OCR 서비스 인스턴스화
ocr_service = OCRService()
ocrRouter = APIRouter()

@ocrRouter.post("/", response_model=List[str])
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

@ocrRouter.post("/url", response_model=List[str])
async def process_image_from_url(image_url: str):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # 에러가 발생하면 HTTPException을 발생시킵니다.
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    image_bytes = BytesIO(response.content)
    image_path = f"temp_{image_url.split('/')[-1]}"
    
    with open(image_path, 'wb') as image_file:
        image_file.write(image_bytes.read())

    texts = ocr_service.perform_ocr(image_path)
    
    os.remove(image_path)
    
    return texts
