from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
from datetime import datetime, timedelta

import jwt

from os import getenv
from dotenv import load_dotenv

from db import User, Ads, Config


app=FastAPI()
Config.migrate()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()


SECRET = getenv("JWT_SECRET")
ALGORITHM = getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.post("/token") 
async def token (form: OAuth2PasswordRequestForm = Depends()): 
    with Config.SESSION as session: 
        user = session.exec(select(User).where(User.username == form.username)).first()
        if user and jwt.decode(user.password, SECRET, algorithms=[ALGORITHM])["password"] == form.password:
            access_token = jwt.encode({"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}, SECRET, algorithm=ALGORITHM)
            return {"access token": access_token, "token, type": "bearer"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dont have such user")


@app.post("/register")
async def register(user:User, data: dict):
    jwt_token = jwt.encode({"password": user.password}, SECRET, algorithm=ALGORITHM)
    user.password = jwt_token

    with Config.SESSION as session:
        data = user
        session.add(data)
        session.commit()
        session.refresh(data)
        return user


@app.get("/users/")
async def users(token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        return session.exec(select(User)).all()


@app.post("/ads/")
async def add_ads(data: Ads, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    

@app.get("/read-ads/")
async def read_ads():
    with Config.SESSION as session:
        return session.exec(select(Ads)).all()
    

@app.delete("buy-ads")
async def delete_ads(ads_id:int, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        data = session.get(Ads, ads_id)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We dont have this ads")
        session.delete(data)
        session.commit()
        return "You successfully buy this ads"