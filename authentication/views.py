from fastapi import APIRouter,Depends,Request,HTTPException
from authentication.models import NewUser,UserLogin
import uuid
from config import db
from utils.password import pwd_context,create_access_token,create_refresh_token
import json
from authentication.auth_config import google
from fastapi.responses import RedirectResponse


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
                    access_token = create_access_token(user_data)
                    refresh_token = create_refresh_token(user_data)
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
                return {"message": "Not registerd user", "status_code": 40}


        except Exception as e:
            return {"message": f"{str(e)}", "status_code": 500}


    async def login(self, request: Request):
        # Generate a new state value and store it in the session
        state = str(uuid.uuid4())
        request.session['state'] = state
        
        redirect_uri = request.url_for("auth_login")  # Redirect after successful login
        redirect_uri("redirect>>>>",redirect_uri)
        google_auth_url = google.authorize_url(
            redirect_uri=redirect_uri,
            state=state,  # Send the state with the request
            scope=["openid", "email", "profile"]
        )
        
        return RedirectResponse(url=google_auth_url)

    async def auth(self, request: Request):
        # Fetch the state from session and received state from URL
        state_sent = request.session.get('state')
        state_received = request.query_params.get('state')

        print(state_received, state_sent)
        
        # Compare state values
        if state_sent != state_received:
            raise HTTPException(status_code=400, detail="CSRF token mismatch")
        
        # Proceed with OAuth token exchange
        try:
            token = await google.authorize_access_token(request)
            user_info = await google.get("userinfo", token=token)
            return {"message": "Authentication successful", "user_info": user_info.json()}
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=400, detail="Authentication failed")