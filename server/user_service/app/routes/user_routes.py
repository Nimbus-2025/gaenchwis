from fastapi import APIRouter, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict
import logging
from ..repositories.user_repository import UserRepository
from ..schemas.user_schemas import ApplyCreate, ApplyResponse, ApplyUpdate, ApplyDetailResponse, EssayJobPostingResponse, BookmarkCreate, BookmarkResponse, InterestCompanyCreate, InterestCompanyResponse
from ..core.security.token_validator import TokenValidator

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

router = APIRouter()
user_repository = UserRepository()
token_validator = TokenValidator()

@router.get("/healthcheck")
async def healthcheck():
    return {"status": "healthy", "message": "건강합니다"}

def get_user_tokens(
    access_token: str | None = Header(None, alias="access_token", convert_underscores=False), 
    id_token: str | None = Header(None, alias="id_token", convert_underscores=False),
    user_id: str | None = Header(None, alias="user_id", convert_underscores=False)
) -> Dict[str, str]:
    logger.info("Validating user tokens...")
    
    # 필수 헤더 확인
    if not access_token:
        logger.error("Missing access_token header")
        raise HTTPException(status_code=401, detail="access_token is required")
    if not id_token:
        logger.error("Missing id_token header")
        raise HTTPException(status_code=401, detail="id_token is required")
    if not user_id:
        logger.error("Missing user_id header")
        raise HTTPException(status_code=401, detail="user_id is required")
    
    try:
        logger.info(f"Attempting to validate token for user: {user_id}")
        validator = TokenValidator()
        decoded_token = validator.decode_and_validate_token(id_token)
        
        # 토큰에서 추출한 user_id와 헤더의 user_id가 일치하는지 확인
        token_user_id = decoded_token.get('cognito:username')
        logger.info(f"Token user_id: {token_user_id}, Header user_id: {user_id}")
        
        if user_id != token_user_id:
            logger.error(f"User ID mismatch. Token: {token_user_id}, Header: {user_id}")
            raise HTTPException(status_code=401, detail="Invalid user ID")
        
        logger.info("Token validation successful")
        return {
            "access_token": access_token,
            "id_token": id_token,
            "user_id": user_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/apply")
def create_apply(
    apply_data: ApplyCreate, 
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        # 이미 지원한 공고인지 확인
        existing_apply = user_repository.get_apply(
            tokens["user_id"],
            apply_data.post_id
        )
        if existing_apply:
            raise HTTPException(
                status_code=400,
                detail="Already applied to this job posting"
            )
            
        # 새로운 지원 생성
        created_apply = user_repository.create_apply(
            tokens["user_id"],
            apply_data
        )
        
        return ApplyResponse(**created_apply)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/apply/{post_id}")
def cancel_apply(
    post_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        # 지원 내역이 있는지 확인
        existing_apply = user_repository.get_apply(
            tokens["user_id"],
            post_id
        )
        if not existing_apply:
            raise HTTPException(
                status_code=404,
                detail="지원 내역을 찾을 수 없습니다"
            )
            
        # 지원 취소(삭제)
        success = user_repository.delete_apply(
            tokens["user_id"],
            post_id
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="지원 취소 중 오류가 발생했습니다"
            )
            
        return {"message": "지원이 취소되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.patch("/apply/{post_id}")
def update_apply(
    post_id: str,
    apply_data: ApplyUpdate,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        # 지원 내역이 있는지 확인
        existing_apply = user_repository.get_apply(
            tokens["user_id"],
            post_id
        )
        if not existing_apply:
            raise HTTPException(
                status_code=404,
                detail="지원 내역을 찾을 수 없습니다"
            )
            
        # 지원 내역 업데이트
        updated_apply = user_repository.update_apply(
            tokens["user_id"],
            post_id,
            apply_data
        )
        
        if not updated_apply:
            raise HTTPException(
                status_code=500,
                detail="지원 내역 수정 중 오류가 발생했습니다"
            )
            
        return ApplyResponse(**updated_apply)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.get("/apply-result/{post_id}", response_model=ApplyDetailResponse)
def get_apply_detail(
    post_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        # post_id에서 공백과 개행 문자 제거
        cleaned_post_id = post_id.strip()
        
        apply_detail = user_repository.get_apply_detail(
            tokens["user_id"],
            cleaned_post_id
        )
        
        if not apply_detail:
            raise HTTPException(
                status_code=404,
                detail="지원 내역을 찾을 수 없습니다"
            )
            
        return ApplyDetailResponse(**apply_detail)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/apply/{post_id}/essays")
def get_essays_by_post(
    post_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        # post_id 공백 제거 (이전 이슈 방지)
        cleaned_post_id = post_id.strip()
        
        essays = user_repository.get_essays_by_post(
            tokens["user_id"],
            cleaned_post_id
        )
        
        if not essays:
            return EssayJobPostingResponse(essays=[])
            
        return EssayJobPostingResponse(essays=essays)
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.post("/bookmark")
def create_bookmark(
    bookmark_data: BookmarkCreate,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        # 이미 북마크한 공고인지 확인
        existing_bookmark = user_repository.get_bookmark(
            tokens["user_id"],
            bookmark_data.post_id
        )
        if existing_bookmark:
            raise HTTPException(
                status_code=400,
                detail="이미 북마크된 공고입니다"
            )
            
        # 새로운 북마크 생성
        created_bookmark = user_repository.create_bookmark(
            tokens["user_id"],
            bookmark_data
        )
        
        return BookmarkResponse(**created_bookmark)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.delete("/bookmark/{post_id}")
def delete_bookmark(
    post_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        # 북마크가 있는지 확인
        existing_bookmark = user_repository.get_bookmark(
            tokens["user_id"],
            post_id
        )
        if not existing_bookmark:
            raise HTTPException(
                status_code=404,
                detail="북마크를 찾을 수 없습니다"
            )
            
        # 북마크 삭제
        success = user_repository.delete_bookmark(
            tokens["user_id"],
            post_id
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="북마크 삭제 중 오류가 발생했습니다"
            )
            
        return {"message": "북마크가 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.get("/bookmarks")
def get_user_bookmarks(
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        bookmarks = user_repository.get_user_bookmarks(tokens["user_id"])
        return {"bookmarks": [BookmarkResponse(**bookmark) for bookmark in bookmarks]}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.post("/interest-company")
def create_interest_company(
    company_data: InterestCompanyCreate,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        existing_company = user_repository.get_interest_company(
            tokens["user_id"],
            company_data.company_id
        )
        if existing_company:
            raise HTTPException(
                status_code=400,
                detail="이미 관심기업으로 등록된 기업입니다"
            )
            
        created_company = user_repository.create_interest_company(
            tokens["user_id"],
            company_data
        )
        
        return InterestCompanyResponse(**created_company)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.delete("/interest-company/{company_id}")
def delete_interest_company(
    company_id: str,
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        existing_company = user_repository.get_interest_company(
            tokens["user_id"],
            company_id
        )
        if not existing_company:
            raise HTTPException(
                status_code=404,
                detail="관심기업을 찾을 수 없습니다"
            )
            
        success = user_repository.delete_interest_company(
            tokens["user_id"],
            company_id
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="관심기업 삭제 중 오류가 발생했습니다"
            )
            
        return {"message": "관심기업이 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/interest-companies")
def get_user_interest_companies(
    tokens: Dict = Depends(get_user_tokens)
):
    try:
        companies = user_repository.get_user_interest_companies(tokens["user_id"])
        return {"companies": [InterestCompanyResponse(**company) for company in companies]}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

# CORS preflight 요청을 처리하는 핸들러 
@router.options("/{full_path:path}")
def options_handler(full_path: str):
    return JSONResponse(
        content={"message": "OK"},
        status_code=200
    )