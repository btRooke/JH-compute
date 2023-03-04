import random

class Deck:
    def __init__(self, seed = None) -> None:
        values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        suits = ["Spades", "Clubs", "Hearts", "Diamonds"]

        # Create a deck and shuffle it
        deck = [(suit, value) for suit in suits for value in values]
        
        rng = random.Random(seed) if seed is not None else random.Random()
        rng.shuffle(deck)

        # Expose the iterator
        self.cards = iter(deck)
 
    
    def get_card(self):
        return next(self.cards)