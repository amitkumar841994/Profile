from fastapi import APIRouter,Depends,Request
from authentication.models import NewUser
import uuid
from config import db




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

