from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="web.defacement100@gmail.com",
    MAIL_PASSWORD="minqtzdzyweutudi",
    MAIL_FROM="web.defacement100@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="web.defacement100@gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='./template'
)

def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )

    fm = FastMail(conf)

    background_tasks.add_task(
        fm.send_message, message, template_name='email.html')