
from dataclasses import dataclass
from app import setting
import emails  # type: ignore
from jinja2 import Template
from pathlib import Path
from typing import Any
@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content

def generate_test_email(email_to: str) -> EmailData:
    project_name = setting.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": setting.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def send_email(
    
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert setting.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(setting.EMAILS_FROM_NAME, setting.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": setting.SMTP_HOST, "port": setting.SMTP_PORT}
    if setting.SMTP_TLS:
        smtp_options["tls"] = True
    elif setting.SMTP_SSL:
        smtp_options["ssl"] = True
    if setting.SMTP_USER:
        smtp_options["user"] = setting.SMTP_USER
    if setting.SMTP_PASSWORD:
        smtp_options["password"] =str(setting.SMTP_PASSWORD)
    # print("smtp_options", smtp_options)
    response = message.send(to=email_to, smtp=smtp_options)
    return response



# from app import setting
# from fastapi import BackgroundTasks
# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# import json
 
# conf = ConnectionConfig(
#     MAIL_USERNAME=setting.MAIL_USERNAME,
#     MAIL_PASSWORD=str(setting.MAIL_PASSWORD),
#     MAIL_FROM=setting.MAIL_FROM,
#     MAIL_PORT=setting.MAIL_PORT,
#     MAIL_SERVER=setting.MAIL_SERVER,
#     MAIL_FROM_NAME=setting.MAIL_FROM_NAME,
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True,
#     TEMPLATE_FOLDER='app/templates'
# )

# async def send_email_async(subject: str, email_to: str, body: dict):
#     body_str = json.dumps(body) 
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         body=body_str,
#         subtype='html',
#     )
    
#     fm = FastMail(conf)
#     await fm.send_message(message, template_name='email.html')

# def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
#     body_str = json.dumps(body) 
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         body=body_str,
#         subtype='html',
#     )
#     fm = FastMail(conf)
#     background_tasks.add_task(
#        fm.send_message, message, template_name='email.html')

