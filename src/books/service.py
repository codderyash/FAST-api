from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from sqlmodel import select,desc
from .models import Book
from .schemas import UpdateBookModel,BookCreateModel
from datetime import datetime
class BookService:
    async def get_all_books(self,session:AsyncSession):
        statement=select(Book).order_by(desc(Book.created_at))
        result=await session.execute(statement)
        return result.scalars().all()
    
    async def get_book(self,book_id,session:AsyncSession):
        statement=select(Book).where(Book.uid==book_id)
        result=await session.execute(statement)
        return result.scalar()
    
    async def create_book(self,book_data:BookCreateModel,session:AsyncSession):
        book_data_dict=book_data.model_dump()
        new_book=Book(**book_data_dict)
        # new_book.published_date=datetime.strptime(book_data_dict['published_date'],"%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
    
    async def update_book(self,book_id:str,update_data:UpdateBookModel,session:AsyncSession):
        book_data=await self.get_book(book_id,session)
        if book_data is not None:
            update_data_dict=update_data.model_dump()
            for key,val in update_data_dict.items():
                setattr(book_data,key,val)
            
            await session.commit()
            return book_data
        else:
            return None
    
    async def delete_book(self,book_id:str,session:AsyncSession):
        book_data=await self.get_book(book_id,session)
        if book_data is not None:
            await session.delete(book_data)
            await session.commit()
        else:
            return None

    