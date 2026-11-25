<script lang="ts">
  const distinctions = [
    { kicker: 'Peak Day', val: '6', label: 'ships in one day', meta: '18 NOV 2026 · tied Sep/Oct', highlight: true },
    { kicker: 'Busiest Week', val: '24', label: 'ships in seven days', meta: 'WEEK OF 14 SEP 2026' },
    { kicker: 'Peak Month', val: '99', label: 'ships · 3.5 / day', meta: 'SEPTEMBER 2026' },
    { kicker: 'Longest Streak', val: '22', label: 'consecutive days shipping', meta: '09 SEP → 30 SEP 2026' },
    { kicker: 'Widest Day', val: '10', label: 'repositories at once', meta: '25 SEP 2026' },
    { kicker: 'Most-Shipped', val: 'Vidar', label: '30 ships · portfolio leader', meta: 'SOVEREIGN ENGINE' },
    { kicker: 'Inventive Day', val: '4', label: 'inventions & doctrines', meta: '09 OCT 2026' },
    { kicker: 'Debut Class', val: '4', label: 'engines first logged Nov', meta: 'EAT · PC · RDOM · RROM' },
  ];
</script>

<div class="mb-8">
  <div class="flex items-center justify-between mb-3">
    <div class="flex items-center gap-2">
      <span class="w-1.5 h-1.5 rounded-full bg-[#1E67FF]"></span>
      <h3 class="text-[12px] font-mono uppercase tracking-widest text-[#E8E8EC] font-semibold">Distinctions</h3>
    </div>
    <span class="text-[11px] font-mono text-[#5A5A6B]">Computed live from the log · No award self-nominated</span>
  </div>

  <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-4 gap-3">
    {#each distinctions as d}
      <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-3 hover:border-[#1E67FF]/30 transition-all {d.highlight ? 'bg-gradient-to-br from-[#111318] to-[#161922] border-[#1E67FF]/30' : ''}">
        <div class="text-[10px] font-mono uppercase tracking-wider text-[#8B8B9B] mb-1">{d.kicker}</div>
        <div class="text-[20px] font-mono font-semibold tracking-tight text-[#E8E8EC] {d.highlight ? 'text-[#4A8AFF]' : ''}">{d.val}</div>
        <div class="text-[11px] text-[#8B8B9B] leading-snug font-sans">{d.label}</div>
        <div class="text-[9px] font-mono text-[#5A5A6B] mt-1 uppercase tracking-tight">{d.meta}</div>
      </div>
    {/each}
  </div>
</div>
