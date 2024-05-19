import os
import time
import shutil
import zipfile
import getpass
import requests
import subprocess
from tqdm import tqdm

Logo = """
    \033[96m

 _______ _______        _______  ______  ______ _______ _______   ______  _______
    |    |______ |      |______ |  ____ |_____| |_____| |  |  |   |     | |______
    |    |______ |_____ |______ |_____| |    |_ |     | |  |  |   |____/| ______|
    
    \033[0m
    """

def clear():
    os.system("cls")
    print(Logo)

clear()

def OK(Text):
    print(f"\033[92m[OK!] - {Text}\033[97m")

def Info(message):
    print(f"\033[96m[Info] {message}\033[0m")

def Error(message):
    print(f"\033[31m[Error] {message}\033[0m")

def Enter(text):
    data = input(f"\033[96m{text}\033[97m")
    
    return data

try:
    username = getpass.getuser()
    standard_path_telegram = f"C:\\Users\\{username}\\AppData\\Roaming\\Telegram Desktop"

    Telegram_Url = "https://telegram.org/dl/desktop/win64_portable"
    download_path = os.path.join(os.path.expanduser("~"), "Desktop", "telegram_win64_portable.zip")

    script_dir = os.path.dirname(os.path.realpath(__file__))
    tdat_path = os.path.join(script_dir, "Telegram", "tdata")
    Telegram_portable = os.path.join(script_dir, "Telegram", "Telegram.exe")

    def create_session():
        global path_to_file
        
        clear()
        path_to_file = Enter("Enter path to Session file: ")
        
        if os.path.isfile(path_to_file) and path_to_file.endswith('.zip'):
            Info("ZIP file was found!")
        else:
            Error("ZIP file was not found!")
            Info("Click to try again!")
            os.system('pause')
            create_session()
        starting_session()

    def starting_session():
        Info("Starting...")
        with open(os.devnull, 'w') as devnull:
            os.system("taskkill /f /im Telegram.exe >nul 2>&1")
        
        Info("Telegram is closed")
        
        with zipfile.ZipFile(path_to_file, 'r') as zip_ref:
            file_count = len(zip_ref.infolist())

        with zipfile.ZipFile(path_to_file, 'r') as zip_ref:
            for file_info in tqdm(zip_ref.infolist(), total=file_count, desc="Extracting files"):
                file_name = file_info.filename
                zip_ref.extract(file_name, tdat_path)
        
        OK(f"Done!")
        subprocess.Popen(f"{Telegram_portable}")
        os.system('pause')
    
    def create_tdat():
        if not os.path.exists(tdat_path):
            os.makedirs(tdat_path)
            Info("Folder created successfully.")
        else:
            Info("Folder already exists.")

    def clear_tdat():
        os.system("taskkill /f /im Telegram.exe >nul 2>&1")
        time.sleep(2)
        Info("Please wait...")
        if os.path.exists(tdat_path):
            shutil.rmtree(tdat_path)
            Info("Folder deleted successfully.")
            OK("Done!")
            create_tdat()
        else:
            Error("Folder does not exist")
    
    def download():
        try:
            response = requests.get(Telegram_Url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(download_path, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))
            Info("Download completed!")

            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(script_dir)
            os.remove(download_path)
        
        except Exception as e:
            Error(f"An error occurred during download: {e}")

    def help():
        clear()
        print("\033[92mCommands:\n1. dataclear - clear tdata folder\n2. download - TG\n3. Tdata - Create Folder\n4. Session - create session\n5. cls or clear - clear console\033[97m")
    
    def check_command(command):
        if command == "dataclear" or command.lower() == "cleardata":
            clear_tdat()
        elif command == "download" or command == "Download":
            download()
        elif command == "tdata" or command == "Tdata":
            create_tdat()
        elif command == "session" or command == "Session":
            create_session()
        elif command == "clear" or command == "cls":
            clear()
        elif command == "help" or command == "Help":
            help()
        elif command == "":
            pass
        else:
            Error("Command not found!")
        
    while True:
        command = input(">>> ")
        check_command(command)

except PermissionError as e:
    Error(f"Permission denied: {e.filename}. Please make sure the file is not in use by another process.")
    os.system('pause')

except KeyboardInterrupt:
    Info("Exiting...")

except Exception as e:
    Error(e)
    os.system('pause')