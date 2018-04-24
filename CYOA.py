import time
import random

# colored text
purple = '\033[95m'
cyan = '\033[96m'
darkcyan = '\033[36m'
blue = '\033[94m'
green = '\033[92m'
yellow = '\033[93m'
red = '\033[91m'
bold = '\033[1m'
underline = '\033[4m'
end = '\033[0m'

redbold = red + bold

# Extra stuff
counter = 0  # for oof (??)
inventory = []
invCapacity = 8
health = 100

ping_phrases = ['pls',
                'pls stop',
                'pls stop doing this',
                'pls just continue the game',
                'just play the game',
                'y u do dis',
                'stop',
                'stop doing this']
looping_oof = ["oof"]

# armor
head = None
chest = None
legs = None
feet = None

# classes


class Room(object):
    def __init__(self, name, description, north, south, east, west, up, down, character, items):
        self.NAME = name
        self.DESCRIPTION = description
        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.up = up
        self.down = down
        self.character = character
        self.items = items

    def print_descriptions(self):
        print(blue + self.NAME + end)
        print(self.DESCRIPTION)
        if not self.items:
            pass
        else:
            print("It seems you can take:")
            for item in self.items:
                print("\t" + bold + item.name.lower() + end)


    def move(self, directions):
        global current_node
        current_node = globals()[getattr(self, directions)]

    def jump(self):
        if current_node == BEDROOM or current_node == LIVING_ROOM:
            time.sleep(.5)
            print(bold + "oh woop there's a ceiling fan there" + end)
            time.sleep(1)
            print(RED + "You hit the ceiling fan while it was on. Your head gets chopped off" + end)
            quit(0)
        else:
            print(redbold + "ow" + end)
            time.sleep(.5)

    def oof(self):
        print(bold + "".join(looping_oof) + end)
        time.sleep(.5)
        looping_oof.append("oof")

    def ping(self):
        if counter <= 2:
            print(bold + UNDERLINE + "pong" + end)
        elif counter == 3:
            print(GREEN + bold + "don't waste your time doing this" + end)
        elif counter == 4:
            print(YELLOW + bold + "pls you have more important things other than this" + end)
        elif counter == 5:
            print(cyan + bold + "pls" + end)
        elif counter <= 9:
            print(bold + PURPLE + random.choice(ping_phrases) + end)
        elif counter == 10:
            print(redbold + "You typed in ping too much that the game got tired of you and decided to quit")
            quit(0)

    def flush(self):
        if current_node == BATHROOM:
            print(bold + "..." + end)
            time.sleep(1)
            print(bold + RED + "a man rises from the toilet and kills you" + end)
            quit(0)
        else:
            print(redbold + "There's no toilet here u stupid" + end)


class Character(object):
    def __init__(self, name, description, dialogue, inv, hp):
        self.name = name
        self.description = description
        self.dialogue = dialogue
        self.inventory = inv
        self.health = hp
        self.isAlive = True
        self.hasTalked = False
        self.counter = 0  # counter for number of encounters of character

    def print_descriptions(self):
        print(GREEN + bold + self.name + end)
        print(self.description)

    def talk(self):
        if self.dialogue is None:
            print(blue + bold + "This person doesn't seem to say anything." + end)
        else:
            print("He says...")
            time.sleep(1)
            print(self.dialogue)
            time.sleep(.5)
            self.hasTalked = True

    def kill(self):
        print(bold + RED + "oh woops you killed " + self.name.lower() + end)
        self.isAlive = False
        # if None not in self.inventory:


class Item(object):
    def __init__(self, name, desc):
        self.name = name
        self.description = desc

    def print_descriptions(self):
        print(PURPLE + bold + self.name + end)
        print(self.description)

    def take(self):
        if len(inventory) == invCapacity:
            print(redbold + "Your inventory is full." + end)
        else:
            inventory.append(self)
            current_node.items.pop(current_node.items.index(self))
            print(cyan + bold + "You take the " + self.name.lower() + "." + end)

    def drop(self):
        inventory.pop(inventory.index(self))
        current_node.items.append(self)
        print(cyan + bold + "You drop the " + self.name.lower() + '.' + end)


