import uvicorn
from fastapi import FastAPI
from facebook_scraper import *
from pymongo import MongoClient

app = FastAPI()
db = MongoClient('127.0.0.1', 27017)['Farouk']
collection = db.farouk


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/scrape/{page}")
def scrape_posts(page: str):
    posts = []
    for post in get_posts(page, pages=5):
        collection.update_one({'post': post}, {'$set': post}, upsert=True)
    return {"posts": posts}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)