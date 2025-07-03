#!/usr/bin/env python3
"""
Classify URLs Based on Tag Occurrences

This script:
1. Loads a CSV with tags per category.
2. Downloads and cleans HTML content from each URL.
3. Counts occurrences of tags in the content and URL.
4. Generates a CSV with classifications and detected tags.

How to use:
1. Adjust TAGS_CSV_PATH, INPUT_URLS_PATH, and OUTPUT_CSV_PATH below.
2. Run: python classify_urls_by_tags.py
"""

import os
import time
import csv
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib3

TAGS_CSV_PATH = "data/csv_output/url_classification/tags_dictionary.csv"
INPUT_URLS_PATH = "data/csv_output/url_classification/inputs_pre_tagging.csv"
OUTPUT_CSV_PATH = "data/csv_output/url_classification/categorized_tags.csv"

CATEGORIES = [
    "ALDR", "REL", "PORN", "PROV", "POLR", "HUMR", "ENV", "MILX", "HATE", "NEWS", "XED", "PUBH",
    "GMB", "ANON", "DATE", "GRP", "LGBT", "FILE", "HACK", "COMT", "MMED", "HOST", "SRCH", "GAME",
    "CULTR", "ECON", "GOVT", "COMM", "CTRL", "IGO", "MISC"
]
CATEGORIES = [h.lower() for h in CATEGORIES]


def remove_duplicate_urls(file_path):
    """
    Remove duplicate URLs from the input file.
    """
    df = pd.read_csv(file_path)
    df_clean = df.drop_duplicates(subset=["url"])
    df_clean.to_csv(file_path, index=False)
    print(f"Duplicates removed: {file_path}")


def fetch_html_text(url, retries=2, delay=5):
    """
    Download and clean text from a URL.
    """
    attempt = 0
    session = requests.Session()
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/123.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }
    session.headers.update(headers)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    while attempt < retries:
        try:
            response = session.get(url, timeout=30, verify=False)
            response.raise_for_status()
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup(["script", "style"]):
                element.extract()
            return " ".join(soup.get_text().split()).strip()
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Error fetching URL (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
    return ""


def load_tags(tags_csv_path):
    """
    Load tags per category from a CSV.
    """
    categories = {}
    with open(tags_csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            code = row[0].strip().lower()
            tags = [tag.strip().lower() for tag in row[1].split(",")]
            categories[code] = tags
    return categories


def classify_text_and_url(text, categories, url):
    """
    Count occurrences of each tag in text and URL.
    """
    results = {}
    detected_tags = []

    for category, tags in categories.items():
        for tag in tags:
            count_text = len(re.findall(rf"\b{re.escape(tag)}\b", text, re.IGNORECASE))
            count_url = len(re.findall(re.escape(tag), url, re.IGNORECASE))
            total = count_text + count_url

            if total > 0:
                results[category] = results.get(category, 0) + total
                detected_tags.append(tag)

    return results, detected_tags


def deduce_categories(counts):
    """
    Deduce main categories based on counts.
    """
    if not counts:
        return None

    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    max_value = sorted_items[0][1]
    top_categories = [k for k, v in sorted_items if v == max_value]

    if len(top_categories) >= 2:
        return top_categories

    if len(sorted_items) > 1:
        return [sorted_items[0][0], sorted_items[1][0]]
    return [sorted_items[0][0]]


def save_classification_row(output_path, url, counts, tags):
    """
    Append classification row to output CSV.
    """
    write_header = not os.path.exists(output_path)
    header = ["url", "detected_tags"] + CATEGORIES + ["deduction"]

    with open(output_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow(
            [url, tags]
            + [counts.get(cat, 0) for cat in CATEGORIES]
            + [deduce_categories(counts)]
        )


def main():
    tags = load_tags(TAGS_CSV_PATH)

    with open(INPUT_URLS_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        urls = [row[0] for row in reader]

    for url in urls:
        print(f"Processing URL: {url}")
        text = fetch_html_text(url)
        counts, detected_tags = classify_text_and_url(text, tags, url)
        save_classification_row(OUTPUT_CSV_PATH, url, counts, detected_tags)


if __name__ == "__main__":
    main()
