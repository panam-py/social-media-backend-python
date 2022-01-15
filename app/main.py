from http.client import HTTPException
from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{'title':'title of post 1', 'content':'content of post 1', 'id':1}, {'title':'favorite foods', 'content':'I like pizza', 'id':2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

@app.get('/')
def root():
    return {'message':'Welcome to my API nigga!'}

@app.get('/posts')
def get_posts():
    return {'data': my_posts}

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    selected_post = find_post(id, False)
    if selected_post == None:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="'No post found with that id'")
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'No post found with that id'}
    return {'data':selected_post}

@app.post('/posts')
def create_post(post: Post, response: Response):
    id = my_posts[-1]['id'] + 1
    post = post.dict()
    post['id'] = id
    my_posts.append(post)
    response.status_code = status.HTTP_201_CREATED
    return {'data':post}

@app.delete('/posts/{id}')
def delete_post(id: int, response: Response):
    index = find_index(id)
    if not index:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'No post found with that id'}
    my_posts.pop(index)
    response.status_code = status.HTTP_204_NO_CONTENT
    return None

@app.put('/posts/{id}')
def update_post(id: int, response: Response, post: Post):
    index = find_index(id)
    print(index)
    if index == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'No post found with that id'}
    post = post.dict()
    post[id] = id
    my_posts[index] = post
    post['id'] = id
    return {"data":post}