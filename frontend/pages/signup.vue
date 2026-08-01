<script setup lang="ts">
definePageMeta({ layout: false });

const { signUp, signInWithGoogle } = useAuth();
const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const done = ref(false);

async function onSubmit() {
  error.value = "";
  loading.value = true;
  try {
    await signUp(email.value, password.value);
    done.value = true;
  } catch (e: any) {
    error.value = e?.message || "Couldn't create your account. Try again.";
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
        <template v-if="!done">
          <h1 class="text-2xl font-semibold text-parchment">Chart your course</h1>
          <p class="mt-1 text-sm text-gray-400">Create an account to build your Opportunity DNA.</p>

          <form class="mt-8 space-y-4" @submit.prevent="onSubmit">
            <div>
              <label class="waypoint-label mb-2 block">Email</label>
              <input v-model="email" type="email" required class="input-field" placeholder="you@example.com" />
            </div>
            <div>
              <label class="waypoint-label mb-2 block">Password</label>
              <input v-model="password" type="password" required minlength="6" class="input-field" placeholder="At least 6 characters" />
            </div>
            <p v-if="error" class="text-sm text-coral">{{ error }}</p>
            <button type="submit" class="btn-beacon w-full" :disabled="loading">
              {{ loading ? "Creating account..." : "Create account" }}
            </button>
          </form>

          <div class="my-6 flex items-center gap-3">
            <div class="h-px flex-1 bg-navy-700" />
            <span class="text-xs text-gray-400">or</span>
            <div class="h-px flex-1 bg-navy-700" />
          </div>

          <button class="btn-ghost w-full" @click="signInWithGoogle">Continue with Google</button>

          <p class="mt-6 text-center text-sm text-gray-400">
            Already have an account?
            <NuxtLink to="/login" class="text-chart hover:underline">Sign in</NuxtLink>
          </p>
        </template>

        <template v-else>
          <h1 class="text-2xl font-semibold text-parchment">Check your inbox</h1>
          <p class="mt-3 text-gray-400">
            We sent a confirmation link to <strong class="text-parchment">{{ email }}</strong>.
            Confirm your email, then sign in to build your profile.
          </p>
          <NuxtLink to="/login" class="btn-beacon mt-6 inline-flex">Go to sign in</NuxtLink>
        </template>
      </div>
    </div>
  </div>
</template>