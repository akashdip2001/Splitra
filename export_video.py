import os
import json
import shutil

def find_video_folders():
    return [d for d in os.listdir('.') if os.path.isdir(d) and 'manifest.json' in os.listdir(d)]

def recombine(folder_name):
    manifest_path = os.path.join(folder_name, "manifest.json")
    with open(manifest_path, "r") as mf:
        manifest = json.load(mf)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, manifest['original_file'])

    total_chunks = len(manifest['chunks'])

    with open(output_file_path, 'wb') as out:
        for i, chunk_name in enumerate(manifest['chunks']):
            chunk_path = os.path.join(folder_name, chunk_name)
            with open(chunk_path, 'rb') as chunk_file:
                out.write(chunk_file.read())
            percent = round(((i + 1) / total_chunks) * 100, 2)
            print(f"[{percent}%] Recombining: {chunk_name}")

    print(f"\n✅ Video successfully rebuilt at: {output_file_path}")

    # Ask whether to delete folder
    user_input = input(f"Do you want to delete the folder '{folder_name}' with the split files? (y/n): ").strip().lower()
    if user_input == 'y':
        shutil.rmtree(folder_name)
        print(f"🗑️ Deleted folder: {folder_name}")
    else:
        print("📁 Split files kept for future use.")

def main():
    folders = find_video_folders()
    if not folders:
        print("No video folders with manifest.json found.")
        return

    print("Select a video folder to export:")
    for i, folder in enumerate(folders):
        print(f"{i + 1}. {folder}")

    choice = int(input("Enter number: ")) - 1
    selected_folder = folders[choice]

    recombine(selected_folder)

if __name__ == "__main__":
    main()
