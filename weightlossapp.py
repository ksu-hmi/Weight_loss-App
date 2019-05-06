import pandas as pd
import datetime as dt 
import pytz as tz
import numpy as np

#list of affirmative and negative answers
affirmative = ['yes','yea','yeah','y','yessir','yep','roger','roger wilco','affirmative','aye','true']
negative = ['no','n','nope','nah','never','negative','nada','false','neh','nea','nei','nay']

#global data variables
daily_inputs = {'DATE': 0.0, 'WEIGHT': 0.0, 'DAILY_CHG': 0.0, 'TOTAL_CHG': 0.0}

#global username/password vars saved at login
global_username = ""
global_password = ""
global_index = 0

"""
Wish list:
    - MatPlotLib graph of weight change over time
    - Host DB on awiede.net 
    - encrypt username.csv file and/or host securly on awiede.net
    - include some exercise tracker (length, type, frequency)
    - password recovery questions
    - hide password characters in terminal
    - add cache timeout to global username and password storage
    - automatically setup goal based on initial weight, height, age, gender, etc.
"""

def get_current_date(): 
    ''' Gets current timestamp (EST) and writes it to daily_inputs global dictionary '''
    #create timestamp object
    utc = dt.datetime.utcnow()
    #create eastern timezone object
    eastern_tz = tz.timezone('US/Eastern')
    #convert utc timestamp to est equivalent
    est = utc.replace(tzinfo=tz.utc).astimezone(eastern_tz)
    #print est.strftime('Today is, %A, %B %d, %Y.')
    daily_inputs['DATE'] = est 

#Add login credentials
def create_user():
    users = pd.read_csv('test_usernames.csv', header=0, index_col=0)
    print ("Welcome to Andreas's Weight Loss Tracker!")
    print ("======================================================")
    print ("Please provide some information to create your account")
    print ("======================================================")
    print ("What is your first name?")
    first_name = input(">>> ")
    print ("What is your last name?")
    last_name = input(">>> ")
    username = first_name.lower()[0]+last_name.lower()
    print ("Your username is:",username)
    print ("Please create a password:")
    password = input(">>> ")
    file_name = username+"_weight_loss_data.csv"
    new_users = users.append([{'FIRST_NAME':first_name, 'LAST_NAME':last_name, 'USERNAME':username, 'PASSWORD':password, 'DATA_FILE':file_name}], ignore_index=True)
    new_users.to_csv('test_usernames.csv')

def password_change():
    if login():
        users = pd.read_csv('usernames.csv', header=0, index_col=0)
        new_password = ""
        while True:
            print ("Enter a new password")
            pass_attempt1 = input(">>> ")
            print ("Enter your new password again")
            pass_attempt2 = input(">>> ")
            if pass_attempt1 == pass_attempt2:
                new_password = pass_attempt1
                break
            else:
                print ("Passwords do not match")
        #index = users[users]['USERNAME']==global_username.index
        users = users.set_value(global_index, 'PASSWORD', new_password)
        users.to_csv('test_usernames.csv')


def enter_weight():
    valid_weight_flag = False
    while not valid_weight_flag:
        print ("What is your weight today?")
        try:
            weight = float(input(">>> "))
            print (weight)
            valid_weight_flag = True
            daily_inputs['WEIGHT'] = weight
        except NameError:
            print ("NameError. Let's try this again...")
        except SyntaxError:
            print ("SyntaxError. Let's try this again...")

def daily_chg():
    data = pd.read_csv('weight_loss_data.csv', header=0, index_col=0)
    yesterday_weight = data.get_value(data.last_valid_index(),'WEIGHT')
    weight_today = daily_inputs['WEIGHT']
    change = (weight_today - yesterday_weight)
    print ("You have lost:",change,"lbs. since your last visit.")
    daily_inputs['DAILY_CHG'] = change

def total_chg():
    data = pd.read_csv('weight_loss_data.csv', header=0, index_col=0)
    initial_weight = data.get_value(0, 'WEIGHT')
    weight_today = daily_inputs['WEIGHT']
    change = (weight_today - initial_weight)
    print ("You have lost:",change,"lbs. since you started.")
    daily_inputs['TOTAL_CHG'] = change

def login(): 
    ''' Returns boolean for success/failure '''
    users = pd.read_csv('usernames.csv', header=0, index_col=0)
    usernames = users.as_matrix(['USERNAME', 'PASSWORD'])
    #username check
    while True:
        input_username = input("Username: ").lower()
        input_password = input("Password: ")
        user_password = ""
        user_index = 0
        valid_username_flag = False
        for el in usernames:
            if el[0] == input_username:
                user_password = el[1]
                valid_username_flag = True
                user_index = el.index
                break
        if valid_username_flag and input_password == user_password:
            global_username = input_username
            global_password = user_password
            global_index = user_index
            return True
        else:
            print ("The username or password you entered is incorrect.")
            #handle allowing user to create account
            while True:
                try_again = input("Would you like to try again? ").lower()
                if try_again in affirmative:
                    break
                elif try_again in negative:
                    return False
                else:
                    print ("I'm sorry, I didn't understand.")



def main():
    data = pd.read_csv('weight_loss_data.csv', header=0, index_col=0)
    begin_app()
    get_current_date()
    enter_weight()
    daily_chg()
    total_chg()
    weight_data = data.append([daily_inputs], ignore_index=True)
    print (weight_data )
    weight_data.to_csv('weight_loss_data.csv')

def begin_app():
    print ("Welcome to your Weight Loss Tracker!")
    print ("Remember, you can do it!")
    print ("======================================================")
    print ("|                     ==    ==                       |")
    print ("|                        ||                          |")
    print ("|                    =        =                      |")
    print ("|                     ========                       |")
    print ("======================================================")
    while True:
        response = str(input("Do you have an account? $ ")).lower()
        if response in affirmative:
            break
        elif response in negative:
            create_user()
            break
        else:
            print ("I'm sorry, I did not understand your response.")
