from fastapi import FastAPI
from app.routers import users, workouts, exercises
from app.database.session import Base, engine
from app.auth import routes
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)
# app.include_router(workouts.router)
# app.include_router(exercises.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fitness Apps!"}

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import random
# from datetime import datetime, timedelta
#
# def generate_verification_code() -> str:
#     """
#     Генерирует случайный 6-значный код подтверждения.
#     """
#     return str(random.randint(100000, 999999))
#
# def send_verification_email(email: str, code: str):
#     """
#     Отправляет код подтверждения на указанный email.
#     """
#     sender_email = "dedvassi@gmail.com"  # Ваш email
#     sender_password = "oiqb udmd sfbl lewh"  # Ваш пароль
#
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = email
#     message["Subject"] = "Код подтверждения"
#
#     body = f"Ваш код подтверждения: {code}"
#     message.attach(MIMEText(body, "plain"))
#
#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Укажите SMTP сервер
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, email, message.as_string())
#         print(f"Код подтверждения отправлен на {email}")
#     except Exception as e:
#         print(f"Ошибка при отправке email: {e}")
#
#
# em = 'dedvassi@gmail.com'
# code = generate_verification_code()
# send_verification_email(em, code)