from fastapi import FastAPI
from src.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origin = [
    'http://localhost:8082',
    'http://localhost:8000',
    '*'
]

app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

