from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import report_router

app = FastAPI()

app.include_router(report_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
