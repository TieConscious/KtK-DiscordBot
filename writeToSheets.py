import pygsheets
import os
import json

# For local testing
gc = pygsheets.authorize(service_file='ktk-playtester-1611548901474-1547c6217fc8.json')

# Authorization
# gc = pygsheets.authorize(service_account_env_var='GDRIVE_CREDENTIALS')


def checkNewPlaytester(user_name_discriminator):
    spreadsheet = gc.open('Playtest Signup').sheet1
    user_list = spreadsheet.get_col(2, returnas='matrix', include_tailing_empty=False)
    
    # If name exists
    if user_name_discriminator in user_list:
        return False
    else:
        return True


def steamKeysAvailable():
    gsheet = gc.open('Playtest Signup')
    key_sheet = gsheet.worksheet('title', 'SteamKeys')
    cell = len(key_sheet.get_col(2, returnas='matrix', include_tailing_empty=False))
    key_sheet.update_value('B' + str(cell), 'Yes')

    return key_sheet.get_value('A' + str(cell))


def recordNewPlaytester(user_answers):
    gsheet = gc.open('Playtest Signup')

    # Find available Steam Key
    new_key = steamKeysAvailable()

    # Record new user
    spreadsheet = gsheet.worksheet('title', 'Playtesters')
    user_answers.append(new_key)
    list_len = len(spreadsheet.get_col(2, returnas='cell', include_tailing_empty=False))
    spreadsheet = spreadsheet.insert_rows(list_len, number=1, values=user_answers)
    
    return(new_key)


def findSteamKey(user_name_discriminator):
    spreadsheet = gc.open('Playtest Signup').sheet1
    user_list = spreadsheet.get_col(2, returnas='matrix', include_tailing_empty=False)
    
    try:
        cell = user_list.index(user_name_discriminator)
        key = spreadsheet.get_value('F' + str(cell + 1))
        if key == "":
            return "unavailable"
        return key
    except ValueError:
        return None
