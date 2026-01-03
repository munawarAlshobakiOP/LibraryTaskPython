import uvicorn

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

from app.api import author, book, borrower, loan, auth
from app.core.security import require_api_key_and_jwt
from app.core.exceptions import (
    NotFoundException,
    BookAlreadyBorrowedException,
    ActiveLoanExistsException,
    BorrowerNotFoundException,
)
from app.schemas.internal_event import LoanValidationFailed
from app.core.events import publish_internal_event
from app.core.producer import get_kafka_producer
from app.core.producer import publish_message

load_dotenv()
# Base.metadata.create_all(engine)

app = FastAPI(title="Library Management System", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    """
    Test Kafka connection on startup and log any connection issues.
    """
    print("Testing Kafka connection...")
    test_message = {"test": "startup_connection_check"}
    error = publish_message("system_startup", test_message)

    if error:
        publish_internal_event(error)
    else:
        print("Kafka connection successful!")


app.include_router(auth.router)
app.include_router(author.router, dependencies=[Depends(require_api_key_and_jwt)])
app.include_router(book.router, dependencies=[Depends(require_api_key_and_jwt)])
app.include_router(borrower.router, dependencies=[Depends(require_api_key_and_jwt)])
app.include_router(loan.router, dependencies=[Depends(require_api_key_and_jwt)])


@app.exception_handler(NotFoundException)
async def handle_not_found(request, exc: NotFoundException):
    """
    Handle cases when a requested resource is not found.
    """
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(BookAlreadyBorrowedException)
async def handle_already_borrowed(request, exc: BookAlreadyBorrowedException):
    """
    Handle cases when a book is already borrowed.
    """
    publish_internal_event(
        LoanValidationFailed(
            reason="BookAlreadyBorrowed", validation_errors={"message": str(exc)}
        )
    )
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(ActiveLoanExistsException)
async def handle_active_loan(request, exc: ActiveLoanExistsException):
    """
    Handle cases when an active loan exists.
    """
    publish_internal_event(
        LoanValidationFailed(
            reason="ActiveLoanExists", validation_errors={"message": str(exc)}
        )
    )
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(BorrowerNotFoundException)
async def handle_borrower_not_found(request, exc: BorrowerNotFoundException):
    """
    Handle cases when a borrower is not found.
    """
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(IntegrityError)
async def handle_integrity_error(request, exc: IntegrityError):
    """
    Handle cases when a data integrity violation occurs.
    """
    return JSONResponse(
        status_code=409,
        content={"detail": "Data integrity violation"},
    )


@app.get("/")
def home():
    """
    Home endpoint returning a welcome message.
    """
    return {"message": "Welcome to Library Management System"}


if __name__ == "__main__":
    """Run the application using Uvicorn."""

    uvicorn.run(app, host="0.0.0.0", port=8000)
