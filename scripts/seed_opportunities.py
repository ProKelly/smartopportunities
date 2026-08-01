"""One-off script: seeds the `opportunities` table with a curated starter dataset
and computes embeddings for each row so semantic search works immediately.

Usage (from backend/):
    python -m scripts.seed_opportunities
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.supabase_client import get_service_client  # noqa: E402
from app.services.embedding_service import embed_texts  # noqa: E402

DATA_FILE = Path(__file__).parent / "seed_data.json"


def main():
    with open(DATA_FILE) as f:
        opportunities = json.load(f)

    print(f"Loaded {len(opportunities)} opportunities to seed.")

    texts = [
        f"{o['title']}. {o['description']}. Skills: {', '.join(o.get('skills', []))}"
        for o in opportunities
    ]
    print("Computing embeddings locally (fastembed)...")
    vectors = embed_texts(texts)

    for o, v in zip(opportunities, vectors):
        o["embedding"] = v

    db = get_service_client()
    print("Inserting into Supabase...")
    res = db.table("opportunities").insert(opportunities).execute()
    print(f"Inserted {len(res.data)} rows.")


if __name__ == "__main__":
    main()
