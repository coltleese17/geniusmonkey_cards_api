import pytest
from cardapi.deck import DeckService
from cardapi.models import Card, SUITS, RANKS

def build_deck_list():
    """Utility: canonical ordered list of (rank, suit) tuples."""
    return [(r, s) for s in SUITS for r in RANKS]


def test_initial_order():
    svc = DeckService()
    expected = build_deck_list()
    top_to_bottom = [(c.rank, c.suit) for c in svc.deck_state()]
    assert top_to_bottom == expected
    assert svc.deck_size == 52 and svc.discard_size == 0


def test_shuffle_changes_order():
    svc = DeckService()
    before = svc.deck_state().copy()
    svc.shuffle()
    after = svc.deck_state()
    # Extremely small probability a shuffle leaves order intact
    assert before != after
    assert set(before) == set(after)        # no cards lost


def test_cut_at_various_indices():
    svc = DeckService()
    for idx in (1, 25, 51):
        svc.reset()
        old_order = svc.deck_state().copy()
        svc.cut(idx)
        new_order = svc.deck_state()
        assert new_order == old_order[idx:] + old_order[:idx]


def test_discard_and_sizes():
    svc = DeckService()
    dealt_card = svc.deal()        # always 2♠ from a fresh deck
    svc.discard(dealt_card)

    assert svc.deck_size == 51
    assert svc.discard_size == 1
    assert svc.discard_state()[-1] == dealt_card


def test_rebuild_merges_and_orders():
    svc = DeckService()
    top = [svc.deal() for _ in range(5)]
    for c in top:
        svc.discard(c)
    svc.shuffle()
    svc.rebuild()
    # Full deck again, correctly ordered
    assert svc.deck_size == 52 and svc.discard_size == 0
    ordered = build_deck_list()
    assert [(c.rank, c.suit) for c in svc.deck_state()] == ordered


def test_peek_and_deal_sync():
    svc = DeckService()
    first = svc.peek()
    second = svc.deal()
    assert first == second
    assert svc.deck_size == 51


def test_deal_empty_deck_raises():
    svc = DeckService()
    for _ in range(52):
        svc.deal()
    with pytest.raises(RuntimeError):
        svc.deal()


def test_cut_invalid_index_raises():
    svc = DeckService()
    with pytest.raises(ValueError):
        svc.cut(0)
    with pytest.raises(ValueError):
        svc.cut(52)

