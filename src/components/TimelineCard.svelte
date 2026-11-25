<script lang="ts">
  interface Milestone {
    title: string;
    short: string;
    kind: 'invention' | 'doctrine';
  }

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
    milestones?: Milestone[];
    milestoneTitle?: string;
    milestoneShort?: string;
    milestoneKind?: string;
  }

  let { win, density = 'expanded', onSelectRepo, onSelectSphere }: {
    win: Win;
    density?: 'expanded' | 'compact';
    onSelectRepo?: (repo: string) => void;
    onSelectSphere?: (sphere: string) => void;
  } = $props();

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  let dayOfWeek = $derived.by(() => {
    const d = new Date(win.date + 'T12:00:00Z');
    return dayNames[d.getUTCDay()];
  });

  const sphereColors: Record<string, string> = {
    execution: '#1E67FF',
    platform: '#8E939B',
    topology: '#D2A93B',
    sensors: '#3D5F8F',
    voice: '#2DCB70',
    identity: '#B8BCC4',
  };

  const hasInvention = $derived(win.milestones?.some(m => m.kind === 'invention') || win.milestoneKind === 'invention');
  const hasDoctrine = $derived(win.milestones?.some(m => m.kind === 'doctrine') || win.milestoneKind === 'doctrine');
  const milestoneLabel = $derived(
    win.milestones?.[0]?.short || win.milestoneShort || (hasInvention ? 'Invention' : hasDoctrine ? 'Doctrine' : '')
  );
</script>

<article
  class="command-card rounded-lg p-4 transition-all duration-200 border border-[#1A1D24] bg-[#161922] hover:bg-[#1A1D28] hover:border-[#1E67FF]/40 group"
  class:p-3={density === 'compact'}
  id="{win.id}"
>
  <!-- Meta Header -->
  <div class="flex flex-wrap items-center justify-between gap-2 mb-2 font-mono text-[12px]">
    <div class="flex items-center gap-2">
      <span class="text-[#E8E8EC] font-medium tracking-tight">{win.date}</span>
      <span class="text-[#5A5A6B] text-[11px] font-sans">({dayOfWeek})</span>

      <!-- Sphere Tag -->
      {#each win.spheres as sp}
        <button
          type="button"
          class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] bg-[#111318] border border-[#1A1D24] text-[#8B8B9B] hover:text-white transition-colors cursor-pointer"
          onclick={() => onSelectSphere?.(sp)}
          title="Filter by sphere: {sp}"
        >
          <span class="w-1.5 h-1.5 rounded-full" style="background-color: {sphereColors[sp] || '#8B8B9B'}"></span>
          <span class="capitalize">{sp}</span>
        </button>
      {/each}
    </div>

    <div class="flex items-center gap-1.5">
      <!-- Milestones: Invention or Doctrine -->
      {#if hasInvention}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium text-[#E3B341] bg-[#E3B341]/10 border border-[#E3B341]/30 tracking-wide shadow-[0_0_12px_rgba(227,179,65,0.15)]">
          <span>★</span>
          <span>{milestoneLabel || 'INVENTION'}</span>
        </span>
      {:else if hasDoctrine}
        <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-mono font-medium text-[#4A8AFF] bg-[#1E67FF]/10 border border-[#1E67FF]/30 tracking-wide shadow-[0_0_12px_rgba(30,103,255,0.15)]">
          <span>◆</span>
          <span>{milestoneLabel || 'DOCTRINE'}</span>
        </span>
      {/if}

      <!-- Repositories -->
      {#each win.repos as repo}
        <button
          type="button"
          class="px-2 py-0.5 rounded text-[11px] font-mono bg-[#111318] border border-[#1A1D24] text-[#8B8B9B] hover:text-[#4A8AFF] hover:border-[#1E67FF]/40 transition-colors cursor-pointer"
          onclick={() => onSelectRepo?.(repo)}
          title="Filter by repository: {repo}"
        >
          {repo}
        </button>
      {/each}
    </div>
  </div>

  <!-- Shipped Title -->
  <div class="text-[14px] leading-relaxed text-[#E8E8EC] font-sans font-normal mb-1.5 group-hover:text-white transition-colors">
    {win.shipped}
  </div>

  <!-- So What / Impact -->
  {#if density === 'expanded'}
    <div class="flex items-start gap-2 text-[13px] leading-relaxed text-[#8B8B9B] font-sans pl-1 border-l-2 border-[#1A1D24] group-hover:border-[#1E67FF]/40 transition-colors mt-2 pt-0.5">
      <span class="text-[#1E67FF] font-mono font-bold select-none shrink-0">→</span>
      <p class="text-[#8B8B9B]">{win.impact}</p>
    </div>
  {/if}
</article>
