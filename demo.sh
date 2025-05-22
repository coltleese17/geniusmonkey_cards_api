#!/usr/bin/env bash
# demo.sh – cURL walkthrough for the Deck Dealer API
# Usage: start the API with
#   uvicorn cardapi.main:app --reload
# then run:  ./demo.sh
# (jq is optional, purely for pretty-printing)

BASE=http://127.0.0.1:8000        # adjust if needed

jqp() { command -v jq >/dev/null && jq -C "$@" || cat; }

#####################################################################
# 0. Hard-reset the in-memory game state ----------------------------
#####################################################################
echo "♻️  0. Rebuild – ensure full 52-card ordered deck & empty discard"
curl -s -X POST $BASE/rebuild | jqp '.'
echo

#####################################################################
# 1. Fresh state check ----------------------------------------------
#####################################################################
echo "▶️  1. Verify starting deck"
curl -s $BASE/deck-state | jqp '.'
echo "▶️  Verify starting discard pile"
curl -s $BASE/discard-state | jqp '.'
echo

#####################################################################
# 2. Cheat -----------------------------------------------------------
#####################################################################
echo "▶️  2. Cheat – peek at the next card"
curl -s $BASE/cheat | jqp '.'
echo

#####################################################################
# 3. Deal ------------------------------------------------------------
#####################################################################
echo "▶️  3. Deal one card"
DEAL_RAW=$(curl -s -X POST $BASE/deal)   
echo "$DEAL_RAW" | jqp '.'               
CARD_JSON=$(echo "$DEAL_RAW" | jq -c '.card')

echo "Deck & discard sizes after dealing:"
curl -s $BASE/deck-state    | jqp '{size}'
curl -s $BASE/discard-state | jqp '{size}'
echo

#####################################################################
# 4. Discard ---------------------------------------------------------
#####################################################################
echo "▶️  4. Discard the dealt card"
curl -s -X POST -H "Content-Type: application/json" \
     -d "$CARD_JSON" \
     $BASE/discard | jqp '.'
echo

echo "Discard pile now:"
curl -s $BASE/discard-state | jqp '.'
echo

#####################################################################
# 5. Shuffle ---------------------------------------------------------
#####################################################################
echo "▶️  5. Shuffle remaining deck"
curl -s -X POST $BASE/shuffle | jqp '.'
echo "Top card after shuffle:"
curl -s $BASE/cheat | jqp '.'
echo

#####################################################################
# 6. Cut -------------------------------------------------------------
#####################################################################
echo "▶️  6. Cut deck at position 10"
curl -s -X POST $BASE/cut/10 | jqp '.'
echo "Top card after cut:"
curl -s $BASE/cheat | jqp '.'
echo

#####################################################################
# 7. Order -----------------------------------------------------------
#####################################################################
echo "▶️  7. Order remaining deck back to default order"
curl -s -X POST $BASE/order | jqp '.'
echo "Top card should be 2♠ again:"
curl -s $BASE/cheat | jqp '.'
echo

#####################################################################
# 8. Rebuild ---------------------------------------------------------
#####################################################################
echo "▶️  8. Rebuild deck (merge discard pile then re-order full deck)"
curl -s -X POST $BASE/rebuild | jqp '.'
echo

echo "Final state:"
curl -s $BASE/deck-state    | jqp '{size}'
curl -s $BASE/discard-state | jqp '{size}'
echo
echo "✅  Demo complete."
