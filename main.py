from googleapiclient.discovery import build
from google.oauth2 import service_account

from config import Config

import re
import time

def update_amounts(lines, current_amounts):
    for line in lines: 
        # m = re.match("(\d{2}:\d{2}:\d{2},\d{3}) - \[([^\]]+)\] (.*)", line)
        m = re.search("Vous avez ramassé (\d+)x (.+?)\s+\.\s*$", line)
        if m:
            if m.group(2) not in current_amounts.keys():
                current_amounts[m.group(2)] = int(m.group(1))
            else:
                current_amounts[m.group(2)] += int(m.group(1))
        

creds = service_account.Credentials.from_service_account_file(
        Config.GOOGLE_KEY_FILE,
        scopes=Config.SHEETS_SCOPES)

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
current_line_count = 0

while True:
    with open(Config.FILENAME, "r", encoding="utf-8") as f:
        lines = f.readlines()
        n = len(lines)
        if n != current_line_count:
            response = (sheet.values().batchGet(spreadsheetId=Config.SPREADSHEET_ID,
                                    ranges="A2:B", majorDimension='ROWS').execute())['valueRanges'][0]
            amounts = {}
            if 'values' in response.keys():
                for row in response['values']:
                    if row[0] not in amounts.keys():
                        amounts[row[0]] = int(row[1])
                    else:
                        amounts[row[0]] += int(row[1])
            if n < current_line_count:
                update_amounts(lines, amounts)
            elif n > current_line_count:
                update_amounts(lines[current_line_count:], amounts)
                
            current_line_count = n

            values = []
            for item in amounts.keys():
                values += [[item, amounts[item]]]
            value_range = {
                "valueInputOption" : "RAW",
                "data": {
                    "range": f"Feuille 1!A2:B{len(values)+1}",
                    "majorDimension": 'ROWS',
                    "values": values
                }
            }
            sheet.values().batchUpdate(spreadsheetId=Config.SPREADSHEET_ID, body=value_range).execute()
    time.sleep(30)