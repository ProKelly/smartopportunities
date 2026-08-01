<script setup lang="ts">
const api = useApi();
const matches = ref<any[]>([]);
const loading = ref(false);
const error = ref("");
const hasSearched = ref(false);

async function findOpportunities() {
  loading.value = true;
  error.value = "";
  try {
    const res: any = await api.post("/recommend");
    matches.value = res.matches;
    hasSearched.value = true;
  } catch (e: any) {
    error.value = e?.data?.detail || "Couldn't run the matching engine. Try again.";
  } finally {
    loading.value = false;
  }
}

async function saveOpportunity(id: string) {
  try {
    await api.post(`/opportunities/${id}/save`);
  } catch (e) {
    // non-fatal
  }
}
</script>

<template>
  <div>
    <AppNav />
    <main class="mx-auto max-w-5xl px-6 py-12">
      <p class="waypoint-label mb-2">Phase 4 · The matching engine</p>
      <h1 class="text-3xl font-semibold text-parchment">Find opportunities</h1>
      <p class="mt-2 max-w-2xl text-navy-600">
        We embed your profile, pull the closest opportunities by semantic search, then
        have the AI rank and explain the best fits.
      </p>

      <button class="btn-beacon mt-8" :disabled="loading" @click="findOpportunities">
        {{ loading ? "Scanning the opportunity landscape..." : "Find opportunities" }}
      </button>

      <p v-if="error" class="mt-4 text-sm text-coral">{{ error }}</p>

      <div v-if="hasSearched && !loading" class="mt-10">
        <p v-if="!matches.length" class="text-navy-600">
          No strong matches yet — try broadening your profile's skills or interests.
        </p>

        <ul v-else class="space-y-6">
          <li v-for="m in matches" :key="m.opportunity_id" class="card">
            <div class="flex flex-wrap items-start justify-between gap-4">
              <div>
                <span class="rounded-full border border-navy-600 px-2 py-0.5 text-xs text-navy-600">
                  {{ m.opportunity?.category }}
                </span>
                <NuxtLink :to="`/opportunities/${m.opportunity_id}`" class="mt-2 block text-xl font-medium text-parchment hover:text-chart">
                  {{ m.opportunity?.title }}
                </NuxtLink>
                <p class="text-sm text-navy-600">{{ m.opportunity?.organization }} · {{ m.opportunity?.country }}</p>
              </div>
              <div class="text-right">
                <p class="font-mono text-2xl font-semibold text-signal">{{ m.match_score }}%</p>
                <p class="waypoint-label">match</p>
              </div>
            </div>

            <p class="mt-4 text-parchment">{{ m.reason }}</p>
            <p v-if="m.missing_skill" class="mt-2 text-sm text-coral">Missing skill: {{ m.missing_skill }}</p>
            <p class="mt-2 text-sm text-chart">Next step: {{ m.next_step }}</p>

            <div class="mt-5 flex flex-wrap gap-3">
              <NuxtLink :to="`/opportunities/${m.opportunity_id}`" class="btn-ghost !px-4 !py-2 text-sm">View details</NuxtLink>
              <button class="btn-ghost !px-4 !py-2 text-sm" @click="saveOpportunity(m.opportunity_id)">Save</button>
              <NuxtLink :to="`/career-coach?opportunity_id=${m.opportunity_id}`" class="btn-ghost !px-4 !py-2 text-sm">Prepare me</NuxtLink>
            </div>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>