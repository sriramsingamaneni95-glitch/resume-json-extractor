
import argparse
import json
from pathlib import Path
from dotenv import load_dotenv

from orchestrator import run_pipeline
from feedback import record_correction
from tools.pdf_parser import parse_pdf

load_dotenv()
OUTPUT_FILE = "output.json"


def read_resume(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Could not find resume file at '{path}'.")
    if p.suffix.lower() == ".pdf":
        content = parse_pdf(str(p))
    elif p.suffix.lower() in {".txt", ".md"}:
        content = p.read_text(encoding="utf-8").strip()
    else:
        raise ValueError("Unsupported resume format. Use .txt, .md, or .pdf")
    if not content.strip():
        raise ValueError("Resume is empty or no extractable text was found.")
    return content.strip()


def read_optional_text(path: str | None) -> str | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Could not find job description at '{path}'.")
    return p.read_text(encoding="utf-8").strip() or None


def run_human_feedback_loop(result: dict, resume_name: str):
    fields = result["low_confidence_fields"]
    if not fields:
        return
    print(f"\n⚠️ Low-confidence fields need review: {fields}")
    for field_name in fields:
        current_val = result["data"].get(field_name)
        answer = input(f"  Is '{field_name}' = {current_val!r} correct? (y/n/skip): ").strip().lower()
        if answer == "n":
            corrected = input(f"  Enter corrected value for {field_name}: ").strip()
            record_correction(resume_name, field_name, current_val, corrected)
            print("  ✅ Correction saved.")


def main():
    parser = argparse.ArgumentParser(description="Agentic Resume JSON Extractor")
    parser.add_argument("resume", nargs="?", default="sample_resume.txt", help="Path to .txt/.md/.pdf resume")
    parser.add_argument("--jd", help="Optional job-description text file")
    parser.add_argument("--output", default=OUTPUT_FILE, help="Output JSON path")
    args = parser.parse_args()
    try:
        resume_text = read_resume(args.resume)
        jd_text = read_optional_text(args.jd)
        result = run_pipeline(resume_text, resume_name=Path(args.resume).name, jd_text=jd_text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nSaved result to '{args.output}'")
        print(f"Agent path taken: {' -> '.join(result['agent_trace'])}")
        run_human_feedback_loop(result, Path(args.resume).name)
    except (FileNotFoundError, ValueError, RuntimeError, ImportError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
