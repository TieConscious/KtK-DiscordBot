import pygsheets
import os
import json



# Authorization
# gc = pygsheets.authorize(service_account_env_var='GDRIVE_CREDENTIALS')

# For local testing
gc = pygsheets.authorize(service_file='ktk-playtester-1611548901474-1547c6217fc8.json')
user_list = {}

def cacheUserList():
    spreadsheet = gc.open('Playtest Signup').sheet1
    sh_user_list = spreadsheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    for info in sh_user_list:
        # info[1] == user name, info[5] == steam key
        user_list[info[1]] = info[5]
    print(len(user_list))


def checkNewPlaytester(user_name_discriminator):
    if len(user_list) == 0:
       cacheUserList()

    # If name exists
    if user_name_discriminator in user_list:
        return False
    else:
        return True


def recordNewPlaytester(user_answers):
    gsheet = gc.open('Playtest Signup')

    # Find available Steam Key
    key_sheet = gsheet.worksheet('title', 'SteamKeys')
    cell = len(key_sheet.get_col(1, returnas='cell', include_tailing_empty=False))
    key_sheet.update_value('B' + str(cell), 'Yes')
    new_key = key_sheet.get_value('A' + str(cell))

    # Record new user
    spreadsheet = gsheet.worksheet('title', 'Playtesters')
    user_answers.append(new_key)
    last_row = len(user_list)
    spreadsheet = spreadsheet.insert_rows(last_row, number=1, values=user_answers)
    
    # Add user to cache
    user_list[user_answers[1]] = new_key
    return(new_key)


def findSteamKey(user_name_discriminator):
    if len(user_list) == 0:
        cacheUserList()
    
    return user_list.get(user_name_discriminator)
