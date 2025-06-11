# Splitra

> **Splitra** is a simple Python-based command-line tool to split large video files into smaller parts (e.g. 25 MB chunks) and later reconstruct them using a header file. This is ideal for uploading large videos to platforms like GitHub which have individual file size limits.

<img src="img/img (1).png">

---

## 📃 Project Description

> `Splitra` is a command-line Python tool that allows users to split large video files into smaller chunks (e.g. 25MB parts), store them separately (ideal for GitHub uploads), and later rebuild the full-quality original video. The tool automatically generates a header (`manifest.json`) to track and reassemble chunks. This is especially useful when your platform (like GitHub) has a strict file size limit.

---

---

## 🧠 Project Concept

GitHub limits individual file uploads to 25 MB. Large video files (used in media projects, portfolios, or educational demos) often exceed this limit. To address this:

1. `Splitra` lets users:

   * Choose a video from the current directory
   * Specify the split size (default or custom)
   * Automatically splits the file into sequential chunks
   * Stores them in a dedicated folder with a `manifest.json` header.

2. The `export` script:

   * Lists available video folders
   * Reconstructs the full video using the `manifest.json`
   * Asks the user whether to delete the split files afterward
   * Exports the rebuilt file to an `output/` folder

---

## 📁 File Structure

```
Splitra/
├── split_video.py           # Script to split videos
├── recombine_video.py       # Script to export/recombine videos
├── MyVideo.mp4              # (example original video)
├── MyVideo/                 # (auto-generated split folder)
│   ├── chunk_000
│   ├── chunk_001
│   └── manifest.json
├── output/
│   └── MyVideo.mp4          # Final recombined video
└── README.md
```

---

## 🖼️ System Architecture Diagram

```
+-------------------+
| User Video Folder |
+-------------------+
         |
         v
+-------------------------+
| split_video.py (Script) |
+-------------------------+
         |
         v
+-------------------------------+
| Create folder: MyVideo/      |
| Create chunk_000, chunk_001  |
| Create manifest.json         |
+-------------------------------+
         |
         v
+-------------------------+
| Upload to GitHub safely |
+-------------------------+

(Recombine Step)
         |
         v
+--------------------------+
| recombine_video.py       |
+--------------------------+
         |
         v
+-----------------------------+
| Read manifest.json          |
| Combine chunks              |
| Export full video to /output|
+-----------------------------+
         |
         v
+--------------------------+
| Ask: Delete split files? |
+--------------------------+
```

---

## 🐍 Full Source Code

✅ Already included above. You'll copy both `split_video.py` and `recombine_video.py` into your GitHub repo.

---

## 🧪 Example Usage

<img src="img/img (2).png">

### 1. Split a video:

```bash
python split_video.py
```

* Select the video from the list
* Enter chunk size (e.g., 25 MB)
* Outputs: `MyVideo/` folder with split files and `manifest.json`

---

<img src="img/img (3).png">

### 2. Recombine the video:

```bash
python export_video.py
```

* Select folder to export
* Rebuilds video into `output/`
* Optionally deletes the split folder after success

---

## 🎯 project demonstration

https://github.com/user-attachments/assets/b992d648-f023-4c1a-8933-595769b5c66c

---

</br>
</br>

<div style="display: flex; align-items: center; gap: 10px;" align="center">
  
# ⭐ split_video.py ⭐
</div>

</br>
</br>

```python
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
```
</br>
</br>

<div style="display: flex; align-items: center; gap: 10px;" align="center">
  
# ⭐ export_video.py ⭐
</div>

</br>
</br>

```python
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
```

## 🟢 combine this two script into one [`splitra.py`](https://github.com/akashdip2001/Splitra/blob/main/splitra.py)

---

## 🎯 Need Future Upgrade

- If user want - add passward when Increft & pass must requird to Export.
- add a Output folder for Output videos.
- Fix error handaling.
