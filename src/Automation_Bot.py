import os
import pandas
import requests

from dotenv import load_dotenv

load_dotenv()
base_url = 'https://api.telegram.org/bot' + os.getenv('TOKEN_BOT')
chat_id = os.getenv('CHAT_ID_BOT')
df = pandas.read_csv(os.getenv('SCRIPT_PATH_TSV'), sep='\t')


def read_message(offsets):
    parameter = {
        'offset': offsets
    }

    response = requests.get(base_url + '/getUpdates', data=parameter)
    data = response.json()
    print(data)

    for result in data['result']:
        # send_message(result['message']['text'])
        send_message_mention(result)

    if data['result']:
        return data['result'][-1]['update_id'] + 1


def send_answer(message):
    answer = df.loc[df['Question'].str.lower() == message.lower()]
    if not answer.empty:
        answer = answer.iloc[0]['Answer']
        return answer
    else:
        return 'Sorry I could not understand you'


def send_message(message):
    answer = send_answer(message)
    parameter = {'chat_id': chat_id, 'text': answer}
    response = requests.get(base_url + '/sendMessage', data=parameter)

    print(response.text)
    # print('Done!')


def send_message_mention(message):
    text = message['message']['text']
    message_id = message['message']['message_id']

    answer = send_answer(text)

    parameter = {'chat_id': chat_id, 'text': answer, 'reply_to_message_id': message_id}
    response = requests.get(base_url + '/sendMessage', data=parameter)

    print(response.text)
    # print('Done!')

if __name__ == '__main__':
    offset = 0
    while True:
        offset = read_message(offset)
