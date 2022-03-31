# PSV Stats Web App
# main.py

# imports
from pyparsing import col
import streamlit as st
from pandas import DataFrame
# for spreadsheet info
from gspread_pandas import Spread, Client
from google.oauth2 import service_account

# Disable certificate verification
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Auth connect object
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)
spreadsheetname = "PSV-H2-Overall-Stats"
spread = Spread(spreadsheetname,client = client)

# Check if connection is established
#st.write(spread.url)

# Call our spreadsheet
sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

# Get our worksheet names
def worksheet_names():
    sheet_names = []
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)
    return sheet_names

# Get the sheet as a dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_values())
    return df

# Update the sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Suggestion', 'Time_stamp']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname, index = False)
    st.sidebar.info('Suggestion added to GoogleSheet')

# Load data from worksheets
what_sheets = worksheet_names()
#st.sidebar.write(what_sheets)
ws_choice = st.sidebar.radio('Select a sheet', what_sheets)
df = load_the_spreadsheet(ws_choice)

header = st.container()
dataset = st.container()
#slider = st.sidebar()

# Header and caption
with header:
    st.title('Welcome to the PSV⚾Stats📊 Web App🤖')
    st.caption('Web App to display current PSV H2 stats')

with dataset:
    # Print results of selected Google Sheet
    st.table(df)
    
   