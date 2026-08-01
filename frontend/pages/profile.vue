<script setup lang="ts">
const api = useApi();

const form = reactive({
  full_name: "",
  country: "",
  education_level: "",
  skills: "",
  interests: "",
  goals: "",
  preferred_industries: "",
  preferred_countries: "",
  availability: "",
  expected_salary: "",
  languages: "",
  resume_text: "",
});

const dna = ref<any>(null);
const loading = ref(false);
const saving = ref(false);
const error = ref("");
const loaded = ref(false);

function toList(v: string) {
  return v.split(",").map((s) => s.trim()).filter(Boolean);
}
function toCsv(v: string[] | undefined) {
  return (v || []).join(", ");
}

async function loadProfile() {
  loading.value = true;
  try {
    const existing: any = await api.get("/profile");
    if (existing) {
      form.full_name = existing.full_name || "";
      form.country = existing.country || "";
      form.education_level = existing.education_level || "";
      form.skills = toCsv(existing.skills);
      form.interests = toCsv(existing.interests);
      form.goals = existing.goals || "";
      form.preferred_industries = toCsv(existing.preferred_industries);
      form.preferred_countries = toCsv(existing.preferred_countries);
      form.availability = existing.availability || "";
      form.expected_salary = existing.expected_salary || "";
      form.languages = toCsv(existing.languages);
      form.resume_text = existing.resume_text || "";
      dna.value = existing.opportunity_dna;
    }
  } catch (e) {
    // no profile yet — that's fine, this is the creation form
  } finally {
    loading.value = false;
    loaded.value = true;
  }
}

async function onSubmit() {
  error.value = "";
  saving.value = true;
  try {
    const payload = {
      full_name: form.full_name,
      country: form.country,
      education_level: form.education_level,
      skills: toList(form.skills),
      interests: toList(form.interests),
      goals: form.goals,
      preferred_industries: toList(form.preferred_industries),
      preferred_countries: toList(form.preferred_countries),
      availability: form.availability,
      expected_salary: form.expected_salary || null,
      languages: toList(form.languages),
      resume_text: form.resume_text || null,
    };
    const result: any = await api.post("/profile", payload);
    dna.value = result.opportunity_dna;
  } catch (e: any) {
    error.value = e?.data?.detail || "Couldn't save your profile. Try again.";
  } finally {
    saving.value = false;
  }
}

onMounted(loadProfile);
</script>

<template>
  <div>
    <AppNav />
    <main class="mx-auto max-w-4xl px-6 py-12">
      <p class="waypoint-label mb-2">Phase 1 · Chart yourself</p>
      <h1 class="text-3xl font-semibold text-parchment">Your profile</h1>
      <p class="mt-2 text-navy-600">
        Plain questions, not a 40-field form. This feeds your Opportunity DNA — the
        summary the AI uses to find and explain your matches.
      </p>

      <form v-if="loaded" class="card mt-8 space-y-6" @submit.prevent="onSubmit">
        <div class="grid gap-6 sm:grid-cols-2">
          <div>
            <label class="waypoint-label mb-2 block">Full name</label>
            <input v-model="form.full_name" required class="input-field" />
          </div>
          <div>
            <label class="waypoint-label mb-2 block">Country</label>
            <input v-model="form.country" required class="input-field" placeholder="e.g. Cameroon" />
          </div>
        </div>

        <div>
          <label class="waypoint-label mb-2 block">Current education level</label>
          <input v-model="form.education_level" required class="input-field" placeholder="e.g. Year 4 Computer Engineering student" />
        </div>

        <div>
          <label class="waypoint-label mb-2 block">Skills <span class="text-navy-600 normal-case">(comma-separated)</span></label>
          <input v-model="form.skills" class="input-field" placeholder="Django, Vue.js, PostgreSQL, Flutter" />
        </div>

        <div>
          <label class="waypoint-label mb-2 block">Interests <span class="text-navy-600 normal-case">(comma-separated)</span></label>
          <input v-model="form.interests" class="input-field" placeholder="AI, fintech, civic tech" />
        </div>

        <div>
          <label class="waypoint-label mb-2 block">Goals</label>
          <textarea v-model="form.goals" rows="3" class="input-field" placeholder="What are you trying to do in the next 6-12 months?" />
        </div>

        <div class="grid gap-6 sm:grid-cols-2">
          <div>
            <label class="waypoint-label mb-2 block">Preferred industries <span class="text-navy-600 normal-case">(comma-sep)</span></label>
            <input v-model="form.preferred_industries" class="input-field" />
          </div>
          <div>
            <label class="waypoint-label mb-2 block">Preferred countries <span class="text-navy-600 normal-case">(comma-sep)</span></label>
            <input v-model="form.preferred_countries" class="input-field" />
          </div>
        </div>

        <div class="grid gap-6 sm:grid-cols-3">
          <div>
            <label class="waypoint-label mb-2 block">Availability</label>
            <input v-model="form.availability" class="input-field" placeholder="e.g. Immediately" />
          </div>
          <div>
            <label class="waypoint-label mb-2 block">Expected salary <span class="text-navy-600 normal-case">(optional)</span></label>
            <input v-model="form.expected_salary" class="input-field" />
          </div>
          <div>
            <label class="waypoint-label mb-2 block">Languages <span class="text-navy-600 normal-case">(comma-sep)</span></label>
            <input v-model="form.languages" class="input-field" placeholder="English, French" />
          </div>
        </div>

        <div>
          <label class="waypoint-label mb-2 block">Resume text <span class="text-navy-600 normal-case">(optional — paste it in)</span></label>
          <textarea v-model="form.resume_text" rows="4" class="input-field" />
        </div>

        <p v-if="error" class="text-sm text-coral">{{ error }}</p>
        <button type="submit" class="btn-beacon" :disabled="saving">
          {{ saving ? "Generating your Opportunity DNA..." : "Save & generate Opportunity DNA" }}
        </button>
      </form>

      <section v-if="dna" class="card mt-8 border-signal/30">
        <p class="waypoint-label mb-3">Your Opportunity DNA™</p>
        <p class="text-parchment">{{ dna.summary }}</p>

        <div class="mt-6 grid gap-6 sm:grid-cols-2">
          <div>
            <h3 class="mb-2 text-sm font-semibold text-chart">Strengths</h3>
            <ul class="space-y-1 text-sm text-navy-600">
              <li v-for="s in dna.strengths" :key="s">· {{ s }}</li>
            </ul>
          </div>
          <div>
            <h3 class="mb-2 text-sm font-semibold text-coral">Watch-outs</h3>
            <ul class="space-y-1 text-sm text-navy-600">
              <li v-for="w in dna.weaknesses" :key="w">· {{ w }}</li>
            </ul>
          </div>
        </div>

        <div class="mt-6 flex flex-wrap gap-2">
          <span v-for="c in dna.recommended_categories" :key="c" class="rounded-full border border-signal/40 px-3 py-1 text-xs text-signal">
            {{ c }}
          </span>
        </div>

        <NuxtLink to="/opportunities/find" class="btn-beacon mt-8 inline-flex">Find my opportunities</NuxtLink>
      </section>
    </main>
  </div>
</template>