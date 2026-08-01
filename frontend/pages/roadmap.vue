<script setup lang="ts">
import { ref, onMounted } from 'vue';

const api = useApi();
const goal = ref("");
const roadmap = ref<any>(null);
const loading = ref(false);
const error = ref("");
const past = ref<any[]>([]);

async function loadPast() {
  try {
    past.value = await api.get("/roadmap");
  } catch (e) {
    // ignore
  }
}
onMounted(loadPast);

async function generate() {
  if (!goal.value.trim()) return;
  loading.value = true;
  error.value = "";
  try {
    roadmap.value = await api.post("/roadmap", { goal: goal.value });
    await loadPast();
  } catch (e: any) {
    error.value = e?.data?.detail || "Couldn't generate a roadmap. Try again.";
  } finally {
    loading.value = false;
  }
}

async function selectRoadmap(id: string) {
  loading.value = true;
  error.value = "";
  try {
    roadmap.value = await api.get(`/roadmap/${id}`);
  } catch (e: any) {
    error.value = e?.data?.detail || "Couldn't load roadmap details.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div>
    <AppNav />
    <main class="mx-auto max-w-3xl px-6 py-12">
      <p class="waypoint-label mb-2">Phase 6 · The roadmap generator</p>
      <h1 class="text-3xl font-semibold text-parchment">Roadmap</h1>
      <p class="mt-2 text-gray-400">Tell us where you want to go. We'll chart the months to get there.</p>

      <form class="card mt-8" @submit.prevent="generate">
        <label class="waypoint-label mb-2 block">Your goal</label>
        <input v-model="goal" class="input-field" placeholder="e.g. I want to become an AI Engineer" />
        <button type="submit" class="btn-beacon mt-4" :disabled="loading">
          {{ loading ? "Charting your roadmap..." : "Generate roadmap" }}
        </button>
        <p v-if="error" class="mt-3 text-sm text-coral">{{ error }}</p>
      </form>

      <section v-if="roadmap" class="mt-10">
        <h2 class="text-xl font-semibold text-parchment">{{ roadmap.goal }}</h2>
        <p class="mt-1 text-gray-400">{{ roadmap.summary }}</p>

        <ol class="mt-6 space-y-4">
          <li v-for="m in roadmap.months" :key="m.month" class="card flex gap-6">
            <span class="font-mono text-signal">M{{ m.month }}</span>
            <div>
              <h3 class="font-medium text-parchment">{{ m.title }}</h3>
              <div class="mt-2 flex flex-wrap gap-2">
                <span v-for="f in m.focus_areas" :key="f" class="rounded-full border border-chart/40 px-3 py-1 text-xs text-chart">{{ f }}</span>
              </div>
              <ul class="mt-3 space-y-1 text-sm text-gray-400">
                <li v-for="ms in m.milestones" :key="ms">· {{ ms }}</li>
              </ul>
            </div>
          </li>
        </ol>
      </section>

      <section v-if="past.length" class="mt-12">
        <h2 class="mb-4 text-lg font-semibold text-parchment">Past roadmaps</h2>
        <ul class="space-y-2">
          <li v-for="r in past" :key="r.id">
            <button @click="selectRoadmap(r.id)" class="text-sm text-gray-400 hover:text-parchment text-left transition-colors">
              · {{ r.goal }}
            </button>
          </li>
        </ul>
      </section>
    </main>
  </div>
</template>