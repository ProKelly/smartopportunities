# CityOS AI 

**Your AI-powered opportunity navigator.**

Full-stack implementation: **Nuxt 3** frontend, **FastAPI** backend, **Supabase**
(Postgres + pgvector + Auth) for data and auth, **Groq** for LLM reasoning, and a
local **fastembed** model for semantic-search embeddings.

```
smartopportunities/
├── backend/     FastAPI app, Supabase schema, seed data
└── frontend/    Nuxt 3 app
```

## 1. Set up Supabase

1. Create a project at supabase.com.
2. Open **SQL Editor** and run `backend/supabase/schema.sql` — this creates every
   table, enables Row Level Security, and installs pgvector plus the
   `match_opportunities` semantic-search function.
3. In **Authentication → Providers**, enable Email, and optionally Google OAuth.
4. Grab your keys from **Project Settings → API**:
   - `Project URL` → `SUPABASE_URL`
   - `anon public` key → `SUPABASE_ANON_KEY` (frontend uses this too)
   - `service_role` key → `SUPABASE_SERVICE_ROLE_KEY` (backend only — never expose
     this to the frontend)
   - **Project Settings → API → JWT Settings** → `JWT Secret` → `SUPABASE_JWT_SECRET`

## 2. Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your Supabase + Groq keys
```

Get a free Groq API key at console.groq.com → `GROQ_API_KEY`.

Seed the opportunity knowledge base (curated starter dataset, embedded locally):

```bash
python -m scripts.seed_opportunities
```

Run the API:

```bash
uvicorn app.main:app --reload --port 8000
```

Docs at `http://localhost:8000/docs`.

## 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env   # fill in NUXT_PUBLIC_API_BASE + your Supabase URL/anon key
npm run dev
```

App at `http://localhost:8000/`.

## How the AI pipeline works

1. **Profile → Opportunity DNA** (`POST /profile`): Groq reads the raw profile and
   returns a structured summary — strengths, weaknesses, career interests, and
   recommended categories. Stored as JSON on the `profiles` row.
2. **Opportunity embeddings**: every opportunity is embedded locally (fastembed,
   `bge-small-en-v1.5`, 384-dim) and stored in a `vector(384)` pgvector column.
3. **Matching** (`POST /recommend`): the user's profile is embedded, pgvector's
   cosine-distance operator (via the `match_opportunities` RPC) pulls the top ~20
   candidates, and Groq re-ranks/explains the top 5 with a match score, a
   plain-English reason, a missing skill (if any), and a concrete next step.
4. **Roadmap** (`POST /roadmap`): Groq turns a stated goal into a month-by-month
   plan, optionally informed by the user's profile.
5. **Career Coach** (`POST /career-coach`): Groq generates CV notes, a cover-letter
   draft, portfolio suggestions, skills to learn, interview tips, and a timeline —
   general, or targeted at one opportunity.

## What's intentionally out of scope (v1)

Per the original build plan: continuous web crawling, multi-agent workflows, social
features, messaging, company dashboards, a mobile app, a browser extension, complex
analytics, and payments. The seed dataset (20 real, well-known programs) stands in
for full-scale opportunity ingestion — a good next step is a scheduled scraper that
calls `POST /opportunities` for each new listing it finds (it embeds and indexes
automatically).

## Notes on the design

The frontend uses a "night navigator" visual theme — a dark chart-like background,
a gold "signal/beacon" accent for primary actions, and a teal "charted route" accent
for matches and progress — built around the idea of *charting a course* to an
opportunity rather than just listing search results.


Hosted application is accessible at [https://cityos-tau.vercel.app](https://cityos-tau.vercel.app).