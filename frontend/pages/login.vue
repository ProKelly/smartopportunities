<script setup lang="ts">
definePageMeta({ layout: false });

const { signIn, signInWithGoogle } = useAuth();
const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function onSubmit() {
  error.value = "";
  loading.value = true;
  try {
    await signIn(email.value, password.value);
    await navigateTo("/dashboard");
  } catch (e: any) {
    error.value = e?.message || "Couldn't sign in. Check your details and try again.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center px-6">
    <div class="w-full max-w-md">
      <NuxtLink to="/" class="mb-8 inline-block text-sm text-gray-400 hover:text-parchment">← Back home</NuxtLink>
      <div class="card">
        <h1 class="text-2xl font-semibold text-parchment">Welcome back</h1>
        <p class="mt-1 text-sm text-gray-400">Sign in to see what's charted for you.</p>

        <form class="mt-8 space-y-4" @submit.prevent="onSubmit">
          <div>
            <label class="waypoint-label mb-2 block">Email</label>
            <input v-model="email" type="email" required class="input-field" placeholder="you@example.com" />
          </div>
          <div>
            <label class="waypoint-label mb-2 block">Password</label>
            <input v-model="password" type="password" required class="input-field" placeholder="••••••••" />
          </div>
          <p v-if="error" class="text-sm text-coral">{{ error }}</p>
          <button type="submit" class="btn-beacon w-full" :disabled="loading">
            {{ loading ? "Signing in..." : "Sign in" }}
          </button>
        </form>

        <div class="my-6 flex items-center gap-3">
          <div class="h-px flex-1 bg-navy-700" />
          <span class="text-xs text-gray-400">or</span>
          <div class="h-px flex-1 bg-navy-700" />
        </div>

        <button class="btn-ghost w-full" @click="signInWithGoogle">Continue with Google</button>

        <p class="mt-6 text-center text-sm text-gray-400">
          New here?
          <NuxtLink to="/signup" class="text-chart hover:underline">Create an account</NuxtLink>
        </p>
      </div>
    </div>
  </div>

  </template>
