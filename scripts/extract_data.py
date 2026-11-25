import json
import re
import os

worktree = '/Users/nate/src/github.com/nwalker85/wins/feat-nwalker-command-center-ui'
data_dir = os.path.join(worktree, 'src/data')
os.makedirs(data_dir, exist_ok=True)

with open(os.path.join(worktree, 'index.html')) as f:
    html = f.read()

# 1. WINS
m_wins = re.search(r'const WINS = (\[.*?\]);', html, re.DOTALL)
wins = json.loads(m_wins.group(1))

new_wins = [
    {
        'id': 'win-291',
        'date': '2026-11-23',
        'week': '2026-11-23',
        'month': '2026-11',
        'shipped': 'Released `@ravenhelm/ratatoskr-svelte` `v0.1.0` and `v0.1.1` on sovereign npm with binary `RATA` (`0x52415441`) wire protocol, `FastDeedHeader` lazy hex conversion, 4 KiB CSPRNG pool, and adaptive microtask burst coalescing (`WireOp.Batch`; PR #1, #2)',
        'impact': 'pushed pipelined RPC burst throughput to 337,722 ops/sec (17.61× vs REST, 2.12× vs raw WebSocket) and cut 16 KB binary payload frames by 4× while achieving 16,881 ops/sec streaming.',
        'repos': ['Ratatoskr'],
        'spheres': ['execution', 'platform'],
        'isMilestone': True,
        'milestones': [{'title': 'Binary RATA Wire Protocol & Microtask Burst Coalescing', 'short': 'RATA Wire Protocol', 'kind': 'doctrine'}],
        'milestoneTitle': 'Binary RATA Wire Protocol & Microtask Burst Coalescing',
        'milestoneShort': 'RATA Wire Protocol',
        'milestoneKind': 'doctrine'
    },
    {
        'id': 'win-292',
        'date': '2026-11-23',
        'week': '2026-11-23',
        'month': '2026-11',
        'shipped': 'Shipped Ullr Wave 13 Agent Client Protocol (ACP) sovereign IDE adapter, zero-allocation transport scratch buffering, adaptive burst coalescing, and sub-10ns `EpochCancellationBarrier` instant cancellation (`ullr acp`, PR #157, #158)',
        'impact': 'enabled zero-context-waste IDE integration for DeepAI Code and Zed, cutting token serialization overhead to 1.81 µs/frame and proving 21.67 µs cancellation roundtrips with Git Ontic Trace (`got v0.1.0`) execution receipts synchronized to sovereign Git CAS.',
        'repos': ['Ullr'],
        'spheres': ['execution', 'platform'],
        'isMilestone': True,
        'milestones': [{'title': 'Ullr Wave 13 Sovereign Agent Client Protocol (ACP) Adapter', 'short': 'Ullr ACP Adapter', 'kind': 'doctrine'}],
        'milestoneTitle': 'Ullr Wave 13 Sovereign Agent Client Protocol (ACP) Adapter',
        'milestoneShort': 'Ullr ACP Adapter',
        'milestoneKind': 'doctrine'
    },
    {
        'id': 'win-293',
        'date': '2026-11-23',
        'week': '2026-11-23',
        'month': '2026-11',
        'shipped': 'Hardened EAT substrate with Unicode char-boundary safe ADR scanning, scope-wide single-query relation collapse, multi-process SurrealKV reader lock backoff retry, and 8 composite secondary occurrence indexes (`v0.1.1`, PR #2, ADR-0002)',
        'impact': 'cut `eat prime` on `yager` from 35.3s to 0.39s (90.5× speedup), eliminated parallel agent dispatch aborts, and enabled sub-millisecond paginated filesystem queries across 120k+ occurrences without table scans.',
        'repos': ['EAT'],
        'spheres': ['topology'],
        'isMilestone': False,
        'milestones': [],
        'milestoneTitle': '',
        'milestoneShort': '',
        'milestoneKind': 'doctrine'
    },
    {
        'id': 'win-294',
        'date': '2026-11-23',
        'week': '2026-11-23',
        'month': '2026-11',
        'shipped': 'Shipped Photon EAT zero-copy Cap\'n Proto wire serialization and content-addressed Wasmtime execution memoization (`51cee49`, Photon)',
        'impact': 'dropped deterministic execution lookup latency from 15.9ms to 215.8 µs (73.9× speedup) while establishing 14,709 entities/sec silicon coordinate ingestion and 9,753 traversals/sec 2-hop hyperedge graph traversal.',
        'repos': ['Photon', 'EAT'],
        'spheres': ['topology', 'execution'],
        'isMilestone': False,
        'milestones': [],
        'milestoneTitle': '',
        'milestoneShort': '',
        'milestoneKind': 'doctrine'
    },
    {
        'id': 'win-295',
        'date': '2026-11-23',
        'week': '2026-11-23',
        'month': '2026-11',
        'shipped': 'Published the canonical Ratatoskr & EAT Performance Improvements Catalog in `runestack` (PR #14)',
        'impact': 'codified estate-wide wire protocol specifications, headline benchmarks, and verification provenance ledgers across runtime and knowledge layers.',
        'repos': ['Runestack', 'Ratatoskr', 'EAT'],
        'spheres': ['platform', 'topology'],
        'isMilestone': True,
        'milestones': [{'title': 'Estate Performance Improvements & Benchmark Catalog', 'short': 'Performance Catalog', 'kind': 'doctrine'}],
        'milestoneTitle': 'Estate Performance Improvements & Benchmark Catalog',
        'milestoneShort': 'Performance Catalog',
        'milestoneKind': 'doctrine'
    }
]
wins.extend(new_wins)

with open(os.path.join(data_dir, 'wins.json'), 'w') as f:
    json.dump(wins, f, indent=2)
print(f'Wrote {len(wins)} wins to src/data/wins.json')

# 2. SPHERES
m_spheres = re.search(r'const SPHERES = (\{.*?\});', html, re.DOTALL)
spheres = json.loads(m_spheres.group(1))
with open(os.path.join(data_dir, 'spheres.json'), 'w') as f:
    json.dump(spheres, f, indent=2)
print(f'Wrote {len(spheres)} spheres to src/data/spheres.json')

# 3. REPOS
m_repos = re.search(r'const REPOS = (\{.*?\});', html, re.DOTALL)
repos = json.loads(m_repos.group(1))
with open(os.path.join(data_dir, 'repos.json'), 'w') as f:
    json.dump(repos, f, indent=2)
print(f'Wrote {len(repos)} repos to src/data/repos.json')

# 4. Copy estate & estate-infra
with open(os.path.join(worktree, 'estate.json')) as f:
    estate = json.load(f)
with open(os.path.join(data_dir, 'estate.json'), 'w') as f:
    json.dump(estate, f, indent=2)

with open(os.path.join(worktree, 'estate-infra.json')) as f:
    infra = json.load(f)
with open(os.path.join(data_dir, 'estate-infra.json'), 'w') as f:
    json.dump(infra, f, indent=2)
print('Copied estate and estate-infra JSON')
