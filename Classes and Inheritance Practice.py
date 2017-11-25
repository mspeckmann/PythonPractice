'''Melinda Speckmann
Assignment 3
Due Date: 10/30/2017'''


class Pet:
    #Create two variables kind and color; assign values
    kind = 'animal'
    color = 'brown'


    def __init__(self, name):
        #In the constructor, initialize the pets name
        self.name = name

    #Print the name of the pet and that it is doing tricks
    def __str__ (self):
        return 'My name is {0}'.format(self.name)

    def do_tricks(self):
        print('{0} is doing tricks'.format(self.name))

    def speak(self):
        pass

    def jump(self):
        pass

class Jumper:
    'This is a mixin class for jump'
    def jump(self):
    #Create jump method that prints that a Pet is jumping and the pets name
        return '{0} is jumping'.format(self.name)

class Dog(Jumper, Pet):  #You will need to inherit for this to work

    #Change kind to canine
    kind = 'canine'

    def __str__(self):
        #Return the name and description of dog
        return 'I am a dog named {0}'.format(self.name)


    def __call__(self, action, owner = ''):
        #Rollover action prints the name of the dog and that it is rolling over

        if action == 'rollover':
            print('{0} is rolling over'.format(self.name))

        #Owner action returns the name of the owner
        elif action == 'owner' and owner != '':
            return 'My owner is {0}.'.format(owner)

        elif action == 'both' and owner != '':
            print('{0} is rolling over'.format(self.name))
            return 'My owner is {0}.'.format(owner)


class BigDog(Dog):  #You will need to inherit for this to work
    # Change the color to tan
    color = 'tan'

    def __str__(self):
        # Return the name and description of BigDog
        return '{0} is a large, muscular dog'.format(self.name)

    def speak(self):
        # Print dogs name and what it says
        print ('{0} says Woof!!!'.format(self.name))

class SmallDog(Dog):  #You will need to inherit for this to work

    # Change the color to brindle
    color = 'brindle'

    def __str__(self):
        #Return the name and description of SmallDog
        return '{0} is a tiny, cute dog'.format(self.name)

    def speak(self):
        # Print dogs name and what it says
        print ('{0} says Yip!'.format(self.name))

class Cat(Jumper, Pet):  #You will need to inherit for this to work

    #Change the kind to feline
    kind = 'feline'

    def __str__(self):
        #Return the name and description of cat
        return 'I am a cat named {0}'.format(self.name)

    def speak(self):
        # Print cats name and what it says
        print('{0} says Meow!!!'.format(self.name))

    def climb(self):
        #Prints the name of the cat and that it is climbing
        return '{0} is climbing the curtains again'.format(self.name)

class HouseCat(Cat):  #You will need to inherit for this to work
    #Change the color to white
    color = 'white'

    def __str__(self):
        #Return the name and description of cat
        return '{0} is a cat with fluffy, white fur'.format(self.name)

    def speak(self):
        # Print cats name and what it says
        print ('{0} says Purr'.format(self.name))




#Instantiate each class

p_taz = Pet('Taz')
C_Lion = Cat('Lion')
D_Roo = Dog('Roo')
d_Noah = BigDog('Noah')
d_Lucky = SmallDog('Lucky')
c_Zebra = HouseCat('Zebra')


#list of instantiated objects
animals = [p_taz,C_Lion,D_Roo,d_Noah,d_Lucky,c_Zebra]

x = 0
while x < len(animals):
    print(animals[x])
    print (animals[x].kind)
    print (animals[x].color)
    animals[x].do_tricks()
    animals[x].speak()

    if isinstance(animals[x], Cat) or isinstance(animals[x], Dog):
        print(animals[x].jump())
    else:
        pass

    if isinstance(animals[x], Dog):
        print(animals[x].__call__('both', 'George'))
    elif isinstance(animals[x], Cat):
        print (animals[x].climb())
    else:
        pass

    print('-----------------------')

    x += 1
    continue


