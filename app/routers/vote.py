from os import stat
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.status import HTTP_409_CONFLICT
from .. import schemas, database, models, oauth2


router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: dict = Depends(oauth2.get_current_user)):

    vote_post = db.query(models.Post).filter(
        models.Post.id == vote.post_id).first()

    if not vote_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {vote.post_id} does not exist.')

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if int(vote.dir) == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()

        return {'success': 'Successfully liked the post.'}

    if not found_vote:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail='Vote does not exist.')

    db.delete(found_vote)
    db.commit()

    return {'success': 'Successfully removed the vote.'}