class Weapon(Item):
    def __init__(self, name, desc, damage):
        super(Weapon, self).__init__(name, desc)
        self.damage = damage

    def hit(self): current_node.character.health -= self.damage

    def check_stats(self): print(bold + blue + "Damage: " + end + str(self.damage))


class Sword(Weapon):
    def __init__(self, name, desc, damage):
        super(Sword, self).__init__(name, desc, damage)

    def hit(self):
        random_number = random.randint(0, 10)
        if random_number % 2 == 0:  # crit
            current_node.character.health -= damage * 2
        else:
            current_Node.character.health -= damage


class BackwardsGun(Weapon):
    def __init__(self, name, desc):
        super(BackwardsGun, self).__init__(name, desc, 100)

    def shoot(self):
        print(redbold + "you shot yourself and died" + end)
        quit(0)


class Hammer(Weapon):
    def __init__(self, name):
        super(Hammer, self).__init__(name, desc, 1)

    def break_door(self):
        print(bold + "..." + end)
        time.sleep(1)
        print(bold + blue + "Why is this hammer made of rubber?" + end)


class Consumable(Item):
    def __init__(self, name, desc):
        super(Consumable, self).__init__(name, desc)

    def use(self):
        inventory.pop(inventory.index(self))


class Food(Consumable):
    def __init__(self, name, desc):
        super(Food, self).__init__(name, desc)

    def eat(self):
        inventory.pop(inventory.index(self))
        print(PURPLE + bold + "yummy" + end)


class Drink(Consumable):
    def __init__(self, name, desc):
        super(Drink, self).__init__(name, desc)

    def drink(self):
        inventory.pop(inventory.index(self))
        print(blue + bold + "You drink the %s and its bottle disappears..." + end % self.name.lower())


class Container(Item):
    def __init__(self, name, desc, capacity):
        super(Container, self).__init__(name, desc)
        self.capacity = capacity
        self.inventory = []
        self.isOpen = False
        self.isEmpty = False

    def put_item_in(self, item_name):
        if self.inventory.len() == capacity:
            print(redbold + "Your inventory is full." + end)
        else:
            self.inventory.append(item_name)
            print(cyan + bold + "You put the %s in the %s." + end % (item_name.lower(), self.name.lower()))

    def take_out(self, item_name):
        self.inventory.pop(self.inventory.index(item_name))
        inventory.append(item_name)
        print(cyan + bold + "You take the %s out of the %s." + end % (item_name.lower(), self.name.lower()))

    def open(self):
        if not self.isOpen:
            self.isOpen = True
            print(blue + bold + "You open the " + self.name.lower() + "." + end)
        else:
            print(redbold + "That is already open." + end)

    def close(self):
        if self.isOpen:
            self.isOpen = False
            print(blue + bold + "You close the " + self.name.lower() + "." + end)
        else:
            print(redbold + "That is already closed." + end)

    # def drop(self):
    #     for items in self.inventory:
    #         current_node.items = items
    #         self.inventory.pop(self.inventory.index(items))


class Box(Container):
    def __init__(self, name, desc):
        super(Box, self).__init__(name, desc, 4)

    def put_item_in(self, item_name):
        if self.inventory.len() == capacity:
            print(redbold + "Your inventory is full." + end)
        else:
            self.inventory.append(item_name)
            print(cyan + bold + "You put the %s in the box" + end % item_name.lower())

    def wear(self):
        global head
        head = self


