from dataclasses import dataclass, asdict

SUITS = ["spades", "hearts", "clubs", "diamonds"]
RANKS = [str(n) for n in range(2, 11)] + ["Jack", "Queen", "King", "Ace"]


@dataclass(frozen=True, slots=True)
class Card:
    rank: str
    suit: str

    def model_dump(self) -> dict:
        return asdict(self)

    @classmethod
    def from_strs(cls, rank: str, suit: str) -> "Card":
        rank, suit = rank.strip(), suit.strip().lower()
        if suit not in SUITS or rank not in RANKS:
            raise ValueError("Invalid card")
        return cls(rank, suit)

