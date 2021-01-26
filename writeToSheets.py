import pygsheets
import os

#Authorization
def recordNewPlaytester(user_answers):
    credentials = os.environ.get('GDRIVE_CREDENTIALS')
    gc = pygsheets.authorize(client_secret=credentials)

    #Open the google spreadsheet
    spreadsheet = gc.open('Playtest Signup').sheet1

    # Update a single cell.
    cells = spreadsheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    last_row = len(cells)
    spreadsheet = spreadsheet.insert_rows(last_row, number=1, values=user_answers)

