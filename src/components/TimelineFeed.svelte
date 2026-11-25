<script lang="ts">
  import TimelineCard from './TimelineCard.svelte';
  import DistinctionsGrid from './DistinctionsGrid.svelte';

  interface Win {
    id: string;
    date: string;
    week: string;
    month: string;
    shipped: string;
    impact: string;
    repos: string[];
    spheres: string[];
    isMilestone?: boolean;
    milestoneTitle?: string;
    milestoneShort?: string;
    milestoneKind?: string;
  }

  let {
    wins = [],
    totalCount = 0,
    activeSphere = 'all',
    activeRepo = 'all',
    activeDate = '',
    milestonesOnly = false,
    searchQuery = '',
    onSelectRepo,
    onSelectSphere,
    onClearFilter
  }: {
    wins: Win[];
    totalCount: number;
    activeSphere: string;
    activeRepo: string;
    activeDate: string;
    milestonesOnly: boolean;
    searchQuery: string;
    onSelectRepo: (r: string) => void;
    onSelectSphere: (s: string) => void;
    onClearFilter: (type: string) => void;
  } = $props();

  let sortOrder = $state<'desc' | 'asc'>('desc');
  let density = $state<'expanded' | 'compact'>('expanded');

  // Sorted wins
  let sortedWins = $derived.by(() => {
    return [...wins].sort((a, b) => {
      return sortOrder === 'desc'
        ? b.date.localeCompare(a.date)
        : a.date.localeCompare(b.date);
    });
  });

  // Group by Month
  const monthNames: Record<string, string> = {
    '2026-06': 'June 2026',
    '2026-07': 'July 2026',
    '2026-08': 'August 2026',
    '2026-09': 'September 2026',
    '2026-10': 'October 2026',
    '2026-11': 'November 2026',
  };

  let groupedByMonth = $derived.by(() => {
    const groups: { monthKey: string; monthTitle: string; items: Win[] }[] = [];
    const map = new Map<string, Win[]>();

    for (const w of sortedWins) {
      if (!map.has(w.month)) {
        map.set(w.month, []);
      }
      map.get(w.month)!.push(w);
    }

    for (const [m, items] of map.entries()) {
      groups.push({
        monthKey: m,
        monthTitle: monthNames[m] || m,
        items
      });
    }

    return groups;
  });
</script>