class Ball(Item):
    def __init__(self, name, desc):
        super(Ball, self).__init__(name, desc)

    def throw(self):
        inventory.pop(inventory.index(ball))
        print("You throw the ball and in a blink of "
                  "an eye, one of the dogs zoom in a blink "
                  "of an eye and catch the ball.")
        time.sleep(4)
        print(YELLOW + bold + "The dog then hovers and starts floating to orbit.")
        time.sleep(3)
        print(YELLOW + bold + "The dog comes back with a bucket with even more balls.")
        time.sleep(1)

class Wearable(Item):
    def __init__(self, name, desc, body):
        super(Wearable, self).__init__(name, desc)
        self.body = body

    def equip(self):
        if self.body is not None:
            print(redbold + "You're already wearing something." + end)
        else:
            self.body = self
            inventory.pop(inventory.index(self))
            print(blue + bold + "You wear the " + self.name + end)

    def un_equip(self):
        self.body = None
        print(blue + bold + "You take off the " + self.name + end)
        inventory.append(self)


class Mask(Wearable):
    def __init__(self, name, desc):
        super(Mask, self).__init__(name, desc, head)

    def equip(self):
        global head
        if head is not None:
            print(redbold + "You're already wearing something." + end)
        else:
            head = self
            inventory.pop(inventory.index(self))
            print(blue + bold + "You wear the " + self.name + end)

    def un_equip(self):
        global head
        head = None
        inventory.append(self)


class Shirt(Wearable):
    def __init__(self, name, desc):
        super(Shirt, self).__init__(name, desc, chest)

    def equip(self):
        global chest
        if chest is None:
            print(redbold + "You're already wearing something." + end)
        else:
            chest = self
            inventory.pop(inventory.index(self))
            print(blue + bold + "You wear the %s." + end + self.name.lower())

    def un_equip(self):
        global chest
        print(blue + bold + "You take off the %s." + end + self.name.lower())
        chest = None
        inventory.append(self)


class Book(Item):
    def __init__(self, name, desc, read_text):
        super(Book, self).__init__(name, desc)
        self.readText = read_text

    def read(self):
        print(self.read_text)


# Characters and Items

Cookie = Character("Cookiezi", "This person seems to be sitting behind a desk with a computer mashing his keyboard\n"
                               "slightly, but you could definitely hear it. On his monitor, he seems to be clicking "
                               "circles...", None, None, None)
jeff = Character("jeff", "he's sitting on a chair playing a game on the left side of the room", "stop", ['pen'], 50)

cookie = Food("Cookie", "A chocolate chip cookie. Seems delicious.")
bed = Item("Bed", "Your average-looking bed.")
ball = Ball("Ball", "A regular, old tennis ball.")
techRoomKey = Item("Key", "The key has a message engraved that says 'Tech Room Key'...")
backwardsGun = BackwardsGun("Gun", "It's a gun, but its barrel is pointing the opposite way.")
water = Drink("Water Bottle", "A water bottle that has an off-center label that says 'Fiji'.")
cookieMask = Mask("Mask", "A mask of a smiling man wearing glasses with slits in the eyes. Wonder what you'd use it "
                          "for.")
shirt = Shirt("Shirt", "Just a plain white shirt.")
weirdBag = Container("Backpack", "Just a regular backpack.", 4)

# Rooms

BEDROOM = Room("Bedroom",
               "You are in a bedroom full of anime posters, figures, etc."
               "\nYou have a computer sitting on a desk to your north, and a door to the east.",
               "COMPUTER", None, "HALLWAY", None, None, None, None, [bed])
COMPUTER = Room("Computer",
                "On the desk lies a computer with a crappy membrane keyboard and a mouse. "
                "On the computer lies a weird game called 'osu!'...",
                None, "BEDROOM", "HALLWAY", None, None, None, None, [weirdBag])
HALLWAY = Room("Hallway",
               "The hallway has a few paintings with a dull red carpet on the wooden floor."
               "\nThere are stairs leading down to the south, as well as another room across yours.",
               "DINING_ROOM", "EMPTY_ROOM", "BATHROOM", "BEDROOM", None, "DINING_ROOM", None, [])
