from pydantic import BaseModel, ConfigDict


class NotificationCreate(BaseModel):
    user_id: int
    channel: str
    message: str
    priority: str
    recipient: str


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    channel: str
    message: str
    priority: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class PreferencesRequest(BaseModel):
    email: bool
    sms: bool
    push: bool



class PreferencesResponse(BaseModel):
    user_id: int
    email: bool
    sms: bool
    push: bool

    model_config = ConfigDict(from_attributes=True)


