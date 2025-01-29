from typing import TypedDict, Optional
from datetime import datetime

class User(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    
    # Attributes
    user_id: str                # user_id
    user_sns: Optional[str]     # 로그인 SNS 종류
    user_name: str              # 유저 이름
    user_phone: Optional[str]   # 유저 핸드폰 번호
    user_email: str             # 유저 이메일 
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys: UserIndex
    GSI1PK: str          # USER#ALL
    GSI1SK: str          # <created_at>

class UserTag(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # TAG#<tag_id>
    
    # Attributes
    user_id: str            # user_id
    tag_id: str             # 유저가 선택한 tag_id
    created_at: datetime
    
    # GSI Keys: UserTagIndex
    GSI1PK: str          # TAG#<tag_id>
    GSI1SK: str          # USER#<user_id>

class InterestCompany(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # COMPANY#<company_id>
    
    # Attributes
    user_id: str            # user_id
    company_id: str         # 유저의 관심기업 company_id
    company_name: str       # 기업명
    created_at: datetime
    
    # GSI Keys: InterestCompanyIndex
    GSI1PK: str          # COMPANY#<company_id>
    GSI1SK: str          # USER#<user_id>

class Schedule(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # SCHEDULE#<schedule_id>
    
    # Attributes
    schedule_id: str            # 해당 유저의 schedule_id
    user_id: str                # user_id
    schedule_date: datetime     # 일정 날짜
    schedule_title: str         # 일정 이름
    schedule_content: str       # 일정 내용
    is_completed: bool          # 일정 완료 여부 
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys: ScheduleIndex
    GSI1PK: str          # SCHEDULE#ALL
    GSI1SK: str          # <schedule_date>

class Bookmark(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # POST#<post_id>
    
    # Attributes
    user_id: str            # user_id
    post_id: str            # 유저의 북마크 공고 post_id
    post_name: str          # 공고명
    created_at: datetime
    
    # GSI Keys: BookmarkIndex
    GSI1PK: str          # POST#<post_id>
    GSI1SK: str          # USER#<user_id>

class Applies(TypedDict):
    # Primary Key
    PK: str               # USER#<user_id>
    SK: str               # APPLY#<post_id>
    
    # Attributes
    user_id: str                                # user_id
    post_id: str                                # post_id
    post_name: str                              # 공고명
    deadline_date: Optional[datetime]           # 공고 마감일
    document_result_date: Optional[datetime]    # 서류 합격 발표 일정
    interview_date: Optional[datetime]          # 면접 일정
    final_date: Optional[datetime]              # 최종 발표 일정
    memo: Optional[str]                         # 공고 일정 메모 
    created_at: datetime
    updated_at: datetime
    
    # GSI Keys: ApplyIndex
    GSI1PK: str          # POST#<post_id>
    GSI1SK: str          # <apply_date>