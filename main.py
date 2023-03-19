from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4

app = FastAPI()

posts = []

# Posts Model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    create_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False # por defecto false


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return posts

@app.get("/post/{post_id}")
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code = 404, detail = "Post not found")

@app.post("/posts")
def create_post(post: Post):
    post.id = str(uuid4()) # uuid4 devuelve una clase,la paso a string
    posts.append(post.dict()) # paso a diccionario lo que me devuelve el post
    return post[-1] # devuelvo el ultimo item de la lista

@app.delete("/post/{post_id}")
def delete_post(post_id : str):
    for ind, post in enumerate(posts): # para poder usar el ind
        if post["id"] == post_id:
            posts.pop(ind)
            return {"message": "Post deleted"}
    raise HTTPException(status_code = 404, detail = "Post not found")

@app.put("/post/{post_id}")
def update_post(post_id:str,updated_post:Post):
    for ind, post in enumerate(posts): # para poder usar el ind
        if post["id"] == post_id:
            posts[ind]["title"] = updated_post.title
            posts[ind]["author"] = updated_post.author
            posts[ind]["content"] = updated_post.content
            return {"message": "Post Updated"}
    raise HTTPException(status_code = 404, detail = "Post not found")