<main class="flex-1 overflow-y-auto px-6 py-8 lg:px-10 lg:py-10 max-w-5xl mx-auto w-full space-y-8">
  <!-- Top Headline & Executive Summary -->
  <div class="space-y-4 border-b border-[#1A1D24] pb-8">
    <div class="flex items-center gap-2 text-xs font-mono text-[#1E67FF] uppercase tracking-widest font-semibold">
      <span>Evidentiary Record</span>
      <span>·</span>
      <span>June – November 2026</span>
    </div>

    <h1 class="text-3xl lg:text-4xl font-bold font-sans tracking-tight text-[#E8E8EC] leading-tight">
      Shipped Capability <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#1E67FF] via-[#4A8AFF] to-[#E8E8EC]">Continuum</span>
    </h1>

    <div class="bg-gradient-to-br from-[#111318] to-[#161922] border-l-4 border-l-[#1E67FF] border-y border-r border-[#1A1D24] rounded-r-xl p-5 shadow-lg">
      <div class="text-[11px] font-mono uppercase tracking-wider text-[#4A8AFF] font-medium mb-1">Executive Statement</div>
      <p class="text-base lg:text-lg font-sans text-[#E8E8EC] leading-relaxed font-normal">
        One architect, 198 sovereign engines, from capability kernel to operator cockpit — <strong>{totalCount} dated receipts in six months</strong>, making the case that accountability is a property of the architecture, not a report generated afterward.
      </p>
    </div>
  </div>

  <!-- Distinctions Grid -->
  {#if activeSphere === 'all' && activeRepo === 'all' && !searchQuery && !activeDate && !milestonesOnly}
    <DistinctionsGrid />
  {/if}

  <!-- Sticky Controls Header -->
  <div class="sticky top-0 z-20 bg-[#0B0C0F]/90 backdrop-blur-md py-3 border-b border-[#1A1D24] flex flex-wrap items-center justify-between gap-3">
    <!-- Active Filters & Counter -->
    <div class="flex flex-wrap items-center gap-2 text-xs font-mono">
      <span class="text-[#8B8B9B]">Showing <strong class="text-[#E8E8EC]">{sortedWins.length}</strong> of {totalCount} ships</span>

      {#if activeSphere !== 'all'}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#1E67FF]/15 border border-[#1E67FF]/40 text-[#4A8AFF]">
          <span class="capitalize">{activeSphere}</span>
          <button type="button" class="hover:text-white cursor-pointer ml-1" onclick={() => onClearFilter('sphere')}>✕</button>
        </span>
      {/if}

      {#if activeRepo !== 'all'}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#1E67FF]/15 border border-[#1E67FF]/40 text-[#4A8AFF]">
          <span>Repo: {activeRepo}</span>
          <button type="button" class="hover:text-white cursor-pointer ml-1" onclick={() => onClearFilter('repo')}>✕</button>
        </span>
      {/if}

      {#if activeDate}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#1E67FF]/15 border border-[#1E67FF]/40 text-[#4A8AFF]">
          <span>Date: {activeDate}</span>
          <button type="button" class="hover:text-white cursor-pointer ml-1" onclick={() => onClearFilter('date')}>✕</button>
        </span>
      {/if}

      {#if milestonesOnly}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#E3B341]/15 border border-[#E3B341]/40 text-[#E3B341]">
          <span>★ Inventions Only</span>
          <button type="button" class="hover:text-white cursor-pointer ml-1" onclick={() => onClearFilter('milestone')}>✕</button>
        </span>
      {/if}

      {#if searchQuery}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#1E67FF]/15 border border-[#1E67FF]/40 text-[#4A8AFF]">
          <span>"{searchQuery}"</span>
          <button type="button" class="hover:text-white cursor-pointer ml-1" onclick={() => onClearFilter('search')}>✕</button>
        </span>
      {/if}
    </div>

    <!-- View Toggles (Density & Sort) -->
    <div class="flex items-center gap-2">
      <!-- Sort Order Toggle -->
      <button
        type="button"
        class="px-2.5 py-1 rounded-md text-xs font-mono border border-[#1A1D24] bg-[#111318] text-[#8B8B9B] hover:text-white transition-colors cursor-pointer flex items-center gap-1.5"
        onclick={() => sortOrder = sortOrder === 'desc' ? 'asc' : 'desc'}
        title="Toggle sort order"
      >
        <span>{sortOrder === 'desc' ? '↓ Latest First' : '↑ Oldest First'}</span>
      </button>

      <!-- Density Toggle -->
      <button
        type="button"
        class="px-2.5 py-1 rounded-md text-xs font-mono border border-[#1A1D24] bg-[#111318] text-[#8B8B9B] hover:text-white transition-colors cursor-pointer"
        onclick={() => density = density === 'expanded' ? 'compact' : 'expanded'}
        title="Toggle card detail density"
      >
        <span>{density === 'expanded' ? 'Compact' : 'Expanded'}</span>
      </button>
    </div>
  </div>

  <!-- Timeline Stream -->
  {#if sortedWins.length === 0}
    <div class="bg-[#111318] border border-[#1A1D24] rounded-xl p-12 text-center text-[#8B8B9B] space-y-2">
      <div class="text-2xl">🔍</div>
      <div class="text-sm font-mono text-[#E8E8EC]">No ships match current filters</div>
      <p class="text-xs text-[#5A5A6B]">Try adjusting your search terms or resetting the active filters in the sidebar.</p>
    </div>
  {:else}
    <div class="space-y-10">
      {#each groupedByMonth as group}
        <section class="space-y-3">
          <!-- Month Divider Header -->
          <div class="flex items-center justify-between sticky top-12 z-10 bg-[#0B0C0F]/90 backdrop-blur-md py-2 border-b border-[#1A1D24]/60">
            <h2 class="text-xs font-mono uppercase tracking-widest text-[#E8E8EC] font-bold flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-[#1E67FF]"></span>
              <span>{group.monthTitle}</span>
            </h2>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-[#161922] text-[#8B8B9B] border border-[#1A1D24]">
              {group.items.length} {group.items.length === 1 ? 'ship' : 'ships'}
            </span>
          </div>

          <!-- Cards in Month -->
          <div class="space-y-2.5">
            {#each group.items as win (win.id)}
              <TimelineCard
                {win}
                {density}
                onSelectRepo={onSelectRepo}
                onSelectSphere={onSelectSphere}
              />
            {/each}
          </div>
        </section>
      {/each}
    </div>
  {/if}

  <!-- Footer -->
  <footer class="pt-12 pb-16 border-t border-[#1A1D24] text-center text-xs font-mono text-[#5A5A6B] space-y-2">
    <div>Nathan Walker · Ravenhelm Sovereign Fleet</div>
    <div class="text-[11px] text-[#3E424E]">Every ship dated · Every claim attributable · Zero SaaS scaffolding</div>
  </footer>
</main>
