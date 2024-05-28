import random

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
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Define functions for gameplay
def take_bet():
    while True:
        try:
            bet = int(input("How much would you like to bet? "))
            if bet > 0:
                return bet
        except ValueError:
            print("Please enter a valid number.")


def hit(deck, hand):
    hand.add_card(deck.deal_card())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing  # to control an upcoming while loop

    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")

        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False
        else:
            print("Sorry, please try again.")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


# Gameplay logic
while True:
    print("Welcome to Blackjack!")

    # Create and shuffle the deck, deal two cards to each player
    deck = Deck()

    player_hand = Hand()
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    # Set up the player's chips and bet
    player_chips = 100  # Starting chips
    bet = take_bet()

    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    playing = True
    while playing:  # recall this variable from our hit_or_stand function
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)

        # If player's hand exceeds 21, player busts
        if player_hand.value > 21:
            print("Player busts! Dealer wins.")
            player_chips -= bet
            break

    # If player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Test different winning scenarios
        if dealer_hand.value > 21:
            print("Dealer busts! Player wins.")
            player_chips += bet
        elif dealer_hand.value > player_hand.value:
            print("Dealer wins.")
            player_chips -= bet
        elif dealer_hand.value < player_hand.value:
            print("Player wins!")
            player_chips += bet
        else:
            print("It's a tie! Push.")

    # Inform Player of their chips total
    print(f"\nPlayer's chips total: {player_chips}")

    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    if new_game[0].lower() != 'y':
        print("Thanks for playing!")
        break