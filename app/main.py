import uvicorn
from fastapi import FastAPI
from api.endpoints import api_router
from db.database import engine
from models import users

# models.Base.metadata.create_all(bind=engine)
users.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=9393)