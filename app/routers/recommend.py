from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.deps import CurrentUser, get_current_user, get_scoped_db
from app.models.opportunity import MatchResult, RecommendResponse
from app.services import embedding_service, groq_service

router = APIRouter(prefix="/recommend", tags=["recommend"])


def _profile_to_text(profile: dict) -> str:
    parts = [
        profile.get("goals", ""),
        " ".join(profile.get("skills", []) or []),
        " ".join(profile.get("interests", []) or []),
        " ".join(profile.get("preferred_industries", []) or []),
        profile.get("education_level", ""),
    ]
    return " ".join(p for p in parts if p)


@router.post("", response_model=RecommendResponse)
def recommend(
    current_user: CurrentUser = Depends(get_current_user),
    db: Client = Depends(get_scoped_db),
):
    """The core AI Matching Engine pipeline:
    1. Load the user's profile (+ Opportunity DNA).
    2. Embed the profile text.
    3. Vector-search the top ~20 candidate opportunities via a Postgres RPC (pgvector).
    4. Hand the shortlist to Groq (LLM reasoning) to rank the top 5 and explain each match.
    """
    profile_res = db.table("profiles").select("*").eq("user_id", current_user.id).limit(1).execute()
    if not profile_res.data:
        raise HTTPException(status_code=400, detail="Create a profile first")
    profile = profile_res.data[0]

    query_vector = embedding_service.embed_text(_profile_to_text(profile))

    # match_opportunities is a Postgres function using pgvector's <=> cosine distance
    # operator (see backend/supabase/schema.sql). Falls back to a plain select if the
    # RPC isn't installed yet, so the demo still works before Supabase is fully set up.
    try:
        candidates_res = db.rpc(
            "match_opportunities",
            {"query_embedding": query_vector, "match_count": 20},
        ).execute()
        candidates = candidates_res.data or []
    except Exception:
        candidates = db.table("opportunities").select("*").limit(20).execute().data or []

    if not candidates:
        return RecommendResponse(matches=[])

    candidate_slim = [
        {
            "id": c["id"],
            "title": c["title"],
            "organization": c.get("organization"),
            "description": c.get("description", "")[:500],
            "category": c.get("category"),
            "country": c.get("country"),
            "deadline": c.get("deadline"),
            "skills": c.get("skills"),
        }
        for c in candidates
    ]

    try:
        ranked = groq_service.rank_and_explain_opportunities(profile, candidate_slim)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI matching failed: {exc}")

    by_id = {c["id"]: c for c in candidates}
    matches = []
    for m in ranked.get("matches", []):
        opp = by_id.get(m["opportunity_id"])
        matches.append(
            MatchResult(
                opportunity_id=m["opportunity_id"],
                match_score=m["match_score"],
                reason=m["reason"],
                missing_skill=m.get("missing_skill"),
                next_step=m["next_step"],
                opportunity=opp,
            )
        )

    # Cache the recommendation batch for the dashboard's "Recommendations" card.
    try:
        db.table("recommendations").insert(
            {"user_id": current_user.id, "results": [m.model_dump() for m in matches]}
        ).execute()
    except Exception:
        pass  # non-critical; recommendations are still returned to the caller

    return RecommendResponse(matches=matches)
