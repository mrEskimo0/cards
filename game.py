from collections import namedtuple
import random
import time


class Game:

    def __init__(self):
        self.deck = Deck()
        self._players = []
        self._cards_per_player = 5
        self._score = {}
        self._add_players()

    def _add_players(self):
        players = input(
            'Enter player names seperated by a comma (i.e. "Bill, Ted, Jerry"):\n')
        formatted_players = self._clean_player_input(players)
        for p in formatted_players:
            self._players.append(Player(p))

    @staticmethod
    def _clean_player_input(user_input):
        player_list = user_input.split(',')
        formatted = map(lambda p: p.strip().upper(), player_list)
        return set(formatted)

    def _deal(self):
        for i in range(0, self._cards_per_player):
            for p in self._players:
                card = self.deck.draw()
                card.owner = p
                p.add_to_hand(card)

    @property
    def score(self):
        output = 'SCORE BOARD\n'
        for p in self._players:
            output = output + f"{p.name}: {self._score.get(p.name, 0)}\n"
        return output

    @score.setter
    def score(self, score):
        prev_score = self._score.get(score['player'], 0)
        self._score[score['player']] = prev_score + score['points']

    def start_game(self):
        self._deal()
        for card in range(0, self._cards_per_player):
            round = Round(self._players)
            self.score = round.play_round()
            print(self.score)
            time.sleep(1.5)

    def score_game(self):
        winner = max(self._score, key=self._score.get) if self._score else None
        if winner:
            print(f'{winner} wins!')
        return winner


class Deck:

    def __init__(self):
        self.suits = {
            "❤️": 0.3,
            "💎": 0.2,
            "☘️": 0.1,
            "♤": 0,
        }
        self.ranks = {
            'A': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'J': 11,
            'Q': 12,
            'K': 13,
        }
        self.deck = self._build_deck()
        self.shuffle()

    def _build_deck(self):
        '''Construct the deck using the suits and ranks'''
        deck = []
        for suit in self.suits.keys():
            for rank in self.ranks.keys():
                num_rank = self._compute_num_rank(
                    self.suits[suit],
                    self.ranks[rank]
                )
                deck.append(Card(suit, rank, num_rank))
        return deck

    @staticmethod
    def _compute_num_rank(*args):
        return sum(args)

    def shuffle(self):
        '''Shuffle the deck'''
        random.shuffle(self.deck)

    def draw(self):
        '''Draw card off the "top" of the deck and return it'''
        return self.deck.pop(0)

    def add_to_bottom(self, card_list):
        '''Add given card to "bottom" of the deck'''
        self.deck.extend(card_list)


class Card:
    def __init__(self, suit, rank, numeric_rank):
        self.suit = suit
        self.rank = rank
        self.numeric_rank = numeric_rank
        self.owner = None

    def _lookup_rank(self, symbol):
        value = self._rankings.get(symbol, self._rankings, 0)
        return value

    def __gt__(self, other):
        return self.numeric_rank > other.numeric_rank

    def __lt__(self, other):
        return self.numeric_rank < other.numeric_rank

    def __repr__(self):
        return self.suit + ' ' + self.rank


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def add_to_hand(self, card):
        self.hand.add_card(card)

    def play_card(self, card_num):
        card_index = int(card_num) - 1
        return self.hand.play_card(card_index)

    def __repr__(self):
        return self.name


class Hand:
    def __init__(self):
        self._cards = []

    def add_card(self, card):
        self._cards.append(card)

    def play_card(self, card_num):
        return self._cards.pop(card_num)

    def sort_hand(self):
        pass

    def length(self):
        return len(self._cards)

    def __repr__(self):
        return str(self._cards)


class Round:
    def __init__(self, players):
        self.board = Board()
        self.players = players
        self.score = 0
        self._award = 1

    def play_round(self):
        print('**** NEW ROUND ****')
        time.sleep(1)
        for player in self.players:
            self._take_turn(player)
        score = self._score_the_round()
        return score

    def _score_the_round(self):
        high_card = max(self.board.board)
        print(f'\n\n**** {high_card.owner} wins this round! ****')
        return {
            'player': high_card.owner.name,
            'points': self._award
        }

    def _take_turn(self, player):
        turn = self._create_turn(player)
        played_card = turn.choose_card()
        self._add_card_to_board(played_card)

    def _create_turn(self, player):
        '''Instantiate new turn with current player'''
        return Turn(player)

    def _add_card_to_board(self, card):
        self.board.add(card)
        print(f'\nBoard:\n{self.board}')
        time.sleep(0.5)


class Turn:
    def __init__(self, player):
        self.player = player
        print(f"\nIt is now {self.player}'s turn")

    def choose_card(self):
        confirmed = False
        while not confirmed:
            chosen_card_index = input(
                f'Choose a card from your hand:\n{self.player.hand}\n')
            if 0 < int(chosen_card_index) <= self.player.hand.length():
                confirmed = True
            else:
                print('Selection out of range, try again!!')
                time.sleep(1.5)
        return self.player.play_card(chosen_card_index)


class Board:
    def __init__(self):
        self.board = []

    def clear(self):
        return [self.board.pop(0) for c in self.board]

    def add(self, card):
        self.board.append(card)

    def undo(self):
        if len(self.board) > 0:
            return self.board.pop(-1)
        print("Can't undo...   ¯\_(ツ)_/¯")
        return

    def __repr__(self):
        return str(self.board)
