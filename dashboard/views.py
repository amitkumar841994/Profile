from fastapi import APIRouter,Depends,Request,HTTPException
from dashboard.models import UserExpericeModel
from config import db
import requests


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
        self.router.add_api_route('/git/repo/',self.gitrepocreate,methods=['GEt'])


    def gitrepocreate(self):
        username ="amitkumar841994"
        api_url = f"https://api.github.com/users/{username}/repos"
        try:
            response = requests.get(api_url)
            repo_count = len(response.json())
            repo_list=[]
            for link in response.json():
                print("repo_count",link.get('full_name'))
                repo_list.append(link.get('full_name'))

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


