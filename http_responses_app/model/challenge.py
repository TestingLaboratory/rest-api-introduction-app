from pydantic import BaseModel


class ChallengeSecret(BaseModel):
    secret: str


class PhoneCall(BaseModel):
    person: str
    phone_number: str
    subject: str
