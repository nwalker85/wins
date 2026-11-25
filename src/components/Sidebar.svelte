<script lang="ts">
  import MiniHeatmap from './MiniHeatmap.svelte';

  interface Win {
    id: string;
    date: string;
    shipped: string;
    impact: string;
    repos: string[];
    spheres: string[];
    isMilestone?: boolean;
  }

  let {
    wins = [],
    searchQuery = $bindable(''),
    selectedSphere = $bindable('all'),
    selectedRepo = $bindable('all'),
    milestonesOnly = $bindable(false),
    selectedDate = $bindable(''),
    onOpenDrawer
  }: {
    wins: Win[];
    searchQuery: string;
    selectedSphere: string;
    selectedRepo: string;
    milestonesOnly: boolean;
    selectedDate: string;
    onOpenDrawer: (tab: 'thesis' | 'infrastructure' | 'registry') => void;
  } = $props();

  const spheresList = [
    { id: 'all', name: 'All Spheres', color: '#E8E8EC' },
    { id: 'execution', name: 'Flight Deck & Execution', color: '#1E67FF' },
    { id: 'platform', name: 'Platform & Infra', color: '#8E939B' },
    { id: 'topology', name: 'Topology & Governance', color: '#D2A93B' },
    { id: 'sensors', name: 'Sensors & Telemetry', color: '#3D5F8F' },
    { id: 'voice', name: 'Voice & Presence', color: '#2DCB70' },
    { id: 'identity', name: 'Identity & PKI', color: '#B8BCC4' },
  ];

  // Top engines by frequency
  let topRepos = $derived.by(() => {
    const counts = new Map<string, number>();
    for (const w of wins) {
      for (const r of w.repos) {
        counts.set(r, (counts.get(r) || 0) + 1);
      }
    }
    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 14);
  });

  const milestoneCount = $derived(wins.filter(w => w.isMilestone).length);

  function resetAllFilters() {
    searchQuery = '';
    selectedSphere = 'all';
    selectedRepo = 'all';
    milestonesOnly = false;
    selectedDate = '';
  }

  const hasActiveFilters = $derived(
    searchQuery.trim() !== '' ||
    selectedSphere !== 'all' ||
    selectedRepo !== 'all' ||
    milestonesOnly ||
    selectedDate !== ''
  );
</script>

