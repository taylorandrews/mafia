import numpy as np
import random
from numpy.random import choice

class Character(object):
    char_dict = {'mafia0': 0, 'mafia1': 0, 'mafia2': 0, 'mafia3': 0, 'mafia4': 0, 'mafia5': 0, 'godfather': 0, 'cop': 1, 'doctor': 1, 'slut': 1, 'vigilante': 1, 'werewolf': 1, 'treestump': 1, 'joker': 2}
    team_dict = {0: 'mafia', 1: 'townspeople', 2: 'joker'}

    def __init__(self, role):
        self.role = role
        self.alive = True
        self.investigated = False
        self.team = Character.team_dict[Character.char_dict[self.role]]
        self.suspects = {}
        self.another_boolean = False
        if self.role in ['mafia1', 'mafia2', 'mafia3', 'mafia4', 'mafia5', 'joker']:
            self.suspicious = True
        else:
            self.suspicious = False
        if self.role == 'cop':
            self.investigated = True

    def __repr__(self):
        # team = Character.team_dict[Character.char_dict[self.role]]
        # return '{}. (member of {})'.format(self.role, self.team)
        return self.role

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

def reweight_dict(d):
    factor = 1.0/sum(d.itervalues())
    for k in d:
        d[k] = d[k]*factor
    return d

def woke_maifa(squad, night_num):
    possible_killers = []
    for player in squad.members:
        if player.alive == True and player.team == 'mafia':
            possible_killers.append(player)
    suspects = possible_killers[0].suspects
    suspects = reweight_dict(suspects)
    target = choice(suspects.keys(), 1, p=suspects.values())[0]
    killer = random.choice(possible_killers)
    print 'night {}: the mafia is targeting the {} ({}%) with {} preforming the killing'.format(night_num, target.role, round(100*suspects[target], 1), killer.role)
    return killer, target

def woke_cop(squad, night_num):
    for player in squad.members:
        if player.role == 'cop':
            suspects = player.suspects
            suspects = reweight_dict(suspects)
            investigee = player
            while investigee.investigated == True:
                investigee = choice(suspects.keys(), 1, p=suspects.values())[0]
                chance = round(100*suspects[investigee], 1)
            investigee.investigated = True
            if investigee.suspicious == True:
                player.suspects[investigee] *= 5
                result = 'positive'
            else:
                player.suspects[investigee] /= 3
                result = 'negative'
    print 'night {}: the cop investigated the {} ({}%) and they came up {}'.format(night_num, investigee, chance, result)

def woke_doctor(squad, night_num):
    for player in squad.members:
        if player.role == 'doctor':
            possible_savees = player.suspects
            if night_num == 1:
                savee = player
                print 'night {}: the doctor saved themselves'.format(night_num)
            else:
                for possible_savee in possible_savees:
                    if possible_savee.suspicious == True:
                        possible_savees[possible_savee] /= 3
                    else:
                        possible_savees[possible_savee] *= 3
                        if possible_savee.role == 'cop':
                            possible_savees[possible_savee] *= 2
                possible_savees = reweight_dict(possible_savees)
                savee = choice(possible_savees.keys(), 1, p=possible_savees.values())[0]
                print 'night {}: the doctor saved the {} ({}%)'.format(night_num, savee, round(100*possible_savees[savee], 1))
    return savee

def woke_slut(squad, night_num):
    for player in squad.members:
        if player.role == 'slut':
            occupee = choice(player.suspects.keys(), 1, player.suspects.values())[0]
            print 'night {}: the slut occupied the {} ({}%)'.format(night_num, occupee, round(100*player.suspects[occupee], 1))
    return occupee

def woke_werewolf(squad, night_num):
    [target_1, target_2] = [0, 0]
    for player in squad.members:
        if player.role == 'werewolf':
            if min(0.5, (night_num - 1)/4.) > random.random():
                player.another_boolean = True
                [target_1, target_2] = choice(player.suspects.keys(), 2, player.suspects.values())[0:2]
    return [target_1, target_2]

def night(squad, night_num):
    killer, target_m = woke_maifa(squad, night_num)
    woke_cop(squad, night_num)
    savee = woke_doctor(squad, night_num)
    occupee = woke_slut(squad, night_num)
    target_w1, target_w2 = woke_werewolf(squad, night_num)

# def day(squad)
    # vigilante
    # werewolf
    # hang

if __name__ == '__main__':
    num_players = raw_input('enter number of players (6-13): ')
    squad = Squad(int(num_players))
    print squad
    for n in [1, 2]:
        night(squad, n)
