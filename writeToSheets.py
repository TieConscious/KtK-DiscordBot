import pygsheets
import os
import json


try:
    # For local testing
    gc = pygsheets.authorize(service_file='ktk-playtester-1611548901474-1547c6217fc8.json')
except FileNotFoundError:
    # Authorization
    gc = pygsheets.authorize(service_account_env_var='GDRIVE_CREDENTIALS')

gsheet = gc.open('Playtest Signup')
key_sheet = gsheet.worksheet('title', 'SteamKeys')
spreadsheet = gsheet.worksheet('title', 'Playtesters')


def checkNewPlaytester(user_name_discriminator):
    user_list = spreadsheet.get_col(2, returnas='matrix', include_tailing_empty=False)
    
    # If name exists
    if user_name_discriminator in user_list:
        return False
    else:
        return True


def steamKeysAvailable():
    redeemedLen = len(key_sheet.get_col(2, returnas='matrix', include_tailing_empty=False))
    keyLen = len(key_sheet.get_col(1, returnas='matrix', include_tailing_empty=False))

    if redeemedLen != keyLen:
        key_sheet.update_value('B' + str(redeemedLen+1), 'Yes')
        return key_sheet.get_value('A' + str(redeemedLen+1))
    return None
    

def recordNewPlaytester(user_answers):
    # Find available Steam Key
    new_key = steamKeysAvailable()

    if new_key != None:
        # Record new user
        user_answers.append(new_key)
        list_len = len(spreadsheet.get_col(2, returnas='cell', include_tailing_empty=False))
        spreadsheet.insert_rows(list_len, number=1, values=user_answers)
        
        return(new_key)
    else:
        new_key = "unavailable"
        user_answers.append(new_key)
        list_len = len(spreadsheet.get_col(2, returnas='cell', include_tailing_empty=False))
        spreadsheet.insert_rows(list_len, number=1, values=user_answers)
        
        return(None)


def findSteamKey(user_name_discriminator):
    user_list = spreadsheet.get_col(2, returnas='matrix', include_tailing_empty=False)
    
    try:
        cell = user_list.index(user_name_discriminator)
        key = spreadsheet.get_value('F' + str(cell+1))
        return key
    except ValueError:
        return None


def needMoreKeys():
    redeemedLen = len(key_sheet.get_col(2, returnas='matrix', include_tailing_empty=False))
    keyLen = len(key_sheet.get_col(1, returnas='matrix', include_tailing_empty=False))

    if redeemedLen == keyLen:
        return True
    return False


def whoNeedsKeys():
    user_list = []
    no_key = spreadsheet.get_col(6, returnas='matrix', include_tailing_empty=False)
    for i, key in enumerate(no_key):
        if key == "unavailable":
            user = spreadsheet.get_value('B' + str(i+1))
            user_list.append(user)

    return user_list


def rainCheckKey(user_name_discriminator):
    key = steamKeysAvailable()
    user_list = spreadsheet.get_col(2, returnas='matrix', include_tailing_empty=False)
    
    try:
        cell = user_list.index(user_name_discriminator)
        spreadsheet.update_value('F' + str(cell+1), key)
        return key
    except ValueError:
        return None


def getNewestPlaytesters():
    col = 0
    target_date = "2/22/2022"
    sheet = gc.open('Single Player Playtest Signup (Responses)')
    old_sheet = sheet.worksheet('title', 'Sheet1')

    date_list = old_sheet.get_col(1, returnas='matrix', include_tailing_empty=False)
    end = len(date_list)
    for i, date in enumerate(date_list):
        if target_date in date:
            col = i+1
            break

    try:
        user_list = old_sheet.get_values('D' + str(col), 'D' + str(end), returnas='matrix', include_tailing_empty=False)
    except ValueError:
        print("No users on attempt")
        return None

    return user_list