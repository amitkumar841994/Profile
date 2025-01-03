from fastapi import APIRouter,Depends,Request
from authentication.models import NewUser,UserLogin
import uuid
from config import db
from utils.password import pwd_context




class NewUserRegistration:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/items", self.register, methods=["POST"])
        # self.router.add_api_route("/items", self.create_item, methods=["POST"])

    async def register(self, new_user:NewUser):
            if not new_user.user_id:
                new_user.user_id = uuid.uuid4()

            try:
                result = db.User.find_one({ '$or': [{'email':new_user.email}, {'mobile':new_user.mobile}]})
                print("User>>>>>>>", result)
                if result:
                    if new_user.email== result['email'] :
                        return {  "message": f"{new_user.email} already registered"}
                    if new_user.mobile== result['mobile'] :
                        return {  "message": f"{new_user.mobile} already registered"}   
                else :   
                    new_user.password =pwd_context.hash(new_user.password)  
                    result = db.User.insert_one(new_user.model_dump())
                    return {
                    "message": "registered successfully",
                    "data": new_user.model_dump()
                    }
            except Exception as e:
                 print("Error inserting",e)
        
            return {
                "message": "Item created",
                "data": new_user.model_dump()
            }
    async def user_login(self,login:UserLogin):
         pass
         
