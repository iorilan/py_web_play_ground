from typing import List
from pydantic import BaseModel


class TODOBase(BaseModel):
    desc: str
    title: str

class TODOCreate(TODOBase):
    pass

class TODOUpdate(TODOBase):
    pass

class TODOInfo(TODOBase):
    id: int
    created_at: int
    class Config:
        orm_mode = True