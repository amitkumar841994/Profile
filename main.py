from fastapi import FastAPI
from authentication.routes import router as auth_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,  
    allow_methods=["*"],     
    allow_headers=["*"],     
)
# Include routers from each app
app.include_router(auth_routes, prefix="/app1", tags=["App1"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with Class-Based Views"}