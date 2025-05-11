import random
import pygame as pg
from collections import Counter
from itertools import islice
import time
from settings import Config
from cards import Card, Deck
from treys import Card as TreysCard, Evaluator, Deck as TreysDeck


class HandEvaluator:

    rank_value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    hand_ranking = {
        "High Card": 1, "One Pair": 2, "Two Pair": 3, "Three of a Kind": 4, "Straight": 5,
        "Flush": 6, "Full House": 7, "Four of a Kind": 8, "Straight Flush": 9
    }
    
    @staticmethod
    def evaluate_hand(hand):
        ranks = [card.rank for card in hand]
        suits = [card.suit for card in hand]
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        is_flush = any(count >= 5 for count in suit_counts.values())
        is_straight = HandEvaluator.is_straight(ranks)

        if is_flush and is_straight:
            return HandEvaluator.get_cards(hand, "Straight Flush")
        elif 4 in rank_counts.values():
            return HandEvaluator.get_cards(hand, "Four of a Kind")
        elif 3 in rank_counts.values() and 2 in rank_counts.values():
            return HandEvaluator.get_cards(hand, "Full House")
        elif is_flush:
            return HandEvaluator.get_cards(hand, "Flush")
        elif is_straight:
            return HandEvaluator.get_cards(hand, "Straight")
        elif 3 in rank_counts.values():
            return HandEvaluator.get_cards(hand, "Three of a Kind")
        elif list(rank_counts.values()).count(2) == 3:
            return HandEvaluator.get_cards(hand, "Three Pair")
        elif list(rank_counts.values()).count(2) == 2:
            return HandEvaluator.get_cards(hand, "Two Pair")
        elif 2 in rank_counts.values():
            return HandEvaluator.get_cards(hand, "One Pair")
        else:
            return HandEvaluator.get_cards(hand, "High Card")

    @staticmethod
    def get_cards(hand, function):
        return HandEvaluator.check_highest_value_cards(hand, function)

    @staticmethod
    def is_straight(ranks):
        rank_values = sorted(set(HandEvaluator.rank_value_map[rank] for rank in ranks))
        for i in range(len(rank_values) - 4):
            if rank_values[i:i + 5] == list(range(rank_values[i], rank_values[i] + 5)):
                return True
        return {14, 2, 3, 4, 5}.issubset(rank_values)

    @staticmethod
    def rank_to_value(rank):
        value_map = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
            '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }
        return value_map[rank]

    @staticmethod
    def calculate_card_value(card):
        rank_value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        suit_value_map = {'♣': 1, '♦': 2, '♥': 3, '♠': 4}
        fake_value = (rank_value_map[card.rank]*100) + suit_value_map[card.suit]
        return [rank_value_map[card.rank], suit_value_map[card.suit], fake_value]


    @staticmethod
    def check_highest_value_cards(hand, function):
        rank_value_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        suit_value_map = {'♣': 1, '♦': 2, '♥': 3, '♠': 4}
        ranks = [card.rank for card in hand]
        suits = [card.suit for card in hand]
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)

        if function == "High Card":
            best_card = max(hand, key=lambda card: HandEvaluator.calculate_card_value(card)[2])
            return ("High Card", [best_card])

        elif function == "One Pair":
            pair = [rank for rank, count in rank_counts.items() if count == 2]
            sorted_pairs = sorted(pair, key=lambda rank: rank_value_map[rank], reverse=True)
            top_pairs = sorted_pairs[:1]
            result_cards = [card for card in hand if card.rank in top_pairs]
            return ("One Pair", result_cards)

        elif function == "Two Pair" or function == "Three Pair":
            pairs = [rank for rank, count in rank_counts.items() if count == 2]
            sorted_pairs = sorted(pairs, key=lambda rank: rank_value_map[rank], reverse=True)
            top_pairs = sorted_pairs[:2] # get last 2
            result_cards = [card for card in hand if card.rank in top_pairs]
            return ("Two Pair", result_cards)

        elif function == "Three of a Kind":
            pairs = [rank for rank, count in rank_counts.items() if count == 3]
            sorted_pairs = sorted(pairs, key=lambda rank: rank_value_map[rank], reverse=True)
            top_pairs = sorted_pairs[:1]
            result_cards = [card for card in hand if card.rank in top_pairs]
            return ("Three of a Kind", result_cards)

        elif function == "Straight":
            sorted_hand = sorted(hand, key=lambda card: HandEvaluator.rank_to_value(card.rank))
            rank_values = {}
            
            # (handle duplicates)
            for card in sorted_hand:
                value = HandEvaluator.rank_to_value(card.rank)
                if value not in rank_values:
                    rank_values[value] = card  

            sorted_values = sorted(rank_values.keys())  
            consecutive_cards = []
            best_straight = []

            for i in range(len(sorted_values) - 1):
                if sorted_values[i] + 1 == sorted_values[i + 1]:
                    consecutive_cards.append(rank_values[sorted_values[i]])
                else:
                    consecutive_cards = []  # Reset if sequence breaks

                if len(consecutive_cards) == 4:  # Need one more card for a straight
                    consecutive_cards.append(rank_values[sorted_values[i + 1]])
                    best_straight = consecutive_cards[:]  # Store the best straight
                    break

            if {14, 2, 3, 4, 5}.issubset(set(sorted_values)):
                best_straight = [ rank_values[14], rank_values[2], rank_values[3], rank_values[4], rank_values[5]]

            return ("Straight", best_straight) if best_straight else ("No Straight", [])

        elif function == "Flush":
            suit_counts = Counter(card.suit for card in hand)
            flush_suit = next((suit for suit, count in suit_counts.items() if count >= 5), None)

            if flush_suit:
                flush_cards = [card for card in hand if card.suit == flush_suit]
                return ("Flush", flush_cards)

        elif function == "Full House":
            rank_counts = Counter(card.rank for card in hand)
            three_of_kind = [rank for rank, count in rank_counts.items() if count == 3]
            pair = [rank for rank, count in rank_counts.items() if count == 2]

            if three_of_kind and pair:
                # return ("Full House", [three_of_kind[0], pair[0]])
                return ("Full House", hand)

        elif function == "Four of a Kind":
            rank_counts = Counter(card.rank for card in hand)
            four_of_kind = [rank for rank, count in rank_counts.items() if count == 4]

            if four_of_kind:
                return ("Four of a Kind", hand[:4])

        elif function == "Straight Flush":
            # Group cards by suit
            suit_groups = {}
            for card in hand:
                if card.suit not in suit_groups:
                    suit_groups[card.suit] = []
                suit_groups[card.suit].append(card)

            # Variable to track the best straight flush
            best_straight_flush = []

            # Check each suit group for a straight flush
            for suit, cards in suit_groups.items():
                if len(cards) >= 5:  # A straight flush requires at least 5 cards of the same suit
                    sorted_cards = sorted(cards, key=lambda card: HandEvaluator.rank_to_value(card.rank))
                    rank_values = [HandEvaluator.rank_to_value(card.rank) for card in sorted_cards]

                    # Check for a normal straight flush
                    for i in range(len(rank_values) - 4):  # Ensure at least 5 cards are available
                        # Slice out the next 5 consecutive cards
                        consecutive_cards = sorted_cards[i:i + 5]
                        consecutive_values = rank_values[i:i + 5]

                        # Check if the cards are consecutive
                        if all(consecutive_values[j] + 1 == consecutive_values[j + 1] for j in range(4)):
                            # Update if this straight flush is better (higher rank)
                            if not best_straight_flush or HandEvaluator.rank_to_value(consecutive_cards[-1].rank) > HandEvaluator.rank_to_value(best_straight_flush[-1].rank):
                                best_straight_flush = consecutive_cards

                    # Check for the Wheel Straight (A-2-3-4-5)
                    if {14, 2, 3, 4, 5}.issubset(rank_values):
                        wheel_straight = [card for card in sorted_cards if HandEvaluator.rank_to_value(card.rank) in {14, 2, 3, 4, 5}]
                        if len(wheel_straight) == 5:  # Ensure it's exactly 5 cards
                            if not best_straight_flush or HandEvaluator.rank_to_value(wheel_straight[-1].rank) > HandEvaluator.rank_to_value(best_straight_flush[-1].rank):
                                best_straight_flush = wheel_straight

            if best_straight_flush:
                return ("Straight Flush", best_straight_flush)
            else:
                return ("No Straight Flush", [])
                
    @staticmethod
    def compare_hands(hand1, hand2):
        hand1_type, hand1_cards = HandEvaluator.evaluate_hand(hand1)
        hand2_type, hand2_cards = HandEvaluator.evaluate_hand(hand2)

        hand_rankings = {
            "High Card": 1, "One Pair": 2, "Two Pair": 3, "Three of a Kind": 4,
            "Straight": 5, "Flush": 6, "Full House": 7, "Four of a Kind": 8,
            "Straight Flush": 9
        }

        if hand_rankings[hand1_type] > hand_rankings[hand2_type]:
            return (f"You win with {hand1_type} ({hand1_cards})", "hand1")
        elif hand_rankings[hand1_type] < hand_rankings[hand2_type]:
            return (f"Bot win with {hand2_type} ({hand2_cards})", "hand2")

        hand1_values = sorted([HandEvaluator.rank_to_value(card.rank) for card in hand1_cards], reverse=True)
        hand2_values = sorted([HandEvaluator.rank_to_value(card.rank) for card in hand2_cards], reverse=True)
        # print("hand1_values", hand1_values)
        # print("hand2_values", hand2_values)

        # Compare values one by one
        for v1, v2 in zip(hand1_values, hand2_values):
            if v1 > v2:
                return (f"You win with {hand1_type} ({hand1_cards})", "hand1")
            elif v1 < v2:
                return (f"Bot win with {hand2_type} ({hand2_cards})", "hand2")

        return "It's a tie!", "tie"

    
    @staticmethod
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

            opp_hand = sim_deck[:2]

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

        return round(100 * (wins + ties / 2) / num_simulations, 2)


