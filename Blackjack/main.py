import random

# Define the Card class to represent a playing card
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"

# Define the Deck class to create and manage a deck of cards
class Deck:
    def __init__(self):
        self.cards = []
        # Define the suits and ranks for the cards
        suits = ["spades", "clubs", "hearts", "diamonds"]
        ranks = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            # ... (other ranks)
            {"rank": "K", "value": 10},
        ]

        # Create a deck by combining suits and ranks
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # Shuffle the deck (if it has more than one card)
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        # Deal a specified number of cards from the deck
        for x in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt

# Define the Hand class to represent a player's or dealer's hand
class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        # Add a list of cards to the hand
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "A":
                has_ace = True

        # Adjust the value if there's an Ace and the total value is over 21
        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        # Check if the hand has a value of 21, indicating a blackjack
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        # Display the hand, hiding the first card if it's the dealer's and not revealed
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                print("hidden")
            else:
                print(card)

        if not self.dealer:
            print("Value:", self.get_value())
        print()

# Define the Game class to manage the gameplay
class Game:
    def play(self):
        game_number = 0
        games_to_play = 0

        # Get the number of games to play from the user
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except:
                print("You must enter a number.")

        # Play the specified number of games
        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            # Deal two cards to both player and dealer
            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            choice = ""
            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("Please choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please enter 'Hit' or 'Stand' (or H/S) ").lower()
                    print()
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_cards=True)

            if self.check_winner(player_hand, dealer_hand):
                continue

            print("Final Results")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)

            self.check_winner(player_hand, dealer_hand, True)

        print("\nThanks for playing!")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("Dealer wins!")
                return True
            elif dealer_hand.get_value() > 21:
                print("You win! ")
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both players have blackjack! Tie! ")
                return True
            elif player_hand.is_blackjack():
                print("You have blackjack. You win! ")
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has blackjack. Dealer wins! ")
                return True
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("You win! ")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("Tie! ")
            else:
                print("Dealer wins. ")
            return True

# Create a game object and start playing
g = Game()
g.play()
