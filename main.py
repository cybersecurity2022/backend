from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.auth import auth_router
from api.store import store_router
from api.monitor import monitor_router
from api.email import email_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/home")
def home():
    return "welcome"

app.include_router(auth_router)
# app.include_router(store_router)
app.include_router(monitor_router)
app.include_router(email_router)