EMPTY_ROOM = Room("Empty Room",
                  "You enter an empty room, but in the southern-most corner there's a table with what seems to be "
                  "a drawing tablet, as well as a keyboard.",
                  "HALLWAY", "TABLE", None, None, None, None, jeff, [backwardsGun])
TABLE = Room("Table",
             "On the table there is a key and empty boxes with labels saying "
             "'HyperX Alloy FPS Mechanical Gaming Keyboard' as well as another\n"
             "box that says 'Huion Graphics Tablet'...",
             "EMPTY_ROOM", None, None, None, None, None, None, [techRoomKey])
BATHROOM = Room("Bathroom",
                "The bathroom is set with two sinks, a bathtub and a toilet.\n"
                "There are also toiletries sitting on top of the sink counter.",
                None, None, None, "HALLWAY", None, None, None, [])
DINING_ROOM = Room("Dining Room",
                   "The dining room has a table with a fancy green cloth and a basket full of fake fruit."
                   "\nThe kitchen leads east, and the living room to the west.",
                   None, "HALLWAY", "KITCHEN1", "LIVING_ROOM", "HALLWAY", None, None, [cookie])
KITCHEN1 = Room("Entrance to Kitchen",
                "In the kitchen there's a refrigerator and a pantry full of "
                "food,\nas well as a long counter to eat food on. There's more stuff farther south.",
                "DINING_ROOM", "KITCHEN2", None, None, None, None, None, [])
KITCHEN2 = Room("Farther Side of Kitchen",
                "This side of the Kitchen has a flat screen tv mounted to the wall\nwith a smaller table below "
                "it that holds the cable box, and an old,\nuseless game console. There's what seems to be a "
                "laundry room to the\nwest as well as a slide door leading outside east.",
                "KITCHEN1", None, "BACKYARD1", "LAUNDRY_ROOM", None, None, None, [])
LAUNDRY_ROOM = Room("Laundry Room",
                    "The Laundry Room has a washing and drying machine, as well as a cabinet.",
                    "CABINET", None, "KITCHEN2", None, None, None, None, [water])
CABINET = Room("Inside of Cabinet",
               "Inside the cabinet contains jackets and sweaters. The shelf above it has a \n"
               "few boxes put for storage, but there's a paper mask of a man's face here...",
               # osu! joke, don't worry about it
               None, "LAUNDRY_ROOM", "KITCHEN2", None, None, None, None, [cookieMask])
BACKYARD1 = Room("Backyard",
                 "The empty backyard had little to no grass, making it look like a desert.\nNot only that, there "
                 "are two dogs that seem to not care about it at all\nand just have fun with the tennis balls "
                 "around them.",
                 "BACKYARD2", None, None, "KITCHEN2", None, None, None, [ball])
BACKYARD2 = Room("Farther side of the Backyard",
                 "This side of the backyard has an unused grill and a bench lying at the wall of the house. And "
                 "more tennis balls...", None, "BACKYARD1", None, None, None, None, None, [ball])
LIVING_ROOM = Room("Living Room",
                   "The living room has couches set with a large TV.\nThe exit seems to go the south.",
                   None, "DOOR", "DINING_ROOM", None, None, None, None, [])
DOOR = Room("Door",
            "You stand at the exit of the house, where lies a bunch of shoes.\nThe door faces west, "
            "and there's another door to the south.",
            "LIVING_ROOM", "LOCKED_DOOR", None, 'PORCH', None, None, None, [])
LOCKED_DOOR = Room("Locked Door", "This room's door is locked.", "DOOR", None, None, None, None, None, None, [])
PORCH = Room("Porch",
             "You exit the house into the porch, where there are short, dull, plants.\nYou can go more to "
             "the west to exit the porch and into the driveway.",
             None, None, "DOOR", "DRIVEWAY", None, None, None, [])
