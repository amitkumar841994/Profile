from fastapi import FastAPI,Request
from authentication.routes import router as auth_routes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],     
    allow_headers=["*"],     
)
templates = Jinja2Templates(directory='Template')
app.mount("/static", StaticFiles(directory="static"), name="static")


# Include routers from each app
app.include_router(auth_routes, prefix="/app1", tags=["App1"])

@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})