<script setup lang="ts">
const api = useApi();
const summary = ref<any>(null);
const loading = ref(true);
const errorMsg = ref("");

async function load() {
  loading.value = true;
  try {
    summary.value = await api.get("/dashboard/summary");
  } catch (e: any) {
    errorMsg.value = e?.data?.detail || "Couldn't load your dashboard.";
  } finally {
    loading.value = false;
  }
}
onMounted(load);

const cards = computed(() => {
  const s = summary.value;
  if (!s) return [];
  return [
    { label: "Opportunities found", value: s.opportunities_found, accent: "text-chart" },
    { label: "Saved", value: s.saved_count, accent: "text-signal" },
    { label: "Applied", value: s.applied_count, accent: "text-coral" },
    { label: "Profile strength", value: `${s.profile_strength}%`, accent: "text-parchment" },
  ];
});
</script>

<template>
  <div>
    <AppNav />
    <main class="mx-auto max-w-6xl px-6 py-12">
      <!-- Logo added to header area -->
      <div class="flex items-center gap-4 mb-8">
        <img src="/cityos.png" alt="CityOS Logo" class="h-10 w-auto" />
        <div>
          <p class="waypoint-label mb-1">Mission control</p>
          <h1 class="text-3xl font-semibold text-parchment">Dashboard</h1>
        </div>
      </div>

      <div v-if="loading" class="mt-8 text-navy-600">Charting your dashboard...</div>

      <template v-else-if="summary">
        <div v-if="!summary.opportunity_dna" class="card mt-8 border-signal/40">
          <p class="text-parchment">You haven't built a profile yet — do that first so we can find matches for you.</p>
          <NuxtLink to="/profile" class="btn-beacon mt-4 inline-flex">Build my profile</NuxtLink>
        </div>

        <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="c in cards" :key="c.label" class="card">
            <p class="waypoint-label mb-2">{{ c.label }}</p>
            <p class="text-3xl font-display font-semibold" :class="c.accent">{{ c.value }}</p>
          </div>
        </div>

        <div class="mt-10 grid gap-8 lg:grid-cols-2">
          <section class="card">
            <div class="mb-4 flex items-center justify-between">
              <h2 class="text-lg font-semibold text-parchment">Recommendations</h2>
              <NuxtLink to="/opportunities/find" class="text-sm text-chart hover:underline">Refresh matches →</NuxtLink>
            </div>
            <div v-if="!summary.recommendations?.length" class="text-sm text-gray-400">
              No matches yet. Head to Find Opportunities to run the AI matching engine.
            </div>
            <ul v-else class="space-y-4">
              <li v-for="m in summary.recommendations" :key="m.opportunity_id" class="border-t border-navy-700 pt-4 first:border-0 first:pt-0">
                <div class="flex items-start justify-between gap-4">
                  <div>
                    <NuxtLink :to="`/opportunities/${m.opportunity_id}`" class="font-medium text-parchment hover:text-chart">
                      {{ m.opportunity?.title }}
                    </NuxtLink>
                    <p class="text-sm text-gray-400">{{ m.opportunity?.organization }}</p>
                  </div>
                  <span class="font-mono text-sm text-signal">{{ m.match_score }}%</span>
                </div>
              </li>
            </ul>
          </section>

          <section class="card">
            <h2 class="mb-4 text-lg font-semibold text-parchment">Upcoming deadlines</h2>
            <div v-if="!summary.upcoming_deadlines?.length" class="text-sm text-gray-400">
              Nothing tracked yet — save or apply to opportunities to see deadlines here.
            </div>
            <ul v-else class="space-y-3">
              <li v-for="d in summary.upcoming_deadlines" :key="d.opportunity_id" class="flex items-center justify-between text-sm">
                <span class="text-parchment">{{ d.opportunity?.title }}</span>
                <span class="font-mono text-coral">{{ d.opportunity?.deadline }}</span>
              </li>
            </ul>
          </section>
        </div>
      </template>

      <p v-if="errorMsg" class="mt-6 text-sm text-coral">{{ errorMsg }}</p>
    </main>
  </div>
</template>