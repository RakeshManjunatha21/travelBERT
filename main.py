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


# Set your GitHub credentials and repository information
GITHUB_TOKEN = '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'
GITHUB_USERNAME = 'RakeshManjunatha21'
GITHUB_REPO = 'travelBERT'  # Just the repository name, not the full URL
GITHUB_FILE_PATH = 'updated_list.csv'  # The file path within the repository, pointing to the raw content

# Function to read the CSV file from GitHub
def read_csv_from_github():
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()['content'])
        return pd.read_csv(io.StringIO(content.decode('utf-8')))  # Updated import statement
    else:
        st.error(f"Error reading file: {response.status_code}")
        return pd.DataFrame(columns=["Questions", "Suggestions"])

# Function to write the CSV file to GitHub
def write_csv_to_github(df):
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_FILE_PATH}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()['sha']
        content = base64.b64encode(df.to_csv(index=False).encode('utf-8')).decode('utf-8')
        data = {
            'message': 'Updating updated_list.csv',
            'content': content,
            'sha': sha
        }
        response = requests.put(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            st.success('Database Updated...')
        else:
            st.error(f"Error updating file: {response.status_code}")
    else:
        st.error(f"Error reading file: {response.status_code}")

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

# Load the existing DataFrame from a CSV file or create a new one
try:
    df = read_csv_from_github()
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
        
        # Save the updated DataFrame to a CSV file
        # df.to_csv("updated_list.csv", index=False)
        write_csv_to_github(df)
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
