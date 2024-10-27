from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from db import models


def get_all_authors_paginated(db: Session, page: int = 0, size: int = 10):
    offset = page * size
    selected_authors = select(models.Author).offset(offset).limit(size)
    return db.execute(selected_authors).scalars().all()


def get_all_books_paginated(
        db: Session, author_id: int, page: int = 0, size: int = 10
):
    queryset = db.query(models.Book)
    if author_id is not None:
        queryset = queryset.filter(models.Book.author_id == author_id)
    offset = page * size
    return queryset.offset(offset).limit(size).all()


def get_author_by_id(db: Session, author_id: int):
    return (db.query(models.Author).
            filter(models.Author.id == author_id).first())


def get_author_by_name(db: Session, name: str):
    return (db.query(models.Author).
            filter(models.Author.name == name).first())


def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author


def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()


def create_book_for_author(db: Session, book: schemas.BookCreate):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book
