from fastapi import APIRouter, Header, Depends, HTTPException, Body, Query
from typing import Dict, Optional
import logging
from ..schemas.essay_schema import CreateEssaysRequest, UpdateEssayRequest, SortOrder, EssayListResponse, EssayDetailResponse, SearchType
from ..repositories.essay_repository import EssayRepository

router = APIRouter()
essay_repository = EssayRepository()

@router.options("/{path:path}")
def preflight():
    return {"status": "ok", "message": "Preflight"}

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy", "message": "건강합니다"}

def get_user_tokens(
    access_token: str | None = Header(None, alias="access_token", convert_underscores=False), 
    id_token: str | None = Header(None, alias="id_token", convert_underscores=False),
    user_id: str | None = Header(None, alias="user_id", convert_underscores=False)
) -> Dict[str, str]:
    # 헤더에서 토큰 정보를 가져오는 헬퍼 함수
    if not access_token or not id_token:
        raise HTTPException(status_code=401, detail="Authentication tokens required")
    logging.info("토큰 검증 완료") 
    return {"access_token": access_token, "id_token": id_token, "user_id": user_id}

@router.get("/applied-jobs")
def get_user_applied_jobs(
    tokens: Dict = Depends(get_user_tokens),
):
    try:
        applied_jobs = essay_repository.get_user_applied_jobs(tokens["user_id"])
        
        return {
            "message": "지원한 채용공고 목록을 성공적으로 조회했습니다",
            "applied_jobs": applied_jobs
        }
    except Exception as e:
        logging.error(f"Error getting applied jobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get applied jobs: {str(e)}"
        )

@router.post("/essays")
def create_essay(
    request_body: CreateEssaysRequest = Body(...),  # Body(...) 명시적으로 지정
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        user_id = tokens["user_id"]
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        print(f"Creating essay for user: {user_id}")
        logging.info(f"Creating essay for user: {user_id}")

        # job_posting_ids 대신 job_postings 사용
        essay_ids = essay_repository.create_essays_and_links(
            user_id=user_id,
            questions=[question.dict() for question in request_body.questions],
            job_postings=[posting.dict() for posting in request_body.job_postings] if request_body.job_postings else None
        )
        
        logging.info(f"Created essay with ID: {user_id}")

        return {
            "message": "자기소개서가 성공적으로 저장되었습니다",
            "essay_ids": essay_ids
        }
        
    except Exception as e:
        print(f"Error creating essay: {str(e)}")  # 에러 로깅
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create essay: {str(e)}"
        )

@router.patch("/essays/{essay_id}")
async def update_essay(
    essay_id: str,
    request_body: UpdateEssayRequest = Body(...),
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        user_id = tokens["user_id"]
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        # None이 아닌 필드만 추출
        update_data = request_body.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400, 
                detail="No fields to update provided"
            )
        
        logging.info(f"Updating essay {essay_id} for user: {user_id}")
        
        essay_repository.update_essay(
            user_id=user_id,
            essay_id=essay_id,
            update_data=update_data
        )
        
        return {
            "message": "자기소개서가 성공적으로 수정되었습니다",
            "essay_id": essay_id
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error updating essay: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update essay: {str(e)}"
        )
        
@router.delete("/essays/{essay_id}")
async def delete_essay(
    essay_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        user_id = tokens["user_id"]
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        logging.info(f"Deleting essay {essay_id} for user: {user_id}")
        
        essay_repository.delete_essay(
            user_id=user_id,
            essay_id=essay_id
        )
        
        return {
            "message": "자기소개서가 성공적으로 삭제되었습니다",
            "essay_id": essay_id
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error deleting essay: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete essay: {str(e)}"
        )

@router.get("/essays/search", response_model=EssayListResponse)
def search_essays(
    search_type: SearchType = Query(..., description="검색 유형 (question/content)"),
    keyword: str = Query(..., description="검색어"),
    sort_order: SortOrder = Query(SortOrder.DESC, description="정렬 순서"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=50, description="페이지당 항목 수"),
    tokens: Dict = Depends(get_user_tokens)
):
    if not keyword or keyword.strip() == "":
        raise HTTPException(status_code=400, detail="검색어를 입력해주세요")
    
    try:
        result = essay_repository.search_essays(
            user_id=tokens["user_id"],
            search_type=search_type,
            keyword=keyword.strip(),  
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/essays", response_model=EssayListResponse)
def get_essay_list(
    tokens: Dict = Depends(get_user_tokens),
    sort_order: SortOrder = Query(SortOrder.DESC, description="정렬 순서 (desc: 최신순, asc: 오래된순)"),
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=10, description="페이지당 항목 수")
):
    try:
        user_id = tokens["user_id"]
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")
            
        logging.info(f"Fetching essay list for user: {user_id}, page: {page}")
        
        result = essay_repository.get_essay_list(
            user_id=user_id,
            sort_order=sort_order,
            page=page,
            page_size=page_size
        )
        
        return result
        
    except Exception as e:
        logging.error(f"Error fetching essay list: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch essay list: {str(e)}"
        )

@router.get("/essays/{essay_id}", response_model=EssayDetailResponse)
async def get_essay_detail(
    essay_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        user_id = tokens["user_id"]
        if not user_id:
            raise HTTPException(status_code=401, detail="User not authenticated")
        
        logging.info(f"Fetching essay detail for essay: {essay_id}, user: {user_id}")
        
        result = essay_repository.get_essay_detail(
            user_id=user_id,
            essay_id=essay_id
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logging.error(f"Error fetching essay detail: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch essay detail: {str(e)}"
        )
