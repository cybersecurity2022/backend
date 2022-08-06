import os.path

from fastapi import BackgroundTasks, APIRouter, Depends

from send_email import send_email_background
from models import User
from utils import get_current_user

email_router = APIRouter(prefix="/store", tags=['Store'])


@email_router.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(message: str, background_tasks: BackgroundTasks,
                               current_user: User = Depends(get_current_user)):
    send_email_background(background_tasks, "Defacement Update", current_user.email, message)
    return {
        "message": "Email send Successfully"
    }
