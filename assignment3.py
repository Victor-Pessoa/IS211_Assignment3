import argparse
import urllib.request
import csv
import re


def main(url):
    print(f"Downloading log file from URL = {url}...")
    filename = "web_log.txt"
    urllib.request.urlretrieve(url, filename)
    print(f"Log file saved as {filename}.")

    browser_counts = {"Firefox": 0, "Chrome": 0, "Internet Explorer": 0, "Safari": 0}
    with open(filename, "r") as logfile:
        reader = csv.reader(logfile)
        headers = next(reader)  # skip the first line (headers)
        image_count = 0
        total_count = 0
        for row in reader:
            total_count += 1
            path, datetime, browser, status, size = row
            if re.search(r"\.(jpg|gif|png)$", path, re.IGNORECASE):
                image_count += 1

            if re.search(r"Firefox", browser, re.IGNORECASE):
                browser_counts["Firefox"] += 1
            elif re.search(r"Chrome", browser, re.IGNORECASE):
                browser_counts["Chrome"] += 1
            elif re.search(r"MSIE|Trident", browser, re.IGNORECASE):
                browser_counts["Internet Explorer"] += 1
            elif re.search(r"Safari", browser, re.IGNORECASE):
                browser_counts["Safari"] += 1

        image_percent = (image_count / total_count) * 100
        print(f"Image requests account for {image_percent:.1f}% of all requests.")

        most_popular = max(browser_counts, key=browser_counts.get)
        print(f"The most popular browser is {most_popular}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the log file", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
