from typing import List

from fastapi_mail import MessageSchema, FastMail

from app.email.schemas import SendEmail


class ServiceEmail():
    async def send_email_async(self, fm: FastMail, subject: str, email_to_list: List[str], body: SendEmail):
        message = MessageSchema(
            subject=subject,
            recipients=email_to_list,
            template_body=body.dict(),
            subtype='html',
        )

        await fm.send_message(message, template_name='email.html')

    async def send_create_user_link_email_async(self, fm: FastMail, subject: str, email_to_list: List[str],
                                                body: SendEmail):
        message = MessageSchema(
            subject=subject,
            recipients=email_to_list,
            template_body=body.dict(),
            subtype='html',
        )

        await fm.send_message(message, template_name='user_create_link.html')

    async def send_certification_user_link_email_async(self, fm: FastMail, subject: str, email_to_list: List[str],
                                                       body: SendEmail):
        message = MessageSchema(
            subject=subject,
            recipients=email_to_list,
            template_body=body.dict(),
            subtype='html',
        )

        await fm.send_message(message, template_name='user_certification.html')


service_email = ServiceEmail()
