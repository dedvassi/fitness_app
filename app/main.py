from fastapi import FastAPI
from app.routers import users, workouts, exercises

app = FastAPI()

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(exercises.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fitness App!"}
