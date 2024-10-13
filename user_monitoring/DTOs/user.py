from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    risk: str

    def dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'risk': self.risk
        }
