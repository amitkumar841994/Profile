from fastapi import APIRouter,Depends,Request,HTTPException

class UserDashboard:
    def __init__(self):
        self.router = APIRouter()

    def userbasicdetails(self):
        