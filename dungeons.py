from random import randint
import os

def main():
    print('Let\'s play a little game!\n')
    x = 0
    ourGuy = Hero()
    play = True
    while (play):
        while ( x < 10 ):
            room = Place(ourGuy)
            # print( room.getName())
            room.__visitRoom__() ## remove underscores
            x += 1
            if ( ourGuy.listHealth() == 0):
                print ('OHH snap you died\n')
                x = 10
        again = input('play again? yes : no\n')
        if (again == 'no' or again == 'n'):
            play = False
    

class Place:
    def __init__(self, hero):
        nouns = ['desert', 'swamp', 'glade', 'sea', 'forrest', 'lair', 'field', 'pit']
        adjitives = ['arcane ', 'southern ', 'boistrous ', 'lovely ', 'last ' ]
        loot = ['a pointy ', 'a brilliant ', 'a magical ', 'Thor\'s ']
        loot2 = ['stick', 'poo', 'diamond', 'cheese grater', 'zombified head']
        self.name = 'The ' + adjitives[randint(0,5)] + nouns[randint(0,7)]
        self.monsters = []
        self.hero = hero
        self.treasure = loot[randint(0,3)] + loot2[randint(0,4)]
        x = randint(0,10)
        y = x
        if ( x > 3 ):
            y = 1 + x % 2
        x = 0 
        while (x < y):
            self.monsters[x] = Monster()
    
    def __visitRoom__(self):
        os.system('clear')
        print ('Entering ' + self.name + '\n')
        print ('There are ' + len(self.monsters) + 'monsters in the room')
        monMax = 0
        heroFirst = False
        for monster in self.monsters:
            roll = randint(1,6)
            if (roll > monMax):
                monMax = roll
        if (randint(1,6) > monMax):
            fight = input('They don\'t see you yet. Do you stay and fight? yes : no\n')
            if (fight == 'yes' or fight == 'y'):
                heroFirst = True
            else:
                os.system('clear')
                print('Coward\n')
                return
        else:
            print ('They see you first FIGHT!!!\n')
        self.fight(heroFirst)
    
    def fight(self, heroFirst):
        while (self.hero.listHealth() and self.monsters[0].listHealth()):
            if( heroFirst):
                if (self.hero.rollDice() >= self.monsters[0].rollDice()):
                    print('You punch him in the face\n')
                    self.monsters[0].getHurt()
            if (self.monsters[0].hero.rollDice() > self.hero.rollDice()):
                    print('He punches you in the face\n')
                    self.hero.getHurt()
                    heroFirst = True
            if ( self.monsters[0].listHealth() == 0):
                print('You killed the monster\n')
                self.monsters.remove(self.monsters[0])
                x = len(self.monsters)
                if ( x > 0):
                    os.system('clear')
                    input('There are still ' + x + 'monsters in the room\n')
        if (self.hero.listHealth()):
            self.hero.getLoot(self.treasure)
            input (' you killed all the monsters and you found ' + self.treasure + '\n')
            
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
            y = randint(1,6)
            if( y > max):
                max = y
        return max