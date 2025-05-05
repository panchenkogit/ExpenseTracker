from email.mime.text import MIMEText
from aiosmtplib import SMTP, SMTPException
from fastapi import FastAPI, Request, Response, Depends, HTTPException

from common_utils.redis import EmailReminder

app = FastAPI()


@app.post("/send_notification")
async def send_email(email: EmailReminder):
    sender = "odosaol@ya.ru"
    password = "unmzdaposipjydow"

    # Используем свойство text
    msg = MIMEText(email.message, "plain", "utf-8")
    msg["From"] = sender
    msg["Subject"] = email.theme

    try:
        server = SMTP(hostname="smtp.yandex.ru", port=587, start_tls=True)

        await server.connect()
        await server.login(sender, password)
        await server.send_message(msg, recipients=[email.email])

        return "Письмо отправлено!"
    except SMTPException as _ex:
        return f"Ошибка SMTP: {_ex}"
    except Exception as _ex:
        return f"Ошибка: {_ex}"
    finally:
        await server.quit()
