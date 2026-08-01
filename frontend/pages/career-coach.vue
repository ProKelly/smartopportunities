<script setup lang="ts">
const route = useRoute();
const api = useApi();
const opportunityId = ref((route.query.opportunity_id as string) || "");
const result = ref<any>(null);
const loading = ref(false);
const error = ref("");

async function prepareMe() {
  loading.value = true;
  error.value = "";
  try {
    result.value = await api.post("/career-coach", {
      opportunity_id: opportunityId.value || null,
    });
  } catch (e: any) {
    error.value = e?.data?.detail || "Couldn't generate prep guidance. Try again.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div>
    <AppNav />
    <main class="mx-auto max-w-3xl px-6 py-12">
      <p class="waypoint-label mb-2">Phase 5 · The AI career coach</p>
      <h1 class="text-3xl font-semibold text-parchment">Prepare me</h1>
      <p class="mt-2 text-navy-600">
        CV notes, a cover-letter draft, and interview tips — targeted at a specific
        opportunity if you give us one, otherwise general prep based on your profile.
      </p>

      <div class="card mt-8">
        <label class="waypoint-label mb-2 block">Opportunity ID <span class="text-navy-600 normal-case">(optional — auto-filled from "Prepare me" links)</span></label>
        <input v-model="opportunityId" class="input-field" placeholder="Leave blank for general prep" />
        <button class="btn-beacon mt-4" :disabled="loading" @click="prepareMe">
          {{ loading ? "Preparing you..." : "Prepare me" }}
        </button>
        <p v-if="error" class="mt-3 text-sm text-coral">{{ error }}</p>
      </div>

      <section v-if="result" class="mt-10 space-y-8">
        <div class="card">
          <h2 class="mb-3 text-lg font-semibold text-parchment">CV suggestions</h2>
          <ul class="space-y-1 text-sm text-navy-600">
            <li v-for="s in result.cv_suggestions" :key="s">· {{ s }}</li>
          </ul>
        </div>

        <div class="card">
          <h2 class="mb-3 text-lg font-semibold text-parchment">Cover letter draft</h2>
          <p class="whitespace-pre-line text-sm text-parchment">{{ result.cover_letter_draft }}</p>
        </div>

        <div class="grid gap-8 sm:grid-cols-2">
          <div class="card">
            <h2 class="mb-3 text-lg font-semibold text-parchment">Portfolio improvements</h2>
            <ul class="space-y-1 text-sm text-navy-600">
              <li v-for="p in result.portfolio_improvements" :key="p">· {{ p }}</li>
            </ul>
          </div>
          <div class="card">
            <h2 class="mb-3 text-lg font-semibold text-parchment">Skills to learn</h2>
            <ul class="space-y-1 text-sm text-navy-600">
              <li v-for="s in result.skills_to_learn" :key="s">· {{ s }}</li>
            </ul>
          </div>
        </div>

        <div class="card">
          <h2 class="mb-3 text-lg font-semibold text-parchment">Interview tips</h2>
          <ul class="space-y-1 text-sm text-navy-600">
            <li v-for="t in result.interview_tips" :key="t">· {{ t }}</li>
          </ul>
        </div>

        <div class="card">
          <h2 class="mb-3 text-lg font-semibold text-parchment">Timeline</h2>
          <ul class="space-y-1 text-sm text-navy-600">
            <li v-for="t in result.timeline" :key="t">· {{ t }}</li>
          </ul>
        </div>
      </section>
    </main>
  </div>
</template>