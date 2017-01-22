# draw a cards randomly
import random

marks = ["club", "diamond", "spade", "heart"]
numbers = range(1,14)
cards = [(m,n) for m in marks for n in numbers]

random.choice(cards)

