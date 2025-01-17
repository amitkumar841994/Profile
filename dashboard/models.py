from pydantic import BaseModel,Field
from uuid import UUID, uuid4
from datetime import datetime

class UserExpericeModel(BaseModel):
    userexp_id: UUID = Field(default_factory=uuid4)
    user_id : UUID
    company_name :str 
    title :str
    start_date :datetime
    end_date :datetime
    description :str