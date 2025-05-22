import random
from typing import List
from cardapi.models import Card, SUITS, RANKS

class DeckService:
    """In-memory deck + discard pile (not persisted across restarts)."""

    # ---------- init / reset ---------- #
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._deck: List[Card] = [Card(r, s) for s in SUITS for r in RANKS]
        self._discard: List[Card] = []

    # ---------- public operations ---------- #
    def deal(self) -> Card:
        if not self._deck:
            raise RuntimeError("Deck is empty")
        return self._deck.pop(0)

    def peek(self) -> Card:
        if not self._deck:
            raise RuntimeError("Deck is empty")
        return self._deck[0]

    def shuffle(self) -> None:
        random.shuffle(self._deck)

    def cut(self, index: int) -> None:
        if not (0 < index < len(self._deck)):
            raise ValueError("Cut index out of bounds")
        self._deck = self._deck[index:] + self._deck[:index]

    def order(self) -> None:
        self._deck.sort(key=self._natural_order_key)

    def discard(self, card: Card) -> None:
        self._discard.append(card)

    def rebuild(self) -> None:
        self._deck.extend(self._discard)
        self._discard.clear()
        self.order()

    # ---------- state helpers ---------- #
    def deck_state(self) -> List[Card]:
        """Copy of cards currently in the deck (top-to-bottom)."""
        return list(self._deck)

    def discard_state(self) -> List[Card]:
        """Copy of cards in the discard pile (oldest-first)."""
        return list(self._discard)

    # ---------- internals ---------- #
    @staticmethod
    def _natural_order_key(card: Card) -> tuple[int, int]:
        return SUITS.index(card.suit), RANKS.index(card.rank)

    # ---------- readonly props ---------- #
    @property
    def deck_size(self) -> int:
        return len(self._deck)

    @property
    def discard_size(self) -> int:
        return len(self._discard)

