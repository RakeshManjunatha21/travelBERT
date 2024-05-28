import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st
from gspread.exceptions import APIError
import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import json
import google.generativeai as genai
import requests
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode
import requests
import base64
import io

# Replace 'your_google_sheet_id' with your actual Google Sheet ID
SPREADSHEET_ID = '1BJtkta1n1vwZScjsOx82zh_aoNVa4IBe70EZ04DLby4'
WORKSHEET_NAME = 'updated_list.csv'  # Replace with your sheet name if different

# Google Sheets credentials
CREDENTIALS = {
  "type": "service_account",
  "project_id": "hale-acumen-424710-p5",
  "private_key_id": "8448d8afe26fc07a6e49479559ff88346f7b5301",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDAL8skCAPcueDQ\nq966xmE2HP+PFEWNQ8u3TK3W0oZV/JrpLtQ1EZNK/da80GgF9S8nf0WPhsBuZvGU\nV5WXXyzcSYF/hGJkYSj1aDen+1dQmpdhUf/H0RfeKQ77wwWHa3SzVnemODwl231g\nncrX5aQ/pOBMixxaaIB567nvMz9REofmE63WlH2Tn1d3L+/VI7AutzqshjtlBVof\ntbdl+bb6TK+LFgm1ZfAlKmlKCUP5sabLtHOdxPNNUIwdlhYQHiRx8VLo2/2zZfd9\nJ6R+vklYO7Rov7xzjmBQ5VyPMBKBuBBZjIUgJjMrXxuTcJfvnHjcLCUQmfwTEUYw\n/JBavlW5AgMBAAECggEAFrqgSPzcrhJapPsqnoa/MPXpgHuqhRw3P9Ck/5LK2ekD\nzh+gb71KIPSX3KE+KDQ41TA/YwvR/syUdhGMqsgSB2R3GQRoWYxHGozuhiKazzjV\nPeiDeld/feH3uG02Xm9mMB6CDIm6jVShxZcryfBKBk/iyhKqsgOJbEHlbcVvD9CP\ndvV4fGGnfkJhhz8zCAg2KL34eyICTwFLQoj+lrHR1mhNdlklR/DNOn1Qy8520qDL\nxBxotK1C6snaQAo+AFpVBLvFuqN9fIXCsRyWtKYUlVR6Kr92rKQGN4ff/HEpI5P5\nFsyalzdNjUpEY+e5fqWr/U4S0KOtRAyhrURh9YpqjQKBgQDn5ZE3hBiPdCVXZttW\nBvX2WciWGGEuSswsRKNsoNPFiYKggd43lYSB7bjk1FjOVK3VsLSDqAgRf3foeVBe\nDDBt9BT3xyj0+ROkJYW4k3m56crBjMNajHc275nUOYUBRbjAt9v10o33HZR8xXBp\nVLlV8bn6UsSA6wrsMxvei6H8FQKBgQDUKZmTe8Yoq3lyHf86Xleqn5gfyCyRNb/r\nsigUMymsojAZGtoc8vM4J6dxxxsIJFaIiRJS9jFsB3ClXN0fZsPpG0SFyqb7jH5t\nxRCmNisUNhEdbSTvud38GokXBJoQHJuVIdxgX/AEWOfSAJbUtmDhu9TlJolLX1Gg\nI/mKnUQIFQKBgG20cQqud2AGNlQu2LzN9jZhKz+2sOLRh925awbM3uKotx9v0MzC\n8zj0WXAH9StHbCWXvw45w/djMjrMiXS0l4Ss3+6ITZv26Y/SIHy9Z+zH6Z+/E/wW\nT5+xojiALaf4b/rcADc/MOIjIEgWr6Nk7Xj3LmB6H3RNvZEYbKrPrAYxAoGASE7l\nSJ6mqrXGbl5K3lnJBx3devd+OP9YqbvObRQC4BNm0SeVrsgenMTnDKAPVncMBvyw\nghXmQitG+RTtSAZ+PrRMZkzrHFCFxmOjiQJtLDZBHwZT0GBIh+ODVZT77QHTBMDF\nmxMXemPSnoAU5+pAmq6poG/B2y5hY3LfWZ6/0QECgYB1BOSS9rcNsxXRn2kG7aOB\nFJ6YXu+iULeoOTFUD+kYmng7GRhu3TCLljOHpfJItX9Y0phd6VFjeVIwpFIzrcRW\nRmJgufsDB11oAcsRsOwH5gPp2Bxih7Gokp+9xOliFIYgWpEiLGiOXNydaq4XC3mZ\nA0aBeNrrCyqETM+FGNcIqw==\n-----END PRIVATE KEY-----\n",
  "client_email": "travelbertsheet@hale-acumen-424710-p5.iam.gserviceaccount.com",
  "client_id": "104859650707433647407",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/travelbertsheet%40hale-acumen-424710-p5.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Google Sheets setup
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(CREDENTIALS, scopes=SCOPES)
gc = gspread.authorize(credentials)

# Function to read data from Google Sheets
def read_data_from_google_sheets():
    try:
        sheet = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except APIError as e:
        st.error(f"APIError reading from Google Sheets: {e}")
        return pd.DataFrame(columns=["Questions", "Suggestions"])
    except Exception as e:
        st.error(f"Error reading from Google Sheets: {e}")
        return pd.DataFrame(columns=["Questions", "Suggestions"])

# Function to write data to Google Sheets
def write_data_to_google_sheets(df):
    try:
        sheet = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET_NAME)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        st.success('Database Updated...')
    except APIError as e:
        st.error(f"APIError updating Google Sheets: {e}")
    except Exception as e:
        st.error(f"Error updating Google Sheets: {e}")

