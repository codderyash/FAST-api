from fastapi import APIRouter, HTTPException, Header,Depends
from fastapi import status
from typing import List
from src.books.books_data import books
from .schemas import Book, UpdateBookModel,BookCreateModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import BookService

from src.auth.dependencies import HTTPBearerToken
access_token_bearer=HTTPBearerToken()
book_router = APIRouter()

book_service=BookService()

@book_router.post("/", status_code=status.HTTP_201_CREATED,response_model=Book)
async def create_book(book_data:BookCreateModel ,session:AsyncSession=Depends(get_session)) -> dict:
    created_book=await book_service.create_book(book_data,session)
    return created_book


# response model is use for masking the data and converted into required schema.
@book_router.get("/", response_model=List[Book])
async def get_all_books(session:AsyncSession=Depends(get_session),user_details=Depends(access_token_bearer)):
    books=await book_service.get_all_books(session)
    return books

@book_router.get("/{book_id}",response_model=Book)
async def get_book(book_id: str,session:AsyncSession=Depends(get_session)) -> dict:
    book= await book_service.get_book(book_id,session)
    if book:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")



@book_router.patch("/{book_id}",response_model=Book)
async def update_book(book_id: str, book_update_data: UpdateBookModel,session:AsyncSession=Depends(get_session)):
    updated_book=await book_service.update_book(book_id,book_update_data,session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str,session:AsyncSession=Depends(get_session)):
    deleted_book=await book_service.delete_book(book_id,session)
    if deleted_book:
        return delete_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


# @book_router.get("/get_headers", status_code=201)
# async def get_headers(
#     accept: str = Header(None),
#     content_type: str = Header(None),
#     user_agent: str = Header(None),
#     host: str = Header(None),
# ):
#     request_headers = {}
#     request_headers["Accept"] = accept
#     request_headers["Content-Type"] = content_type
#     request_headers["User-Agent"] = user_agent
#     request_headers["Host"] = host

#     return request_headers
