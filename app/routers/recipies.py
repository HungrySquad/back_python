# pylint: disable=invalid-name
# pylint: disable=redefined-builtin
# pylint: disable=relative-beyond-top-level
"""
Main routing module for API for the recipies with defined REST HTTP methods
"""

from sqlalchemy.orm import Session
from fastapi import Depends, Response, status, HTTPException, APIRouter
from fastapi_pagination import Page, paginate

from .. import models, schemas
from ..database import engine, get_db
from ..models import Recipy

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/recipies", tags=["Recipies"])


@router.get("/", response_model=Page[schemas.RecipyResponse])
def get_recipies(db: Session = Depends(get_db)):
    """
    Get all recipies
    """
    recipies = db.query(models.Recipy).all()
    # cursor.execute("""SELECT * FROM recipies""")
    # recipies = cursor.fetchall()
    return paginate(recipies)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.RecipyResponse
)
def create_recipy(recipy: schemas.RecipyCreate, db: Session = Depends(get_db)):
    """
    Creates a recipy from API call and adds it to the database
    """
    # Does the same as above but quicker and cleaner
    new_recipy = models.Recipy(**recipy.dict())
    # Add new entry to the db
    db.add(new_recipy)
    db.commit()
    db.refresh(new_recipy)
    return new_recipy


@router.get("/{id}", response_model=schemas.RecipyResponse)
def get_recipy(id: int, db: Session = Depends(get_db)):
    """
    Get single recipy by ID
    """
    recipy = db.query(models.Recipy).filter(models.Recipy.id == id).first()
    if not recipy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipy with id: {id} does not exist",
        )
    return recipy

@router.get("/search/{search_string}", response_model=Page[schemas.RecipyResponse])
def search_recipies_by_name(search_string: str, db: Session = Depends(get_db)):
    """
    Search using iLike through the recepies names. Returns paged response with found items
    """
    search = f"%{search_string}%"
    recipies = db.query(Recipy).filter(Recipy.name.ilike(search)).all()
    if not recipies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sorry, no recepies with {search_string} in the name.",
        )
    return paginate(recipies)

@router.delete("/{id}")
def remove_recipy(id: int, db: Session = Depends(get_db)):
    """
    Delete single recipy from database by ID
    """
    recipy_query = db.query(models.Recipy).filter(models.Recipy.id == id)
    # conn.commit()

    if recipy_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipy with id: {id} does not exist",
        )
    recipy_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.RecipyResponse)
def update_recipy(id: int, recipy: schemas.RecipyCreate, db: Session = Depends(get_db)):
    """
    Update single recipy by id using the passed data from API
    """

    recipy_query = db.query(models.Recipy).filter(models.Recipy.id == id)
    updated_recipy = recipy_query.first()

    if updated_recipy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recipy with the id: {id} wasn't found.",
        )

    recipy_query.update(recipy.dict(), synchronize_session=False)

    db.commit()

    return recipy_query.first()
