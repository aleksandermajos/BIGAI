import random
from itertools import combinations

# Define the card deck and values
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


# Define a card class
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Define a deck class
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()


# Define a hand class
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def __str__(self):
        return ', '.join([str(card) for card in self.cards])


# Function to determine hand rank (simplified)
def hand_rank(hand):
    # Sort cards by rank
    ranks = sorted([card.rank for card in hand], key=lambda x: values[x], reverse=True)
    # This is a simplified version: it only considers high card
    return values[ranks[0]]


# Function to get the best hand from community and player cards
def best_hand(player_hand, community_cards):
    all_cards = player_hand.cards + community_cards
    best = None
    best_rank = -1
    for comb in combinations(all_cards, 5):
        rank = hand_rank(comb)
        if rank > best_rank:
            best = comb
            best_rank = rank
    return best


# Poker game logic
def poker_game():
    print("Welcome to Texas Hold'em Poker!")

    deck = Deck()

    # Deal two cards to each player
    player1_hand = Hand()
    player2_hand = Hand()

    for _ in range(2):
        player1_hand.add_card(deck.deal_card())
        player2_hand.add_card(deck.deal_card())

    # Deal five community cards
    community_cards = []
    for _ in range(5):
        community_cards.append(deck.deal_card())

    print("Player 1's hand:", player1_hand)
    print("Player 2's hand:", player2_hand)
    print("Community cards:", ', '.join([str(card) for card in community_cards]))

    player1_best_hand = best_hand(player1_hand, community_cards)
    player2_best_hand = best_hand(player2_hand, community_cards)

    print("Player 1's best hand:", ', '.join([str(card) for card in player1_best_hand]))
    print("Player 2's best hand:", ', '.join([str(card) for card in player2_best_hand]))

    if hand_rank(player1_best_hand) > hand_rank(player2_best_hand):
        print("Player 1 wins!")
    elif hand_rank(player1_best_hand) < hand_rank(player2_best_hand):
        print("Player 2 wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    poker_game()