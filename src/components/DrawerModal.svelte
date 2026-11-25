<script lang="ts">
  import thesisData from '../data/thesis.json';
  import infraData from '../data/estate-infra.json';
  import estateData from '../data/estate.json';

  let { isOpen = false, activeTab = 'thesis', onClose }: {
    isOpen: boolean;
    activeTab: 'thesis' | 'infrastructure' | 'registry';
    onClose: () => void;
  } = $props();

  let registrySearch = $state('');

  let filteredEngines = $derived.by(() => {
    if (!registrySearch.trim()) return estateData;
    const q = registrySearch.toLowerCase();
    return estateData.filter(e => e.name.toLowerCase().includes(q) || (e.desc && e.desc.toLowerCase().includes(q)));
  });
</script>

{#if isOpen}
  <!-- Backdrop -->
  <div
    class="fixed inset-0 bg-black/80 backdrop-blur-md z-40 transition-opacity"
    onclick={onClose}
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    tabindex="0"
    role="button"
    aria-label="Close modal overlay"
  ></div>

  <!-- Slide-Over Drawer -->
  <div class="fixed inset-y-0 right-0 w-full max-w-3xl bg-[#0B0C0F] border-l border-[#1A1D24] shadow-2xl z-50 flex flex-col overflow-hidden">
    <!-- Header -->
    <div class="flex items-center justify-between px-6 py-4 border-b border-[#1A1D24] bg-[#111318]">
      <div class="flex items-center gap-3">
        <button
          type="button"
          class="px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all cursor-pointer {activeTab === 'thesis' ? 'bg-[#1E67FF] text-white font-medium' : 'text-[#8B8B9B] hover:text-white bg-[#161922]'}"
          onclick={() => activeTab = 'thesis'}
        >
          Architectural Thesis
        </button>
        <button
          type="button"
          class="px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all cursor-pointer {activeTab === 'infrastructure' ? 'bg-[#1E67FF] text-white font-medium' : 'text-[#8B8B9B] hover:text-white bg-[#161922]'}"
          onclick={() => activeTab = 'infrastructure'}
        >
          Estate Telemetry
        </button>
        <button
          type="button"
          class="px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider transition-all cursor-pointer {activeTab === 'registry' ? 'bg-[#1E67FF] text-white font-medium' : 'text-[#8B8B9B] hover:text-white bg-[#161922]'}"
          onclick={() => activeTab = 'registry'}
        >
          Engine Registry ({estateData.length})
        </button>
      </div>

      <button
        type="button"
        class="w-8 h-8 rounded-lg bg-[#161922] border border-[#1A1D24] flex items-center justify-center text-[#8B8B9B] hover:text-white transition-colors cursor-pointer"
        onclick={onClose}
        aria-label="Close panel"
      >
        ✕
      </button>
    </div>

    <!-- Scrollable Content -->
    <div class="flex-1 overflow-y-auto p-6 space-y-6 text-[#E8E8EC]">
      {#if activeTab === 'thesis'}
        <div>
          <div class="text-[11px] font-mono uppercase tracking-widest text-[#1E67FF] font-semibold mb-1">Foundational Doctrine</div>
          <h2 class="text-2xl font-bold font-sans tracking-tight mb-2">{thesisData.title}</h2>
          <p class="text-sm font-mono text-[#8B8B9B] mb-6">{thesisData.subtitle}</p>

          <!-- Diagnosis -->
          <div class="bg-[#111318] border border-[#1A1D24] rounded-xl p-5 mb-6">
            <h3 class="text-xs font-mono uppercase tracking-wider text-[#4A8AFF] font-medium mb-2">The Diagnosis</h3>
            <p class="text-[13px] leading-relaxed text-[#8B8B9B]">{thesisData.diagnosis}</p>
          </div>

          <!-- The Seven Axioms -->
          <div class="mb-6">
            <h3 class="text-xs font-mono uppercase tracking-wider text-[#E8E8EC] font-semibold mb-3">The Seven Non-Negotiable Axioms</h3>
            <div class="space-y-2">
              {#each thesisData.axioms as axiom, i}
                <div class="flex items-start gap-3 bg-[#111318] border border-[#1A1D24] rounded-lg p-3">
                  <span class="w-6 h-6 rounded-full bg-[#1E67FF]/10 border border-[#1E67FF]/30 text-[#4A8AFF] font-mono text-xs flex items-center justify-center shrink-0">
                    {i + 1}
                  </span>
                  <div class="text-[13px] text-[#E8E8EC] font-sans font-medium pt-0.5">{axiom}</div>
                </div>
              {/each}
            </div>
          </div>

          <!-- The Four Pillars -->
          <div class="space-y-4 mb-6">
            <h3 class="text-xs font-mono uppercase tracking-wider text-[#E8E8EC] font-semibold mb-1">The 4-Pillar Sovereign Architecture</h3>
            {#each thesisData.pillars as pillar}
              <div class="bg-[#111318] border border-[#1A1D24] rounded-xl p-5 hover:border-[#1E67FF]/30 transition-colors">
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-xs font-mono text-[#1E67FF] font-bold">Pillar {pillar.roman} ·</span>
                  <h4 class="text-sm font-sans font-semibold text-[#E8E8EC]">{pillar.title}</h4>
                </div>
                <div class="text-[11px] font-mono text-[#5A5A6B] mb-3">{pillar.subtitle}</div>
                <p class="text-[13px] leading-relaxed text-[#8B8B9B]">{pillar.body}</p>
              </div>
            {/each}
          </div>

          <!-- Receipts -->
          <div class="bg-gradient-to-br from-[#111318] to-[#161922] border border-[#1E67FF]/30 rounded-xl p-5">
            <h3 class="text-xs font-mono uppercase tracking-wider text-[#4A8AFF] font-medium mb-1">The Receipts</h3>
            <p class="text-[13px] leading-relaxed text-[#8B8B9B]">{thesisData.receipts}</p>
          </div>
        </div>

      {:else if activeTab === 'infrastructure'}
        <div>
          <div class="text-[11px] font-mono uppercase tracking-widest text-[#1E67FF] font-semibold mb-1">Physical Surface & Heimdall Telemetry</div>
          <h2 class="text-2xl font-bold font-sans tracking-tight mb-2">The Estate Infrastructure</h2>
          <p class="text-sm font-mono text-[#8B8B9B] mb-6">Live inventory · 3 sites · 628 observed devices</p>

          <!-- Telemetry Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
            <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-3">
              <div class="text-[10px] font-mono uppercase text-[#8B8B9B] mb-1">Physical Sites</div>
              <div class="text-xl font-mono font-semibold text-[#E8E8EC]">{infraData.sites}</div>
              <div class="text-[10px] text-[#5A5A6B]">Lab, Mobile, Travel</div>
            </div>
            <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-3">
              <div class="text-[10px] font-mono uppercase text-[#8B8B9B] mb-1">Devices Observed</div>
              <div class="text-xl font-mono font-semibold text-[#4A8AFF]">{infraData.devices_catalogued}</div>
              <div class="text-[10px] text-[#5A5A6B]">Identities persist</div>
            </div>
            <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-3">
              <div class="text-[10px] font-mono uppercase text-[#8B8B9B] mb-1">Services Running</div>
              <div class="text-xl font-mono font-semibold text-[#2DCB70]">{infraData.services_running}</div>
              <div class="text-[10px] text-[#5A5A6B]">Resident daemons</div>
            </div>
            <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-3">
              <div class="text-[10px] font-mono uppercase text-[#8B8B9B] mb-1">Security Zones</div>
              <div class="text-xl font-mono font-semibold text-[#E8E8EC]">{infraData.vlans}</div>
              <div class="text-[10px] text-[#5A5A6B]">Segmented VLANs</div>
            </div>
          </div>

          <!-- Identity Thesis -->
          <div class="bg-[#111318] border border-[#1A1D24] rounded-xl p-5 mb-6">
            <h3 class="text-xs font-mono uppercase tracking-wider text-[#4A8AFF] font-medium mb-2">The Identity Thesis</h3>
            <p class="text-[13px] leading-relaxed text-[#8B8B9B]">
              A randomized hardware address is not an identity; it is a costume the device changes on a schedule. Heimdall collapses those costumes onto one durable identity by correlating <strong class="text-[#E8E8EC]">JA4 TLS similarity (0.55)</strong>, <strong class="text-[#E8E8EC]">SNI overlap (0.30)</strong>, and <strong class="text-[#E8E8EC]">silence-gap timing (0.15)</strong>, then predicts ownership from a thirty-day behavioural signature using nearest-centroid classification with a reject option — answering <strong class="text-[#4A8AFF]">"a new phone just appeared; whose is it?"</strong>
            </p>
          </div>

          <!-- Services Breakdown -->
          <div class="bg-[#111318] border border-[#1A1D24] rounded-xl p-5">
            <h3 class="text-xs font-mono uppercase tracking-wider text-[#E8E8EC] font-semibold mb-3">Service Distribution</h3>
            <div class="space-y-2 text-xs font-mono">
              {#each Object.entries(infraData.services_breakdown || {}) as [tier, count]}
                <div class="flex items-center justify-between py-1 border-b border-[#1A1D24] last:border-0">
                  <span class="text-[#8B8B9B] capitalize">{tier.replace('_', ' ')}</span>
                  <span class="text-[#E8E8EC] font-semibold">{count}</span>
                </div>
              {/each}
            </div>
          </div>
        </div>

      {:else if activeTab === 'registry'}
        <div>
          <div class="text-[11px] font-mono uppercase tracking-widest text-[#1E67FF] font-semibold mb-1">Repository Surface</div>
          <h2 class="text-2xl font-bold font-sans tracking-tight mb-2">Engine Registry</h2>
          <p class="text-sm font-mono text-[#8B8B9B] mb-4">{estateData.length} sovereign engines under custody · 55 narrated in done log</p>

          <!-- Search filter -->
          <div class="mb-4">
            <input
              type="text"
              bind:value={registrySearch}
              placeholder="Filter engines (e.g. vidar, ullr, photon, ratatoskr)..."
              class="w-full bg-[#111318] border border-[#1A1D24] rounded-lg px-3.5 py-2 text-sm text-[#E8E8EC] placeholder-[#5A5A6B] focus:outline-none focus:border-[#1E67FF]"
            />
          </div>

          <!-- Grid of engines -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
            {#each filteredEngines as engine}
              <div class="bg-[#111318] border border-[#1A1D24] rounded-lg p-3 flex items-center justify-between {engine.narrated ? 'border-l-2 border-l-[#1E67FF]' : ''}">
                <div>
                  <div class="text-[#E8E8EC] font-medium">{engine.name}</div>
                  {#if engine.desc}
                    <div class="text-[11px] text-[#8B8B9B] font-sans truncate max-w-[220px]">{engine.desc}</div>
                  {/if}
                </div>
                <div class="flex items-center gap-2">
                  <span class="px-1.5 py-0.5 rounded text-[10px] bg-[#161922] text-[#5A5A6B] uppercase">{engine.kind}</span>
                  {#if engine.narrated}
                    <span class="w-1.5 h-1.5 rounded-full bg-[#1E67FF]" title="Narrated in Done Log"></span>
                  {/if}
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </div>
  </div>
{/if}
