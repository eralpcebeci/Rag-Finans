# RAG Finans

KAP faaliyet raporları üzerinde çalışan, parçaları değiştirilebilir bir RAG laboratuvarı.

## Kurulum

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env                 # Windows: copy .env.example .env
pre-commit install                   # önce git init gerekir
```

## Qdrant'ı başlat

```bash
docker compose -f docker/docker-compose.yml up -d
```

Dashboard: http://localhost:6333/dashboard

## API'yi çalıştır

```bash
uvicorn rag.api.main:app --reload
```

Kontrol: http://localhost:8000/health → `{"api":"up","qdrant":"up",...}`

## Test ve kalite

```bash
pytest
ruff check . && ruff format .
mypy src
```

## Yol haritası

1. Faz 1: İskelet (bu adım)
2. Faz 2: Ingestion (PDF parse, chunking, embedding, indeksleme)
3. Faz 3: Retrieval + generation + endpoint
4. Faz 4: Hybrid search, rerank, kaynak gösterme
5. Faz 5: Evaluation ve CI
