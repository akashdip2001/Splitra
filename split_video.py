import os
import json
import sys

def list_videos():
    return [f for f in os.listdir('.') if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]

def split_file(video_file, chunk_size_mb):
    chunk_size = int(chunk_size_mb * 1024 * 1024)
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    out_dir = os.path.join(os.getcwd(), video_name)

    os.makedirs(out_dir, exist_ok=True)

    chunks = []
    file_number = 0
    file_size = os.path.getsize(video_file)

    with open(video_file, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunk_name = f"chunk_{file_number:03d}"
            chunk_path = os.path.join(out_dir, chunk_name)
            with open(chunk_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunks.append(chunk_name)
            file_number += 1
            percent = round((f.tell() / file_size) * 100, 2)
            print(f"[{percent}%] Split: {chunk_name}")

    manifest = {
        "original_file": os.path.basename(video_file),
        "chunk_count": file_number,
        "chunks": chunks
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as mf:
        json.dump(manifest, mf)

    print(f"\n✅ Splitting completed. {file_number} chunks saved in folder: {video_name}/")

def main():
    videos = list_videos()
    if not videos:
        print("No video files found in current directory.")
        return

    print("Select a video to split:")
    for i, v in enumerate(videos):
        print(f"{i + 1}. {v}")

    while True:
        try:
            choice = int(input("Enter number: ")) - 1
            if 0 <= choice < len(videos):
                break
            else:
                print(f"Please enter a number between 1 and {len(videos)}.")
        except ValueError:
            print("Please enter a valid number.")

    selected_video = videos[choice]

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

if __name__ == "__main__":
    main()
