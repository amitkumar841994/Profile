
from fastapi import APIRouter,Depends


class NewUserRegistration:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/items", self.register, methods=["POST"])
        # self.router.add_api_route("/items", self.create_item, methods=["POST"])

    async def register(self):
        # data =data.request
        print("Registering")
        return {"message": "Item created",}
        

    # async def create_item(self):
    #     return {"message": "Item created",}