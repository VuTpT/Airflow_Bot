import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()
base_url = 'https://api.telegram.org/bot' + os.getenv('TOKEN_BOT')
chat_id_group = os.getenv('CHAT_ID_GROUP')

questions = ['1', '2', '3']
photos_url = [
    'https://unsplash.com/photos/a-person-walking-down-a-street-holding-an-umbrella-qwjsIoQ4nJY',
    'https://unsplash.com/photos/a-table-with-a-laptop-camera-and-other-items-on-it-vn84zYYtR3E'
]

image_path = os.getenv('PATH_TEMP_DIR') + '/image/1.jpg'
audio_path = os.getenv('PATH_TEMP_DIR') + '/image/1.jpg'
document_path = os.getenv('PATH_TEMP_DIR') + '/processed_user.csv'


def check_path(path):
    # Check if the file exists
    if os.path.isfile(image_path):
        return True
    else:
        return False


def ping_bot():
    ping_url = base_url + '/getUpdates'

    response = requests.get(ping_url)

    print(response.text)


def send_message(messages):
    send_url = base_url + '/sendMessage'

    for message in messages:
        parameter = {
            'chat_id': chat_id_group,
            'text': message
        }
        time.sleep(10)

        response = requests.get(send_url, data=parameter)

        print(response.text)  # Correct way to access the text of the response


def send_photo(photos, location, path):
    send_url = base_url + '/sendPhoto'

    if location == 'local':
        parameter = {
            'chat_id': chat_id_group,
            'caption': 'caption'
        }

        check = check_path(path)

        if check:
            with open(path, 'rb') as photo_local:
                # Do something with the photo
                files = {
                    'photo': photo_local
                }

                time.sleep(3)

                response = requests.get(send_url, data=parameter, files=files)

                print(response.text)  # Correct way to access the text of the response

        else:
            print(f"File not found: {image_path}")

    else:
        for photo in photos:
            parameter = {
                'chat_id': chat_id_group,
                'photo': photo,
                'caption': 'caption'
            }
            time.sleep(3)

            response = requests.get(send_url, data=parameter)

            print(response.text)  # Correct way to access the text of the response


def send_audio(audios, path):
    send_url = base_url + '/sendAudio'

    check = check_path(path)

    if check:
        with open(path, 'rb') as audio:
            # Do something with the photo
            parameter = {
                'chat_id': chat_id_group,
                'caption': 'caption'
            }

            files = {
                'audio': audio
            }

            time.sleep(3)

            response = requests.get(send_url, data=parameter, files=files)

            print(response.text)  # Correct way to access the text of the response

    else:
        print(f"File not found: {image_path}")


def send_document(documents, path, caption):
    send_url = base_url + '/sendDocument'

    check = check_path(path)

    if check:
        with open(path, 'rb') as document:
            # Do something with the photo
            parameter = {
                'chat_id': chat_id_group,
                'caption': caption
            }

            files = {
                'document': document
            }

            time.sleep(3)

            response = requests.get(send_url, data=parameter, files=files)

            print(response.text)  # Correct way to access the text of the response

    else:
        print(f"File not found: {image_path}")


if __name__ == '__main__':
    # send_message(questions)
    # send_photo(photos_url, 'web')
    # send_photo('', 'local', image_path
    # send_audio('', audio_path)
    send_document('', document_path, 'My document')
