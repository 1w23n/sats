#!/bin/env python

import random

drawcards = []
card_mark = ["s", "h", "c", "d"]

def draw():
  #for m in card_mark:
  #  for i in range(1, 14):
  #    drawcards.append([m, i])
  #random.shuffle(drawcards)

  marks = ["club", "diamond", "spade", "heart"]
  numbers = range(1,14)
  cards = [(m,n) for m in marks for n in numbers]

  random.choice(cards)
  
def blackjack():
  draw()

if __name__ == "__main__":
  blackjack()
  print(cards)
