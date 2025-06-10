#!/usr/bin/env python3

import os
import sys
import json
import subprocess

def install_dependencies():
    try:
        from colorama import init
        from termcolor import colored
        import pyfiglet
        from tqdm import tqdm
        return True
    except ImportError:
        import urllib.request
        try:
            urllib.request.urlopen('https://pypi.org', timeout=3)
            subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "pyfiglet", "termcolor", "tqdm"])
            return True
        except Exception:
            print("No internet connection. Running in basic mode without colors.")
            return False

has_colors = install_dependencies()

if has_colors:
    from colorama import init, Fore, Style
    from termcolor import colored
    import pyfiglet
    from tqdm import tqdm
    init(autoreset=True)
else:
    Fore = type("Fore", (), {"GREEN": "", "YELLOW": "", "RED": "", "CYAN": ""})()
    Style = type("Style", (), {"BRIGHT": "", "RESET_ALL": ""})()
    def colored(text, *args, **kwargs): return text
    def tqdm(x, **kwargs): return x
    class pyfiglet:
        @staticmethod
        def figlet_format(text): return text

def print_banner():
    banner = pyfiglet.figlet_format("Splitra")
    print(colored(banner, "cyan"))
    print(colored("Created by Akashdip Mahapatra".center(80, " "), "yellow"))
    print("-" * 80)

def list_videos():
    return [f for f in os.listdir('.') if f.lower().endswith(('.mp4', '.avi', '.mkv'))]

def split_file(filename, chunk_size_mb):
    chunk_size = int(chunk_size_mb * 1024 * 1024)
    folder_name = os.path.splitext(filename)[0]
    os.makedirs(folder_name, exist_ok=True)
    part_files = []

    with open(filename, 'rb') as f:
        part_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_filename = os.path.join(folder_name, f'part_{part_num:05d}')
            with open(part_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
            part_files.append(f'part_{part_num:05d}')
            part_num += 1

    with open(os.path.join(folder_name, 'header.json'), 'w') as header:
        json.dump({'original_filename': filename, 'parts': part_files}, header, indent=4)

    with open(os.path.join(folder_name, 'export_video.py'), 'w') as export_script:
        export_script.write(f"""import os
import json

def recombine():
    with open("header.json", "r") as f:
        data = json.load(f)
    with open("output_" + data['original_filename'], "wb") as outfile:
        for part in data['parts']:
            with open(part, "rb") as infile:
                outfile.write(infile.read())
    print("Video recombined successfully as output_" + data['original_filename'])

if __name__ == "__main__":
    recombine()
""")

    print(Fore.GREEN + f"Video successfully split into folder: {folder_name}")
    print(Fore.YELLOW + f"Use '{folder_name}/export_video.py' to recombine without this tool.")

def recombine_video():
    folders = [d for d in os.listdir('.') if os.path.isdir(d) and 'header.json' in os.listdir(d)]
    if not folders:
        print("No valid chunk folders found.")
        return

    print("Select folder to export video from:")
    for i, f in enumerate(folders):
        print(f"{i + 1}. {Fore.CYAN + Style.BRIGHT}{f}{Style.RESET_ALL}")

    while True:
        try:
            choice = int(input("Enter number: ")) - 1
            if 0 <= choice < len(folders):
                break
            else:
                print(f"Please enter a number between 1 and {len(folders)}.")
        except ValueError:
            print("Please enter a valid number.")

    folder = folders[choice]
    with open(os.path.join(folder, 'header.json'), 'r') as f:
        data = json.load(f)

    output_path = os.path.join('output_' + data['original_filename'])

    with open(output_path, 'wb') as outfile:
        for part in tqdm(data['parts'], desc="Recombining"):
            part_path = os.path.join(folder, part)
            with open(part_path, 'rb') as infile:
                outfile.write(infile.read())

    print(Fore.GREEN + f"Video exported successfully to {output_path}")

    delete = input("Do you want to delete the chunk files? (y/N): ").strip().lower()
    if delete == 'y':
        for part in data['parts']:
            os.remove(os.path.join(folder, part))
        os.remove(os.path.join(folder, 'header.json'))

        export_script = os.path.join(folder, 'export_video.py')
        if os.path.exists(export_script):
            os.remove(export_script)

        if not os.listdir(folder):
            os.rmdir(folder)
            print(Fore.RED + f"Chunk folder '{folder}' removed.")
        else:
            print(Fore.YELLOW + f"Folder '{folder}' not empty, manual check recommended.")
        print(Fore.GREEN + "Chunk files deleted successfully.")

def main():
    print_banner()
    print("What would you like to do?")
    print("1. Split a video")
    print("2. Export a video from chunks")

    while True:
        choice = input("Enter choice (1/2): ").strip()
        if choice == '1':
            videos = list_videos()
            if not videos:
                print("No video files found.")
                return
            print("Select a video to split:")
            for i, v in enumerate(videos):
                print(f"{i + 1}. {Fore.CYAN + Style.BRIGHT}{v}{Style.RESET_ALL}")
            while True:
                try:
                    v_choice = int(input("Enter number: ")) - 1
                    if 0 <= v_choice < len(videos):
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(videos)}.")
                except ValueError:
                    print("Please enter a valid number.")
            selected_video = videos[v_choice]
            while True:
                try:
                    size = float(input("Enter chunk size in MB (e.g. 25): "))
                    if size > 0:
                        break
                    else:
                        print("Size must be greater than 0.")
                except ValueError:
                    print("Please enter a valid number.")
            split_file(selected_video, size)
            break
        elif choice == '2':
            recombine_video()
            break
        else:
            print("Please enter 1 or 2.")

    if has_colors:
        cleanup = input("Do you want to remove installed libraries (to save space)? (y/N): ").strip().lower()
        if cleanup == 'y':
            os.system(f"{sys.executable} -m pip uninstall -y colorama pyfiglet termcolor tqdm")
            print("Dependencies removed.")

if __name__ == "__main__":
    main()
