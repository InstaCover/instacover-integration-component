from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel


class SessionParams(BaseModel):
    sessionId: str
    sessionCreatedAt: datetime
    sessionFinished: bool
    sessionFinishedAt: datetime
    sessionCanceledAt: Optional[datetime]
    sessionExpireAt: Optional[datetime]
    sessionValid: bool
    photos: List[dict]


class CreateSessionResponse(BaseModel):
    link: str
    sessionId: str
    expireAt: Union[datetime, None]
