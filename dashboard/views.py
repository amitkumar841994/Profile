from fastapi import APIRouter,Depends,Request,HTTPException,Form,UploadFile
from dashboard.models import UserExpericeModel,UserFileUpload
from config import db
import requests
from datetime import datetime, timedelta


class UserDashboard:
    def __init__(self):
        self.router = APIRouter()
    

    def userbasicdetails(self):
        pass


class UserJobsExperience:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route('/experice/create',self.create,methods=['POST'])


    def userccheck(self,user_id):
        user  = db.User.find_one({'user_id': user_id})
        if user:
            return True
        else:
            return False

    def create(self,userexp:UserExpericeModel):
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
        self.router.add_api_route('/upload/resume/',self.upoload_file,methods=['GET'])
        pass
    def upoload_file(self,fileUpload:UserFileUpload):    
        user_id: str = Form(...),
        file_name: str = Form(...),
        description: Optional[str] = Form(None),
        file: UploadFile = File(...)

    