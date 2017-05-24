import numpy as np
import random

class Character(object):
    char_dict = {'mafia0': 0, 'mafia1': 0, 'mafia2': 0, 'mafia3': 0, 'mafia4': 0, 'mafia5': 0, 'godfather': 0, 'cop': 1, 'doctor': 1, 'slut': 1, 'vigilante': 1, 'werewolf': 1, 'treestump': 1, 'joker': 2}
    team_dict = {0: 'mafia', 1: 'townspeople', 2: 'joker'}

    def __init__(self, role):
        self.role = role
        self.alive = True
        self.team = Character.team_dict[Character.char_dict[self.role]]

    def __repr__(self):
        # team = Character.team_dict[Character.char_dict[self.role]]
        return '{}. (member of {})'.format(self.role, self.team)

    def kill(self):
        self.alive = False

    def print_str(self):
        return str(self.role)

class Squad(object):
    def __init__(self, num_players):
        self.members = []
        players_order = ['joker', 'cop', 'doctor', 'slut', 'vigilante', 'werewolf', 'treestump']
        i, j = 0, 0
        for player in range(num_players):
            if len(self.members) < (num_players-1)/2:
                self.members.append(Character('mafia{}'.format(j)))
                j += 1
            else:
                self.members.append(Character(players_order[i]))
                i += 1
        self.members.pop(0)
        self.members.insert(0, Character('godfather'))

    def __len__(self):
        return len(self.members)

    def __repr__(self):
        starter = 'the players in this game are: '
        for player in self.members:
            starter = starter + player.print_str() + ', '
        all_players = starter[:-2]
        return all_players

def woke_maifa(squad, night_num):
    possible_killees, possible_killers = [], []
    for player in squad.members:
        if player.alive == True and player.team != 'mafia':
            possible_killees.append(player)
        elif player.alive == True and player.team == 'mafia':
            possible_killers.append(player)
    if night_num == 1:
        killee = random.choice(possible_killees)
        killer = random.choice(possible_killers)
        killee.alive = False
    else:
        pass
    return squad


def night(squad, night_num):
    # squad
    # yo. you were thinking about player knowledge and how to add it into the game. probably through a know attribute of the character class. do you need different classes for different roles? of just general knowledge attrbutes/functions?
    
    squad = woke_maifa(squad, night_num)


if __name__ == '__main__':
    num_players = raw_input('enter number of players: ')
    squad = Squad(int(num_players))
    print squad
    night_num = 1
    night(squad, night_num)
