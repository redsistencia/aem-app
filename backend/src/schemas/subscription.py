from pydantic import BaseModel, EmailStr

class SubscriptionCreate(BaseModel):
    name: str
    email: EmailStr
    privacy_policy: bool
    newsletter_consent: bool