<aside class="w-full lg:w-[380px] shrink-0 bg-[#0B0C0F] border-r border-[#1A1D24] p-5 flex flex-col gap-5 overflow-y-auto h-full">
  <!-- Brand / Header -->
  <div>
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2.5">
        <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-[#1E67FF] to-[#111318] border border-[#1E67FF]/40 flex items-center justify-center font-mono font-bold text-xs text-white shadow-[0_0_12px_rgba(30,103,255,0.25)]">
          NW
        </div>
        <div>
          <h1 class="text-xs font-mono font-bold uppercase tracking-wider text-[#E8E8EC]">Nathan Walker</h1>
          <p class="text-[10px] font-mono text-[#5A5A6B] uppercase tracking-tight">Sovereign Computing Fleet</p>
        </div>
      </div>
      <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-mono text-[#2DCB70] bg-[#2DCB70]/10 border border-[#2DCB70]/30">
        <span class="w-1.5 h-1.5 rounded-full bg-[#2DCB70] animate-pulse"></span>
        <span>CONTINUUM</span>
      </span>
    </div>

    <div class="text-[13px] leading-relaxed text-[#8B8B9B] font-sans">
      The evidentiary record of an autonomous engineering fleet: 198 sovereign engines from capability kernel to operator cockpit.
    </div>
  </div>

  <!-- Search Box -->
  <div class="relative">
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#5A5A6B]">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
      </svg>
    </div>
    <input
      type="text"
      bind:value={searchQuery}
      placeholder="Search 295 ships (PR #, keywords)..."
      class="w-full bg-[#111318] border border-[#1A1D24] rounded-lg pl-9 pr-8 py-2 text-xs text-[#E8E8EC] placeholder-[#5A5A6B] focus:outline-none focus:border-[#1E67FF] transition-all font-mono"
    />
    {#if searchQuery}
      <button
        type="button"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-xs text-[#8B8B9B] hover:text-white cursor-pointer"
        onclick={() => searchQuery = ''}
      >
        ✕
      </button>
    {/if}
  </div>

  <!-- KPI Badges -->
  <div class="grid grid-cols-2 gap-2 text-center font-mono">
    <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-2.5">
      <div class="text-[10px] uppercase text-[#8B8B9B]">Dated Ships</div>
      <div class="text-lg font-bold text-[#E8E8EC]">{wins.length}</div>
      <div class="text-[9px] text-[#5A5A6B]">100% Attributable</div>
    </div>
    <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-2.5">
      <div class="text-[10px] uppercase text-[#8B8B9B]">Working Days</div>
      <div class="text-lg font-bold text-[#4A8AFF]">116</div>
      <div class="text-[9px] text-[#5A5A6B]">24 Active Weeks</div>
    </div>
  </div>

  <!-- Reset Filters Pill -->
  {#if hasActiveFilters}
    <div class="flex items-center justify-between bg-[#1E67FF]/10 border border-[#1E67FF]/30 rounded-lg px-3 py-1.5 text-xs font-mono text-[#4A8AFF]">
      <span>Filters active</span>
      <button
        type="button"
        class="text-[11px] underline hover:text-white cursor-pointer"
        onclick={resetAllFilters}
      >
        Reset All
      </button>
    </div>
  {/if}

  <!-- Milestone Filter -->
  <button
    type="button"
    class="w-full py-2 px-3 rounded-lg border text-xs font-mono flex items-center justify-between transition-all cursor-pointer {milestonesOnly ? 'bg-[#E3B341]/15 border-[#E3B341] text-[#E3B341] font-semibold shadow-[0_0_14px_rgba(227,179,65,0.2)]' : 'bg-[#111318] border-[#1A1D24] text-[#8B8B9B] hover:text-white hover:border-[#1A1D24]'}"
    onclick={() => milestonesOnly = !milestonesOnly}
  >
    <div class="flex items-center gap-2">
      <span class="text-[#E3B341]">★</span>
      <span>Inventions & Doctrines</span>
    </div>
    <span class="px-1.5 py-0.5 rounded text-[10px] bg-[#161922] font-mono">{milestoneCount}</span>
  </button>

  <!-- Spheres Filter -->
  <div>
    <div class="text-[11px] font-mono uppercase tracking-wider text-[#8B8B9B] mb-2">Strategic Spheres</div>
    <div class="space-y-1">
      {#each spheresList as s}
        {@const isActive = selectedSphere === s.id}
        <button
          type="button"
          class="w-full px-3 py-1.5 rounded-lg text-xs font-sans flex items-center justify-between transition-all cursor-pointer {isActive ? 'bg-[#1E67FF] text-white font-medium shadow-[0_0_12px_rgba(30,103,255,0.3)]' : 'text-[#8B8B9B] hover:text-[#E8E8EC] hover:bg-[#111318]'}"
          onclick={() => selectedSphere = s.id}
        >
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full" style="background-color: {s.color}"></span>
            <span>{s.name}</span>
          </div>
          {#if s.id === 'all'}
            <span class="text-[11px] font-mono opacity-60">{wins.length}</span>
          {/if}
        </button>
      {/each}
    </div>
  </div>

  <!-- Top Engines / Repos -->
  <div>
    <div class="flex items-center justify-between text-[11px] font-mono uppercase tracking-wider text-[#8B8B9B] mb-2">
      <span>Top Engines</span>
      {#if selectedRepo !== 'all'}
        <button
          type="button"
          class="text-[10px] text-[#4A8AFF] hover:underline cursor-pointer"
          onclick={() => selectedRepo = 'all'}
        >
          Clear
        </button>
      {/if}
    </div>
    <div class="flex flex-wrap gap-1.5">
      {#each topRepos as [repo, count]}
        {@const isActive = selectedRepo === repo}
        <button
          type="button"
          class="px-2 py-1 rounded text-[11px] font-mono border transition-all cursor-pointer {isActive ? 'bg-[#1E67FF] border-[#1E67FF] text-white font-semibold' : 'bg-[#111318] border-[#1A1D24] text-[#8B8B9B] hover:text-white hover:border-[#1E67FF]/40'}"
          onclick={() => selectedRepo = isActive ? 'all' : repo}
        >
          <span>{repo}</span>
          <span class="opacity-50 text-[10px]">({count})</span>
        </button>
      {/each}
    </div>
  </div>

  <!-- Mini Heatmap -->
  <MiniHeatmap
    {wins}
    {selectedDate}
    onSelectDate={(d) => selectedDate = d}
  />

  <!-- Reference Drawers -->
  <div class="pt-2 border-t border-[#1A1D24] space-y-2">
    <button
      type="button"
      class="w-full py-2.5 px-3 rounded-lg bg-[#111318] border border-[#1A1D24] text-xs font-mono uppercase tracking-wider text-[#8B8B9B] hover:text-[#4A8AFF] hover:border-[#1E67FF]/30 flex items-center justify-between transition-colors cursor-pointer"
      onclick={() => onOpenDrawer('thesis')}
    >
      <span>Architectural Thesis (7 Axioms)</span>
      <span>→</span>
    </button>
    <button
      type="button"
      class="w-full py-2.5 px-3 rounded-lg bg-[#111318] border border-[#1A1D24] text-xs font-mono uppercase tracking-wider text-[#8B8B9B] hover:text-[#4A8AFF] hover:border-[#1E67FF]/30 flex items-center justify-between transition-colors cursor-pointer"
      onclick={() => onOpenDrawer('infrastructure')}
    >
      <span>Estate Telemetry & Hardware</span>
      <span>→</span>
    </button>
    <button
      type="button"
      class="w-full py-2.5 px-3 rounded-lg bg-[#111318] border border-[#1A1D24] text-xs font-mono uppercase tracking-wider text-[#8B8B9B] hover:text-[#4A8AFF] hover:border-[#1E67FF]/30 flex items-center justify-between transition-colors cursor-pointer"
      onclick={() => onOpenDrawer('registry')}
    >
      <span>Engine Registry (198/211)</span>
      <span>→</span>
    </button>
  </div>
</aside>
