from fastapi import FastAPI, Request
from endpoints import users, subscribers, activities
from db.session import engine
from db.base import Base
from fastapi.responses import JSONResponse
from exceptions.base import AppException


# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema SQLAlchemy + Supabase")

# Manejador global de excepciones personalizadas
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message
        }
    )

app.include_router(users.router)
app.include_router(subscribers.router)
app.include_router(activities.router)
