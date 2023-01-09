from pydantic import BaseModel

class CreateMedcard(BaseModel):
    title: str
    fio: str

class Medcard:
    def __init__(self, id: int, title: str, fio: str) -> None:
        self.id = id
        self.title = title
        self.fio = fio