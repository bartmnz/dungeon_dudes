#!usr/bin/env python3
from random import *
import random
import os
import time
import sys



class Place:
    def __init__(self, hero, *args):
        """Create an instance of Place with a random name, and number of monsters
            and random treasure
        
        Args:
            hero: a hero class object to store
            *args: if present will set the place to 'hell'
        Returns:
            No return value
        
        """
        nouns = ['desert', 'swamp', 'glade', 'sea', 'forrest', 'lair', 'field', 'pit']
        adjitives = ['arcane ', 'southern ', 'boistrous ', 'lovely ', 'last ' ]
        loot = ['a pointy ', 'a brilliant ', 'a magical ', 'Thor\'s ']
        loot2 = ['stick', 'poo', 'diamond', 'cheese grater', 'zombified head']
        self.name = 'The ' + random.choice(adjitives) + random.choice(nouns)
        self.monsters = []
        self.hero = hero
        self.treasure = random.choice(loot) + random.choice(loot2)
        x = randint(0,100)
        y = 2 #28% chance of staying 2
        if ( not x % 2 ): # 50% chance 
            y = 1
        elif ( not x % 3): # 17% chance
            y = 0
        elif ( not x % 7): # 5% 
            y = 3
        if (len(args)):
            self.name = "Special place in Hell for cowards"
            y = 4
        self.hasMon = y
        x = 0 
        while (x < y):
            self.monsters.append(Monster())
            x += 1
        if (len(args)):
            self.monsters[3].makeBoss()
            
    def visitRoom(self):
        """ Prompts the user for direction about what they would like to do
            
            Args: 
                None
            Return:
                None
        
        """
        os.system('clear')
        print ('Entering ' + self.name )
        time.sleep(.75)
        monMax = 0
        heroFirst = False
        for roll in self.monsters:
            roll = randint(1,6)
            if (roll > monMax):
                monMax = roll
        if (randint(1,6) > monMax):
            heroFirst = True
        time.sleep(1)
        while ( len(self.monsters) == 0):
            result = self.printOptions()
            if (result == '5'):
                print('No monsters to fight')
            if (result == '2'):
                return
        self.__fight(heroFirst)
    
    def __fight(self, heroFirst):
        """ Initiates a turn based battle between the hero and the monsters in a room
            Once the battle is started it is to the death.
            
            Args: 
                heroFirst: boolean describing if the hero will attack first.
            Returns:
                None
        """
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
            self.hero.notCoward()
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
                time.sleep(.9)
                if ( x > 0):
                    continue
                else:
                    break
            if (self.monsters[0].rollDice() > self.hero.rollDice()):
                    print('He punches you in the face')
                    self.hero.getHurt()
            else:
                print('He missed')
            heroFirst = True
            time.sleep(.9)
        if (self.hero.listHealth()):
            self.hero.getLoot(self.treasure)
            input (' You killed all the monsters and you found ' + self.treasure + '\n')
        if ( self.hero.listHealth() == 0 ):
            return
        go = '1'
        while ( not go == '2'):
            go = self.printOptions()
            
    def printOptions(self):
        """
        Outputs the options for the place and captures the user's choice
        
        Args:
            None
        Return:
            either 2 or 5 depending on the user's choice
        
        """
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
                # Thanks for the idea Follensbee
                print('He\'s dead Jim')
                time.sleep(.75)
                return self.printOptions()
            return value
        else:
            print('Please input a valid option')
            time.sleep(.4)
        return self.printOptions()


class Monster:
    def __init__(self):
        self.hitsLeft = randint(1,3)
        self.numDice = randint(1,3)
    
    def listHealth(self):
        return self.hitsLeft
    
    def getHurt(self):
        self.hitsLeft -= 1
    
    def makeBoss(self):
        self.numDice = 4
        self.hitsLeft = 10
        
    def rollDice(self):
        max = 0
        for x in range(0,self.numDice):
            x = randint(1,6)
            if( x > max):
                max = x
        return max
        

class Hero:
    def __init__(self):
        self.__hitsLeft = 10
        self.__potion = True
        self.__lootBag = []
        self.__hasFought = False
    
    def listLoot(self):
        for loot in self.__lootBag:
            print(loot)
    
    def getLoot(self, loot):
        self.__lootBag.append(loot)
    
    def listHealth(self):
        return self.__hitsLeft
    
    def getHurt(self):
        self.__hitsLeft -= 1
        
    def notCoward(self):
        self.__hasFought = True
    
    def trialByCombat(self):
        return not self.__hasFought
    
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
        survived = True
        while ( x < 10 ):
            room = Place(ourGuy)
            room.visitRoom() ## remove underscores
            x += 1
            if ( ourGuy.listHealth() == 0):
                print ('OHH snap you died')
                survived = False
                time.sleep(1)
                x = 10
        os.system('clear')
        if ( survived and ourGuy.trialByCombat()):
            room = Place(ourGuy, 'hell')
            while( ourGuy.trialByCombat()):
                room.visitRoom()
            if ( ourGuy.listHealth() == 0):
                print ('Suprise you died!!')
                print ('Next time fight!!!')
                survived = False
                time.sleep(1)
            else:
                print ('Holy crap how did you survive???')
        if ( survived):
            print('You have reached the end of the dungeon!! You found:')
            ourGuy.listLoot()
        again = input('play again? yes : no\n')
        if (again == 'no' or again == 'n'):
            play = False
        else:
            x = 0

if __name__ == "__main__":
    main()