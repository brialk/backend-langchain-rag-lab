# Planning Notes: LangChain RAG Runbook API

## Who does the endpoint support?
On-call engineers and incident responders on the platform/reliability team who need fast, trustworthy runbook guidance during an incident.

## What business or reliability problem does it solve?
During an outage people lose time searching many runbooks. The endpoint retrieves the right approved runbook chunks and summarizes them, which shortens time to mitigation and keeps responses consistent.

## Why should the model answer come from the approved runbook context?
Models can invent plausible but wrong steps. Restricting answers to retrieved, approved runbook text keeps advice accurate, auditable (each answer lists its sources), and safe to follow in an incident.

## What should a successful response include?
- `answer`: a concise answer based only on the retrieved context
- `sources`: metadata (source_id, title, category, section, chunk_id, distance), never the full text
- `langchain`: debug info (chain expression, components, retrieved count/ids, top_k, context size, fallback flag, score type)

## What should the system do when no approved context is available?
Do not call the model. Return the safe fallback answer ("I do not have enough approved runbook context to answer that reliably."), an empty `sources` list, and `langchain.fallback = true`.

## Manual RAG workflow mapping
1. Receive the question -> `lib/validation.py` + Flask route
2. Retrieve context -> `lib/vector_store.py`
3. Build the prompt -> `lib/prompt_templates.py`
4. Call the model -> `ChatOllama` in `lib/langchain_rag_service.py`
5. Parse/format output -> `StrOutputParser` + `lib/response_formatter.py`
6. Return sources -> `format_sources`
7. Verify quality -> pytest suite
