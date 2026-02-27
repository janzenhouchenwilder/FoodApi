from dataclasses import dataclass, asdict

@dataclass
class Token:
    access_token: str
    token_type: str
    expires_in: int
    
    def to_dict(self) -> dict:
        return asdict(self)
