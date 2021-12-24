import pickle
import random
import sys
import os
import keyboard
from random import randrange


class Character:
    def __init__(self):
        self.name = ""
        self.membersList = []
        self.guild = ""
        self.health = 200
        self.health_max = 200
        self.damage = 0
        self.guilds = []
        self.userNames = {}
        self.username = 0
        self.password = 0

    # PlayerDamage
    def do_damage(self, enemy):
        self.damage = min(max(randrange(0, self.health) -
                          randrange(0, enemy.health), 0), enemy.health)
        enemy.health = enemy.health - self.damage
        if self.damage == 0:
            print("Mr.%s evades %s-san's attack." % (enemy.name, self.name))
        else:
            print("%s-san hurts Mr.%s!" % (self.name, enemy.name))
            print(" damage by player: %d " % self.damage)
        return enemy.health <= 0

    # EnemyDamage
    def do_damage_2(enemy, self):
        print("Mr.%s's health: %d/%d" % (enemy.name, enemy.health, enemy.health_max))
        damage_2 = min(max(randrange(0, enemy.health) -randrange(0, self.health), 0), self.health)
        self.health = self.health - damage_2
        if damage_2 == 0:
            print("%s-san evades Mr.%s attack." % (self.name, enemy.name))
        else:
            print("%s-san hurts Mr.%s!" % (enemy.name, self.name))
            print("damage by enemy: %d" % damage_2)
        return self.health <= 0


class Enemy(Character):
    def __init__(self, player):
        Character.__init__(self)
        x = randrange(1, 6)
        if x == 1:
            self.name = 'Slime'
            self.health_max = randrange(10, 50)
            self.health = self.health_max
        elif x == 2:
            self.name = 'Witch'
            self.health_max = randrange(50, 200)
            self.health = self.health_max

        elif x == 3:
            self.name = 'BigWorm'
            self.health_max = randrange(200, 300)
            self.health = self.health_max

        elif x == 4:
            self.name = 'Demon General'
            self.health_max = randrange(50000, 90000)
            self.health = self.health_max

        elif x == 5:
            self.name = 'DemonSlayer'
            self.health_max = randrange(80000, 90000)
            self.health = self.health_max

        elif x == 6:
            self.name = 'DemonLord'
            self.health_max = randrange(70000, 100000)
            self.health = self.health_max


