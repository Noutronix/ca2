import csv
import copy
import random

names = {"green", "mustard", "peacock", "plum", "scarlett","white"}
weapons = {"candlestick", "knife", "pistol", "pipe", "rope", "wrench"}
rooms = {"conservatory", "ballroom", "kitchen", "diningroom", 
         "lounge", "hall", "study", "billiardroom","library"}
everything = {"green", "mustard", "peacock", "plum", "scarlett","white", "candlestick", 
             "knife", "pistol", "pipe", "rope", "wrench", "conservatory", 
             "ballroom", "kitchen", "diningroom", "lounge", "hall", "study", "billiardroom","library"}


def check(ans: str, group: list):
    while True:
        if ans in group:
            return ans
        else:
            raise NameError


def translate_turn(turn, me, opponents, op_data):
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
        card_gotten = check(turn[5], everything)
    else:
        card_gotten = None
    return [char, weapon, room, taker, giver, card_gotten]


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
    with open("ca2_names.csv", "r" ) as f1:
        op_data = [[i[0].lower(), int(i[1])] for i in [x for x in csv.reader(f1)]]
    with open("ca2_cards.csv", "r") as f2:
        cards = [i.lower() for i in [x for x in csv.reader(f2)][0]]
        cards = [x.replace(" ", "") for x in cards]
    with open("ca2_turns.csv", "r") as f3:
        turns = [[i.lower() for i in x] for x in csv.reader(f3)]
        turns = [[i.replace(" ", "") for i in x] for x in turns]

    opponents = create_opponents(op_data, cards)
    me = player(cards)
    dh(turns, opponents, me, op_data)
    op_options(turns, opponents, me, op_data)
    cfile_contents(turns, opponents, me, op_data)
    with open("ca2_output.txt", "w") as f4:
        f4.write("Cards in file:\n")
        f4.write("{}, {}, {}\n".format(cfile.name, cfile.weapon, cfile.room))
        for op in opponents:
            f4.write("\n{}'s cards:\n".format(op.name))
            for card in op.cards:
                f4.write("{}\n".format(card))


def dh(turns, opponents, me, op_data):

    for turn in turns:
        items = translate_turn(turn, me, opponents, op_data)
        char = items[0]
        weapon = items[1]
        room = items[2]
        taker = items[3]
        giver = items[4]
        card_gotten = items[5]

        others = []

        if taker == me:
            if giver == None:
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
            else:
                giver.cards.add(card_gotten)
                others = opponents[:opponents.index(giver)]
                for op in opponents:
                    if op != giver:
                        op.doesnt_have.add(card_gotten)
                
        else: #if taker is someone else
            if giver == me:
                others = opponents[opponents.index(taker)+1:]
            elif giver == None:
                others = [x for x in opponents if x != taker]
                #things in file not included here
            else: #opponents
                first = opponents[0]
                while True:
                    if opponents[0] != taker:
                        opponents.append(opponents[0])
                        opponents.pop(0)
                    else:
                        others = opponents[opponents.index(taker)+1:opponents.index(giver)]
                        break
                while True:
                    if opponents[0] != first:
                        opponents.append(opponents[0])
                        opponents.pop(0)
                    else:
                        break

        if others != []: #at end
            for op in others:
                op.doesnt_have.update([char, weapon, room])


def op_options(turns, opponents, me, op_data):  
    for turn in turns:
        items = translate_turn(turn, me, opponents, op_data)
        char = items[0]
        weapon = items[1]
        room = items[2]
        taker = items[3]
        giver = items[4]
        if taker != me:
            if giver != None and giver != me:
                if not any(x in giver.cards for x in [char, weapon, room]):
                    options = [x for x in [char, weapon, room] if not x in giver.doesnt_have]
                    if len(options) == 1:
                        giver.cards.add(options[0])
                        for op in opponents:
                            if op != giver:
                                op.doesnt_have.add(options[0])


def cfile_contents(turns, opponents, me, op_data):
    
    names_found = set([[x for x in i.cards if x in names] for i in opponents+[me]][0])
    weapons_found = set([[x for x in i.cards if x in weapons] for i in opponents+[me]][0])
    rooms_found = set([[x for x in i.cards if x in rooms] for i in opponents+[me]][0])

    if len(names - names_found) == 1:
        n = list(names-names_found)[0]
        cfile.name = n
        for op in opponents:
            op.doesnt_have.add(n)

    if len(weapons - weapons_found) == 1:
        w = list(weapons-weapons_found)[0]
        cfile.weapon = w
        for op in opponents:
            op.doesnt_have.add(w)
    
    if len(rooms - rooms_found) == 1:
        r = list(weapons - weapons_found)[0]
        cfile.room = r
        for op in opponents:
            op.doesnt_have.add(r)

    for thing in everything:
        if not thing in me.cards:
            if all([thing in i.doesnt_have for i in opponents]):
                #doesnt need dh
                if thing in names:
                    cfile.name = thing
                if thing in weapons:
                    cfile.weapon = thing
                if thing in rooms:
                    cfile.room = thing


def testing():
    Mycards = {"lounge", "white", "billiardroom", "pistol"}
    Scards = {"rope", "candlestick", "pipe", "library", "scarlett"}
    Fcards = {"conservatory", "diningroom", "study", "ballroom", "peacock"}
    Dcards = {"hall", "green", "mustard", "wrench"}
    ppl = [Scards, Fcards, Dcards, Mycards]
    with open("ca2_turns.csv", "w") as f:
        for i in range(5):            
            for person in ["sophie", "fiona", "david", "self"]:
                ppl.append(ppl[0])
                ppl.pop(0)
                name = random.choice(list(names))
                weapon = random.choice(list(weapons))
                room = random.choice(list(rooms))
                f.write("{}, ".format(name))
                f.write("{}, ".format(weapon)) 
                f.write("{}, ".format(room))
                f.write("{}, ".format(person))
                for num, u in enumerate(ppl):
                    if num == 3:
                        f.write("none\n")
                        break
                    if any(x in u for x in [name, weapon, room]):
                        if u == Scards:
                            f.write("sophie")
                        elif u == Fcards:
                            f.write("fiona")
                        elif u == Dcards:
                            f.write("david")
                        else:
                            f.write("self")

                        if person == "self":
                            for k in u:
                                if k in [name, weapon, room]:
                                    f.write(", {}\n".format(k))
                                    break
                        else:
                            f.write("\n")
                        break
    
                    
answer()

