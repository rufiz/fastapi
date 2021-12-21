#from typing import Optional
#from pydantic import BaseModel
#from typing import Optional, List
#import psycopg2
#from psycopg2.extras import RealDictCursor
#from pydantic import BaseSettings
# #from operator import pos
#from sqlalchemy.orm import Session, session

from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.sql.expression import false, table, update

import app.utils
import app.models
import app.schemas
from app.database import engine, SessionLocal, get_db
from app.routers import users, post, auth, vote
from app.config import settings

# app.models.Base.metadata.create_all(bind=engine)  # Creating the tables
"""create_all is commented out because alembic will take care of it"""

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# my_posts = [
#     {'id': 1, 'title': 'post1 title', 'content': 'post1 content'},
#     {'id': 2, 'title': 'post2 title', 'content': 'post2 content'}
# ]


# def find_id(id):
#     for i in my_posts:
#         if i['id'] == id:
#             return i


# def index_to_delete(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@app.get('/')
def root():
    return {'message': 'Welcome to my api!'}
