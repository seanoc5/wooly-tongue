import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

# Define the scope of Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Credentials JSON file downloaded from Google Cloud Console
creds = '/opt/docs/stackedcone-bbec38745789.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(creds, scope)

# Authenticate using the credentials
client = gspread.authorize(credentials)

# Create a new Google Sheets workbook
workbook = client.create('StackedCone')

# Add two sheets named 'one' and 'two'
sheet_one = workbook.add_worksheet(title='one', rows="10", cols="2")
sheet_two = workbook.add_worksheet(title='two', rows="2", cols="1")
sheet_three = workbook.add_worksheet(title='StackyStack', rows="2", cols="1")

# Populate 'one' sheet with random numbers
for i in range(1, 11):
    sheet_one.update_cell(i, 1, random.randint(1, 100))
    sheet_one.update_cell(i, 2, random.randint(1, 100))

# Add formulas to 'two' sheet to sum each column
sheet_two.update_cell(1, 1, "=SUM(one!A:A)")
sheet_two.update_cell(2, 1, "=SUM(one!B:B)")

sheet_three.update_cell(1, 1, "This is a stackedcone test")

# Share the workbook with anyone with the link
workbook.share("", perm_type='anyone', role='reader')

print("Workbook created successfully!")
print(f"Url: {workbook.url}!")
