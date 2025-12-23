from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.api import author, book, borrower, loan
from app.core.exceptions import (
    NotFoundException,
    BookAlreadyBorrowedException,
    ActiveLoanExistsException,
    BorrowerNotFoundException,
)
from app.core.db import Base, engine

Base.metadata.create_all(engine)

app = FastAPI(title="Library Management System", version="1.0.0")

app.include_router(author.router)
app.include_router(book.router)
app.include_router(borrower.router)
app.include_router(loan.router)


@app.exception_handler(NotFoundException)
async def handle_not_found(request, exc: NotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(BookAlreadyBorrowedException)
async def handle_already_borrowed(request, exc: BookAlreadyBorrowedException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(ActiveLoanExistsException)
async def handle_active_loan(request, exc: ActiveLoanExistsException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(BorrowerNotFoundException)
async def handle_borrower_not_found(request, exc: BorrowerNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(IntegrityError)
async def handle_integrity_error(request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "Data integrity violation"},
    )


@app.get("/")
def home():
    return {"message": "Welcome to Library Management System"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
