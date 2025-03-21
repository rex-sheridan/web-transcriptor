#!/usr/bin/env python3
import sys
import argparse
import webvtt
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

# Import deepmultilingualpunctuation only for full processing.
try:
    from deepmultilingualpunctuation import PunctuationModel
except ImportError:
    PunctuationModel = None

def convert_vtt_to_html_minimal(vtt_file, html_file):
    """
    Minimal processing: Output each caption as-is, with its timestamp and text.
    """
    captions = list(webvtt.read(vtt_file))
    
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
    
    for caption in captions:
        text = caption.text.strip()
        if text:
            html.append("  <div class='caption'>")
            html.append(f"    <div class='timestamp'>{caption.start} — {caption.end}</div>")
            html.append(f"    <p class='text'>{text}</p>")
            html.append("  </div>")
    
    html.append("</body>")
    html.append("</html>")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(html))
    print(f"HTML transcript saved to {html_file}")

def merge_captions_global(captions, min_overlap_words=3):
    """
    Merge consecutive captions by removing overlapping text.
    Returns a list of segments as tuples: (start, end, merged_text).
    """
    if not captions:
        return []
    
    current_start = captions[0].start
    current_end = captions[0].end
    current_text = captions[0].text.strip()
    merged_segments = []
    
    for caption in captions[1:]:
        curr_text = caption.text.strip()
        if not curr_text:
            continue
        
        curr_words = curr_text.split()
        overlap_found = 0
        # Look for the longest prefix (with at least min_overlap_words) of curr_text that appears in current_text.
        for i in range(len(curr_words), min_overlap_words - 1, -1):
            prefix = " ".join(curr_words[:i])
            if prefix in current_text:
                overlap_found = i
                break
        
        if overlap_found >= min_overlap_words:
            non_overlap = " ".join(curr_words[overlap_found:])
            if non_overlap:
                current_text += " " + non_overlap
            current_end = caption.end
        else:
            merged_segments.append((current_start, current_end, current_text))
            current_start = caption.start
            current_end = caption.end
            current_text = curr_text

    merged_segments.append((current_start, current_end, current_text))
    return merged_segments

def refine_segments(segments, min_words=3):
    """
    Merge segments whose text is very short (fewer than min_words) with the previous segment.
    """
    refined = []
    for seg in segments:
        if refined and len(seg[2].split()) < min_words:
            prev_start, prev_end, prev_text = refined.pop()
            merged_text = prev_text + " " + seg[2]
            refined.append((prev_start, seg[1], merged_text.strip()))
        else:
            refined.append(seg)
    return refined

def convert_vtt_to_html_full(vtt_file, html_file):
    """
    Full processing: Merge overlapping captions, refine segments,
    and restore punctuation using deepmultilingualpunctuation.
    """
    if PunctuationModel is None:
        sys.exit("Error: deepmultilingualpunctuation is not installed. Please run 'pip install deepmultilingualpunctuation'.")
    
    captions = list(webvtt.read(vtt_file))
    segments = merge_captions_global(captions, min_overlap_words=3)
    segments = refine_segments(segments, min_words=3)
    
    # Initialize the punctuation restoration model.
    model = PunctuationModel()
    
    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "  <meta charset='utf-8'>",
        "  <title>Transcript</title>",
        "  <style>",
        "    body { font-family: sans-serif; padding: 20px; line-height: 1.5; }",
        "    .segment { margin-bottom: 1em; }",
        "    .timestamp { color: #555; font-size: 0.9em; }",
        "    .text { margin: 0.2em 0 0 0; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>Transcript</h1>"
    ]
    
    for start, end, text in segments:
        if text.strip():
            # Restore punctuation and capitalization.
            text_with_punctuation = model.restore_punctuation(text)
            html.append("  <div class='segment'>")
            html.append(f"    <div class='timestamp'>{start} — {end}</div>")
            html.append(f"    <p class='text'>{text_with_punctuation}</p>")
            html.append("  </div>")
    
    html.append("</body>")
    html.append("</html>")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(html))
    print(f"HTML transcript saved to {html_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Convert a WEBVTT transcript file into a nicely formatted HTML transcript."
    )
    parser.add_argument("input", help="Input WEBVTT file")
    parser.add_argument("output", help="Output HTML file")
    parser.add_argument(
        "--mode",
        choices=["minimal", "full"],
        default="full",
        help="Processing mode: 'minimal' (no merging/punctuation) or 'full' (advanced processing). Default is full."
    )
    args = parser.parse_args()
    
    if args.mode == "minimal":
        convert_vtt_to_html_minimal(args.input, args.output)
    else:
        convert_vtt_to_html_full(args.input, args.output)

if __name__ == "__main__":
    main()
