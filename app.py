import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

RESUME_FILE = "sample_resume.txt"

SCHEMA_INSTRUCTIONS = """Extract the following resume into structured JSON with this exact shape:

{
  "name": string,
  "email": string,
  "phone": string,
  "summary": string,
  "skills": [string],
  "experience": [
    {
      "title": string,
      "company": string,
      "start_date": string,
      "end_date": string,
      "description": string
    }
  ],
  "education": [
    {
      "degree": string,
      "institution": string,
      "year": string
    }
  ]
}

Return ONLY valid JSON. No markdown fences, no explanations, no extra text.
If a field is missing in the resume, use an empty string or empty list as appropriate.
"""


def read_resume(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            raise ValueError(f"'{path}' is empty.")
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find resume file at '{path}'.")


def extract_resume_json(resume_text: str) -> dict:
    prompt = f"{SCHEMA_INSTRUCTIONS}\n\nResume:\n{resume_text}"

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
        resume_text = read_resume(RESUME_FILE)
        structured_data = extract_resume_json(resume_text)

        print(json.dumps(structured_data, indent=2, ensure_ascii=False))

        # Optional: save to a JSON file
        output_path = "resume_structured.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(structured_data, f, indent=2, ensure_ascii=False)
        print(f"\nSaved structured data to '{output_path}'")

    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
