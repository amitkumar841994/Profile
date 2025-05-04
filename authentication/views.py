from fastapi import APIRouter,Depends,Request,HTTPException
from authentication.models import NewUser,UserLogin
import uuid
from config import db
from utils.password import pwd_context,create_access_token,create_refresh_token
from utils.acess_token_handler import AccessToken
import json
from authentication.auth_config import google,oauth
from fastapi.responses import RedirectResponse
import uuid
import secrets

from dotenv import load_dotenv
import os
load_dotenv()

client_id=os.getenv("client_id"),
client_secret=os.getenv("client_secret")


class NewUserRegistration:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/register", self.register, methods=["POST"])
        self.router.add_api_route("/login", self.user_login, methods=["POST"])
        self.router.add_api_route("/login1", self.login, methods=["GET"])
        self.router.add_api_route("/auth_login", self.auth, methods=["GET"],name="login2")


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
                    "data": new_user.model_dump(),
                    "status_code":201
                    }
        except Exception as e:
            return {
                    "message": f"{str(e)}",
                    "status_code":500
                    }

    async def user_login(self,login:UserLogin):
        try:
            print(">>>>>>>>>",login)
            user_details = db.User.find_one(
                {"$or": [{"email": login.username}, {"mobile": login.username}]}
            )
            if user_details:
                is_valid = pwd_context.verify(login.password,user_details.get('password', ''))
                if is_valid:

                    user_data = {
                        "user_id": str(user_details["_id"]),
                        "email": user_details["email"]
                    }
                    access_token = AccessToken(create_access_token(user_data)).encrypt()
                    
                    refresh_token = AccessToken(create_refresh_token(user_data)).encrypt()
                    user_details["access_token"]=access_token
                    user_details["refresh_token"]=refresh_token
                    user_details.pop('_id')
                    return {
                        "message": "Login successful",
                        "UserDetails": user_details,
                        "status_code": 200
                    }
                else:
                    return {"message": "Username or Password is invalid", "status_code": 401}
                
            else:
                return {"message": "Not registerd user", "status_code": 400}


        except Exception as e:
            return {"message": f"{str(e)}", "status_code": 500}




    async def login(self, request: Request):
        print("Login endpoint accessed",client_id)  # Debugging log

        # Generate a unique state value
        state = secrets.token_urlsafe(16)
        print("Generated state:", state)  # Debugging log

        # Store the state in the session
        request.session['state'] = state

        # Generate the redirect URI dynamically
        redirect_uri = request.url_for("login2")  # Matches the route name for 'auth_login'
        print("Redirect URI:", redirect_uri)  # Debugging log

        authorization_url = await google.create_authorization_url(redirect_uri, state=state)

    # Redirect to Google OAuth URL
        # return RedirectResponse(authorization_url)
        print("Google Auth URL:",authorization_url )  # Debugging log

        # Redirect to Google OAuth
        return RedirectResponse(str(authorization_url))



    async def auth(self, request: Request):
        # Fetch the state from session and received state from URL
        state_sent = request.session.get('state')
        state_received = request.query_params.get('state')

        print("state checking",state_received, state_sent)
        
        # Compare state values
        if state_sent != state_received:
            raise HTTPException(status_code=400, detail="CSRF token mismatch")
        
        # Proceed with OAuth token exchange
        try:
            print("OAuth token exchange>>>>>")
            token = await google.authorize_access_token(request)
            print("OAuth token>>>>>>>>",token)
            user_info = await google.get("userinfo", token=token)
            print("OAuth token>>>>>>>>11111111111111")
            return {"message": "Authentication successful", "user_info": user_info.json()}
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=400, detail="Authentication failed")