# Resume JSON Extractor
Reads a resume (sample_resume.txt) and converts it to structured JSON using an LLM (OpenAI gpt-4.1).
Files
	•	app.py — main script
	•	prompt.txt — extraction instructions / JSON schema sent to the model
	•	sample_resume.txt — input resume (plain text)
	•	output.json — generated output (overwritten each run)
	•	.env.example — template for your API key
	•	requirements.txt — Python dependencies
Setup
	1.	pip install -r requirements.txt
	2.	Copy .env.example to .env and add your key:
  cp .env.example .env
  Then edit .env and set OPENAI_API_KEY=<your-key>.
 python app.py
