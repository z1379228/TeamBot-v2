from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Player:

    id: int

    discord_id: int

    username: str

    nickname: str

    avatar: str | None

    elo: int

    win: int

    lose: int

    draw: int

    mvp: int

    created_at: datetime | None = None

    @property
    def games(self) -> int:
        return self.win + self.lose + self.draw

    @property
    def win_rate(self) -> float:

        if self.games == 0:
            return 0.0

        return round((self.win / self.games) * 100, 1)

    @property
    def score(self) -> int:
        return self.win * 3 + self.draw