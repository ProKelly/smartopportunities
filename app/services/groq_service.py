import json
from functools import lru_cache

from groq import Groq

from app.core.config import get_settings

settings = get_settings()


@lru_cache
def get_groq_client() -> Groq:
    return Groq(api_key=settings.groq_api_key)


def _chat_json(system_prompt: str, user_prompt: str, model: str, temperature: float = 0.4) -> dict:
    """Call Groq's chat completion with JSON-object mode and return parsed JSON.
    Falls back to a best-effort parse if the model wraps the JSON in prose."""
    client = get_groq_client()
    completion = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    raw = completion.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end != -1:
            return json.loads(raw[start : end + 1])
        raise


def generate_opportunity_dna(profile: dict) -> dict:
    """Phase 1 AI: turn a raw profile into a structured 'Opportunity DNA' summary."""
    system_prompt = (
        "You are an expert career and opportunity-matching analyst. Given a user's "
        "profile, produce a concise, honest analysis. Respond ONLY with a JSON object "
        "with keys: summary (2-3 sentence string), strengths (array of short strings), "
        "weaknesses (array of short strings), career_interests (array of short strings), "
        "personality_summary (1-2 sentence string), recommended_categories (array from "
        "[Scholarships, Jobs, Internships, Grants, Competitions, Accelerators, Fellowships, "
        "Conferences, Events, Volunteering])."
    )
    return _chat_json(system_prompt, json.dumps(profile), settings.groq_reasoning_model)


def rank_and_explain_opportunities(profile: dict, opportunities: list[dict]) -> dict:
    """Phase 4 AI: given a shortlist of candidate opportunities (already narrowed by
    vector search), pick and rank the top matches with an explanation each."""
    system_prompt = (
        "You are an AI opportunity-matching engine. You are given a user profile and a "
        "list of candidate opportunities (already pre-filtered by semantic search). "
        "Select and rank the best matches (at most 5, fewer if the pool is small). "
        "Respond ONLY with a JSON object: {\"matches\": [{\"opportunity_id\": string, "
        "\"match_score\": integer 0-100, \"reason\": string (why it fits), "
        "\"missing_skill\": string or null, \"next_step\": string (one concrete action)}]}. "
        "Order matches by match_score descending."
    )
    user_prompt = json.dumps({"profile": profile, "opportunities": opportunities})
    return _chat_json(system_prompt, user_prompt, settings.groq_reasoning_model)


def generate_roadmap(goal: str, profile: dict | None = None) -> dict:
    """Phase 6 AI: turn a stated goal into a month-by-month roadmap."""
    system_prompt = (
        "You are a career roadmap planner. Given a goal (and optionally a user profile), "
        "produce a realistic month-by-month plan of 3-6 months. Respond ONLY with JSON: "
        "{\"goal\": string, \"summary\": string, \"months\": [{\"month\": integer, "
        "\"title\": string, \"focus_areas\": [string], \"milestones\": [string]}]}."
    )
    user_prompt = json.dumps({"goal": goal, "profile": profile or {}})
    return _chat_json(system_prompt, user_prompt, settings.groq_reasoning_model)


def generate_career_coach_output(profile: dict, opportunity: dict | None = None) -> dict:
    """Phase 5 AI: CV/cover letter/interview prep guidance, optionally targeted at one opportunity."""
    system_prompt = (
        "You are an AI career coach. Given a user profile and optionally a specific "
        "target opportunity, produce actionable prep guidance. Respond ONLY with JSON: "
        "{\"cv_suggestions\": [string], \"cover_letter_draft\": string, "
        "\"portfolio_improvements\": [string], \"skills_to_learn\": [string], "
        "\"interview_tips\": [string], \"timeline\": [string]}."
    )
    user_prompt = json.dumps({"profile": profile, "opportunity": opportunity})
    return _chat_json(system_prompt, user_prompt, settings.groq_reasoning_model)


def embed_text_fallback_keywords(text: str) -> list[str]:
    """Lightweight keyword extraction used only if a dedicated embedding model isn't
    configured. Real embeddings are produced client-side via the embedding_service."""
    system_prompt = (
        "Extract the 8-15 most important skill/topic keywords from this text. "
        "Respond ONLY with JSON: {\"keywords\": [string]}."
    )
    result = _chat_json(system_prompt, text, settings.groq_fast_model, temperature=0.1)
    return result.get("keywords", [])
