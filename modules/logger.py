# modules/logger.py
import logging
import os

def get_logger(name="MLB_Engine"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # 파일 핸들러 (logs/ 폴더에 저장)
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/pipeline.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # 콘솔 핸들러
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        
    return logger
