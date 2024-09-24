from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from app import models, oauth2, schemas, utils
from sqlalchemy.orm import Session
from app.database import get_db



router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

# @app.get('/posts')
# def get_posts():
#     cur.execute(""" SELECT * FROM posts """)
#     posts = cur.fetchall()
#     print(posts)
#     return{"data": posts}

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit:int=10, skip:int=0, search: Optional[str] = ""):
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return posts


# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cur.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
#     new_post = cur.fetchone()
#     conn.commit()
#     return{"data": new_post}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    # the above line is alternative for the below line
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) 
    # dict() is depriciated, model_dump is the alternative for the same   
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return{"data": new_post}
    return new_post


# @app.get("/posts/{id}")
# def get_post(id: int):
#     cur.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
#     # cur.execute(""" SELECT * FROM posts WHERE id = %(id)s """, {"id":id}) alternative for the above line
#     post =  cur.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
#     return {"post detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # post =  db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")
    
    return post



# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def del_post(id: int):
#     cur.execute(""" DELETE FROM posts where id = %s RETURNING * """, (str(id),))
#     deledted_post = cur.fetchone()
#     conn.commit()
#     if deledted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
   
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")
    
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



# @app.put("/posts/{id}")
# def update_post(id: int, post:Post):
#     cur.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
#     updated_post = cur.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
#     return {"data": updated_post}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    # updated_post = post_query.update({'title': 'updated title', 'content': 'updated content is this'}, synchronize_session=False) am not sure about this line

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform the requested action")
    
    post_query.update(updated_post.model_dump())

    db.commit()

    # return {"data": post_query.first()}
    return post_query.first()
