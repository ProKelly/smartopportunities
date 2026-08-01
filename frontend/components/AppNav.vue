<script setup lang="ts">
import { ref } from 'vue';

const { user, signOut } = useAuth();
const route = useRoute();
const isOpen = ref(false);

const links = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/opportunities/find", label: "Find Opportunities" },
  { to: "/opportunities/saved", label: "Saved" },
  { to: "/roadmap", label: "Roadmap" },
  { to: "/career-coach", label: "Career Coach" },
  { to: "/profile", label: "Profile" },
];
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-navy-800 bg-navy-950/90 backdrop-blur-sm">
    <nav class="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
      <div class="flex items-center gap-4">
        <!-- Hamburger Menu Button -->
        <button 
          @click="isOpen = !isOpen" 
          class="text-navy-600 hover:text-parchment md:hidden focus:outline-none"
          aria-label="Toggle Menu"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!isOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <NuxtLink to="/dashboard" class="flex items-center gap-2">
          <span class="text-lg font-display font-semibold text-parchment">OpportunityOS</span>
          <span class="rounded-full bg-signal/15 px-2 py-0.5 text-[10px] font-mono uppercase tracking-widest text-signal">AI</span>
        </NuxtLink>
      </div>

      <!-- Desktop Links -->
      <ul class="hidden items-center gap-6 md:flex">
        <li v-for="link in links" :key="link.to">
          <NuxtLink
            :to="link.to"
            class="text-sm font-medium transition-colors"
            :class="route.path.startsWith(link.to) ? 'text-signal' : 'text-navy-600 hover:text-parchment'"
          >
            {{ link.label }}
          </NuxtLink>
        </li>
      </ul>

      <div class="flex items-center gap-4">
        <ClientOnly>
          <span class="hidden text-sm text-navy-600 sm:inline">
            {{ user?.email }}
          </span>
        </ClientOnly>
        <button class="btn-ghost !px-4 !py-2 text-sm" @click="signOut">Sign out</button>
      </div>
    </nav>

    <!-- Mobile Navigation Drawer -->
    <div v-if="isOpen" class="border-b border-navy-800 bg-navy-950 px-6 py-4 md:hidden">
      <ul class="space-y-3">
        <li v-for="link in links" :key="link.to">
          <NuxtLink
            :to="link.to"
            @click="isOpen = false"
            class="block text-sm font-medium transition-colors"
            :class="route.path.startsWith(link.to) ? 'text-signal' : 'text-navy-600 hover:text-parchment'"
          >
            {{ link.label }}
          </NuxtLink>
        </li>
      </ul>
    </div>
  </header>
</template>