class Player(Character):
    def __init__(self):
        Character.__init__(self)
        # fish
        self.shrimp = 0
        self.eel = 0
        self.cod = 0
        self.carp = 0
        self.trout = 0
        self.magma = 0
        self.cookedeel = 0
        self.cookedshrimp = 0
        self.cookedcod = 0
        self.cookedcarp = 0
        self.cookedtrout = 0
        self.cookedmagma = 0
        # player
        self.state = 'normal'
        self.health = 50
        self.health_max = 50
        self.gold = 0
        self.credit = 1000
        self.equips = False
        # gatheringskills
        self.Craftskill = 1
        self.Mineskill = 1
        self.Cookskill = 1
        self.Fishskill = 1
        # weapon skills
        self.strength = 0
        self.defense = 0
        self.dexterity = 0
        self.CombatLevel = 0
        self.weaponskills = 0

    def quit(self):
        p.save()
        print("%s-san can't find the way back home, and dies of starvation.\nR.I.P." % self.name)
        self.health = 0

    def help(self):
        print(
            " quit \n guild \n help \n status \n rest \n explore \n flee \n attack \n magic \n fishing \n bank \n food \n mine \n craft \n cook \n skills \n restart \n reset \n login \n register \n join \n profile [****Confidential****]")

    def status(self):
        p.save()
        print("%s-san's health: %d/%d" %
              (self.name, self.health, self.health_max))

    def bank(self):
        p.save()
        print("%s-san's shrimp: %d" % (self.name, self.shrimp))
        print("%s-san's eel: %d" % (self.name, self.eel))
        print("%s-san's ores: %d" % (self.name, self.gold))
        print("%s-san's credits: %d" % (self.name, self.credit))
        print("%s-san's cooked shrimp: %d" % (self.name, self.cookedshrimp))
        print("%s-san's cooked eel: %d" % (self.name, self.cookedeel))
        print("%s-san's cooked cod: %d" % (self.name, self.cookedcod))
        print("%s-san's cooked carp: %d" % (self.name, self.cookedcarp))
        print("%s-san's cooked trout: %d" % (self.name, self.cookedtrout))
        print("%s-san's cooked magma: %d" % (self.name, self.cookedmagma))
        p.save()

    def tired(self):
        p.save()
        print("%s-san feels tired." % self.name)
        self.health = max(1, self.health - 10)
        p.save()

    def rest(self):
        p.save()
        if self.state != 'normal':
            print("%s-san can't rest now!" % self.name)
            self.enemy_attacks()
        else:
            if randrange(0, 2):
                self.enemy = Enemy(self)
                print("%s-san is rudely awakened by Mr.%s!" %
                      (self.name, self.enemy.name))
                self.state = 'fight'
                self.enemy_attacks()
            else:
                print("%s-san rests." % self.name)
                if self.health < self.health_max:
                    self.health = self.health_max
                else:
                    print("%s-san slept too much." % self.name)
                    self.health = self.health - 10
        p.save()

    def explore(self):
        p.save()
        if self.state != 'normal':
            print("%s-san is too busy right now!" % self.name)
            self.enemy_attacks()
        else:
            if randrange(0, 2):
                self.enemy = Enemy(self)
                print("%s-san encounters a %s!" % (self.name, self.enemy.name))
                self.state = 'fight'
            else:
                print("%s-san explores a twisty passage." % self.name)
        p.save()

    def flee(self):
        p.save()
        if self.state != 'fight':
            print("%s-san runs in circles for a while." % self.name)
            self.tired()
        else:
            if randrange(1, self.health + 5) > randrange(1, self.enemy.health):
                self.enemy = Enemy(self)
                print("%s-san flees from Mr.%s." %
                      (self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
            else:
                self.enemy = Enemy(self)
                print("%s-san couldn't escape from Mr.%s!" %
                      (self.name, self.enemy.name))
                self.enemy_attacks()
        p.save()

    def attack(self):
        p.save()
        if self.state != 'fight':
            print("%s-san swats the air, without notable results." % self.name)
            self.tired()
        else:
            if self.do_damage(self.enemy):
                print("%s-san executes Mr.%s!" % (self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
                if randrange(0, self.health) < self.health_max:
                    self.health += 50
                    self.strength += 1
                    print(" damage before lvling: %d" % self.damage)
                    self.damage += random.randrange(20, 30)
                    self.health_max += 50
                    self.credit += randrange(25, 50)
                    print("%s-san feels stronger!" % self.name)
            else:
                self.enemy_attacks()
        p.save()

    def magic(self):
        p.save()
        if self.state != 'fight':
            print("%s-san use magic, without notable results." % self.name)
            self.tired()
        else:
            if self.do_damage(self.enemy):
                print("%s-san executes Mr.%s!" % (self.name, self.enemy.name))
                self.enemy = None
                self.state = 'normal'
                if randrange(0, self.health) < self.health_max:
                    self.health += 60
                    self.defense += 1
                    self.health_max += 60
                    self.credit += randrange(20, 45)
                    print("%s-san feels stronger!" % self.name)
            else:
                self.enemy_attacks()
        p.save()

    def fishing(self):
        p.save()
        '''if random.randrange(0, 2):
            self.enemy = Enemy(self)
            print ("%s-san is disturbed by a %s!" % (self.name, self.enemy.name))
            self.state = 'fight'
            self.enemy_attacks()
        else:'''
        if random.randrange(0, 2):
            print("%s-san catches a shrimp." % self.name)
            self.shrimp += 1
            self.Fishskill += 0.07
        else:
            print("%s-san catches an eel." % self.name)
            self.eel += 1
            self.Fishskill += 0.1
        p.save()

    def cooking(self):
        p.save()
        if self.state == 'fight':
            print("%s-san's food is eaten by a %s." %
                  (self.name, self.enemy.name))
        else:
            if self.shrimp > 0 or self.eel > 0:
                if self.shrimp > 0 and self.eel == 0:
                    print("%s-san cooked shrimp." % self.name)
                    self.cookedshrimp = self.shrimp
                    self.shrimp = 0
                    self.Cookskill += 1
                elif self.shrimp == 0 and self.eel > 0:
                    print("%s-san cooked eel." % self.name)
                    self.cookedeel = self.eel
                    self.eel = 0
                    self.Cookskill += 1.2
                elif self.shrimp > 0 and self.eel > 0:
                    print("%s-san cooked eel and shrimp." % self.name)
                    self.cookedshrimp = self.shrimp
                    self.cookedeel = self.eel
                    self.shrimp = 0
                    self.eel = 0
                    self.Cookskill += 3
            else:
                print("Not enough raw fish")
                self.tired()
            p.save()

    def food(self):
        p.save()
        if self.cookedshrimp > 0 or self.cookedeel > 0:
            if self.health < self.health_max:
                if self.cookedshrimp > 0 and self.cookedeel == 0 and self.cookedmagma == 0:
                    print("%-san eats cooked shrimp" % self.name)
                    self.health += random.randrange(30, 60)
                    self.cookedshrimp -= 1
                    if self.health >= self.health_max:
                        self.health = self.health_max
                elif self.cookedeel > 0 and self.cookedshrimp == 0 and cooked.magma == 0:
                    print("%-san eats cooked eel" % self.name)
                    self.health += random.randrange(60, 90)
                    self.cookedeel -= 1
                    if self.health >= self.health_max:
                        self.health = self.health_max
                elif self.cookedeel > 0 and self.cookedshrimp > 0 and self.cookedmagma == 0:
                    print("%-san eats cooked eel" % self.name)
                    self.health += random.randrange(60, 90)
                    self.cookedeel -= 1
                    if self.health >= self.health_max:
                        self.health = self.health_max
                elif self.cookedmagma > 0 and self.cookedeel > 0 and self.cookedshrimp == 0:
                    print("%-san eats cooked magmafish" % self.name)
                    self.health += random.randrange(5000, 15000)
                    self.cookedmagma -= 500
                    if self.health >= self.health_max:
                        self.health = self.health_max
                elif self.cookedmagma > 0 and self.cookedshrimp > 0 and self.cookedeel == 0:
                    print("%-san eats cooked magmafish" % self.name)
                    self.health += random.randrange(5000, 15000)
                    self.cookedmagma -= 500
                    if self.health >= self.health_max:
                        self.health = self.health_max
                elif self.cookedmagma > 0 and self.cookedshrimp == 0 and self.cookedeel == 0:
                    print("%-san eats cooked magmafish" % self.name)
                    self.health += random.randrange(5000, 15000)
                    self.cookedmagma -= 500
                    if self.health >= self.health_max:
                        self.health = self.health_max
                elif self.cookedmagma > 0 and self.cookedshrimp > 0 and self.cookedeel > 0:
                    print("%-san eats cooked magmafish" % self.name)
                    self.health += random.randrange(5000, 15000)
                    self.cookedmagma -= 500
                    if self.health >= self.health_max:
                        self.health = self.health_max
            elif self.health >= self.health_max:
                self.health = self.health_max
                print("%s-san over ate the food" % self.name)
        else:
            print("%-san doesn't have any cookedfish")
        p.save()

    def mining(self):
        if self.state == 'fight':
            print("%-san is interrupted by a %s" %
                  (self.name, self.enemy.name))
            self.tired()
        else:
            if random.randrange(0, 2):
                print("%-san found a ore" % self.name)
                self.gold += 1
                self.Mineskill += 0.03
            else:
                print("%-san found few ores" % self.name)
                self.gold += 3
                self.Mineskill += 0.1
        p.save()

    def crafting(self):
        if self.state == 'fight':
            print("%-san is interrupted by a %s" %
                  (self.name, self.enemy.name))
            self.tired()
        else:
            if self.health > 50:
                if self.gold > 0:
                    if self.gold >= 10 and self.gold < 20 and self.credit >= 110 and self.equips == False:
                        print(
                            "Bronze equipment set is available\nCrafting is completed")
                        self.health_max += 60
                        self.health = self.health_max
                        self.gold -= 10
                        self.credit -= 110
                        self.Craftskill += 1
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 1
                        self.equips = True
                    elif self.gold >= 20 and self.gold < 30 and self.credit >= 220 and self.equips == False:
                        print(
                            "Iron equipment set is available\nCrafting is completed")
                        self.health_max += 100
                        self.health = self.health_max
                        self.gold -= 20
                        self.credit -= 220
                        self.Craftskill += 1.9
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 2
                        self.equips = True
                    elif self.gold >= 30 and self.gold < 40 and self.credit >= 440 and self.equips == False:
                        print(
                            "Steel equipment set is available\nCrafting is completed")
                        self.health_max += 150
                        self.health = self.health_max
                        self.gold -= 30
                        self.credit -= 440
                        self.Craftskill += 3.5
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 3
                        self.equips = True
                    elif self.gold >= 40 and self.gold < 100 and self.credit >= 600 and self.equips == False:
                        print(
                            "Black equipment set is available\nCrafting is completed")
                        self.health_max += 250
                        self.health = self.health_max
                        self.gold -= 50
                        self.credit -= 600
                        self.Craftskill += 6
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 4
                        self.equips = True
                    elif self.gold >= 100 and self.gold < 500 and self.credit >= 1000 and self.equips == False:
                        print(
                            "Mithril equipment set is available\nCrafting is completed")
                        self.health_max += 500
                        self.health = self.health_max
                        self.gold -= 100
                        self.credit -= 1000
                        self.Craftskill += 10
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 5
                        self.equips = True
                    elif self.gold >= 500 and self.gold < 1000 and self.credit >= 5000 and self.equips == False:
                        print(
                            "Adamantium equipment set is available\nCrafting is completed")
                        self.health_max += 1000
                        self.health = self.health_max
                        self.gold -= 500
                        self.credit -= 5000
                        self.Craftskill += 30
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 10
                        self.equips = True
                    elif self.gold >= 1000 and self.gold < 10000 and self.credit >= 10000 and self.equips == False:
                        print(
                            "Dianium equipment set is available\nCrafting is completed")
                        self.health_max += 5000
                        self.health = self.health_max
                        self.gold -= 1000
                        self.credit -= 10000
                        self.Craftskill += 100
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 50
                        self.equips = True
                    elif self.gold >= 10000 and self.gold < 50000 and self.credit >= 100000 and self.equips == False:
                        print(
                            "Demonic equipment set is available\nCrafting is completed")
                        self.health_max += 10000
                        self.health = self.health_max
                        self.gold -= 10000
                        self.credit -= 100000
                        self.Craftskill += 500
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 250
                        self.equips = True
                    elif self.gold >= 50000 and self.credit >= 500000 and self.equips == False:
                        print(
                            "Cursed equipment set is available\nCrafting is completed")
                        self.health_max += 50000
                        self.health = self.health_max
                        self.gold -= 50000
                        self.credit -= 500000
                        self.Craftskill += 1000
                        self.weaponskills = self.defense + self.dexterity + self.strength
                        self.dexterity += 500
                        self.equips = True
                    elif self.equips == True:
                        print("A set of equipments is already in use!!!")
                else:
                    if self.gold < 10:
                        print("Not enough ores")
                    elif self.credit < 110:
                        print("Not enough money")
                    elif self.credit < 110 and self.gold < 10:
                        print("Not enough resources")
        p.save()

    def skills(self):
        self.weaponskills = self.defense + self.dexterity + self.strength
        if self.weaponskills >= 3:
            if self.weaponskills % 3 == 0 or self.weaponskills % 3 == 1 or self.weaponskills % 3 == 2:
                self.CombatLevel = self.weaponskills // 3
        else:
            self.CombatLevel = 0
        if self.Craftskill >= 1000:
            self.Craftskill = 1000
        print(
            " Crafting Skill: %d \n Mining Skill: %d \n Cooking Skill: %d \n Fishing Skill: %d \n Strength: %d \n Combat Level: %d \n Weapon Skills: %d \n Dexterity: %d \n Defense: %d " % (
                self.Craftskill, self.Mineskill, self.Cookskill, self.Fishskill, self.strength, self.CombatLevel, self.weaponskills, self.dexterity, self.defense))
        p.save()

    def enemy_attacks(self):
        if self.enemy.do_damage_2(self):
            print(
                "%s-san was slaughtered by Mr.%s!!!\nR.I.P." % (self.name, self.enemy.name))

    def guild(self):
        print("%s-san's guild: %s" % (self.name, self.guild))
        for i in self.membersList:
            print(i)
        p.save()

    def save(self):  # Save
        with open('CrossReverieClassic.pickle', 'wb') as f:
            pickle.dump([self.shrimp, self.eel, self.cookedeel, self.cookedshrimp, self.health, self.health_max, self.gold, self.credit, self.Craftskill, self.Mineskill, self.Cookskill, self.Fishskill, self.name, self.guild, self.guilds, self.userNames], f)
        f.close()
    def load(self):  # Load
        with open('CrossReverieClassic.pickle', 'rb') as f:
            self.shrimp, self.eel, self.cookedeel, self.cookedshrimp, self.health, self.health_max, self.gold, self.credit, self.Craftskill, self.Mineskill, self.Cookskill, self.Fishskill, self.name, self.guild, self.guilds, self.userNames = pickle.load(f)
        f.close()
    def cheat(self):
        self.strength += 200
        self.defense += 0
        self.dexterity += 0
        self.Craftskill += 999
        self.Mineskill += 999
        self.Cookskill += 999
        self.Fishskill += 999
        self.health += 2000
        self.health_max += 2000
        self.gold += 999999
        self.credit += 9999999
        self.shrimp += 99
        self.eel += 99
        self.cookedeel += 99
        self.cookedshrimp += 99
        self.cookedmagma += 99

    def joinGuild(self):
        self.guilds.append(self.guild)
        print(self.guilds)
        self.guild = random.choice(self.guilds)
        p.save()

    def logIn(self):
        p.load()
        self.username = input("Enter your username\n")
        while self.username not in self.userNames:
            print("Name not found, try again or register")
            self.username = input("Enter your username\n")
        if self.username in self.userNames:
            self.password = input("Enter Your password\n")
            while self.password != self.userNames[self.username]:
                print("Password not found, try again or type forget")
                self.password = input("Enter Your password\n")
            if self.password == self.userNames[self.username]:
                print(f"Welcome back {self.username}")
                print("type help to get a list of actions)\n")
                print("%s-san enters a dark cave, searching for adventure." % self.name)

    def signUp(self):
        self.username = input("Create your username\n")
        while self.username in self.userNames:
            print("Username not available")
            self.username = input("Create your username\n")
        if self.username not in self.userNames:
            self.password = input("Create your password\n")
            self.userNames[self.username] = self.password
        else:
            print("Catched bug")
        p.name = input("What is your character's name? ")
        p.guild = input("What is your guild's name? ")
        self.guilds.append(p.guild)
        print("type help to get a list of actions)\n")
        print("%s-san enters a dark cave, searching for adventure." % self.name)
        p.save()

    def logOut(self):
        self.shrimp = 0
        self.eel = 0
        self.cookedeel = 0
        self.cookedshrimp = 0
        self.state = 0
        self.gold = 0
        self.credit = 0
        self.Craftskill = 0
        self.Mineskill = 0
        self.Cookskill = 0
        self.Fishskill = 0
        self.name = 0
        self.signUp()

    def profile(self):
        print(f"Your Username: {self.username}")
        print(f"Your Password: {self.password}")

    def reset(self):
        confirmation = input("Are your sure to remove your account?? \n Yes or no?? \n")
        if confirmation == "yes" or confirmation == "Yes" or confirmation == "y" or confirmation == "Y":
            self.userNames.pop(self.username)
            self.signUp()
        elif confirmation == "no" or confirmation == "No" or confirmation == "n" or confirmation == "N":
            print("Ok carry on. ^^ \n ")

    def server(self):
        print(self.userNames)


p = Player()
print("Welcome to this world")
print("You wanna register or login??")
Commands = {
    'quit': Player.quit,
    'guild': Player.guild,
    'help': Player.help,
    'status': Player.status,
    'rest': Player.rest,
    'explore': Player.explore,
    'flee': Player.flee,
    'attack': Player.attack,
    'magic': Player.magic,
    'fishing': Player.fishing,
    'bank': Player.bank,
    'food': Player.food,
    'mine': Player.mining,
    'craft': Player.crafting,
    'cook': Player.cooking,
    'skills': Player.skills,
    'save': Player.save,
    'load': Player.load,
    'cheat': Player.cheat,
    'login': Player.logIn,
    'register': Player.signUp,
    'profile': Player.profile,
    'join': Player.joinGuild,
    'reset': Player.reset,
    'server': Player.server,
    'logout': Player.logOut,
}

while (p.health > 0):
    line = input("> ")
    args = line.split()
    if len(args) > 0:
        commandFound = False
        for c in Commands.keys():
            if args[0] == c[:len(args[0])]:
                Commands[c](p)
                commandFound = True
                break
        if not commandFound:
            print("%s-san, doesn't understand the suggestion." % p.name)