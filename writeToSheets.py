import pygsheets
import os
import json



# Authorization
gc = pygsheets.authorize(service_account_env_var='GDRIVE_CREDENTIALS')

# For local testing
# gc = pygsheets.authorize(service_file='ktk-playtester-1611548901474-1547c6217fc8.json')
user_list = set()

def cacheUserList():
    spreadsheet = gc.open('Playtest Signup').sheet1
    sh_user_list = spreadsheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    for info in sh_user_list:
        user_list.add(info[1])
    print(user_list)


def checkNewPlaytester(user_name_discriminator):
    if len(user_list) == 0:
       cachesUserList():

    # If name exists
    if user_name_discriminator in user_list:
        return False
    else:
        user_list.add(user_name_discriminator)
        return True


def recordNewPlaytester(user_answers):
    # Open the google spreadsheet
    spreadsheet = gc.open('Playtest Signup').sheet1

    # Update a single cell.
    # cells = spreadsheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    last_row = len(user_list)
    spreadsheet = spreadsheet.insert_rows(last_row, number=1, values=user_answers)


def findSteamKey(user_name_discriminator):
    if len(user_list) == 0:
        cacheUserList()
    
