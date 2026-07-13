# # Resume JSON Extractor

## Overview

This project reads a resume (`sample_resume.txt`) and converts it into structured JSON using the OpenAI GPT-4.1 model through Prompt Engineering.

## Files

- `app.py` – Main application script
- `prompt.txt` – Prompt instructions and JSON schema
- `sample_resume.txt` – Input resume file
- `output.json` – Generated structured JSON output
- `.env.example` – Sample environment variables
- `requirements.txt` – Project dependencies

## Setup

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file from `.env.example`.

3. Add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

4. Run the application:

```bash
python app.py
```

## Sample Output

The application extracts resume information such as:
- Name
- Email
- Phone Number
- Summary
- Skills
- Experience
- Education

and returns the data in a structured JSON format.

## Tech Stack

- Python
- OpenAI GPT-4.1 API
- Prompt Engineering
- JSON
- python-dotenv

## Author

**Sriram Singamaneni**
