from pydantic import BaseModel,Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional


class UserExpericeModel(BaseModel):
    userexp_id: UUID = Field(default_factory=uuid4)
    user_id : UUID
    company_name :str 
    title :str
    start_date :datetime
    end_date :datetime
    description :str


class UserFileUpload(BaseModel):
    user_id: str
    file_name: str
    upload_time: Optional[datetime] = None
    file_size: Optional[int] = None
    description: Optional[str] = None