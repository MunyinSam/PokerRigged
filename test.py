import random
from treys import Card as TreysCard, Evaluator, Deck as TreysDeck

class Card:
    def __init__(self, rank, suit):
        self.rank = rank  # '2' to 'A'
        self.suit = suit  # '♠', '♥', '♦', '♣'

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def to_treys(self):
        rank_map = {
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
            '7': '7', '8': '8', '9': '9', 'J': 'J', 'Q': 'Q',
            'K': 'K', 'A': 'A'
        }
        suit_map = {'♠': 's', '♥': 'h', '♦': 'd', '♣': 'c'}

        # Handle '10' as a special case
        if self.rank == '10':
            rank_str = 'T'
        else:
            rank_str = rank_map[self.rank]

        suit_str = suit_map[self.suit]

        return TreysCard.new(f"{rank_str}{suit_str}")

class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♥', '♦', '♣']

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def draw(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card


def calculate_winrate(hand1, community_cards, num_simulations=20000):
    evaluator = Evaluator()

    # Sanity check
    if len(hand1) != 2:
        raise ValueError("Your hand must contain exactly 2 cards.")
    if len(community_cards) > 5:
        raise ValueError("Community cards cannot exceed 5.")

    known_cards = hand1 + community_cards
    known_card_strs = set(repr(c) for c in known_cards)

    # Build custom deck minus known cards
    full_deck = Deck()
    full_deck.cards = [card for card in full_deck.cards if repr(card) not in known_card_strs]

    wins = 0
    ties = 0

    for _ in range(num_simulations):
        sim_deck = full_deck.cards[:]
        random.shuffle(sim_deck)

        # Draw random opponent hand (2 cards)
        opp_hand = sim_deck[:2]

        # Draw remaining community cards
        missing = 5 - len(community_cards)
        board_fill = sim_deck[2:2 + missing]
        full_board = community_cards + board_fill

        # Convert to treys
        hand1_treys = [c.to_treys() for c in hand1]
        hand2_treys = [c.to_treys() for c in opp_hand]
        board_treys = [c.to_treys() for c in full_board]

        # Evaluate
        hand1_score = evaluator.evaluate(hand1_treys, board_treys)
        hand2_score = evaluator.evaluate(hand2_treys, board_treys)

        if hand1_score < hand2_score:
            wins += 1
        elif hand1_score == hand2_score:
            ties += 1
        # else: loss

    return round(100 * (wins + ties / 2) / num_simulations, 2)

my_hand = [Card('3', '♠'), Card('7', '♦')]
community = [Card('2', '♠'), Card('10', '♥'), Card('9', '♣')]

winrate = calculate_winrate(my_hand, community)
print(f"Estimated winrate: {winrate}%")

