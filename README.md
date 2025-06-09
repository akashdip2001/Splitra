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

## 📘 README Template for GitHub

Here’s a ready-to-copy `README.md` for your GitHub repo:

---

### 🛠️ Usage

#### ✅ Split a video

```bash
python split_video.py
```

#### ♻️ Rebuild a video

```bash
python recombine_video.py
```

---

## 🧩 File Structure

```
├── split_video.py
├── recombine_video.py
├── MyVideo.mp4
├── MyVideo/
│   ├── chunk_000
│   ├── chunk_001
│   └── manifest.json
└── output/
    └── MyVideo.mp4
```
