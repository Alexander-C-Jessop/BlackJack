"""
Blackjack, also known as assignment #5
"""
import random

# Unicode symbols for the card deck (they will not appear as a symbol in git bash)
HEART_SYMBOL = '\u2665'
DIAMOND_SYMBOL = '\u2666'
CLUB_SYMBOL = '\u2663'
SPADE_SYMBOL = '\u2660'

# Fundamentals of the deck
CARD_SUITS = [SPADE_SYMBOL, CLUB_SYMBOL, DIAMOND_SYMBOL, HEART_SYMBOL]
CARD_VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]


def create_deck():
    """
    Returns a standard deck of 52 playing cards.

    The deck consists of 4 suits as displayed in the variable CARD_SUITS
    and 13 card values as shown in CARD_VALUES
    Each card is represented as a string with the format: "value + suit"
    """
    deck = []
    for card_type in CARD_SUITS:
        for value in CARD_VALUES:
            deck.append(str(value) + card_type)
    return deck


def shuffle_deck(cards):
    """
    Shuffles a given list.

    Args:
        cards should be a list.
    """
    random.shuffle(cards)


def deal_card(deck):
    """
    Deals a card from the "top" of the deck using the pop() method.

    Args:
        deck, should be a list

    First it checks if the deck is empty, if it is it creates a new
    deck and shuffles it. The function then removes the top card from
    the deck and determines its value based on the value. To get the
    value simply remove the suit of the card since values can be up to
    2 digits long. If the card is an Ace, the function prompts the player
    to choose whether to use it as a value of 1 or 10, and adjusts the
    value accordingly. The function then returns a tuple containing the
    card and its value.
    """
    if len(deck) < 1:
        print("Deck is empty. Creating new deck and shuffling...")
        deck = create_deck()
        shuffle_deck(deck)
        print("Dealing from new deck.")
    card = deck.pop()
    value = card[:-1]
    return card, value


def total_hand(hand, ace_value=None):
    """
    Calculates the total value of a hand of cards.

    If an Ace is present in the hand and `ace_value` is not specified,
    the value of the first Ace in the hand is set to 11, and any
    additional Aces are set to 1; unless the total value of the hand
    is greater than 21, in which case the value of the first Ace is
    set to 1 and any additional Aces are set to 1.
    """
    total = 0
    num_aces = 0
    for card in hand:
        value = card[:-1]
        if value in ["J", "Q", "K"]:
            total += 10
        elif value == "A":
            num_aces += 1
            if num_aces == 1 and ace_value is None:
                total += 11
            else:
                total += 1
        else:
            total += int(value)
    while total > 21 and num_aces > 0:
        total -= 10
        num_aces -= 1
    return total


def start_game():
    """
    Asks the user if they want to start a game of Black Jack.
    """
    response = input("Do you want to play Black Jack? (Y or N): ").strip().upper()
    if not response:
        print("A selection is needed to continue!")
        start_game()
    elif response in ["N", "NO"]:
        print("You walked away from the table. Have a good night!")
        exit()
    elif response not in ["Y", "YES"]:
        print("Invalid selection. Please enter Y or N.")
        start_game()


def player_name():
    """
    Asks the player to enter their name and validates the input.
    """
    while True:
        user_name = input("Please enter your name: ").strip().title()
        if not user_name:
            print("Invalid input, please enter a name.")
            continue
        if any(char.isdigit() for char in user_name):
            print("Invalid input, please enter a name without any numbers.")
            continue
        return user_name


def play_blackjack():
    """
    Main function to play blackjack.
    """
    start_game()

    player = player_name()
    print(f"Welcome {player}, let's play some 21!")

    while True:
        # Initialize game
        deck = create_deck()
        shuffle_deck(deck)
        player_hand = []
        dealer_hand = []
        player_total = 0
        dealer_total = 0

        # Deal initial cards
        for i in range(2):
            player_card, player_value = deal_card(deck)
            player_hand.append(player_card)
            player_total += total_hand(player_hand)
            player_total = total_hand(player_hand)
            print(f"You were dealt: {player_card}")
        print(f"Your hand is: {player_hand[0]}, {player_hand[1]}")
        print(f"Your total is: {player_total}")

        dealer_card, dealer_value = deal_card(deck)
        dealer_hand.append(dealer_card)
        dealer_total += total_hand(dealer_hand)
        print(f"Dealer was dealt: {dealer_card}")

        dealer_card, dealer_value = deal_card(deck)
        dealer_hand.append(dealer_card)
        print("Dealer's second card is face down.")

        # Player turn
        while player_total < 21:
            hit = input("Do you want to hit? (Y or N): ").strip().upper()
            if not hit:
                print("A selection is needed to continue!")
                continue
            elif hit in ["N", "NO"]:
                print(f"You stand with a total of: {player_total}")
                break
            elif hit not in ["Y", "YES"]:
                print("Invalid selection. Please enter Y or N.")
                continue

            player_card, player_value = deal_card(deck)
            player_hand.append(player_card)
            player_total = total_hand(player_hand)
            print(f"You were dealt: {player_card}")
            print(f"Your total is: {player_total}")

            if player_total > 21:
                print(f"You busted with a total of: {player_total}")
                break

        # Dealer turn
        while dealer_total < 17 and player_total <= 21:
            print(f"Dealer's hand is: {dealer_hand[0]}, {dealer_hand[1]}")
            dealer_card, dealer_value = deal_card(deck)
            dealer_hand.append(dealer_card)
            dealer_total = total_hand(dealer_hand)
            print(f"Dealer was dealt: {dealer_card}")
            print(f"Dealer total is: {dealer_total}")

            if dealer_total > 21:
                print(f"Dealer busted with a total of: {dealer_total}")
                break

        # Determine winner
        if dealer_total > 21 or (player_total <= 21 and player_total > dealer_total):
            print(f"{player}, you win with a total of: {player_total}! Congratulations!")
        elif player_total > 21 or player_total < dealer_total:
            print(f"Dealer wins with a total of: {dealer_total}. Better luck next time, {player}!")
        else:
            print(f"It's a tie! Both you and the dealer have a total of: {player_total}.")

        # Ask to play again
        play_again = input("Do you want to play again? (Y or N): ").strip().upper()
        if play_again not in ["Y", "YES"]:
            print("You walked away from the table. Thanks for playing!")
            break


play_blackjack()