DRIVEWAY = Room("Driveway",
                "The drive way has a basketball hoop, but to the west you see a store with a sign that says... "
                "Walm.\nYou can go back north into the porch.", "PORCH", None, None, "STORE", None, None, None, [])
STORE = Room("Walm", "Sorry to keep your hopes up, this store is closed.",
             None, None, "DRIVEWAY", None, None, None, None, [])

TECH_ROOM = Room("Tech Room",
                 "The door you open leads you into room filled with bright looking technology.\n"
                 "The whole room seems to be white-ish. The whole room seems to be some sort of 'man cave'.\n"
                 "You feel so intimidated that you shouldn't touch any of the equipment.",
                 "DOOR", None, None, None, None, None, Cookie, [])

dir1 = ['north', 'south', 'east', 'west', 'up', 'down']
dir2 = ['n', 's', 'e', 'w', 'u', 'd']

current_node = BEDROOM
current_node_hasChanged = True

while True:
    if health == 0:
        print(redbold + "you died" + end)
        break
    print(redbold + "Health: " + end + str(health))
    if current_node_hasChanged:
        current_node.print_descriptions()
        current_node_hasChanged = False
        if current_node.character is not None \
                and current_node.character.isAlive:
            current_node.character.print_descriptions()
    print(inventory)
    command = input('>').lower()
    if command == 'quit':
        quit(0)
    elif 'look' in command or command == 'l':
        current_node.print_descriptions()
        if current_node.character is None or not current_node.character.isAlive:
            continue
        else:
            current_node.character.print_descriptions()
    elif 'jump' in command:
        current_node.jump()
    elif 'inv' in command or 'inventory' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory." + end)
        else:
            print("Your inventory:")
            for item in inventory:
                print(bold + item.name.lower() + end)
    elif 'armor' in command:
        if head is None and chest is None and legs is None and feet is None:
            print(redbold + "You're wearing nothing." + end)
        else:
            print("You are wearing:")
            if head is not None:
                print("\t" + "Head: " + head.name)
            if chest is not None:
                print("\t" + "Chest: " + chest.name)
            if legs is not None:
                print("\t" + "Legs: " + legs.name)
            if feet is not None:
                print("\t" + "Feet: " + feet.name)
    elif command == "oof":
        current_node.oof()
    elif command == "ping":
        current_node.ping()
        counter += 1
    elif command == 'flush':
        current_node.flush()
    elif command == 'beep':
        print('boop')
    elif command in dir2:
        pos = dir2.index(command)
        command = dir1[pos]
        try:
            current_node.move(command)
            current_node_hasChanged = True
        except KeyError:
            print(redbold + "You can't go that way." + end)
            current_node_hasChanged = False
    elif command in dir1:
        try:
            current_node.move(command.lower())
            current_node_hasChanged = True
        except KeyError:
            print(RED + "You can't go that way." + end)
            current_node_hasChanged = False
    elif 'take off' in command or 'unequip' in command:
        if command == 'take off' or command == 'unequip':
            if head is None and chest is None and legs is None and feet is None:
                print(redbold + "You aren't wearing anything." + end)
            else:
                unequip_command = input("What do you want to take off?\n>").lower()
                if head is not None:
                    if head == bed and unequip_command == 'bed':
                        head = None
                        inventory.append(bed)
                        print(blue + bold + "You take off the bed." + end)
                    elif unequip_command == head.name.lower():
                        head.unequip()
                    else:
                        print(redbold + "You aren't wearing that." + end)
                elif chest is not None:
                    if unequip_command == chest.name.lower():
                        chest.unequip()
                    else:
                        print(redbold + "You aren't wearing that." + end)
                elif legs is not None:
                    if unequip_command == legs.name.lower():
                        legs.unequip()
                    else:
                        print(redbold + "You aren't wearing that." + end)
                elif feet is not None:
                    if unequip_command == feet.name.lower():
                        feet.unequip()
                    else:
                        print(redbold + "You aren't wearing that." + end)
                else:
                    print(redbold + "You aren't wearing that.")
        else:
            if head is not None:
                if 'bed' in command:
                    head = None
                    inventory.append(bed)
                    print(blue + bold + "You take off the bed." + end)
                elif head.name.lower() in command:
                    head.unequip()
            elif chest is not None:
                if chest.name.lower() in command:
                    chest.unequip()
            elif legs is not None:
                if legs.name.lower() in command:
                    legs.unequip()
            elif feet is not None:
                if feet.name.lower() in command:
                    feet.unequip()
            else:
                print(redbold + "You aren't wearing anything.")
    elif 'take' in command or 'pickup' in command.strip():
        if not current_node.items:
            print(redbold + "There is nothing here to take." + end)
        elif command == 'take' or command.strip() == 'pickup':
            take_command = input("What do you want to take?\n>").lower().strip()
            for item in current_node.items:
                if take_command == item.name.lower():
                    item.take()
                    break
                elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                    print("ok")
                else:
                    print(redbold + "That item isn't here." + end)
        else:
            for item in current_node.items:
                if command == 'take' or command.strip() == 'pickup':
                    take_command = input("What do you want to take?\n>").lower().strip()
                    if take_command == item.name.lower():
                        item.take()
                        break
                    elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                        print("ok")
                        break
                    else:
                        print(redbold + "That item isn't here." + end)
                elif item.name.lower() in command:
                    item.take()
                    break
                else:
                    print(redbold + "That item isn't here." + end)
                    break
    elif 'drop' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory." + end)
        else:
            for item in inventory:
                if command == 'drop':
                    drop_command = input("What do you want to drop?\n>").lower()
                    if drop_command == item.name.lower():
                        item.drop()
                    elif 'nothing' in drop_command or 'nevermind' in drop_command or 'nvm' in drop_command:
                        print("ok")
                    else:
                        print(redbold + "You don't have that item." + end)
                elif item.name.lower() in command:
                    item.drop()
                    break
                else:
                    print(redbold + "You don't have that item." + end)
                    break





    elif 'throw' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory." + end)
        elif command == 'throw':
            throw_command = input("What do you want to throw?\n>").lower()
            for item in inventory:
                if throw_command == item.name.lower():
                    if item == ball:
                        ball.throw()
                    else:
                        item.drop()
                elif 'nothing' in throw_command or 'nevermind' in throw_command or 'nvm' in throw_command:
                    print("ok")
                else:
                    print(redbold + "You don't have that item." + end)




            if throw_command == 'ball':
                ball.throw()
            elif 'nothing' in throw_command or 'nevermind' in throw_command or 'nvm' in throw_command:
                print("ok")
            else:
                for item in inventory:
                    if throw_command == item:
                        item.drop()
                        break
                    else:
                        print(redbold + "That's not in your inventory." + end)
        else:
            for item in inventory:
                if item.name.lower() in command:
                    if item == ball:
                        ball.throw()
                        ball.isTaken = False
                        break
                    else:
                        item.drop()
                else:
                    print(redbold + "You don't have that in your inventory." + end)
    elif 'talk' in command:
        if current_node.character is None:
            print(redbold + "There is no one here." + end)
        elif command == 'talk':
            talk_command = input("Who do you want to talk to?\n>").lower().strip()
            if talk_command == current_node.character.name:
                if current_node.character.isAlive:
                    current_node.character.talk()
                else:
                    print(redbold + "That person is dead." + end)
            elif 'noone' in talk_command or 'nevermind' in talk_command or 'nvm' in talk_command:
                print("ok")
            else:
                print(redbold + "That person isn't here." + end)
        elif current_node.character.name.lower() in command:
            if current_node.character.isAlive:
                current_node.character.talk()
            elif not current_node.character.isAlive:
                print(redbold + "That person is dead.")
            else:
                print(redbold + "That person isn't here." + end)
        else:
            print(redbold + "That person isn't here." + end)
    elif 'wear' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory." + end)
        else:
            for item in inventory:
                if command == 'wear':
                    wear_command = input("What do you want to wear?\n>").lower()
                    if wear_command == 'bed':
                        time.sleep(1)
                        print("ok")
                        time.sleep(.5)
                        head = bed
                        print(blue + bold + "You wear the bed." + end)
                    elif wear_command == item.name.lower():
                        item.equip()
                    else:
                        print(redbold + "That item isn't in your inventory." + end)
                elif 'bed' in command:
                    time.sleep(1)
                    print("ok")
                    head = bed
                    print(blue + bold + "You wear the bed." + end)
                elif item.name.lower() in command:
                    item.equip()
                else:
                    print(redbold + "You aren't wearing that.")
    elif 'open door' in command:
        if current_node == LOCKED_DOOR:
            if techRoomKey in inventory:
                current_node = TECH_ROOM
                print(blue + bold + "You open the door.\n" + end)
                current_node_hasChanged = True
            else:
                print(redbold + "You don't have a key." + end)
        else:
            print(redbold + "There is no locked door to open.")
    elif 'shoot' in command:
        if backwardsGun in inventory:
            if command == 'shoot':
                backwardsGun_command = input("Who do you want to shoot?\n>").lower()
                if backwardsGun_command == current_node.character.name.lower():
                    backwardsGun.shoot()
                else:
                    print(redbold + "That person isn't here." + end)
            elif current_node.character.name.lower() in command:
                backwardsGun.shoot()
            else:
                print(redbold + "That person isn't here." + end)
        else:
            print(redbold + "You don't have anything to shoot with." + end)
    elif 'check' in command or 'look at' in command:
        for item in inventory:
            if not inventory:
                print(redbold + "You don't have anything in your inventory." + end)
            elif command == 'check' or command.strip() == 'lookat':
                check_command = input("What do you want to check?\n>").lower()
                if check_command == item.name.lower():
                    item.print_descriptions()
                elif 'nothing' in check_command or 'nevermind' in check_command or 'nvm' in check_command:
                    print("ok")
                else:
                    print(redbold + "You don't have that item." + end)
            elif item.name.lower() in command:
                item.print_descriptions()
            else:
                print(redbold + "You don't have that item." + end)
    elif 'drink' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory." + end)
        else:
            for item in inventory:
                if command == 'drink':
                    drink_command = input("What do you want to drink?\n>").lower()
                    if drink_command == item.name.lower():
                        if item == water:
                            water.drink()
                        elif item == bed:
                            time.sleep(1)
                            print("ok")
                            time.sleep(.5)
                            print(blue + bold + "You drink the bed." + end)
                            inventory.pop(inventory.index(bed))
                        else:
                            print(redbold + "You can't drink that." + end)
                    elif 'nothing' in drink_command or 'nevermind' in drink_command or 'nvm' in drink_command:
                        print("ok")
                    else:
                        print(redbold + "That's not in your inventory." + end)
                elif item.name.lower() in command:
                    if item == water:
                        water.drink()
                    elif item == bed:
                        time.sleep(1)
                        print("ok")
                        time.sleep(.5)
                        print(blue + bold + "You drink the bed." + end)
                        inventory.pop(inventoy.index(bed))
                    else:
                        print(redbold + "You can't drink that." + end)
                else:
                    print(redbold + "That's not in your inventory." + end)
    elif 'play' in command:
        if 'computer' in command:
            if head == cookieMask:
                print(PURPLE + bold + "You're so good at this game that the computer exploded" + end)
                time.sleep(1)
                print(PURPLE + bold + "And it pops back..." + end)
            else:
                print(redbold + "You play the game and rage in frustration at why you're so bad at it..." + end)
        elif command == 'play':
            play_command = input("What do you want to play?\n>").lower().strip()
            if play_command == 'computer':
                if head == cookieMask:
                    print(PURPLE + bold + "You're so good at this game that the computer exploded" + end)
                    time.sleep(3)
                    print(PURPLE + bold + "And it pops back..." + end)
                else:
                    print(redbold + "You play the game and rage in frustration at why you're so bad at it..." + end)
            elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                print("ok")
            else:
                print(redbold + "You can't play that." + end)
        else:
            print(redbold + "You can't play that." + end)
    elif 'kill' in command:
        if command == 'kill':
            kill_command = input("Who do you want to kill?\n>").lower()
            if kill_command == 'me' or kill_command == 'self':
                time.sleep(2)
                print("ok")
                time.sleep(.5)
                while health != 0:
                    health -= 1
                    print(redbold + "Health: " + end + str(health))
                    time.sleep(.01)
                    if health == 0:
                        break
            elif kill_command == current_node.character.name.lower():
                if current_node.character.isAlive:
                    current_node.character.kill()
                else:
                    print(redbold + "That person is dead." + end)
            else:
                print(redbold + "That person isn't here." + end)
        elif current_node.character is None:
            print(redbold + "There is no one here." + end)
        elif current_node.character.name.lower() in command:
            if current_node.character.isAlive:
                current_node.character.kill()
            else:
                print(redbold + "That person is dead." + end)
        else:
            print(redbold + "That person isn't here." + end)
    elif 'suicide' in command:
        time.sleep(2)
        print("ok")
        time.sleep(.5)
        while health != 0:
            health -= 1
            print(redbold + "Health: " + end + str(health))
            time.sleep(.01)
            if health == 0:
                break
    elif 'open' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory to open." + end)
        else:
            for item in inventory:
                if command == 'open':
                    open_command = input("What do you want to open?\n>").lower()
                    if open_command == item.name.lower():
                        if isinstance(item, Container):
                            item.open()
                        else:
                            print(redbold + "You can't open that." + end)
                    elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                        print("ok")
                    else:
                        print(redbold + "That isn't in your inventory." + end)
                elif item.name.lower() in command:
                    if isinstance(item, Container):
                        item.open()
                    else:
                        print(redbold + "You can't open that." + end)
                else:
                    print(redbold + "That is not in your inventory." + end)
    elif 'close' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory to close." + end)
        else:
            for item in inventory:
                if command == 'close':
                    open_command = input("What do you want to close?\n>").lower()
                    if open_command == item.name.lower():
                        if isinstance(item, Container):
                            item.close()
                        else:
                            print(redbold + "You can't close that." + end)
                    elif 'nothing' in take_command or 'nevermind' in take_command or 'nvm' in take_command:
                        print("ok")
                    else:
                        print(redbold + "That isn't in your inventory." + end)
                elif item.name.lower() in command:
                    if isinstance(item, Container):
                        item.close()
                    else:
                        print(redbold + "You can't open that." + end)
                else:
                    print(redbold + "That is not in your inventory." + end)







    elif 'put' in command:
        if not inventory:
            print(redbold + "You don't have anything in your inventory." + end)
        else:
            for item in inventory:
                if command == 'put':
                    put_command = input("What do you want to put?\n>").lower()
                    if put_command == item.name.lower():
                        for item2 in inventory:
                            putIn_command = input("Where do you want to put that?\n").lower()
                            if putIn_command == item2.name.lower():
                                if isinstance(item2, Container):
                                    if item2.isOpen:
                                        item2.put_item_in(item)
                                    else:
                                        print(redbold + "That item isn't open." + end)
                                else:
                                    print(redbold + "You can't put that in there." + end)
                            elif putIn_command == put_command:
                                print(redbold + "You can't put that in itself." + end)
                            else:
                                print(redbold + "That isn't in your inventory." + end)
                    else:
                        print(redbold + "That isn't in your inventory." + end)



    else:
        print("Command not Recognized")
        current_node_hasChanged = False