#!/bin/env python

import random

card_mark = ["s", "h", "c", "d"]
drawcards = [(m,i) for m in card_mark for i in range(1,14)]

player_cards = []
dealer_cards = []

def score(card_list):
  i = 0
  score = 0
  while i < len(card_list):
    card_num = card_list[i][1]
    if card_num in [11, 12, 13]:
      score += 10
    elif card_num == 1:
      if score + 11 > 21:
        score += 1
      else:
        score += 11
    else:
      score += int(card_num)
    i += 1
  return score

def draw():
  choice = random.choice(drawcards)
  drawcards.remove(choice)
  return choice

player_cards.append(draw())
player_cards.append(draw())

dealer_cards.append(draw())

player_score = score(player_cards)

print("Player card is", {m + str(n) for m,n in player_cards}, ":Total ", player_score)
print("========================================")
print("Dealer card is", {m + str(n) for m,n in dealer_cards}, "{'??'}")
print("========================================")

dealer_cards.append(draw())
dealer_score = score(dealer_cards)

while(1):
  choice = input("Hit or Stand? (h/s): ")
  if choice == "h":

    player_cards.append(draw())
    player_score = score(player_cards)

    print("========================================")
    print("Player card is", {m + str(n) for m,n in player_cards}, ":Total ", player_score)
    print("========================================")
    player_score = score(player_cards)

    if player_score > 21:
      print("Bust: You lose...")
      raise SystemExit

  if choice == "s":
    break

while(1):
  print("Dealer card is", {m + str(n) for m,n in dealer_cards}, ":Total ", dealer_score)
  print("========================================")

  if dealer_score > 21:
    print("Bust: You win!!")
    break
  elif dealer_score == 21:
    print("Blackjack: You lose...")
    break
  elif dealer_score < 17:
    dealer_cards.append(draw())
    dealer_score = score(dealer_cards)
  elif dealer_score > 16:
    if player_score > dealer_score:
      print("You win!!")
      break
    elif player_score < dealer_score:
      print("You lose...")
      break
    else:
      print("Draw.")
      break
