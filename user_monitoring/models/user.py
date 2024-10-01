class User:
    def __init__(self, user_id: int, risk: str):
        self.user_id = user_id
        self.risk = risk

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, amount={self.risk!r})"
