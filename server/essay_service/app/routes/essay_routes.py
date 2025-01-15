from fastapi import APIRouter, HTTPException
import logging
from ..schemas.essay_schema import CreateEssayRequest, EssayResponse
from ..repositories.essay_repository import EssayRepository

router = APIRouter()
essay_repository = EssayRepository()

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy"}

@router.post("/essays", response_model=dict)
async def create_essay(request: CreateEssayRequest):
   try:
       logging.info(f"Received request data: {request.model_dump_json()}")
       essay_id = await essay_repository.create_essay(request)
       logging.info(f"Created essay with ID: {essay_id}")
       
       return {
           "message": "자기소개서가 성공적으로 저장되었습니다",
           "essay_id": essay_id
       }
       
   except Exception as e:
       print(f"Error creating essay: {str(e)}")  # 에러 로깅
       raise HTTPException(
           status_code=500,
           detail=f"Failed to create essay: {str(e)}"
       )
