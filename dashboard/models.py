from pydantic import BaseModel,Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class UserExperienceModel(BaseModel):
    userexp_id: UUID = Field(default_factory=uuid4)
    user_id : UUID
    title : str
    employment_type :str
    company_name :str 
    start_month :str
    start_year : str
    end_month :Optional[str] = None
    end_year : Optional[str] = None
    location :str
    working : bool



class UserFileUpload(BaseModel):
    user_id: str
    file_name: str
    upload_time: Optional[datetime] = None
    file_size: Optional[int] = None
    description: Optional[str] = None
