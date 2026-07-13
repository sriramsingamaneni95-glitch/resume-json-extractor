from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

with open("sample_resume.txt","r",encoding="utf-8") as f:
    resume = f.read()

prompt = f"""Extract the following resume into structured JSON.
Return only valid JSON.

Resume:
{resume}
"""

response = client.responses.create(
    model="gpt-4.1",
    input=prompt
)

print(response.output_text)
