<script setup lang="ts">
const route = useRoute();
const api = useApi();
const opp = ref<any>(null);
const loading = ref(true);
const error = ref("");
const saved = ref(false);
const applying = ref(false);
const applied = ref(false);

async function load() {
  loading.value = true;
  try {
    opp.value = await api.get(`/opportunities/${route.params.id}`);
  } catch (e: any) {
    error.value = e?.data?.detail || "Couldn't load this opportunity.";
  } finally {
    loading.value = false;
  }
}
onMounted(load);

async function save() {
  await api.post(`/opportunities/${route.params.id}/save`);
  saved.value = true;
}

async function markApplied() {
  applying.value = true;
  try {
    await api.post("/applications", { opportunity_id: route.params.id, status: "applied" });
    applied.value = true;
  } finally {
    applying.value = false;
  }
}
</script>

<template>
  <div>
    <AppNav />
    <main class="mx-auto max-w-3xl px-6 py-12">
      <NuxtLink to="/opportunities/find" class="text-sm text-gray-400 hover:text-parchment">← Back to matches</NuxtLink>

      <div v-if="loading" class="mt-8 text-navy-600">Loading...</div>
      <p v-else-if="error" class="mt-8 text-coral">{{ error }}</p>

      <template v-else-if="opp">
        <span class="waypoint-label mt-8 block">{{ opp.category }}</span>
        <h1 class="mt-2 text-3xl font-semibold text-parchment">{{ opp.title }}</h1>
        <p class="mt-1 text-gray-400">{{ opp.organization }} · {{ opp.country }}</p>

        <div class="card mt-6">
          <p class="text-parchment">{{ opp.description }}</p>

          <dl class="mt-6 grid gap-4 sm:grid-cols-2">
            <div>
              <dt class="waypoint-label">Deadline</dt>
              <dd class="mt-1 text-coral">{{ opp.deadline || "Rolling / not specified" }}</dd>
            </div>
            <div>
              <dt class="waypoint-label">Eligibility</dt>
              <dd class="mt-1 text-parchment">{{ opp.eligibility || "See listing" }}</dd>
            </div>
          </dl>

          <div v-if="opp.skills?.length" class="mt-6 flex flex-wrap gap-2">
            <span v-for="s in opp.skills" :key="s" class="rounded-full border border-navy-600 px-3 py-1 text-xs text-navy-600">
              {{ s }}
            </span>
          </div>

          <div class="mt-8 flex flex-wrap gap-3">
            <a :href="opp.url" target="_blank" rel="noopener" class="btn-beacon">Go to listing ↗</a>
            <button class="btn-ghost" :disabled="saved" @click="save">{{ saved ? "Saved" : "Save" }}</button>
            <NuxtLink :to="`/career-coach?opportunity_id=${opp.id}`" class="btn-ghost">Prepare me</NuxtLink>
            <button class="btn-ghost" :disabled="applying || applied" @click="markApplied">
              {{ applied ? "Marked as applied" : applying ? "Saving..." : "Mark as applied" }}
            </button>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>