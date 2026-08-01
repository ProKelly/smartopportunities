<script setup lang="ts">
const api = useApi();
const saved = ref<any[]>([]);
const loading = ref(true);

async function load() {
  loading.value = true;
  try {
    saved.value = await api.get("/opportunities/saved/list");
  } finally {
    loading.value = false;
  }
}
onMounted(load);

async function unsave(id: string) {
  await api.del(`/opportunities/${id}/save`);
  saved.value = saved.value.filter((o) => o.id !== id);
}
</script>

<template>
  <div>
    <AppNav />
    <main class="mx-auto max-w-4xl px-6 py-12">
      <p class="waypoint-label mb-2">Your shortlist</p>
      <h1 class="text-3xl font-semibold text-parchment">Saved opportunities</h1>

      <div v-if="loading" class="mt-8 text-navy-600">Loading...</div>
      <p v-else-if="!saved.length" class="mt-8 text-navy-600">
        Nothing saved yet. <NuxtLink to="/opportunities/find" class="text-chart hover:underline">Find opportunities →</NuxtLink>
      </p>

      <ul v-else class="mt-8 space-y-4">
        <li v-for="o in saved" :key="o.id" class="card flex items-start justify-between gap-4">
          <div>
            <span class="waypoint-label">{{ o.category }}</span>
            <NuxtLink :to="`/opportunities/${o.id}`" class="mt-1 block text-lg font-medium text-parchment hover:text-chart">
              {{ o.title }}
            </NuxtLink>
            <p class="text-sm text-navy-600">{{ o.organization }} · deadline {{ o.deadline || "rolling" }}</p>
          </div>
          <button class="btn-ghost !px-4 !py-2 text-sm" @click="unsave(o.id)">Remove</button>
        </li>
      </ul>
    </main>
  </div>
</template>