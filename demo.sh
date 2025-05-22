#!/usr/bin/env bash
# demo.sh – cURL walkthrough for the Deck Dealer API

BASE=http://127.0.0.1:8000   # adjust if needed
jqp() { command -v jq >/dev/null && jq -C "$@" || cat; }

#####################################################################
# 0. Hard-reset ------------------------------------------------------
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
echo

#####################################################################
# 4. Discard ---------------------------------------------------------
#####################################################################
echo "▶️  4. Discard the dealt card"
curl -s -X POST -H "Content-Type: application/json" -d "$CARD_JSON" \
     $BASE/discard | jqp '.'
echo "Discard Pile State"
curl -s $BASE/discard-state | jqp '.'
echo

#####################################################################
# 5. Cut -------------------------------------------------------------
#####################################################################
#   Compute middle index (floor(size/2)) on-the-fly
MID=$(curl -s $BASE/deck-state | jq '.size / 2 | floor')
echo "▶️  5. Cut deck exactly in the middle (index $MID)"
curl -s -X POST $BASE/cut/$MID | jqp '.'
echo "Deck snapshot after cut (first 10 cards):"
curl -s $BASE/deck-state | jqp '{top10: .cards[0:10]}'
echo

#####################################################################
# 6. Shuffle ---------------------------------------------------------
#####################################################################
echo "▶️  6. Shuffle remaining deck"
curl -s -X POST $BASE/shuffle | jqp '.'
echo "Deck snapshot after shuffle (first 10 cards):"
curl -s $BASE/deck-state | jqp '{top10: .cards[0:10]}'
echo



#####################################################################
# 7. Order -----------------------------------------------------------
#####################################################################
echo "▶️  7. Order remaining deck back to default order"
curl -s -X POST $BASE/order | jqp '.'
echo "Top card should be 3♠ as 2♠ was discarded:"
curl -s $BASE/cheat | jqp '.'
echo

#####################################################################
# 8. Rebuild ---------------------------------------------------------
#####################################################################
echo "▶️  8. Rebuild deck (merge discard pile then re-order full deck)"
curl -s -X POST $BASE/rebuild | jqp '.'
echo
curl -s $BASE/deck-state    | jqp '{size, top10: .cards[0:10]}'
curl -s $BASE/discard-state | jqp '{size}'
echo
echo "✅  Demo complete."
