import pytest
from httpx import AsyncClient
from cardapi.models import Card  

@pytest.mark.asyncio
async def test_cheat_matches_deal(client: AsyncClient):
    peek = await client.get("/cheat")
    dealt = await client.post("/deal")
    assert peek.json()["next_card"] == dealt.json()["card"]
    assert dealt.json()["remaining"] == 51


@pytest.mark.asyncio
async def test_discard_and_state_endpoints(client: AsyncClient):
    # deal & discard a card
    dealt = (await client.post("/deal")).json()["card"]
    await client.post("/discard", json=dealt)

    discard_state = (await client.get("/discard-state")).json()
    assert discard_state["size"] == 1
    assert discard_state["cards"][0] == dealt

    deck_state = (await client.get("/deck-state")).json()
    assert deck_state["size"] == 51
    assert dealt not in deck_state["cards"]


@pytest.mark.asyncio
async def test_shuffle_then_order_restores_default(client: AsyncClient):
    await client.post("/shuffle")
    first_after_shuffle = (await client.get("/cheat")).json()["next_card"]

    await client.post("/order")
    first_after_order = (await client.get("/cheat")).json()["next_card"]

    assert first_after_shuffle != first_after_order          # order changed
    assert first_after_order == {"rank": "2", "suit": "spades"}


@pytest.mark.asyncio
async def test_cut_endpoint(client: AsyncClient):
    # cut at index 10
    await client.post("/cut/10")
    cheat = (await client.get("/cheat")).json()["next_card"]
    assert cheat == {"rank": "Queen", "suit": "spades"}


@pytest.mark.asyncio
async def test_cut_invalid_returns_400(client: AsyncClient):
    r = await client.post("/cut/0")
    assert r.status_code == 400
    assert "out of bounds" in r.json()["detail"]


@pytest.mark.asyncio
async def test_deal_until_empty_then_error(client: AsyncClient):
    for _ in range(52):
        await client.post("/deal")
    r = await client.post("/deal")
    assert r.status_code == 400
    assert r.json()["detail"] == "Deck is empty"


@pytest.mark.asyncio
async def test_rebuild_endpoint(client: AsyncClient):
    dealt = (await client.post("/deal")).json()["card"]
    await client.post("/discard", json=dealt)
    r = await client.post("/rebuild")
    payload = r.json()
    assert payload["deck_size"] == 52 and payload["discard_size"] == 0
    top = (await client.get("/cheat")).json()["next_card"]
    assert top == {"rank": "2", "suit": "spades"}   # reset order


@pytest.mark.asyncio
async def test_shuffle_api_changes_order(client: AsyncClient):
    before = (await client.get("/cheat")).json()["next_card"]
    await client.post("/shuffle")
    after = (await client.get("/cheat")).json()["next_card"]
    assert before != after

