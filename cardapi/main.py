from fastapi import FastAPI, HTTPException, Body
from cardapi.deck import DeckService         
from cardapi.models import Card               

app = FastAPI(title="Genius Monkey Deck Dealer API", version="1.1.0")
service = DeckService()

@app.post("/deal")
async def deal_card():
    try:
        card = service.deal()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"card": card.model_dump(), "remaining": service.deck_size}


@app.get("/cheat")
async def cheat():
    try:
        card = service.peek()
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"next_card": card.model_dump(), "remaining": service.deck_size}


@app.post("/shuffle")
async def shuffle():
    service.shuffle()
    return {"remaining": service.deck_size}


@app.post("/cut/{index}")
async def cut(index: int):
    try:
        service.cut(index)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"cut_at": index, "top_card": service.peek().model_dump()}


@app.post("/order")
async def order():
    service.order()
    return {"status": "ordered", "top_card": service.peek().model_dump()}


@app.post("/discard")
async def discard(card: Card = Body(...)):
    service.discard(card)
    return {"discarded": card.model_dump(), "discard_pile": service.discard_size}


@app.post("/rebuild")
async def rebuild():
    service.rebuild()
    return {
        "status": "rebuilt",
        "deck_size": service.deck_size,
        "discard_size": service.discard_size,
    }

@app.get("/deck-state")
async def deck_state():
    """Full JSON list of the remaining cards in top-to-bottom order."""
    return {
        "size": service.deck_size,
        "cards": [c.model_dump() for c in service.deck_state()],
    }


@app.get("/discard-state")
async def discard_state():
    """JSON list of discarded cards in the order they were discarded."""
    return {
        "size": service.discard_size,
        "cards": [c.model_dump() for c in service.discard_state()],
    }

