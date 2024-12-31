from fastapi import FastAPI
from authentication.routes import router as auth_routes

app = FastAPI()

# Include routers from each app
app.include_router(auth_routes, prefix="/app1", tags=["App1"])

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with Class-Based Views"}