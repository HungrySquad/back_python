from .. import models, schemas
from ..database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/recipies", tags=["Recipies"])


@router.get("/", response_model=List[schemas.RecipyResponse])
def get_posts(db: Session = Depends(get_db)):
    recipies = db.query(models.Recipy).all()
    # cursor.execute("""SELECT * FROM recipies""")
    # recipies = cursor.fetchall()
    return recipies


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecipyResponse
)
def create_recipy(recipy: schemas.RecipyCreate, db: Session = Depends(get_db)):
    # Does the same as above but quicker and cleaner
    new_recipy = models.Recipy(**recipy.dict())
    # Add new entry to the db
    db.add(new_recipy)
    db.commit()
    db.refresh(new_recipy)
    return new_recipy


@router.get("/{id}", response_model=schemas.RecipyResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    recipy = db.query(models.Recipy).filter(models.Recipy.id == id).first()
    if not recipy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipy with id: {id} does not exist",
        )
    return recipy


@router.delete("/{id}")
def remove_recipy(id: int, db: Session = Depends(get_db)):
    recipy_query = db.query(models.Recipy).filter(models.Recipy.id == id)
    # conn.commit()

    if recipy_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipy with id: {id} does not exist",
        )
    recipy_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.RecipyResponse)
def update_recipy(id: int, recipy: schemas.RecipyCreate, db: Session = Depends(get_db)):

    recipy_query = db.query(models.Recipy).filter(models.Recipy.id == id)
    updated_recipy = recipy_query.first()

    if updated_recipy == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipy with the id: {id} wasn't found.",
        )

    recipy_query.update(recipy.dict(), synchronize_session=False)

    db.commit()

    return recipy_query.first()
