from pydantic import BaseModel,Field
from uuid import UUID, uuid4


class NewUser(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)  # type: ignore
    first_name : str
    last_name : str
    email : str
    mobile : str
    password : str

class UserLogin(BaseModel):
    username:str|None = None
    password:str
    email:str|None =None
