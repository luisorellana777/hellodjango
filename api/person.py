from dataclasses import dataclass


@dataclass
class PersonInfo:
    name: str
    phone_number: str

    @classmethod
    def from_payload(cls, payload: dict) -> "PersonInfo":
        name = payload.get("name")
        phone_number = payload.get("phone_number")

        if not name or not phone_number:
            raise ValueError("Missing required fields: name, phone_number")

        return cls(name=name, phone_number=phone_number)

