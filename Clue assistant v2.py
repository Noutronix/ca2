import csv
import copy

names = ["green", "mustard", "peacock", "plum", "scarlett","white"]
weapons = ["candlestick", "knife", "pistol", "pipe", "rope", "wrench"]
rooms = ["conservatory", "ballroom", "kitchen", "dining room", 
         "lounge", "hall", "study", "billiard room","library"]

def check(ans: str, group: list):
    while True:
        if ans in group:
            return ans
        else:
            raise NameError

class case_file:
    def __init__(self):
        self.name = None
        self.weapon = None
        self.room = None

class player:
    def __init__(self, cards: list):
        self.cards = cards
        

class opponent:
    def __init__(self, name: str, card_number: int, dh: list):
        self.name = name
        self.doesnt_have = set(dh)
        self.card_number = card_number
        self.options = []
        self.cards = set()

def create_opponents(op_data, cards):
    opponents = []
    for name, card_number in op_data:
        op = opponent(name, card_number, copy.copy(cards))
        opponents.append(op)
    return opponents

def answer():
    global cfile
    cfile = case_file()

    #opening files
    f1 = open("ca2_names.csv", "r" )
    op_data = [[i[0].lower(), int(i[1])] for i in [x for x in csv.reader(f1)]]
    f2 = open("ca2_cards.csv", "r")
    cards = [i.lower() for i in [x for x in csv.reader(f2)][0]]
    cards = [x.replace(" ", "") for x in cards]
    f3 = open("ca2_turns.csv", "r")
    turns = [[i.lower() for i in x] for x in csv.reader(f3)]
    turns = [[i.replace(" ", "") for i in x] for x in turns]
    f1.close()
    f2.close()
    f3.close()

    opponents = create_opponents(op_data, cards)
    me = player(cards)
    dh(turns, opponents, me, op_data)

def dh(turns, opponents, me, op_data):

    for turn in turns:
        char = check(turn[0], names)
        weapon = check(turn[1], weapons)
        room = check(turn[2], rooms)
        if turn[3] == "self":
            taker = me
        else:
            taker = [x for x in opponents if x.name == check(turn[3], [i[0] for i in op_data])][0]
        if turn[4] == "self":
            giver = me
        elif turn[4] == "none":
            giver = None
        else:
            giver = [x for x in opponents if x.name == check(turn[4], [i[0] for i in op_data])][0]
        if len(turn) == 6:
            card_gotten = check(turn[5], names+weapons+rooms)
        else:
            card_gotten = None
        others = []

        if taker == me:
            if giver != None:
                giver.cards.add(card_gotten)
                others = opponents[:opponents.index(giver)]
            else:
                for elm in [char, weapon, room]:
                    if not elm in me.cards:
                        if elm in names:
                            cfile.name = elm
                        if elm in weapons:
                            cfile.weapon = elm
                        if elm in rooms:
                            cfile.room = elm
                        for op in opponents:
                            op.doesnt_have.add(elm)
        

        if others != []: #at end
            for op in others:
                op.doesnt_have.update([char, weapon, room])
                e = 1 

answer()