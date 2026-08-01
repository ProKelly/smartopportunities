<script setup lang="ts">
definePageMeta({ layout: false });

const waypoints = [
  { label: "Chart your profile", copy: "Answer a few plain questions — skills, goals, where you want to go. No 40-field forms." },
  { label: "Get your Opportunity DNA", copy: "Our AI reads your profile and summarizes your strengths, gaps, and best-fit categories." },
  { label: "See your matches", copy: "Semantic search plus an AI reasoning pass ranks the opportunities that actually fit — with a plain-English reason for each." },
  { label: "Follow your roadmap", copy: "Tell us a goal and get a realistic, month-by-month plan to get there." },
  { label: "Apply, prepared", copy: "CV notes, a cover-letter draft, and interview tips generated for the specific opportunity you're chasing." },
];
</script>

<template>
  <div class="relative overflow-hidden">
    <!-- Hero -->
    <section class="relative mx-auto flex min-h-[92vh] max-w-7xl flex-col items-center justify-center px-6 text-center">
      <!-- Signature: radar sweep behind the headline -->
      <div class="pointer-events-none absolute left-1/2 top-1/2 -z-0 h-[640px] w-[640px] -translate-x-1/2 -translate-y-1/2 opacity-70">
        <svg viewBox="0 0 640 640" class="h-full w-full">
          <circle cx="320" cy="320" r="120" fill="none" stroke="#262E52" stroke-width="1" />
          <circle cx="320" cy="320" r="220" fill="none" stroke="#262E52" stroke-width="1" />
          <circle cx="320" cy="320" r="300" fill="none" stroke="#1B2140" stroke-width="1" />
          <g class="radar-sweep" style="transform-origin: 320px 320px;">
            <path d="M320 320 L320 20 A300 300 0 0 1 578 170 Z" fill="url(#sweepGradient)" />
          </g>
          <defs>
            <linearGradient id="sweepGradient" x1="320" y1="320" x2="578" y2="170" gradientUnits="userSpaceOnUse">
              <stop offset="0%" stop-color="#F2B84B" stop-opacity="0.35" />
              <stop offset="100%" stop-color="#F2B84B" stop-opacity="0" />
            </linearGradient>
          </defs>
          <!-- charted opportunity points -->
          <circle cx="420" cy="220" r="5" fill="#4FD1C5" class="pulse-ring" style="transform-origin: 420px 220px;" />
          <circle cx="420" cy="220" r="4" fill="#4FD1C5" />
          <circle cx="230" cy="420" r="4" fill="#F2B84B" />
          <circle cx="230" cy="420" r="5" fill="#F2B84B" class="pulse-ring" style="transform-origin: 230px 420px; animation-delay: 1s;" />
          <circle cx="470" cy="410" r="4" fill="#4FD1C5" />
        </svg>
      </div>

      <p class="waypoint-label relative z-10 mb-6">Your AI-powered opportunity navigator</p>
      <h1 class="relative z-10 max-w-3xl text-4xl font-semibold leading-tight text-parchment sm:text-6xl">
        Stop searching for opportunities.
        <span class="text-signal">Get charted a course to them.</span>
      </h1>
      <p class="relative z-10 mt-6 max-w-xl text-lg text-gray-300">
        Tell OpportunityOS AI who you are. It finds the scholarships, jobs, grants, and
        competitions that fit — explains why — and builds the plan to get you there.
      </p>
      <div class="relative z-10 mt-10 flex flex-col gap-4 sm:flex-row">
        <NuxtLink to="/signup" class="btn-beacon">Chart my course</NuxtLink>
        <NuxtLink to="/login" class="btn-ghost">I already have an account</NuxtLink>
      </div>
    </section>

    <!-- Process waypoints (a real sequence, so numbering is meaningful) -->
    <section class="mx-auto max-w-5xl px-6 pb-32">
      <h2 class="mb-12 text-center text-2xl font-semibold text-parchment">How the course is charted</h2>
      <ol class="space-y-6">
        <li v-for="(wp, i) in waypoints" :key="wp.label" class="card flex items-start gap-6">
          <span class="font-mono text-sm text-signal">{{ String(i + 1).padStart(2, "0") }}</span>
          <div>
            <h3 class="text-lg font-medium text-parchment">{{ wp.label }}</h3>
            <p class="mt-1 text-gray-400">{{ wp.copy }}</p>
          </div>
        </li>
      </ol>
    </section>

    <footer class="border-t border-navy-800 py-8 text-center text-sm text-navy-600">
      OpportunityOS AI — built for students and early-career professionals navigating what's next.
    </footer>
  </div>

  </template>