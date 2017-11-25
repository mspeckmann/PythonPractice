'''
Melinda Speckmann
Assignment 2
Due 10/10/17
'''

import os
import random
import csv
import errno

currDir = os.getcwd()
file_path = os.path.join (currDir, 'resources')
print (os.path.exists (file_path)) #Validate Path to file exists

def load_csv_to_list(path_to_file):
    global a_list, n_list, v_list, s_list
    a_path = os.path.join (path_to_file, 'adjectives.csv') #Return a list of items from file
    print (os.path.isfile (a_path))  #Validate file exists
    with open (a_path, 'r') as a_in:
        reader = csv.reader(a_in, delimiter=',')
        a_list = []
        for row in reader:
            a_list.append(row[0])
        print("Adjective List: ",a_list)
    a_in.close()
    n_path = os.path.join (path_to_file, 'nouns.csv') #Return a list of items from file
    print (os.path.isfile (n_path))  #Validate file exists
    with open (n_path, 'r') as n_in:
        reader = csv.reader(n_in, delimiter=',')
        n_list = []
        for row in reader:
            n_list.append(row[0])
        print("Noun List: ",n_list)
    n_in.close()
    v_path = os.path.join (path_to_file, 'verbs.csv') #Return a list of items from file
    print (os.path.isfile (v_path))  #Validate file exists
    with open (v_path, 'r') as v_in:
        reader = csv.reader(v_in, delimiter=',')
        v_list = []
        for row in reader:
            v_list.append(row[0])
        print("Verb List: ",v_list)
    v_in.close()
    s_path = os.path.join (path_to_file, 'sentences.csv') #Return a list of items from file
    print (os.path.isfile (s_path))  #Validate file exists
    with open (s_path, 'r') as s_in:
        reader = csv.reader(s_in, delimiter=',')
        s_list = []
        for row in reader:
            s_list.append(row[0])
        print("Template List: ",s_list) #Return a list of items from file
    s_in.close()


def shuffle(sequence):
    random.shuffle(sequence)
    return sequence


def load_mad_lib_resource(path_to_resource):
    global ADJECTIVES, NOUNS, VERBS, SENTENCES
    load_csv_to_list(path_to_resource) #Call load_csv_to_list
    ADJECTIVES = shuffle(a_list)
    NOUNS = shuffle(n_list)
    VERBS = shuffle(v_list)
    SENTENCES = shuffle(s_list)
    return (ADJECTIVES, NOUNS, VERBS, SENTENCES) #Return a tuple of the shuffled list

try:
    os.makedirs('users')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

user_path = os.path.join (currDir, 'users')

def create_userfile(username):
    global user_path, userfile
    userfile = os.path.join(user_path,username + '.csv')
    try:
        with open(userfile):
            pass
    except IOError:
        print ('Welcome to the game.')
        user_sentences = []
        with open(userfile, "w") as output:
            pass
        output.close()
    else:
        print ('Thank you for playing again.')
        with open(userfile, 'r') as input:
            reader = csv.reader(input, delimiter=',')
            user_sentences = [] #GET THE USER'S SAVED GAMES IF IT EXISTS
            for row in reader:
                user_sentences.append(row[0])
        input.close()
    return user_sentences

def write_file(csvfile, csv_list):
    with open(csvfile, "w") as output:
        writer = csv.writer(output, delimiter=',')
        for item in csv_list:
            writer.writerow([item])

    output.close ()


def play_game(lower_bound=1, upper_bound=10):
    is_keep_playing = 'y'
    global user_sentences
    while is_keep_playing != 'n':
        user_str_number = input(
            "Please provide a number between %s and %s" % (lower_bound, upper_bound)
    )

        try:
            user_number = int(user_str_number.strip().lower())

        except:
            print("Sorry the value provided is not an integer.")
            user_number = None
            continue

        if user_number is not None:
            if user_number < lower_bound:
                print("Sorry the number provided is too small (lower than {})".format(lower_bound))
                break
            elif user_number > upper_bound:
                print("Sorry the number provided is too big (greater than {})".format(upper_bound))
                break
            else:
                sentence_idx = random.randint(user_number, upper_bound) % len(SENTENCES)
                noun_idx = random.randint(user_number, upper_bound) % len(NOUNS)
                verb_idx = random.randint(user_number, upper_bound) % len(VERBS)
                adjective_idx = random.randint(user_number, upper_bound) % len(ADJECTIVES)

                # generate the mad lib sentence
                new_sentence = SENTENCES[sentence_idx].format(
                    noun=NOUNS[noun_idx],
                    verb=VERBS[verb_idx],
                    adjective=ADJECTIVES[adjective_idx],
                )
        US = 0
        while US < len(user_sentences):
            if new_sentence ==user_sentences[US]:
                new_sentence = None
            else:
                US += 1
        if new_sentence ==None:
            print ('Your sentence is not unique.')
            break
        #GENERATE THE SENTENCES AND WRITE TO THE FILE IF NOT ALREADY SAVED
        else:
            print ('Your sentence is unique!')
            user_sentences.append(new_sentence)
            #PRINT ALL OF THE SENTENCES FOR THE USER THUS FAR
            print (user_sentences)
            write_file(userfile, user_sentences)
            break

    is_keep_playing = None  # reset

    while 'y' != is_keep_playing and 'n' != is_keep_playing:
      is_keep_playing = input("Do you want to keep playing? y / n")
      is_keep_playing = is_keep_playing.strip().lower()
      if 'y' != is_keep_playing and 'n' != is_keep_playing:
        print("Sorry, I did not get that.")
        continue
      elif is_keep_playing == 'y':
        play_game()
      elif is_keep_playing == 'n':
        print("Bye!")
        break



if __name__ == '__main__':

    username = input('Please enter your username: ') #PROMPT FOR USERNAME
    #VERIFY THE A USER NAME WAS ENTERED ELSE EXIT THE PROGRAM
    if username == '':
        print ('A username was not entered. The game will now end, please try again.')
    else:
        user_sentences = create_userfile(username) #FIND OUT IF THERE IS AN EXISTING USER SAVED GAMES
        shuff_tuple = (load_mad_lib_resource(file_path))
        print ("Shuffled Tuple:",shuff_tuple)
        play_game() #CALL PLAY GAME FUNCTION
