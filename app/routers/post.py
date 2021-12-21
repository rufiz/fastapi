from .. import models, schemas, oauth2
from .. database import get_db

from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter

from sqlalchemy.orm import Session, session
from sqlalchemy import func
from typing import Optional, List


router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    # cursor.execute("""SELECT * FROM tbl_posts;""")
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)

    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO tbl_posts(title, content, published) VALUES(%s, %s, %s) RETURNING *;""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
# title str, content str


@router.get('/{id}')  # response_model=[schemas.PostOut]
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM tbl_posts WHERE id = %s""", (str(id)))
    # result = cursor.fetchone()

    #result_post = db.query(models.Post).filter_by(id=id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'ID: {id} does not exist.')

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM tbl_posts WHERE id = %s RETURNING *""", str(id))
    # post_to_delete = cursor.fetchone()
    # conn.commit()

    post_to_delete = db.query(models.Post).filter_by(id=id).first()

    if post_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Id: {id} does not exist.')

    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    db.delete(post_to_delete)
    db.commit()

    return Response(content='Succesfully deleted.', status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.PostCreate)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE tbl_posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter_by(id=id)
    post_result = post_query.first()

    if post_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if post_result.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_result
