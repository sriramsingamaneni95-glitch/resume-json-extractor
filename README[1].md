# Resume JSON Extractor — Agentic AI Edition (v2: real dynamic agents)

## What changed from v1
Reviewer feedback: the pipeline looked agentic but was actually a fixed
sequential chain, tools were called manually in Python (not by the model),
and there was no real routing, parallelism, or feedback loop. This version
fixes all of that:

| Gap flagged | Fix |
|---|---|
| Fixed pipeline, no real routing | `agent_graph.py` — custom state machine; routing decisions are made at runtime based on `AgentState` (see routers in `orchestrator.py`) |
| Tools called manually, not by the model | `agents/extraction_agent.py` now uses OpenAI's native `tools=[...]` function-calling API — the model decides when to call `validate_email`/`parse_date`/`normalize_skill` |
| No stateful graph | `AgentGraph` + `AgentState` dataclass carries all shared state between nodes |
| No parallel execution | `node_score` in `orchestrator.py` runs intelligence/ATS/JD-match concurrently via `ThreadPoolExecutor` |
| Memory was just JSON history | `semantic_memory.py` is now integrated into the graph: similar resumes are retrieved before planning and successful runs are stored afterward |
| No human feedback loop | `feedback.py` — corrections a human makes are persisted AND immediately teach `knowledge_base.py` (`teach_entity`), so future runs benefit |

## Actual dynamic routing (not just a diagram — this really branches)

```
retrieve_memory ──► plan ──(messy/OCR-like?)──► clean_text ──► extract
  │
  └──(clean text)─────────────────────► extract
                                            │
                                   (malformed JSON, <3 tries)
                                            │◄────┐
                                            ▼     │ retry
                                         reflect ──┘ (on error, loops back)
                                            │
                                        validate
                                            │
                              (any field confidence < 0.7?)
                              ┌─────yes─────┴─────no──────┐
                              ▼                            ▼
                   targeted_verification                 score
                              │                            │
                              └──────────► score ◄─────────┘
                                            │  (intelligence + ATS + JD-match
                                            │   run IN PARALLEL here)
                                            ▼
                                          memory
                                            │
                                           END
```

Every run prints `agent_trace` — the actual list of nodes visited for that
specific resume. Two different resumes can take two different paths.

## Files (new/changed in v2)
- `agent_graph.py` – the state-machine engine (nodes + conditional routers)
- `orchestrator.py` – builds the graph, defines every routing decision
- `agents/extraction_agent.py` – rewritten to use real OpenAI function/tool calling
- `agents/verification_agent.py` – **new**: targeted re-check, only for low-confidence fields
- `semantic_memory.py` – **new**: embedding-based similarity search over past resumes
- `feedback.py` – **new**: human corrections persist and update the knowledge base
- `knowledge_base.py` – now file-backed (`knowledge_base_store.json`) so feedback can teach it permanently
- `tests/test_agent_graph.py` – **new**: tests the routing logic itself

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env        # add your OPENAI_API_KEY
python app.py path/to/resume.pdf
# or: python app.py sample_resume.txt --jd job_description.txt
```
Pass `--jd job_description.txt` to enable JD matching + ATS scoring. PDF text extraction is built in via PyMuPDF. For image-only scanned PDFs, OCR is not silently claimed; add an OCR engine if that input type is required.
When the run finishes, if any field had low confidence, you'll be prompted
in the terminal to confirm or correct it — corrections are saved and teach
the knowledge base immediately.

## Tests
```bash
pytest -v
```

## Docker
```bash
docker build -t resume-extractor .
docker run --env-file .env resume-extractor
```

## Tech Stack
Python · OpenAI GPT-4.1 (native tool calling) · text-embedding-3-small ·
Pydantic · custom stateful agent graph · pytest · Docker · GitHub Actions

## Author
**Sriram Singamaneni**
