import pygsheets
import os
import json

#Authorization
def recordNewPlaytester(user_answers):
    gc = pygsheets.authorize(service_account_env_var='GDRIVE_CREDENTIALS')
    # gc = pygsheets.authorize(service_file='ktk-playtester-1611548901474-1547c6217fc8.json')

    #Open the google spreadsheet
    spreadsheet = gc.open('Playtest Signup').sheet1

    # Update a single cell.
    cells = spreadsheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    last_row = len(cells)
    spreadsheet = spreadsheet.insert_rows(last_row, number=1, values=user_answers)

