from pydantic import BaseModel, Field


# ---- Request / Input ----
class CheckSessionAccessToken(BaseModel):
    user_id: int = Field(..., alias="UserId")
    access_token: str = Field(..., alias="AccessToken")
    ip_address: str = Field(..., alias="ipAddress")
    user_agent: str = Field(..., alias="userAgent")

    class Config:
        validate_by_name = True


