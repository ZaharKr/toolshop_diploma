from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str | None = None
    expires_in: int | None = None


class Address(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    dob: str = Field(description="YYYY-MM-DD")
    phone: str
    address: Address
