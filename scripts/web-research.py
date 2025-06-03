# scripts/web-research.py
#
# Description:
# This script performs a DuckDuckGo search for a given query,
# then attempts to fetch each search result's webpage, extract the main
# article text (similar to a 'reader mode'), and finally outputs
# the findings in a YAML-like Markdown block format.
#
# Usage:
# python scripts/web-research.py "your search query here"
#
# Example:
# python scripts/web-research.py "latest advancements in AI" > output.md
#
# Dependencies:
# - duckduckgo_search
# - requests
# - newspaper3k
#
# Note: Error messages and progress are printed to stderr.
# The final Markdown output is printed to stdout.

import argparse
from duckduckgo_search import DDGS
from newspaper import Article
import requests
import sys

def format_for_yaml_block(text_content, base_indent="  "):
    """Formats text for YAML block scalar style, handling None or empty input."""
    if text_content is None:
        text_content = ""

    # Strip leading/trailing whitespace from the whole content first
    stripped_content = text_content.strip()

    if not stripped_content: # If content becomes empty after stripping
        return "|\n" + base_indent + "# No content" # Or just "|" if preferred for truly empty

    lines = stripped_content.split('\n')
    # Further strip each line to remove individual line leading/trailing spaces
    # and then apply indent. This handles cases where lines might have mixed spacing.
    formatted_lines = [base_indent + line.strip() for line in lines]
    return "|\n" + "\n".join(formatted_lines)

def main():
    parser = argparse.ArgumentParser(description="Perform a web search and extract content, then output as Markdown.")
    parser.add_argument("query", help="The search query to look up.")
    args = parser.parse_args()

    print(f"Search Query: {args.query}", file=sys.stderr)

    try:
        with DDGS() as ddgs:
            ddg_results = ddgs.text(keywords=args.query, max_results=5)
            if not ddg_results:
                print("No results found by DuckDuckGo.", file=sys.stderr)
                return
    except Exception as e:
        print(f"An error occurred during DuckDuckGo search: {e}", file=sys.stderr)
        return

    markdown_outputs = []
    if ddg_results:
        print("\nProcessing articles (errors and progress will be printed to stderr)...", file=sys.stderr)
        for i, result in enumerate(ddg_results):
            title = result.get('title') or 'No Title Provided'
            url = result.get('href')
            _snippet = result.get('body')

            snippet_for_format = _snippet.strip() if _snippet else "No snippet available."

            print(f"--- Processing Article {i+1}: {title} ---", file=sys.stderr)

            if not url:
                print(f"No URL found for '{title}', skipping.", file=sys.stderr)
                continue

            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                response = requests.get(url, timeout=10, headers=headers)
                response.raise_for_status()

                article = Article(url)
                article.download(input_html=response.text)
                article.parse()

                _extracted_text = article.text
                if not _extracted_text:
                    article.nlp()
                    _extracted_text = article.text

                text_for_format = _extracted_text.strip() if _extracted_text else "Could not extract text automatically."

                # Construct Markdown entry using YAML-like format
                markdown_entry = f"site: [{title}]({url})\n"
                markdown_entry += f"snippet: {format_for_yaml_block(snippet_for_format)}\n"
                markdown_entry += f"text: {format_for_yaml_block(text_for_format)}\n---"
                markdown_outputs.append(markdown_entry)
                print(f"Successfully processed and added: {title}", file=sys.stderr)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching URL {url}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"Error processing article {url} with newspaper3k: {e}", file=sys.stderr)

        if markdown_outputs:
            # Print final markdown to stdout, entries separated by double newline
            print("\n\n".join(markdown_outputs))
        else:
            print("No articles could be processed and formatted into Markdown.", file=sys.stderr)

if __name__ == "__main__":
    main()
