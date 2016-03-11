#!usr/bin/env python3
from random import *
import random
import os
import time
import sys

class Place:
    def __init__(self, hero):
        nouns = ['desert', 'swamp', 'glade', 'sea', 'forrest', 'lair', 'field', 'pit']
        adjitives = ['arcane ', 'southern ', 'boistrous ', 'lovely ', 'last ' ]
        loot = ['a pointy ', 'a brilliant ', 'a magical ', 'Thor\'s ']
        loot2 = ['stick', 'poo', 'diamond', 'cheese grater', 'zombified head']
        self.name = 'The ' + adjitives[randint(0,4)] + nouns[randint(0,6)]
        self.monsters = []
        self.hero = hero
        self.treasure = loot[randint(0,3)] + loot2[randint(0,4)]
        x = randint(0,100)
        y = 0 #28% chance of staying 0
        if ( not x % 2 ): # 50% chance 
            y = 1
        elif ( not x % 3): # 17% chance
            y = 2
        elif ( not x % 7): # 5% 
            y = 3
        self.hasMon = y
        x = 0 
        while (x < y):
            self.monsters.append(Monster())
            x += 1
    
    def __visitRoom__(self):
        os.system('clear')
        print ('Entering ' + self.name )
        time.sleep(.75)
        # if ( len(self.monsters) == 0):
        #     return
        monMax = 0
        heroFirst = False
        for monster in self.monsters:
            roll = randint(1,6)
            if (roll > monMax):
                monMax = roll
        if (randint(1,6) > monMax):
            # fight = input('They don\'t see you yet. Do you stay and fight? yes : no\n')
            # if (fight == 'yes' or fight == 'y'):
            heroFirst = True
            # else:
            #     os.system('clear')
            #     print('Coward')
            #     return
        # else:
        #     print ('They see you first FIGHT!!!')
        # print( str(len(self.monsters)))
        time.sleep(1)
        while ( len(self.monsters) == 0):
            result = self.printOptions()
            if (result == '5'):
                print('No monsters to fight')
            if (result == '2'):
                return
        self.fight(heroFirst)
    
    def fight(self, heroFirst):
        battleStarted = False
        if ( not len(self.monsters)):
            print('No monsters to fight')
        while (self.hero.listHealth() and len(self.monsters)):
            choice = self.printOptions()
            if( choice == '2' and battleStarted == False):
                return
            if (choice == '2'):
                print('You can\'t run away in the middle of a battle')
            battleStarted = True
            if( heroFirst):
                if (self.hero.rollDice() >= self.monsters[0].rollDice()):
                    print('You punch him in the face')
                    self.monsters[0].getHurt()
                else:
                    print('You missed')
            if ( self.monsters[0].listHealth() == 0):
                print('You killed the monster')
                self.monsters.remove(self.monsters[0])
                x = len(self.monsters)
                time.sleep(.5)
                if ( x > 0):
                    continue
                    # os.system('clear')
                else:
                    break
            if (self.monsters[0].rollDice() > self.hero.rollDice()):
                    print('He punches you in the face')
                    self.hero.getHurt()
            else:
                print('He missed')
            heroFirst = True
            time.sleep(.5)
        if (self.hero.listHealth()):
            self.hero.getLoot(self.treasure)
            input (' You killed all the monsters and you found ' + self.treasure + '\n')
        time.sleep(1)
        go = '1'
        while ( not go == '2'):
            go = self.printOptions()
            
    def printOptions(self):
        # input()
        os.system('clear')
        print ('In ' + self.name )
        num = str(len(self.monsters))
        print ('There are ' + num + ' monsters in the room')
        print('1) List items in loot bag')
        print('2) Move to next location')
        print('3) List health')
        print('4) Monster\'s health')
        print('5) Attack the monster')
        print('q for quit')
        value = input()
        if (value == '1'):
            os.system('clear')
            self.hero.listLoot()
            input()
        elif (value == '3'):
            os.system('clear')
            print ('Health left: ' + str(self.hero.listHealth()))
            time.sleep(1)
        elif (value == '4'):
            count = 0
            if (len(self.monsters) ):
                for monster in self.monsters:
                    print('Monster ' +str(count) + ' health: ' + str(monster.listHealth()))
                    count += 1
            else:
                print('There are no monsters in the room')
            input()
        elif ( value == 'quit' or value == 'q'):
            sys.exit()
        elif ( value == '2'):
            return value
        elif ( value == '5' ):
            if (self.hasMon and not len(self.monsters)):
                print('He\'s dead Jim')
                time.sleep(.75)
                return self.printOptions()
            return value
        else:
            print('Please input a valid option')
            time.sleep(.4)
        return self.printOptions()
                
    # def getName(self):
    #     return self.name



class Monster:
    def __init__(self):
        self.hitsLeft = randint(1,3)
        self.numDice = randint(1,3)
    
    def listHealth(self):
        return self.hitsLeft
    
    def getHurt(self):
        self.hitsLeft -= 1
    
    def rollDice(self):
        max = 0
        for x in range(0,self.numDice):
            y = randint(1,6)
            if( y > max):
                max = y
        return max
        

class Hero:
    def __init__(self):
        ## get name
        self.__hitsLeft = 10
        self.__potion = True
        self.__lootBag = []
    
    def listLoot(self):
        for loot in self.__lootBag:
            print(loot)
    
    def getLoot(self, loot):
        self.__lootBag.append(loot)
    
    def listHealth(self):
        return self.__hitsLeft
    
    def getHurt(self):
        self.__hitsLeft -= 1
    
    def rollDice(self):
        max = 0
        for x in range(0,3):
            x = randint(1,6)
            if( x > max):
                max = x
        return max
        
        

def main():
    random.seed(time.time())
    print('Let\'s play a little game!')
    x = 0
    
    play = True
    while (play):
        ourGuy = Hero()
        while ( x < 10 ):
            room = Place(ourGuy)
            # print( room.getName())
            room.__visitRoom__() ## remove underscores
            x += 1
            if ( ourGuy.listHealth() == 0):
                print ('OHH snap you died')
                x = 10
        os.system('clear')
        print('You have reached the end of the dungeon!! You found:')
        ourGuy.listLoot()
        again = input('play again? yes : no\n')
        if (again == 'no' or again == 'n'):
            play = False
        else:
            x = 0

if __name__ == "__main__":
    main()