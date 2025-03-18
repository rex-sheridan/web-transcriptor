#!/usr/bin/env python3
import sys
import webvtt

def convert_vtt_to_html(vtt_file, html_file):
    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "  <meta charset='utf-8'>",
        "  <title>Transcript</title>",
        "  <style>",
        "    body { font-family: sans-serif; padding: 20px; line-height: 1.5; }",
        "    .caption { margin-bottom: 1em; }",
        "    .timestamp { color: #555; font-size: 0.9em; }",
        "    .text { margin: 0.2em 0 0 0; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>Transcript</h1>"
    ]

    for caption in webvtt.read(vtt_file):
        html.append("  <div class='caption'>")
        html.append(f"    <div class='timestamp'>{caption.start} — {caption.end}</div>")
        # caption.text might include some inline HTML-like tags, so we wrap it in a paragraph.
        html.append(f"    <p class='text'>{caption.text}</p>")
        html.append("  </div>")

    html.append("</body>")
    html.append("</html>")

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(html))
    print(f"HTML transcript saved to {html_file}")

def main():
    if len(sys.argv) < 3:
        print("Usage: {} input.vtt output.html".format(sys.argv[0]))
        sys.exit(1)
    vtt_file = sys.argv[1]
    html_file = sys.argv[2]
    convert_vtt_to_html(vtt_file, html_file)

if __name__ == "__main__":
    main()
