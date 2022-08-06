from pydantic import BaseModel


class RegisterUserSchema(BaseModel):
    email: str
    username: str
    password: str


class url_in_json(BaseModel):
    url: str
