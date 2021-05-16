#!/usr/bin/python3

import random
import time

# Replace RPG starter project with this code when new instructions are live
class Police:
    def __init__(self,inventory,hit_rate):
        self.hp = 100
        self.inventory = inventory
        self.hit_rate = hit_rate
    def is_dead(self):
        return self.hp<=0

    def attack(self,terrorist,weapon):
        if weapon == 'm16':
            if random.randint(1,100) <= 100*self.hit_rate:
                terrorist.hp -= 30
                print('You shot terrorist with m16. Terrorist HP -30')
            else:
                print('You missed the shot')
        elif weapon == 'flashbang':
            terrorist.status = 'frozen'
            self.inventory.remove('flashbang')
            print('Terrorist is frozen for a while')
        elif weapon == 'grenade':
            terrorist.hp -= 50
            self.hp -= 25
            self.inventory.remove('grenade')
            print('Both of you are hit by grenade. You HP -25; Terrorist HP -50')
        else:
            print('You don\'t use a weapon, good luck!')

    def negotiate(self,terrorist):
        if terrorist.hp<100:
            return False
        if random.randint(1,10)==2:
            terrorist.status = "persuaded"
            return True
        else: 
            return False

class Terrorist:

    def __init__(self,status,hit_rate):
        self.hp = 100
        self.status = 'insane'
        self.hit_rate = hit_rate

    def is_dead(self):
        return self.hp <= 0

    def attack(self,police):
        if self.status == 'persuaded':
            return
        elif self.status == 'frozen':
            time.sleep(2.5)
            print ('Terrorist is insane again.')
            self.status = 'insane'
            return
        else:
            if  random.randint(1,100) <= 100*self.hit_rate:
                police.hp -=40
                print('you are shot by terrorist! HP -40')
                return
            else:
                print('Luckily, terrorist missed the shot.')
                return




def showInstructions():
  #print a main menu and the commands
  print('''
  RPG Game
  ========
  Commands:
  go [direction]
  get [item]
''')

def showStatus(currentRoom,inventory):
  #print the player's current status
  print('---------------------------')
  print('You are in the ', currentRoom)
  #print the current inventory
  print('Inventory : ', str(inventory))
  #print an item if there is one
  if "item" in rooms[currentRoom]:
    print('You see a '+ display_item(rooms[currentRoom]['item']))
  print("---------------------------")

def display_item(items):
    str =""
    for item in items:
        str += item+' '
    return str

#combat mode
def combat(police,terrorist):
    #print('combatting')
    while True:

        show_combat_status(police,terrorist)    
        if police.negotiate(terrorist):
            print('Terrorist is persuaded. Hostages are rescued. Misson Success!')
            break
        else:
            print('negotiation failed')
            weapon = input(f'What do you want to use? {police.inventory}\n>')
            police.attack(terrorist, weapon)
            if terrorist.is_dead():
                print('Terrorist is elimnated. Mission Success!')
                break
            terrorist.attack(police)
            if police.is_dead():
                print('You are killed by terrorist. Mission failed')
                break

def show_combat_status(police, terrorist):
    print('\n+++++++++++++++++++++++++++++++')
    print(f'police:    HP->{police.hp}    Inventory-> {police.inventory}')
    print(f'terrorist: HP->{terrorist.hp}    Status-> {terrorist.status}')
    print('+++++++++++++++++++++++++++++++\n')



#a dictionary linking a room to other rooms
## A dictionary linking a room to other rooms
rooms = {
            'Outside':{
                'inside': 'Hall',
                'item' : ['m16','flashbang','grenade']
                },
            'Hall' : {
                'outside'  : 'Outside',
                'south' : 'Kitchen',
                'east'  : 'Dining Room',
                },

            'Kitchen' : {
                'north' : 'Hall',
                'item'  : ['terrorist','hostages'],
                },
            'Dining Room' : {
                'west' : 'Hall',
                'south': 'Garden',
                'north' : 'Pantry',
            },
            'Garden' : {
                'north' : 'Dining Room'
            },
            'Pantry' : {
                'south' : 'Dining Room',
                'item'  : ['health pack'],
            }
}

def main():

    #start the player in the Hall
    currentRoom = 'Outside'

    
    #an inventory, which is initially empty
    inventory = []

    #initialize police and terrorist
    police = Police(inventory,0.8)
    terrorist = Terrorist('insane',0.2)
    showInstructions()
    #loop forever
    while True:

        showStatus(currentRoom,inventory)


        #if you are in the kitchen, the enter combat mode
        if currentRoom == 'Kitchen':
            combat(police,terrorist)

        if police.is_dead():
            print('Game over')
            break
        if terrorist.is_dead():
            del rooms[currentRoom]['items']
        #get the player's next 'move'
        #.split() breaks it up into an list array
        #eg typing 'go east' would give the list:
        #['go','east']
        move = ''
        while move == '':
            move = input('>')

        # split allows an items to have a space on them
        # get golden key is returned ["get", "golden key"]          
        move = move.lower().split(" ", 1)

        #if they type 'go' first
        if move[0] == 'go':
            #check that they are allowed wherever they want to go
            if move[1] in rooms[currentRoom]:
            #set the current room to the new room
                currentRoom = rooms[currentRoom][move[1]]
            #there is no door (link) to the new room
            else:
                print('You can\'t go that way!')


        #if they type 'get' first
        if move[0] == 'get' :
            #if the room contains an item, and the item is the one they want to get
            if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
            # add the item to their inventory
                inventory += [move[1]]
                #display a helpful message
                print(move[1] + ' got!')
                #delete the item from the room
                rooms[currentRoom]['item'].remove(move[1])
                if len(rooms[currentRoom]['item'])==0:
                    del rooms[currentRoom]['item']
            #otherwise, if the item isn't there to get
            else:
                #tell them they can't get it
                print('Can\'t get ' + move[1] + '!')

if __name__ == '__main__':
   main()