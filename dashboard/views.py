import json
import uuid
from fastapi import APIRouter,Depends,Request,HTTPException,Form,UploadFile , File
from dashboard.models import UserExperienceModel,UserFileUpload
from config import db,manager
from typing import Optional
import requests
from pathlib import Path
from bson import Binary
from datetime import datetime, timedelta
from io import BytesIO
from fastapi.responses import StreamingResponse
import base64
from bson.json_util import dumps
from fastapi import WebSocket, WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorClient


class UserDashboard:
    def __init__(self):
        self.router = APIRouter()
    

    def userbasicdetails(self):
        pass


class UserJobsExperience:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route('/experice/create',self.create,methods=['POST'])
        self.router.add_api_route('/experice/get/{user_id}',self.get,methods=['GET'])


    def userccheck(self,user_id):
        user  = db.User.find_one({'user_id': user_id})
        if user:
            return True
        else:
            return False

    def create(self,userexp:UserExperienceModel):
        try:
            if self.userccheck(userexp.user_id):
                print("User already exists")
                result =db.UserExperice.insert_one(userexp.model_dump())
                return {
                "message": "added successfully",
                "data": userexp.model_dump(),
                "status_code":201
                }

            else:
                return {
                "message": "User does not exist",
                "status_code":404
                }
        except Exception as e:
            return {
                "message": str(e),
                "status_code":400
                }



    def get(self, user_id: str):
        try:
            # Convert UUID string to Binary with subtype 3
            uuid_obj = uuid.UUID(user_id)
            user_id_bin = Binary(uuid_obj.bytes, subtype=3)

            if self.userccheck(user_id_bin):
                # Query once, store results in a list
                compqny_cursor = db.UserExperice.find({"user_id": user_id_bin})
                compqny_details = list(compqny_cursor)

                # Print and return the same result
                print("compqny_details>>>>>>>>>>>>>>>", json.loads(dumps(compqny_details)))
                return {
                    "message": "added successfully",
                    "data": json.loads(dumps(compqny_details)),
                    "status_code": 200
                }
            else:
                return {
                    "message": "User not found",
                    "data": [],
                    "status_code": 404
                }

        except Exception as e:
            return {
                "message": str(e),
                "data": None,
                "status_code": 400
            }

            

            


class GitRepo:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route('/git/repo/',self.gitrepocreate,methods=['GET'])
        self.router.add_api_route('/git/contro/',self.fetch_contributions,methods=['GET'])


    def gitrepocreate(self):
        username ="amitkumar841994"
        api_url = f"https://api.github.com/users/{username}/repos"
        try:
            response = requests.get(api_url)
            repo_count = len(response.json())
            repo_list=[]
            for link in response.json():
                print("repo_count",link.get('owner').get("avatar_url"))
                # repo_list.append(link.get('full_name'))
                repo_data = {
                    'repo_name':link.get('full_name'),
                    'repo_img' : link.get('owner').get("avatar_url")

                }
                repo_list.append(repo_data)

                
                

            data={"repo_list":repo_list,"repo_count":repo_count}
            return {
                "message": "added successfully",
                "data": data,
                "status_code":200
                }
            

        except Exception as e:
            return {
                "message": str(e),
                "status_code":400
                }         


 


    def fetch_contributions(self, ):
        # Base URL for fetching events
        username ="amitkumar841994"
        api_url = f"https://api.github.com/users/{username}/events"


        try:
            # Make the API request
            response = requests.get(api_url)
            response.raise_for_status()

            # Parse the JSON response
            events = response.json()

            # Process contributions
            contributions = {}
            for event in events:
                if event['type'] in ['PushEvent', 'PullRequestEvent', 'IssuesEvent']:
                    event_date = event['created_at'][:10]  # Extract date in 'YYYY-MM-DD' format
                    contributions[event_date] = contributions.get(event_date, 0) + 1

            # Fill in missing dates for the past year
            today = datetime.utcnow().date()
            one_year_ago = today - timedelta(days=365)

            daily_contributions = []
            current_date = one_year_ago
            while current_date <= today:
                daily_contributions.append({
                    'date': current_date.isoformat(),
                    'count': contributions.get(current_date.isoformat(), 0)
                })
                current_date += timedelta(days=1)

            return {
                "message": "Fetched successfully",
                "data": daily_contributions,
                "status_code": 200
            }

        except requests.exceptions.RequestException as e:
            return {
                "message": f"Error fetching contributions: {str(e)}",
                "status_code": 500
            }


class UploadFileHandler:
    def __init__(self):
        self.router =APIRouter()
        self.router.add_api_route('/upload/resume/',self.upload_file,methods=['POST'])
        self.router.add_api_route('/view/resume/{user_id}',self.get_file_view,methods=['GET'])

    def upload_file(self,user_id: str = Form(...),description: Optional[str] = Form(None),file: UploadFile = File(...)):
        try:
            file_bytes = file.file.read()
            user_file_data = UserFileUpload(
                user_id=user_id,
                file_name=file.filename,
                upload_time=datetime.utcnow(),
                file_size=len(file_bytes),
                description=description
            )

            document = user_file_data.dict()
            document["file"] = Binary(file_bytes)

            db.UserFile.insert_one(document)

            return {"message": "File uploaded successfully", "status_code": 200}
        except Exception as e:
            return {"message": f"{str(e)}", "status_code": 400}
        
    def get_file_view(self,user_id:str):
        try:
            print(">>>>>>>>>>>>>its view file ")
            file_details = db.UserFile.find_one({"user_id":user_id})
            result = []
            if not file_details:
                return {"message": "File not found"}, 404

            pdf_bytes = file_details["file"]  # this is binary
            file_stream = BytesIO(pdf_bytes)

            return StreamingResponse(
                file_stream,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'inline; filename="{file_details["file_name"]}"'
                }
            )
        except Exception as e:
            return {
                "message": f"Error fetching contributions: {str(e)}",
                "status_code": 500
            }

         
class MessageHandler:
    def __init__(self):
        self.router =APIRouter()
  
        self.router.add_api_websocket_route('/message/sender/{user_id}',self.sender)
        client = AsyncIOMotorClient("mongodb+srv://amitkumar841994:bAyyuwJouF5lSctK@cluster0.cl04m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        db = client["Profiledb"]
        self.messages_collection = db["Messages"]


    async def sender(self, websocket: WebSocket, user_id: str):  # changed 'username' -> 'user_id'
        print("WebSocket connection attempt by:", user_id)
        await manager.connect(websocket)  # ✅ accept inside manager.connect

        try:
            while True:
                data = await websocket.receive_text()

            # Save to MongoDB
                await self.messages_collection.insert_one({
                    "user_id": user_id,
                    "message": data,
                    "timestamp": datetime.utcnow()
                })

            await manager.broadcast(f"{user_id}: {data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast(f"{user_id} left the chat.")
            print(f"{user_id} left the chat.")









