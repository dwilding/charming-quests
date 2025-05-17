#!/usr/bin/env python3

from pathlib import Path
import json
import os

import requests


QUEST_DIR = Path(__file__).parent
OUT_DIR = QUEST_DIR / "out"


def main():
    doc = (OUT_DIR / "doc-original.md").read_text()
    instructions = generate_charm_instructions(doc)
    (OUT_DIR / "doc-generated.md").write_text(instructions)
    charm = generate_charm(instructions)
    (OUT_DIR / "src/charm.py").write_text(charm)


def generate_charm(instructions: str) -> str:
    charm = call_gpt(
        0.3,
        instructions,
        "The user will provide instructions that explain how to create a Python file called charm.py. Your task is to follow the instructions and return the contents of charm.py. You must provide Python code - please don't wrap your response in Markdown.",
    )
    return charm


def generate_charm_instructions(doc: str) -> str:
    instructions = call_gpt(
        0.3,
        doc,
        "The user will provide a software tutorial in MyST Markdown format. The tutorial explains how to create a Python file called charm.py, using a combination of code snippets and instructions that explain how to combine the code snippets. Your task is to extract a terse summary of how to construct the final version of charm.py (you don't need to actually construct it) using plain Markdown.",
    )
    return instructions


def call_gpt(temperature: float, user: str, system: str) -> str:
    request_body = {
        "model": "gpt-4.1-mini",
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    key = os.getenv("OPENAPI_KEY")
    if not key:
        raise RuntimeError("OPENAPI_KEY is not set")
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f"Bearer {key}",
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        data=json.dumps(request_body),
    )
    response_body = response.json()
    return response_body["choices"][0]["message"]["content"]


if __name__ == "__main__":
    main()
