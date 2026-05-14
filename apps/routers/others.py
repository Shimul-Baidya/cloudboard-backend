from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
def health():
    logger.info('GET request to /health')
    return {"status": "Okay"}