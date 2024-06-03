from fastapi import APIRouter, File, UploadFile, HTTPException, status, Response
import requests
from typing import List, Dict
import os
from io import BytesIO

from app.service.ocrService import OCRService

# 로깅 설정
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# OCR 서비스 인스턴스화
ocr_service = OCRService()
ocrRouter = APIRouter()

@ocrRouter.post("/ocr", response_model=str)
async def process_image(file: UploadFile = File(...)):
    
    if not file:
        logger.error("No file uploaded")
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    # 임시 저장할 파일 경로
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # OCR 실행
    try:
        texts = ocr_service.perform_ocr(temp_file_path)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Error occurred during OCR")
    finally:
        # 임시 파일 삭제
        os.remove(temp_file_path)
    
    # 인식된 텍스트 리스트 반환
    return texts


@ocrRouter.post("/ocr-from-url", response_model=str)
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

    try:
        texts = ocr_service.perform_ocr(image_path)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Error occurred during OCR")
    finally:
        os.remove(image_path)
    
    return texts

@ocrRouter.post("/ocr-multi", response_model=Dict[str, str])
async def process_multi_images(files: List[UploadFile] = File(...)):
    
    if not files:
        logger.error("No files uploaded")
        raise HTTPException(status_code=400, detail="No files uploaded")
    
    logger.info("Files uploaded")
    
    result_texts = {}
    
    # files 리스트 순회
    for file in files:
        # 파일 임시 저장
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # OCR 실행 및 결과 저장
        try:
            file_texts = ocr_service.perform_ocr(temp_file_path)
            if len(file_texts) > 2:
                result_texts[file.filename] = file_texts
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            # result_texts[file.filename] = "Error occurred during OCR. This file is skipped."
        finally:
            # 임시 파일 삭제
            os.remove(temp_file_path)
    
    logger.info(result_texts)
    
    return result_texts