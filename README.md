# web-transcriptor

web-transcriptor is a simple command-line tool that converts WEBVTT files (captions/subtitles) into a nicely formatted HTML transcript. This lightweight utility is perfect for creating web-friendly transcript pages from VTT files obtained from YouTube or other video platforms.

## Features

- **WEBVTT to HTML Conversion:** Transforms timestamped caption data into structured HTML.
- **Easy to Use:** Run from the command line with minimal dependencies.
- **Customizable Output:** Modify the HTML and CSS in the script to match your style.

## Requirements

- Python 3.6 or higher
- [webvtt-py](https://pypi.org/project/webvtt-py/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/web-transcriptor.git
   cd web-transcriptor
   ```

2. **Install Dependencies:**

Use pip to install the required Python package:

   ```bash
   pip install webvtt-py deepmultilingualpunctuation
   ```

## Usage

To convert a WEBVTT file to an HTML transcript, simply run the script with the input VTT file and the desired output HTML file:

```bash
./web_transcriptor.py input.vtt output.html
```

Alternatively, you can run:

```bash
python web_transcriptor.py input.vtt output.html
```

After execution, you'll find an HTML file with the formatted transcript in your specified location.

## Obtaining WEBVTT Files with yt-dlp

If you haven't yet downloaded the WEBVTT file from a YouTube video, you can use yt-dlp. For example, to download auto-generated English subtitles, run:

```
yt-dlp --skip-download --write-auto-sub --sub-lang en "https://youtu.be/wIWtp0KZa3c?si=9bMSt1W_tEV4kzhd"
```

This command downloads the auto-generated subtitles in WEBVTT format without downloading the video itself.

## License

This project is licensed under the MIT License.
