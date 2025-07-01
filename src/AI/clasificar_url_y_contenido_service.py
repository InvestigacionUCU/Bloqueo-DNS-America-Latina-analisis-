import os
import sys
import json
import typer
import requests
import openai
import csv
from bs4 import BeautifulSoup

app = typer.Typer()

def fetch_and_extract_text(url: str, max_length: int = 2000) -> str:
    try:
        print("Fetching URL...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        html = response.text
        
        print("Extracting text...")
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        print("Truncating text...")
        return text[:max_length] if len(text) > max_length else text
    except Exception as e:
        raise Exception(f"Error fetching or extracting text from URL: {e}")

def get_categories() -> list:
    print("Reading categories...")
    try:
        with open("categorias1.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            categories = [{"code": row["Code"], "name": row["Category"], "description": row["Description"].split(',')} for row in reader]
        return categories
    except Exception as e:
        raise Exception(f"Error reading categorias1.csv: {e}")

def get_tags() -> list:
    print("Reading tags...")
    try:
        with open("tags.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            tags = [{"code": row["code"], "tags": row["tags"].split(',')} for row in reader]
        return tags
    except Exception as e:
        raise Exception(f"Error reading tags.csv: {e}")


@app.command()
def main(
    url: str,
    max_length: int = typer.Option(2000, "--len", help="Maximum length of extracted text (in characters).")
):
    
    openai.api_key = "secret_key"  # Replace with your actual OpenAI API key

    functions = [
        {
            "name": "fetch",
            "description": "Fetches and extracts text content from a URL by removing HTML tags.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to fetch text content from"}
                },
                "required": ["url"]
            }
        },
        {
            "name": "get_categories",
            "description": "Provides a list of predefined categories from categorias1.csv.",
            "parameters": {"type": "object", "properties": {}}
        },
        {
            "name": "get_tags",
            "description": "Provides a list of predefined tags from tags.csv.",
            "parameters": {"type": "object", "properties": {}}
        }
    ]
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a classification assistant. Your task is to categorize webpages based on extracted text and URL structure. "
                "Follow these guidelines:\n"
                "1. Retrieve the full webpage text using the 'fetch' function.\n"
                "2. Use the **predefined list of categories** from 'get_categories'. Only assign categories that exist in this list (use their **codes**).\n"
                "3. Analyze the text and URL structure to determine the most relevant categories.\n"
                "4. **Do not create new categories** beyond those provided in 'get_categories'.\n"
                "5. If no relevant category is found, return an empty dictionary `{}`.\n"
                "6. Return the classification as a dictionary where keys are **category codes** and values are relevance scores.\n"
                "7. **Example output format:** `{'srch': 3, 'med': 1}`."
            )
        },
        {
            "role": "user",
            "content": f"Analyze the webpage at {url}. Extract text **fully and consistently**, then determine the most relevant categories based on 'get_categories'."
        }
    ]

    called_fetch = False
    called_get_categories = False
    called_get_tags = False
    max_iterations = 5
    iterations = 0

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    message = response.choices[0].message

    categories = get_categories()
    tags = get_tags()
    
    while iterations < max_iterations:
        iterations += 1

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            arguments_str = message["function_call"].get("arguments", "{}")

            try:
                arguments = json.loads(arguments_str)
            except json.JSONDecodeError:
                typer.echo("Failed to decode function call arguments.", err=True)
                return None  # No detener el programa, solo devolver None

            if function_name == "fetch":
                url_to_fetch = arguments.get("url")
                if not url_to_fetch:
                    typer.echo("No URL provided in function call arguments.", err=True)
                    return None

                typer.echo(f"Fetching and extracting text from: {url_to_fetch}")
                try:
                    result = fetch_and_extract_text(url_to_fetch, max_length=max_length)
                except Exception as e:
                    typer.echo(f"Error fetching URL: {e}", err=True)
                    return None
                called_fetch = True

            elif function_name == "get_categories" and not called_get_categories:
                typer.echo("Retrieving list of categories...")
                try:
                    categories = get_categories()
                except Exception as e:
                    typer.echo(f"Error retrieving categories: {e}", err=True)
                    return None
                result = json.dumps(categories)
                called_get_categories = True

            elif not called_get_tags:
                typer.echo("Retrieving list of tags...")
                try:
                    tags = get_tags()
                except Exception as e:
                    typer.echo(f"Error retrieving tags: {e}", err=True)
                    return None
                result = json.dumps(tags)
                called_get_tags = True

            else:
                typer.echo(f"Unexpected function call: {function_name}", err=True)
                return None

            messages.append(message)
            messages.append({"role": "function", "name": function_name, "content": result})

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )
            message = response.choices[0].message

        else:
            content_lower = message.get("content", "").lower()
            if ("get_categories" in content_lower or "categories" in content_lower) and not called_get_categories:
                typer.echo("Detected instruction to call get_categories. Simulating function call...")
                try:
                    categories = get_categories()
                except Exception as e:
                    typer.echo(f"Error retrieving categories: {e}", err=True)
                    raise typer.Exit(1)

                messages.append({
                    "role": "function",
                    "name": "get_categories",
                    "content": json.dumps(categories)
                })
                called_get_categories = True

                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                message = response.choices[0].message

            if ("get_tags" in content_lower or "tags" in content_lower) and not called_get_tags:
                typer.echo("Detected instruction to call get_tags. Simulating function call...")
                try:
                    tags = get_tags()
                except Exception as e:
                    typer.echo(f"Error retrieving tags: {e}", err=True)
                    raise typer.Exit(1)

                messages.append({
                    "role": "function",
                    "name": "get_tags",
                    "content": json.dumps(tags)
                })
                called_get_tags = True

                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                message = response.choices[0].message
            else:
                break

    typer.echo(message.get("content", "No content received."))

if __name__ == "__main__":
    app()