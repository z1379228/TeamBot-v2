from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Player:
    id: int
    discord_id: int
    username: str
    nickname: str
    avatar: Optional[str]

    elo: int = 1000

    win: int = 0
    lose: int = 0
    draw: int = 0

    mvp: int = 0