from fastapi import FastAPI
import models
from database import engine
from routers import users, tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Todo API is running. Visit /docs to try it out."}