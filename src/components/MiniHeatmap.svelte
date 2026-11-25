<script lang="ts">
  interface Win {
    id: string;
    date: string;
    shipped: string;
    impact: string;
    repos: string[];
    spheres: string[];
    isMilestone?: boolean;
  }

  let { wins = [], selectedDate = '', onSelectDate }: {
    wins: Win[];
    selectedDate: string;
    onSelectDate: (date: string) => void;
  } = $props();

  // Aggregate count by date
  let dateCounts = $derived.by(() => {
    const map = new Map<string, number>();
    for (const w of wins) {
      map.set(w.date, (map.get(w.date) || 0) + 1);
    }
    return map;
  });

  const months = [
    { name: 'Jun', year: 2026, month: 5, days: 30 },
    { name: 'Jul', year: 2026, month: 6, days: 31 },
    { name: 'Aug', year: 2026, month: 7, days: 31 },
    { name: 'Sep', year: 2026, month: 8, days: 30 },
    { name: 'Oct', year: 2026, month: 9, days: 31 },
    { name: 'Nov', year: 2026, month: 10, days: 30, clamp: 23 },
  ];

  function getLevel(count: number): number {
    if (!count) return 0;
    if (count === 1) return 1;
    if (count <= 2) return 2;
    if (count <= 4) return 3;
    return 4;
  }

  function getLevelClass(level: number): string {
    if (level === 0) return 'bg-[#161922]';
    if (level === 1) return 'bg-[#1E67FF]/30';
    if (level === 2) return 'bg-[#1E67FF]/60';
    if (level === 3) return 'bg-[#1E67FF]';
    return 'bg-[#4A8AFF]';
  }

  function formatDate(year: number, month: number, day: number): string {
    const m = String(month + 1).padStart(2, '0');
    const d = String(day).padStart(2, '0');
    return `${year}-${m}-${d}`;
  }
</script>

<div class="space-y-2">
  <div class="flex items-center justify-between text-[11px] font-mono text-[#8B8B9B] uppercase tracking-wider">
    <span>Temporal Heatmap (Jun–Nov)</span>
    <span class="text-[10px] text-[#5A5A6B]">Click day to jump</span>
  </div>

  <div class="grid grid-cols-6 gap-2 bg-[#111318] p-2.5 rounded-lg border border-[#1A1D24]">
    {#each months as m}
      <div class="flex flex-col items-center">
        <span class="text-[10px] font-mono text-[#8B8B9B] mb-1.5">{m.name}</span>
        <div class="grid grid-cols-5 gap-1">
          {#each Array.from({ length: m.clamp || m.days }, (_, i) => i + 1) as day}
            {@const dateStr = formatDate(m.year, m.month, day)}
            {@const count = dateCounts.get(dateStr) || 0}
            {@const level = getLevel(count)}
            {@const isSelected = selectedDate === dateStr}
            <button
              type="button"
              class="w-2.5 h-2.5 rounded-[2px] transition-all duration-150 cursor-pointer {getLevelClass(level)} {isSelected ? 'ring-1 ring-white' : ''}"
              title="{dateStr}: {count} {count === 1 ? 'ship' : 'ships'}"
              onclick={() => onSelectDate(isSelected ? '' : dateStr)}
            ></button>
          {/each}
        </div>
      </div>
    {/each}
  </div>

  <div class="flex items-center justify-between text-[10px] font-mono text-[#5A5A6B] pt-0.5">
    <span>Less</span>
    <div class="flex items-center gap-1">
      <div class="w-2 h-2 rounded-[2px] bg-[#161922]"></div>
      <div class="w-2 h-2 rounded-[2px] bg-[#1E67FF]/30"></div>
      <div class="w-2 h-2 rounded-[2px] bg-[#1E67FF]/60"></div>
      <div class="w-2 h-2 rounded-[2px] bg-[#1E67FF]"></div>
      <div class="w-2 h-2 rounded-[2px] bg-[#4A8AFF]"></div>
    </div>
    <span>5+ / day</span>
  </div>
</div>
