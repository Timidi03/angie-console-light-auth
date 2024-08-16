from fastapi import FastAPI
from src.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from src.settings import settings

app = FastAPI()
origins = settings.ORIGINS.split(',')

app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)

