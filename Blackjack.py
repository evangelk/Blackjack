import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome_bus = ""
score = 0
game = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []        

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in range(len(self.hand)):
            ans = ans + " " + self.hand[i]
        return ans

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(str(card))

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        ace = False
        for x in self.hand:
            value += VALUES[x[1]]
            if x[1] == 'A':
                ace = True            
        if ace and value <= 11:
            value += 10
        return value
              
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        move = 0
        for x in self.hand:
            card = Card(x[0],x[1])
            card.draw(canvas,[pos[0]+move,pos[1]])  
            move += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i,j))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for i in range(len(self.deck)):
            ans = ans + " " + str(self.deck[i])
        return ans

#define event handlers for buttons
def deal():
    global outcome, outcome_bus, in_play, game
    global GameDeck
    global GamePlayerHand, GameDealerHand
    game += 1
    outcome = ""	
    in_play = True    
    GameDeck = Deck()
    GamePlayerHand = Hand()
    GameDealerHand = Hand()
    GameDeck.shuffle()
    GamePlayerHand.add_card(GameDeck.deal_card())
    GameDealerHand.add_card(GameDeck.deal_card()) 
    GamePlayerHand.add_card(GameDeck.deal_card())
    GameDealerHand.add_card(GameDeck.deal_card()) 
    print "Player's Hand =>",GamePlayerHand
    print "Dealer's Hand =>",GameDealerHand
    print "Player's Points :",str(GamePlayerHand.get_value())
    print "Dealer's Points :",str(GameDealerHand.get_value())
    print "================="    

def hit():
    # if the hand is in play, hit the player   
    # if busted, assign a message to outcome, update in_play and score
    global outcome, outcome_bus, in_play, score
    global GameDeck
    global GamePlayerHand
    if GamePlayerHand.get_value() <= 21:
        GamePlayerHand.add_card(GameDeck.deal_card())
        print "Player's Hand =>",GamePlayerHand
        print "Player's Points :",str(GamePlayerHand.get_value())
        print "================="
    if GamePlayerHand.get_value() > 21:
        outcome_bus = "Player busted!"
        outcome = "-- DEALER WINS --"
        in_play = False        
        print outcome       
    
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global outcome, outcome_bus, in_play, score
    global GameDeck
    global GamePlayerHand,GameDealerHand
    if GamePlayerHand.get_value() > 21:
        outcome_bus = "Player busted!" 
        outcome = "-- DEALER WINS --"
    else:
        while GameDealerHand.get_value() < 17:
            GameDealerHand.add_card(GameDeck.deal_card())
            print "Dealer's Hand =>",GameDealerHand
            print "Dealer's Points :",str(GameDealerHand.get_value())
            print "================="            
        if GameDealerHand.get_value() > 21:
            outcome_bus = "Dealer busted!"
            outcome = "-- PLAYER WINS --"
            score += 1
        else:
            if GameDealerHand.get_value() >= GamePlayerHand.get_value():
                outcome = "-- DEALER WINS --"
                outcome_bus = ""
            else:
                outcome = "-- PLAYER WINS --"
                outcome_bus = ""
                score += 1
    in_play = False
    print outcome

# draw handler    
def draw(canvas):
    global outcome,outcome_bus
    global GamePlayerHand,GameDealerHand   
    canvas.draw_text('BlackJack',(250,30),30,'White','serif')
    canvas.draw_text('Player',(100,180),30,'White','serif')
    canvas.draw_text('Dealer',(100,380),30,'White','serif')
    canvas.draw_text("Wins : "+str(score)+" || "+"Games : "+str(game),(230,100),20,'Yellow','serif')
    if in_play:
        canvas.draw_text('Hit or Stand?',(300,180),25,'Cyan','serif')
        GamePlayerHand.draw(canvas,[100,200])
        GameDealerHand.draw(canvas,[100,400])
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,(CARD_BACK_CENTER[0]+100,CARD_BACK_CENTER[1]+400),CARD_BACK_SIZE) 
    else:
        canvas.draw_text(outcome,(225,75),20,'Cyan','serif')
        canvas.draw_text(outcome_bus,(235,550),30,'Red','serif')
        canvas.draw_text('New Deal?',(300,180),25,'Cyan','serif')
        GamePlayerHand.draw(canvas,[100,200])
        GameDealerHand.draw(canvas,[100,400])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