def TravelScore(text:str):
    senti_analysis_prompt = f"""Analyse the following list of feedback '{text}' and generate Below
    1. What is the Probablity Score of people visiting that place. (Just give one score from 0 to 100% based on Negative aspects and Positive aspects) //Heading: Probalility Score of People Visiting
    2. What is the Negative Aspect, how can a Travel Agence Improve.
    only give above two

    """
    return senti_analysis_prompt

def llm():
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel("gemini-pro",
                                         generation_config=genai.types.GenerationConfig(
                                             max_output_tokens=64000,
                                             temperature=0.0
                                         ))
    return gemini_model

def responseFunc(prompt):
    model = llm()
    response = model.generate_content(prompt)
    return response

# Load the existing DataFrame from Google Sheets or create a new one
try:
    df = read_data_from_google_sheets()
except FileNotFoundError:
    df = pd.DataFrame(columns=["Questions", "Suggestions"])

# Streamlit app title
st.title('Choose a Place to Visit in India')

choices = df["Questions"].tolist()
choices.append("----NEW Place----")
choices = list(set(choices))

# Option to select a place
place = st.selectbox("Select the place you want to visit", choices)

# Form for new place and feedback
with st.form(key='feedback_form'):
    if place == "----NEW Place----":
        new_place = st.text_input("Enter the new place")
        feedback_message = st.text_area('Your Feedback', help='Enter your feedback here')
    else:
        new_place = place
        feedback_message = st.text_area('Your Feedback', help='Enter your feedback here')
    submit_button = st.form_submit_button(label='Submit Feedback')

    if submit_button:
        # Update the DataFrame
        if place == "----NEW Place----" and new_place:
            df = pd.concat([df, pd.DataFrame({"Questions": [new_place], "Suggestions": [feedback_message]})], ignore_index=True)
        else:
            for i in df.index:
                if df["Questions"][i] == place:
                    df.at[i, "Suggestions"] += '@' + feedback_message
        
        # Save the updated DataFrame to Google Sheets
        write_data_to_google_sheets(df)
        st.success('Thank you for your feedback!')

if place != "----NEW Place----": 
    selected_suggestions = df[df["Questions"] == place]["Suggestions"].iloc[0].split("@")

    # Convert suggestions to dataframe
    suggestions_df = pd.DataFrame({"Suggestions": selected_suggestions})

    # Add a column for thumbs up/down
    suggestions_df["Thumbs"] = ""

    # Display suggestions with thumbs up/down buttons
    st.write("Suggestions:")
    gb = GridOptionsBuilder.from_dataframe(suggestions_df)
    thumbs_renderer = JsCode('''
        class ThumbRenderer {
            init(params) {
                this.params = params;
                this.eGui = document.createElement('span');
                if (params.value === '👍') {
                    this.eGui.innerHTML = '👍';
                } else if (params.value === '👎') {
                    this.eGui.innerHTML = '👎';
                } else {
                    this.eGui.innerHTML = 'None';
                }
            }

            getGui() {
                return this.eGui;
            }

            refresh(params) {
                return false;
            }
        }
    ''')

    button_handler = JsCode('''
        function onCellClicked(params) {
            if (params.colDef.field === 'Thumbs') {
                let newValue = params.value === '👍' ? '👎' : '👍';
                params.api.applyTransaction({ update: [{ ...params.data, Thumbs: newValue }] });
            }
        }
    ''')

    gb.configure_column('Thumbs', cellRenderer=thumbs_renderer, onCellClicked=button_handler, editable=False)
    gb.configure_column('Suggestions', wrapText=True, autoHeight=True)
    grid_options = gb.build()

    response = AgGrid(
        suggestions_df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        height=200,
        width='100%',
    )

    # Retrieve updated DataFrame after interaction
    updated_suggestions_df = pd.DataFrame(response['data'])

    # Feedback
    GeminiKeys = [
        "AIzaSyCcVUOyL2M9aNRUhgO6lzTAJ-BjOUXZrt0",
        "AIzaSyC9JxomOkNel9uy0qdqixDcI6UH6KhMcho"
    ]
    os.environ["GOOGLE_API_KEY"] = GeminiKeys[0]
    cmt = []
    for val in suggestions_df['Suggestions']:
        cmt.append(val)
    cmtnd = cmt[:10]
    prompt = TravelScore(cmtnd)
    response = responseFunc(prompt)
    llm_response = response.text
    st.success(llm_response)
