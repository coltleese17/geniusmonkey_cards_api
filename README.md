# Genius Monkey Deck Dealer API

FastAPI micro-service that models a dealer, a live deck, and a discard pile.  
**Endpoints:** deal, cheat (peek), shuffle, cut, order, discard, rebuild, deck-state, discard-state.

---

## 1  Prerequisites

| Tool | Version (tested) |
|------|------------------|
| Python | 3.10 – 3.12 |
| pip | ≥ 22 |
| (optional) `jq` | for pretty printing in the demo script |

---

## 2  Setup & install

```bash
# 1 clone
git clone https://github.com/coltleese17/geniusmonkey_cards_api
cd geniusmonkey_cards_api

# 2 create and activate a virtual-env
python3 -m venv .venv
source .venv/bin/activate             

# 3 install runtime + dev dependencies
pip3 install -r requirements.txt      
```

## 3 Run the service
```bash
uvicorn cardapi.main:app --reload       # http://127.0.0.1:8000
```
## 4 Demo Script

```bash
chmod +x demo.sh
./demo.sh
```
The script will run curl the endpoints and demonstrate all the specified functionality:

Reset the deck (/rebuild)

Peek, deal, discard

Shuffle, cut (middle), order

Rebuild the full deck again

Print deck/discard snapshots throughout

If jq is installed the JSON is colour-formatted.

## 5 Interactive API docs

Swagger UI:	http://127.0.0.1:8000/docs

ReDoc:	http://127.0.0.1:8000/redoc

Generated automatically from the OpenAPI spec

From these docs you can view the endpoints, payloads, and make requests to the endpoints (if the local server is live)
There is also an attached json collection "deck_dealer_collection.json" which can be imported to postman or similar to make hitting the endpoints easier

## 6 Run the tests

From root run: ```pytest -q```
