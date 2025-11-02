"""Module defining configuration for SantaBOT"""

class Config:
    """Class storing configuration constants."""
    # You should not have to touch this line
    SHEETS_SCOPES = ['https://www.googleapis.com/auth/pubsub',
                    'https://www.googleapis.com/auth/spreadsheets']
    # Your Google API key file
    GOOGLE_KEY_FILE = ''

    # ID Of the Spreadsheet
    SPREADSHEET_ID = ''

    SHEET_NAME = 'Feuille 1'

    FILENAME = '/path/to/wakfu_chat.log'
