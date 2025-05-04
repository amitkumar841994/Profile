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
    start_date :datetime
    end_date :datetime
    location :str



class UserFileUpload(BaseModel):
    user_id: str
    file_name: str
    upload_time: Optional[datetime] = None
    file_size: Optional[int] = None
    description: Optional[str] = None
