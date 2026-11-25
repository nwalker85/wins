<script lang="ts">
  import winsData from './data/wins.json';
  import Sidebar from './components/Sidebar.svelte';
  import TimelineFeed from './components/TimelineFeed.svelte';
  import DrawerModal from './components/DrawerModal.svelte';

  let searchQuery = $state('');
  let selectedSphere = $state('all');
  let selectedRepo = $state('all');
  let milestonesOnly = $state(false);
  let selectedDate = $state('');

  let isDrawerOpen = $state(false);
  let drawerTab = $state<'thesis' | 'infrastructure' | 'registry'>('thesis');
  let isMobileSidebarOpen = $state(false);

  // Reactive filtering
  let filteredWins = $derived.by(() => {
    return winsData.filter(w => {
      // 1. Search Query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inShipped = w.shipped.toLowerCase().includes(q);
        const inImpact = w.impact.toLowerCase().includes(q);
        const inRepos = w.repos.some(r => r.toLowerCase().includes(q));
        const inMilestones = w.milestones?.some(m => m.title.toLowerCase().includes(q) || m.short.toLowerCase().includes(q));
        if (!inShipped && !inImpact && !inRepos && !inMilestones) {
          return false;
        }
      }

      // 2. Sphere
      if (selectedSphere !== 'all') {
        if (!w.spheres.includes(selectedSphere)) {
          return false;
        }
      }

      // 3. Repo
      if (selectedRepo !== 'all') {
        if (!w.repos.includes(selectedRepo)) {
          return false;
        }
      }

      // 4. Milestone
      if (milestonesOnly) {
        if (!w.isMilestone) {
          return false;
        }
      }

      // 5. Date
      if (selectedDate) {
        if (w.date !== selectedDate) {
          return false;
        }
      }

      return true;
    });
  });

  function handleOpenDrawer(tab: 'thesis' | 'infrastructure' | 'registry') {
    drawerTab = tab;
    isDrawerOpen = true;
  }

  function handleClearFilter(type: string) {
    if (type === 'sphere') selectedSphere = 'all';
    if (type === 'repo') selectedRepo = 'all';
    if (type === 'date') selectedDate = '';
    if (type === 'milestone') milestonesOnly = false;
    if (type === 'search') searchQuery = '';
  }
</script>

<div class="h-screen w-screen overflow-hidden flex flex-col lg:flex-row bg-[#0B0C0F] text-[#E8E8EC] font-sans selection:bg-[#1E67FF] selection:text-white">
  <!-- Mobile Header Bar -->
  <div class="lg:hidden flex items-center justify-between px-4 py-3 bg-[#111318] border-b border-[#1A1D24] shrink-0 z-30">
    <div class="flex items-center gap-2">
      <div class="w-6 h-6 rounded bg-[#1E67FF] text-white font-mono font-bold text-xs flex items-center justify-center">
        NW
      </div>
      <div class="text-xs font-mono font-bold text-[#E8E8EC] uppercase">Done Log · 295 Ships</div>
    </div>
    <button
      type="button"
      class="px-2.5 py-1 rounded bg-[#161922] border border-[#1A1D24] text-xs font-mono text-[#8B8B9B] hover:text-white"
      onclick={() => isMobileSidebarOpen = !isMobileSidebarOpen}
    >
      {isMobileSidebarOpen ? 'Close Menu ✕' : 'Filters & Metrics ☰'}
    </button>
  </div>

  <!-- Mobile Sidebar Drawer -->
  {#if isMobileSidebarOpen}
    <div class="lg:hidden fixed inset-0 top-[49px] z-40 bg-[#0B0C0F] overflow-y-auto">
      <Sidebar
        wins={winsData}
        bind:searchQuery
        bind:selectedSphere
        bind:selectedRepo
        bind:milestonesOnly
        bind:selectedDate
        onOpenDrawer={(tab) => {
          isMobileSidebarOpen = false;
          handleOpenDrawer(tab);
        }}
      />
    </div>
  {/if}

  <!-- Desktop Fixed Sidebar -->
  <div class="hidden lg:block h-full">
    <Sidebar
      wins={winsData}
      bind:searchQuery
      bind:selectedSphere
      bind:selectedRepo
      bind:milestonesOnly
      bind:selectedDate
      onOpenDrawer={handleOpenDrawer}
    />
  </div>

  <!-- Main Scrollable Timeline Feed -->
  <TimelineFeed
    wins={filteredWins}
    totalCount={winsData.length}
    activeSphere={selectedSphere}
    activeRepo={selectedRepo}
    activeDate={selectedDate}
    {milestonesOnly}
    {searchQuery}
    onSelectRepo={(r) => selectedRepo = r}
    onSelectSphere={(s) => selectedSphere = s}
    onClearFilter={handleClearFilter}
  />

  <!-- Slide-Over Drawer for Thesis, Infrastructure, Registry -->
  <DrawerModal
    isOpen={isDrawerOpen}
    activeTab={drawerTab}
    onClose={() => isDrawerOpen = false}
  />
</div>
