import numpy as np
import random
from numpy.random import choice

class Character(object):
    char_dict = {'mafia0': 0, 'mafia1': 0, 'mafia2': 0, 'mafia3': 0, 'mafia4': 0, 'mafia5': 0, 'godfather': 0, 'cop': 1, 'doctor': 1, 'slut': 1, 'vigilante': 1, 'werewolf': 1, 'treestump': 1, 'joker': 2}
    team_dict = {0: 'mafia', 1: 'townspeople', 2: 'joker'}

    def __init__(self, role):
        self.role = role
        self.alive = True
        self.team = Character.team_dict[Character.char_dict[self.role]]
        self.suspects = {}
        self.know = []

    def __repr__(self):
        # team = Character.team_dict[Character.char_dict[self.role]]
        return '{}. (member of {})'.format(self.role, self.team)

    def set_suspects(self, squad):
        if self.team == 'mafia':
            for player in squad.members:
                if player.team != 'mafia':
                    self.suspects[player] = 0
            for player in self.suspects:
                self.suspects[player] = 1./len(self.suspects)
        elif self.team == 'townspeople':
            for player in squad.members:
                self.suspects[player] = 0
            self.suspects.pop(self)
            for player in self.suspects:
                self.suspects[player] = 1./(len(squad.members) - 1)

    def kill(self):
        self.alive = False

    def print_str(self):
        return str(self.role)

class Squad(object):
    def __init__(self, num_players):
        godfather = Character('godfather')
        mafia1 = Character('mafia1')
        joker = Character('joker')
        cop = Character('cop')
        doctor = Character('doctor')
        slut = Character('slut')
        self.members = [godfather, mafia1, joker, cop, doctor, slut]
        if num_players > 6:
            mafia2 = Character('mafia2')
            self.members.append(mafia2)
        if num_players > 7:
            vigilante = Character('vigilante')
            self.members.append(vigilante)
        if num_players > 8:
            mafia3 = Character('mafia3')
            self.members.append(mafia3)
        if num_players > 9:
            werewolf = Character('werewolf')
            self.members.append(werewolf)
        if num_players > 10:
            mafia4 = Character('mafia4')
            self.members.append(mafia4)
        if num_players > 11:
            treestump = Character('treestump')
            self.members.append(treestump)
        if num_players > 12:
            mafia5 = Character('mafia5')
            self.members.append(mafia5)
        for player in self.members:
            player.set_suspects(self)

    def __len__(self):
        return len(self.members)

    def __repr__(self):
        starter = 'the players in this game are: '
        for player in self.members:
            starter = starter + player.print_str() + ', '
        all_players = starter[:-2]
        return all_players

    def kill_member(self, player):
        self.members.pop(player)
        return self.members

def woke_maifa(squad):
    possible_killers = []
    for player in squad.members:
        if player.alive == True and player.team == 'mafia':
            possible_killers.append(player)
    suspects = possible_killers[0].suspects
    target = choice(suspects.keys(), 1, suspects.values())[0]
    killer = random.choice(possible_killers)
    return killer, target

def woke_cop(squad):
    # investigee = /

def night(squad):
    killer, target = woke_maifa(squad)
    woke_cop(squad)
    # woke_doctor(squad)
    # woke_slut(squad)

# def day(squad)
    # vigilante
    # werewolf
    # hang

if __name__ == '__main__':
    num_players = raw_input('enter number of players (6-13): ')
    squad = Squad(int(num_players))
    print squad
    night(squad)
