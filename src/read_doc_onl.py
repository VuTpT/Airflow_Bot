import os
import pandas as pd
import requests
import time
from dotenv import load_dotenv

load_dotenv()
base_url = 'https://api.telegram.org/bot' + os.getenv('TOKEN_BOT')
chat_id = os.getenv('CHAT_ID_BOT')  # Move this to a variable for easier adjustment

def read_doc():
    try:
        # Get the Google Sheets document ID from environment variable
        sheet_id = os.getenv('TOKEN_DOC')
        if not sheet_id:
            raise ValueError("TOKEN_DOC environment variable is not set.")

        # Construct URL to fetch data from Google Sheets
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

        # Fetch data from Google Sheets
        df = pd.read_csv(url)

        if df.empty:
            print("DataFrame is empty. Check the Google Sheets document for data.")
            return pd.DataFrame()  # Return an empty DataFrame on no data

        # Convert 'time' column to datetime with UTC timezone awareness
        df['time'] = pd.to_datetime(df['time'], utc=True)

        # Calculate current time and previous minute time in UTC
        current_time = pd.Timestamp.now(tz='UTC')
        previous_minute = current_time - pd.Timedelta(minutes=1)

        # Log current and previous minute times
        # print(f"Current time: {current_time}")
        # print(f"Previous minute: {previous_minute}")

        # Filter DataFrame based on time window
        df_filtered = df[(df['time'] > previous_minute) & (df['time'] <= current_time)]
        # print("Filtered DataFrame:")
        # print(df_filtered['message'])

        return df_filtered

    except Exception as e:
        print(f"Error fetching or processing data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error


def send_message(text):
    parameters = {'chat_id': chat_id, 'text': text}
    try:
        response = requests.get(base_url + '/sendMessage', params=parameters)
        response.raise_for_status()
        # print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")


def process_messages(df):
    # print("Received DataFrame:")
    # print(df)

    # Filter non-empty messages
    df_filtered = df[df['message'].str.strip().astype(bool)]
    # print("Filtered messages to send:")
    # print(df_filtered)

    if not df_filtered.empty:
        # Iterate over each row and send the message
        for index, row in df_filtered.iterrows():
            send_message(row['message'])
    else:
        print("No new messages to send")


if __name__ == '__main__':
    while True:
        df = read_doc()
        process_messages(df)
        time.sleep(60)
