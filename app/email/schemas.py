from pydantic import BaseModel


class SendEmail(BaseModel):
    receiver: str
    title: str
    content: str
