import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

RESUME_FILE = "sample_resume.txt"
PROMPT_FILE = "prompt.txt"
OUTPUT_FILE = "output.json"


def read_text_file(path: str, label: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            raise ValueError(f"'{path}' ({label}) is empty.")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find {label} file at '{path}'.")


def extract_resume_json(resume_text: str, schema_prompt: str) -> dict:
    prompt = f"{schema_prompt}\n\nResume:\n{resume_text}"

    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=prompt,
            # Enforces the model to return a JSON object (no stray text/markdown)
            text={"format": {"type": "json_object"}},
        )
    except Exception as e:
        raise RuntimeError(f"OpenAI API call failed: {e}")

    raw_output = response.output_text.strip()

    # Defensive cleanup in case the model still wraps output in ```json fences
    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.lower().startswith("json"):
            raw_output = raw_output[4:].strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model did not return valid JSON.\nError: {e}\nRaw output:\n{raw_output}"
        )


def main():
    try:
        resume_text = read_text_file(RESUME_FILE, "resume")
        schema_prompt = read_text_file(PROMPT_FILE, "prompt")

        structured_data = extract_resume_json(resume_text, schema_prompt)

        print(json.dumps(structured_data, indent=2, ensure_ascii=False))

        Path(OUTPUT_FILE).write_text(
            json.dumps(structured_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"\nSaved structured data to '{OUTPUT_FILE}'")

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
