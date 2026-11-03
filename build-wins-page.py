#!/usr/bin/env python3
"""build-wins-page.py — Build the interactive, hostable Wins Continuum webpage.

Conforms strictly to the ratified Estate Marks & Palette doctrine:
- De-collapses Puter and the platform into 50 distinct sovereign repositories/engines.
- Real macOS app squircle icons (Got, MFAA, Frigg, Doomstadt, Odin's Runes, Photon, Heimdall, Gullveig, Argus, Runestack, Ravenhelm).
- The Rune identifies the tool (Elder Futhark letter + PCB-lead mark), not arbitrary hue.
- Monochromatic Bone on Obsidian with Garnet (#A3222F) witness eye.
- Palette doctrine: Obsidian (#0B0C0E), Bone (#EDE8DC), Matte Silver (#B8BCC4),
  Ash (#8E939B), Garnet (#A3222F), Instrumentation Blue (#3D5F8F), Brass (#8C6A3F / #D2A93B).
"""

import json
import os
import re
import subprocess
import base64
from datetime import datetime, date, timedelta
import calendar

DOCS_DIR = "/Users/nate/docs"
SOURCE_MD = os.path.join(DOCS_DIR, "wins-sanitized.md")
OUTPUT_HTML = os.path.join(DOCS_DIR, "wins.html")

BRAND_DIR = os.path.join(DOCS_DIR, "70-media/brand")

def get_app_icon_base64(path):
    if not os.path.exists(path):
        return ""
    if path.endswith(".icns"):
        out_png = f"/tmp/{os.path.basename(path)}.png"
        subprocess.run(["sips", "-s", "format", "png", path, "--out", out_png, "-Z", "96"], capture_output=True)
        if os.path.exists(out_png):
            with open(out_png, "rb") as f:
                return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    elif path.endswith(".png"):
        with open(path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode()
    return ""

def make_squircle_rune_svg(rune_char):
    return f"""<svg class="app-squircle" viewBox="0 0 100 100" width="22" height="22">
        <rect width="100" height="100" rx="22" fill="#0B0C0E" stroke="rgba(255,255,255,0.12)" stroke-width="2"/>
        <text x="50" y="66" font-family="'IBM Plex Sans', -apple-system, sans-serif" font-size="52" font-weight="600" fill="#EDE8DC" text-anchor="middle">{rune_char}</text>
        <circle cx="78" cy="22" r="7" fill="#A3222F" stroke="none"/>
    </svg>"""

# Load real macOS squircle app icons
ICONS = {
    "got": get_app_icon_base64(os.path.join(BRAND_DIR, "got/v1/renders/appicon-180.png")),
    "mfaa": get_app_icon_base64(os.path.join(BRAND_DIR, "mfaa/v2/renders/appicon-180.png")),
    "frigg": get_app_icon_base64(os.path.join(BRAND_DIR, "frigg/v1/renders/appicon-180.png")),
    "doomstadt": get_app_icon_base64(os.path.join(BRAND_DIR, "doomstadt/v1/renders/appicon-180.png")),
    "odinsrunes": get_app_icon_base64("/Applications/OdinsRunes.app/Contents/Resources/AppIcon.icns"),
    "photon": get_app_icon_base64("/Applications/Photon.app/Contents/Resources/icon.icns"),
    "heimdall": get_app_icon_base64(os.path.join(BRAND_DIR, "mfaa/renders/heimdall-96.png")),
    "gullveig": get_app_icon_base64(os.path.join(BRAND_DIR, "mfaa/renders/gullveig-96.png")),
    "argus": get_app_icon_base64(os.path.join(BRAND_DIR, "mfaa/renders/argus-96.png")),
    "runestack": get_app_icon_base64(os.path.join(BRAND_DIR, "runestack/renders/appicon-180.png")),
    "ravenhelm": get_app_icon_base64(os.path.join(BRAND_DIR, "ravenhelm/renders/appicon-180.png"))
}

SPHERES = {
    "all": {
        "id": "all",
        "name": "All Spheres",
        "short": "All Repos",
        "leadColor": "#EDE8DC",
        "desc": "The complete constellation of 46 sovereign repositories, engines, and protocols"
    },
    "voice": {
        "id": "voice",
        "name": "Voice, Presence & Audio",
        "short": "Voice & Presence",
        "leadColor": "#17C97B",
        "desc": "Conversational turn detection, 3D avatars, causal PCM streaming, local LLM inference & agent telephony"
    },
    "sensors": {
        "id": "sensors",
        "name": "Perception, Sensors & Telemetry",
        "short": "Sensors & Telemetry",
        "leadColor": "#3D5F8F",
        "desc": "Network observability, NetFlow ClickHouse ingestion, endpoint diagnostics, edge video & hardware bench"
    },
    "execution": {
        "id": "execution",
        "name": "Flight Deck & Sovereign Execution",
        "short": "Flight Deck & Execution",
        "leadColor": "#D2A93B",
        "desc": "Git Ontic Trace (Got), out-of-band Týr verification & supervisor seat custody"
    },
    "identity": {
        "id": "identity",
        "name": "Sovereign Identity & PKI",
        "short": "Identity & PKI",
        "leadColor": "#B8BCC4",
        "desc": "Kanidm POSIX directory authority, macOS kernel DAC, passkeys & SVIDs"
    },
    "topology": {
        "id": "topology",
        "name": "Topology, Ontology & Governance",
        "short": "Topology & Governance",
        "leadColor": "#8C6A3F",
        "desc": "Celestial hypergraphs, DIS 1.8 ontology schemas, transcription & policy engines"
    },
    "platform": {
        "id": "platform",
        "name": "Platform, Infrastructure & Tooling",
        "short": "Platform & Infra",
        "leadColor": "#8E939B",
        "desc": "Autonomous Norns runtime, bare-metal provisioning, GitOps & domain modeling"
    }
}

REPOSITORIES = {
    # Voice & Presence
    "Erwin": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "Puter 3D interactive avatar, signal condensation & LookPass",
        "keywords": ["erwin", "lookpass", "three\\.js avatar", "face tracking", "head-gen", "puter face", "signal to sentience"]
    },
    "Ullr": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "Sub-second conversational turns, VAD & 700ms pause flush engine",
        "keywords": ["ullr", "turn detection", "vad", "pause flush", "audio-app"]
    },
    "Vitki": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "TTS deployment rails & conversational UAT harness",
        "keywords": ["vitki"]
    },
    "Qwen3-TTS": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "Causal streaming audio synthesis (PCM16)",
        "keywords": ["qwen3-tts", "qwen3", "pcm16", "causal pcm", "streaming tts"]
    },
    "Mœðr": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "Affective computing, tone mapping & dynamic emotion palettes",
        "keywords": ["mœðr", "mothr", "emotion palette", "affective"]
    },
    "Bouquitala": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "Custom voice persona & expressive synthesis pipeline",
        "keywords": ["bouquitala", "bonquida"]
    },
    "Fenrir": {
        "sphere": "voice",
        "rune": "ᚢ",
        "runeName": "Uruz",
        "desc": "Zero-trust mTLS local LLM inference proxy & model benchmark suite",
        "keywords": ["fenrir"]
    },
    "Gjallarhorn": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "Telephony gateway, SIP signaling, carrier trunking & agent telephony",
        "keywords": ["gjallarhorn", "isip", "telephony", "sip trunk"]
    },
    "Puter": {
        "sphere": "voice",
        "rune": "ᚲ",
        "runeName": "Kenaz",
        "desc": "Sovereign web desktop & conversational computing canvas",
        "keywords": ["puter"]
    },

    # Perception, Sensors & Telemetry
    "Heimdall": {
        "sphere": "sensors",
        "rune": "ᛞ",
        "runeName": "Dagaz",
        "iconKey": "heimdall",
        "desc": "Network observability, ClickHouse NetFlow ingestion & endpoint diagnostics",
        "keywords": ["heimdall", "netflow", "clickhouse", "firewall", "rannsaka", "endpoint-diagnostics"]
    },
    "Huginn": {
        "sphere": "sensors",
        "rune": "ᛇ",
        "runeName": "Eihwaz",
        "desc": "Peripheral sensor aggregator, MQTT & RTL-AIS RF telemetry",
        "keywords": ["huginn", "rtl-ais", "ais"]
    },
    "Muninn": {
        "sphere": "sensors",
        "rune": "ᛇ",
        "runeName": "Eihwaz",
        "desc": "Persistent memory recall & knowledge retrieval engine",
        "keywords": ["muninn"]
    },
    "Ratatoskr": {
        "sphere": "sensors",
        "rune": "ᛚ",
        "runeName": "Laguz",
        "desc": "Edge WebRTC/RTSP media gateway & real-time video distribution",
        "keywords": ["ratatoskr", "webrtc/rtsp", "frigate", "rtsp"]
    },
    "Argus": {
        "sphere": "sensors",
        "rune": "ᚺ",
        "runeName": "Hagalaz",
        "iconKey": "argus",
        "desc": "Edge sensor array, microelectronics & hardware test bench",
        "keywords": ["microelectronics", "bench design", "argus"]
    },
    "The Viking": {
        "sphere": "sensors",
        "rune": "ᛖ",
        "runeName": "Ehwaz",
        "desc": "Sleipner smart RV expedition platform & CAN telemetry bus",
        "keywords": ["the viking", "sleipner", "camper"]
    },

    # Flight Deck & Sovereign Execution
    "Got": {
        "sphere": "execution",
        "rune": "ᚷ",
        "runeName": "Gebo",
        "iconKey": "got",
        "desc": "Git Ontic Trace — Content-addressable Git-backed execution witness",
        "keywords": ["got", "git cas", "execution witness"]
    },
    "Týr": {
        "sphere": "execution",
        "rune": "ᛏ",
        "runeName": "Tiwaz",
        "desc": "Asynchronous out-of-band outcome verification & zero-leakage attestation",
        "keywords": ["týr", "tyr", "outcome verification"]
    },
    "Doomstadt": {
        "sphere": "execution",
        "rune": "ᛞ",
        "runeName": "Dagaz",
        "iconKey": "doomstadt",
        "desc": "Native macOS Flight Deck & supervisor seat custody",
        "keywords": ["doomstadt", "flight deck"]
    },
    "Doom": {
        "sphere": "execution",
        "rune": "ᛞ",
        "runeName": "Dagaz",
        "desc": "Latverian agent engine, slice leases & doombot fleet orchestration",
        "keywords": ["doomcourt", "latveria", "doombot", "supervisor seat", "slice"]
    },
    "Bifröst": {
        "sphere": "execution",
        "rune": "ᛒ",
        "runeName": "Berkano",
        "desc": "Sovereign agent tool gateway & MCP dispatch fabric",
        "keywords": ["bifrost", "bifröst"]
    },
    "Freyr": {
        "sphere": "execution",
        "rune": "ᚠ",
        "runeName": "Fehu",
        "desc": "Tool execution runtime & sandboxed container runner",
        "keywords": ["freyr"]
    },
    "USE": {
        "sphere": "execution",
        "rune": "ᛋ",
        "runeName": "Sowilo",
        "desc": "Universal System Epoch — Stratum 1 Galileo OSNMA GNSS & NetHSM immutable ledger",
        "keywords": ["universal system epoch", "use stratum", "galileo osnma", "nethsm", "stratum 1", "immutable agent ledger"]
    },

    # Sovereign Identity & PKI
    "Kanidm": {
        "sphere": "identity",
        "rune": "ᚠ",
        "runeName": "Fehu",
        "desc": "POSIX LDAPv3 directory authority & macOS kernel DAC agent fencing",
        "keywords": ["kanidm", "posix identity", "ldapv3", "opendirectory"]
    },
    "Frigg": {
        "sphere": "identity",
        "rune": "ᚠ",
        "runeName": "Fehu",
        "iconKey": "frigg",
        "desc": "Apple passkey, FIDO2/WebAuthn sovereign authentication plane",
        "keywords": ["frigg", "fido2", "passkey", "webauthn"]
    },
    "Keycloak": {
        "sphere": "identity",
        "rune": "ᚠ",
        "runeName": "Fehu",
        "desc": "Enterprise OIDC/OAuth2 IdP federation & access management",
        "keywords": ["keycloak", "oidc", "sso", "saml"]
    },
    "Draupnir": {
        "sphere": "identity",
        "rune": "ᚠ",
        "runeName": "Fehu",
        "desc": "Ed25519 cryptographic receipt signing daemon & ring signatures",
        "keywords": ["draupnir", "receipt signing", "ring signature"]
    },
    "MFAA": {
        "sphere": "identity",
        "rune": "ᛏ",
        "runeName": "Tiwaz",
        "iconKey": "mfaa",
        "desc": "Multi-factor attestation authority & hardware security key signing",
        "keywords": ["mfaa", "valkyrie"]
    },
    "SPIRE": {
        "sphere": "identity",
        "rune": "ᛏ",
        "runeName": "Tiwaz",
        "desc": "Cryptographic workload identity & mTLS SVID attestation",
        "keywords": ["spire", "spiffe", "svid"]
    },

    # Topology, Ontology & Governance
    "Photon": {
        "sphere": "topology",
        "rune": "ᛋ",
        "runeName": "Sowilo",
        "iconKey": "photon",
        "desc": "Celestial hypergraph visualizer & 3D astrometric starmap",
        "keywords": ["photon", "starmap"]
    },
    "Yggdrasil": {
        "sphere": "topology",
        "rune": "ᛋ",
        "runeName": "Sowilo",
        "desc": "Ontic hypergraph architecture & W3C RDF/SHACL substrate",
        "keywords": ["yggdrasil", "celestial", "ontic hyperedge", "hypergraph", "shacl"]
    },
    "Odin's Runes": {
        "sphere": "topology",
        "rune": "ᚨ",
        "runeName": "Ansuz",
        "iconKey": "odinsrunes",
        "desc": "Neural audio transcription, Whisper/MLX pipeline & voice intake",
        "keywords": ["odin's runes", "odinsrunes", "transcription", "whisper"]
    },
    "Althing": {
        "sphere": "topology",
        "rune": "ᛗ",
        "runeName": "Mannaz",
        "desc": "Real-time workshop canvas & agent governance assembly",
        "keywords": ["althing"]
    },
    "DIS": {
        "sphere": "topology",
        "rune": "ᚷ",
        "runeName": "Gebo",
        "desc": "Domain Intelligence Schema (DIS 1.8) declarative knowledge modeling",
        "keywords": ["dis", "domain intelligence schema"]
    },
    "RLOM": {
        "sphere": "topology",
        "rune": "ᚱ",
        "runeName": "Raidho",
        "desc": "Ravenhelm Lean Operating Method & systemic throughput",
        "keywords": ["rlom", "operating method", "lean operating method"]
    },
    "Forseti": {
        "sphere": "topology",
        "rune": "ᚱ",
        "runeName": "Raidho",
        "desc": "Cedar policy engine & OpenFGA fine-grained authorization",
        "keywords": ["forseti", "cedar", "openfga"]
    },
    "Gullveig": {
        "sphere": "topology",
        "rune": "ᚠ",
        "runeName": "Fehu",
        "iconKey": "gullveig",
        "desc": "Asset registry, incident command & estate catalog",
        "keywords": ["gullveig", "incident command"]
    },
    "Hliðskjálf": {
        "sphere": "topology",
        "rune": "ᛟ",
        "runeName": "Othala",
        "desc": "High-seat tactical command projection & telemetry overview",
        "keywords": ["hliðskjálf", "hlidskjalf"]
    },
    "MDE": {
        "sphere": "topology",
        "rune": "ᛗ",
        "runeName": "Mannaz",
        "desc": "Markdown Editor & per-file Git DAG ref version control with self-healing identity",
        "keywords": ["mde", "per-file version control", "self-healing identity", "markdown editor"]
    },

    # Platform, Infrastructure & Tooling
    "Norns": {
        "sphere": "platform",
        "rune": "ᛝ",
        "runeName": "Ingwaz",
        "desc": "Autonomous AI agent operator & systemic task orchestrator",
        "keywords": ["norns"]
    },
    "Vidar": {
        "sphere": "platform",
        "rune": "ᛉ",
        "runeName": "Algiz",
        "desc": "Bare-metal infrastructure provisioning & k3s/k0s cluster fabric",
        "keywords": ["vidar", "bare-metal", "k3s", "k0s", "harbor", "argo cd", "traefik", "forgejo"]
    },
    "Snotra": {
        "sphere": "platform",
        "rune": "ᛃ",
        "runeName": "Jera",
        "desc": "Advisory AI code reviewer & GitOps automated gatekeeper",
        "keywords": ["snotra"]
    },
    "Andvari": {
        "sphere": "platform",
        "rune": "ᚹ",
        "runeName": "Wunjo",
        "desc": "Wealth, ledger & recurring subscription billing engine",
        "keywords": ["andvari"]
    },
    "Rig Gateway": {
        "sphere": "platform",
        "rune": "ᛉ",
        "runeName": "Algiz",
        "desc": "Secure host bastion, Cedar IAM & network ingress proxy",
        "keywords": ["rig gateway", "bastion"]
    },
    "Kvasir": {
        "sphere": "platform",
        "rune": "ᛉ",
        "runeName": "Algiz",
        "desc": "Host endpoint enrollment daemon & discovery agent",
        "keywords": ["kvasir"]
    },
    "Ultradex": {
        "sphere": "platform",
        "rune": "ᛈ",
        "runeName": "Perthro",
        "desc": "Opportunity lifecycle automation & relationship engine",
        "keywords": ["ultradex"]
    },
    "Runestack MIS": {
        "sphere": "platform",
        "rune": "ᛏ",
        "runeName": "Tiwaz",
        "iconKey": "runestack",
        "desc": "Management Information System & SurrealDB checkpoints",
        "keywords": ["runestack mis", "runestack", "surrealdb", "surrealcheckpointsaver", "surreal"]
    },
    "EDM": {
        "sphere": "platform",
        "rune": "ᛏ",
        "runeName": "Tiwaz",
        "desc": "Enterprise Domain Model in Rust & WebAssembly",
        "keywords": ["edm"]
    },
    "Publishing": {
        "sphere": "platform",
        "rune": "ᛟ",
        "runeName": "Othala",
        "desc": "Technical essays, foundational research papers (Zenodo DOI) & digital publications",
        "keywords": ["rootfifth", "nwalker\\.cc", "substack", "zenodo", "agentropy"]
    },
    "Odin OS": {
        "sphere": "platform",
        "rune": "ᚨ",
        "runeName": "Ansuz",
        "desc": "Operating system theory, 8-part capability microkernel & silicon interlock",
        "keywords": ["odin project", "odin os", "operating system theory", "8-part architecture", "ambient unix authority"]
    },
    "Ravenhelm Core": {
        "sphere": "platform",
        "rune": "ᚱ",
        "runeName": "Raven",
        "iconKey": "ravenhelm",
        "desc": "Core sovereign estate operations, host setup & foundation",
        "keywords": []
    }
}

def render_repo_icon_html(r_key):
    r_info = REPOSITORIES.get(r_key, {})
    icon_key = r_info.get("iconKey")
    if icon_key and ICONS.get(icon_key):
        return f'<img class="app-squircle-img" src="{ICONS[icon_key]}" alt="{r_key}">'
    rune = r_info.get("rune", "ᚱ")
    return make_squircle_rune_svg(rune)

INVENTIONS_AND_DOCTRINES_CATALOG = [
    # June 2026
    (r"automated domain intelligence schema cdn", "Inverted DIS Source-of-Truth to Git-Driven CDN", "Git-Driven DIS CDN", "doctrine"),
    (r"retired postgresql dual-write in heimdall.*clickhouse", "Migrated High-Volume Telemetry Ingestion to ClickHouse", "ClickHouse Telemetry", "doctrine"),
    (r"repositioned isip repository around autonomous agent telephony", "Created ISIP Sovereign Agent Telephony Protocol", "Created ISIP", "invention"),
    (r"published agentropy original research to zenodo", "Published Agentropy Foundation (Zenodo DOI)", "Agentropy Thesis", "invention"),
    (r"updated linear guidebook doctrine.*code custody to self-hosted forgejo", "Codified Sovereign Code Custody Standard", "Sovereign Custody", "doctrine"),
    (r"implemented heimdall agent-tools api over mtls", "Architected Agent Security Inspection over mTLS", "Agent mTLS Inspection", "doctrine"),
    
    # July 2026
    (r"the 'puter face architecture.*signal to sentience|published the 'puter face", "Published The 'puter Face Architecture (Signal to Sentience)", "The 'puter Face", "invention"),
    (r"bootstrapped `runestack-mis`", "Created Runestack MIS Persistence Architecture", "Created Runestack MIS", "invention"),
    (r"bootstrapped `ble-aggregator`.*rtl-ais", "Created Huginn Peripheral RTL-AIS RF Aggregator", "Created Huginn", "invention"),
    (r"ratified nornatlas data-layer doctrine", "Ratified Multi-Tenant Nornatlas Data Doctrine", "Nornatlas Doctrine", "doctrine"),
    (r"built tmbp v1 protocol", "Created TMBP v1 Agent-to-Human Bus Protocol", "Created TMBP Protocol", "invention"),
    (r"ratified adr-011 and established estate cutover doctrine", "Ratified Sovereign Cutover Doctrine (ADR-011)", "Cutover Doctrine (ADR-011)", "doctrine"),
    (r"landed mandatory forgejo branch protection", "Enforced Sovereign Branch Protection Doctrine", "Branch Protection", "doctrine"),
    (r"implemented mlx stt and tts streaming servers", "Created MLX Moshi Audio Streaming Engine", "MLX Voice Engine", "invention"),
    (r"captured doomstadt endpoint custody enrollment mvp", "Genesis of Doomstadt Workstation Custody", "Genesis of Doomstadt", "invention"),
    (r"established ultradex governed", "Architected Ultradex Governance Projections", "Created Ultradex", "invention"),
    
    # August 2026
    (r"filed adr-006.*session authorization and revocation boundaries", "Ratified Session Authorization Boundaries (ADR-006)", "Session Boundaries (ADR-006)", "doctrine"),
    (r"hardened vedrfolnir mímir entity extraction", "Created Veðrfölnir Sovereign Entity Extractor", "Veðrfölnir Extractor", "invention"),
    (r"ratified adr-008.*týr judgment authority", "Ratified Týr Judgment Authority & Dómr (ADR-008)", "Týr Judgment (ADR-008)", "doctrine"),
    (r"shipped snotra v3 review council", "Architected Snotra v3 Local AI Review Council", "Snotra v3 Council", "invention"),
    (r"bootstrapped `ravenhelm-observability-rs`", "Created Ravenhelm Rust Observability SDK", "Observability SDK", "invention"),
    (r"accepted adr-009.*coherence bus / concurrent responder bus", "Architected Concurrent Coherence Bus (ADR-009)", "Coherence Bus (ADR-009)", "invention"),
    (r"bootstrapped go custody cli \(`custody`\)", "Created Go Custody CLI & Single-History Standard", "Custody Standard", "doctrine"),
    (r"seeded odin's runes local workspace", "Genesis of Odin\x27s Runes Neural Audio Intake", "Genesis of Odin\x27s Runes", "invention"),
    (r"landed mœðr slice a formal affect model", "Formalized Mœðr Dynamic Affect & Emotion Model", "Mœðr Affect Model", "invention"),
    (r"published domain intelligence schema as an open", "Published Domain Intelligence Schema (DIS) Standard", "Published DIS Standard", "invention"),
    
    # September 2026
    (r"bootstrapped vitki next-web scaffold", "Created Vitki Real-time Voice Deployment Rails", "Created Vitki", "invention"),
    (r"ratified mímir grammar v0\.7\.0", "Ratified Mímir Grammar & Closed Predicate Calculus", "Mímir Grammar v0.7.0", "invention"),
    (r"implemented matrix agent issuance via mas admin api", "Implemented Cryptographic Matrix Agent SVIDs (ADR-022)", "Matrix Agent SVIDs", "invention"),
    (r"shipped doomcourt supervisor dispatch contract", "Architected Doomcourt Supervisor Dispatch Contract", "Doomcourt Contract", "doctrine"),
    (r"shipped doomwire nats jetstream engine core", "Created Doomwire JetStream Real-Time Bus (RFC-0034)", "Created Doomwire", "invention"),
    (r"landed ccc mímir v0\.7\.0 workflow engine.*adr-0001", "Ratified Customer Intelligence Architecture (ADR-0001)", "Mímir CCC Engine", "invention"),
    (r"implemented erwin living substrate runtime.*vór", "Created Erwin Living Substrate & Vór Geological Ledger", "Erwin & Vór Ledger", "invention"),
    (r"bootstrapped amp live aid / odin's runes", "Created Odin\x27s Runes Live Audio Transcription", "Created Odin\x27s Runes", "invention"),
    (r"cut over yager to ullr identity", "Created Ullr Sovereign Conversational Runtime (ADR-0014)", "Created Ullr", "invention"),
    (r"ratified mímir grammar v0\.7\.1", "Ratified Mímir ViewSpec Semantic Contracts", "Mímir ViewSpec", "invention"),
    (r"accepted adr-032.*containment hierarchy", "Ratified Containment Hierarchy & Tool Authority (ADR-032)", "Containment Hierarchy", "doctrine"),
    (r"adr-033.*durable supervisor|durable supervisor on norns", "Ratified Durable Supervisor Architecture (ADR-033)", "Durable Supervisor", "doctrine"),
    (r"bootstrapped yggdrasil vocabulary", "Created Yggdrasil Ontic Hypergraph Vocabulary", "Created Yggdrasil", "invention"),
    (r"shipped draupnir v0\.1 ed25519", "Created Draupnir Ed25519 Receipt Signer", "Created Draupnir", "invention"),
    (r"universal system epoch.*stratum 1.*galileo osnma", "Designed Universal System Epoch (USE) Stratum 1", "Designed USE", "invention"),
    (r"released domain intelligence schema \(dis\) 1\.7", "Ratified Domain Intelligence Schema (DIS) 1.7", "DIS 1.7 Standard", "doctrine"),
    (r"enforced immutable build & digest release doctrine", "Ratified Immutable Release Doctrine (ADR-0007)", "Release Doctrine (ADR-0007)", "doctrine"),
    (r"ratified yggdrasil workflow nets", "Ratified Yggdrasil Workflow Nets & Dual-Runtime Engine", "Yggdrasil Workflow Nets", "invention"),
    (r"implemented ullr app server orchestrator", "Created Ullr Kubernetes App Server Orchestrator", "Ullr K3s Server", "invention"),
    (r"built doomstadt macos native desktop application", "Created Doomstadt Native macOS Flight Deck", "Created Doomstadt", "invention"),
    (r"deployed sovereign qwen3-tts streaming service", "Deployed Sovereign Qwen3-TTS Streaming Engine", "Deployed Qwen3-TTS", "invention"),
    (r"yggdrasil attributable runtime engine", "Architected Yggdrasil Attributable Runtime Engine", "Yggdrasil Runtime Engine", "invention"),
    (r"per-file version control on shared filesystems.*mde", "Architected Per-File SCM with Self-Healing Identity (MDE)", "MDE Per-File SCM", "invention"),
    (r"published the sovereign identity standard whitepaper", "Published Sovereign Identity Standard Whitepaper", "Identity Whitepaper", "doctrine"),
    (r"ratified puter v2 architecture", "Ratified Puter v2 Conversational Architecture (ADR-0012)", "Puter v2 (ADR-0012)", "invention"),
    (r"published the odin project.*operating system theory", "Published The Odin Project: An Operating System Theory", "The Odin Project OS", "invention"),
    (r"launched rootfifth storefront", "Launched RootFifth Publishing Storefront", "Launched RootFifth", "invention"),
    (r"ratified adr-036.*sovereign client architecture", "Ratified Sovereign Client Architecture (ADR-036)", "Client Architecture", "doctrine"),
    (r"adr-037.*draupnir attested identity|draupnir attested identity", "Ratified Draupnir Attested Identity (ADR-037)", "Draupnir Attestation", "doctrine"),
    
    # October 2026
    (r"published rlom.*ravenhelm lean operating method", "Published Ravenhelm Lean Operating Method (RLOM)", "Published RLOM", "doctrine"),
    (r"implemented dis 1\.8 grammar extensions", "Architected DIS 1.8 Epistemic Grammar Extensions", "DIS 1.8 Extensions", "invention"),
    (r"declarative governance for ai agents", "Claimed Declarative Governance for AI Agents Category", "Category Creation", "invention"),
    (r"operationalized kanidm ldapv3", "Operationalized Kanidm POSIX Kernel DAC Identity", "Operationalized Kanidm", "invention"),
    (r"invented got \(git as the content-addressable execution ledger", "Invented Got (Git Ontic Trace)", "Invented Got", "invention"),
    (r"formalized computational execution as the ontic hyperedge", "Formalized Ontic Hyperedge Execution Theory", "Ontic Hyperedge Theory", "invention"),
    (r"ratified adr-tyr-asynchronous-outcome-verification", "Ratified Týr Outcome Verification Standard (ADR-Tyr)", "Týr Verification Standard", "doctrine"),
    (r"shipped photon sovereign developer environment v1\.4\.0", "Shipped Photon Sovereign Developer Environment v1.4.0", "Photon v1.4.0", "invention"),
    (r"published foundational research to zenodo.*post-ai hyperedge execution model", "Published Post-AI Hyperedge Execution Model (Zenodo DOI)", "Hyperedge Zenodo Paper", "invention"),
    (r"1,889 trees, a dropped laptop, and the sovereign substrate", "Published The Sovereign Substrate Architectural Essay", "Sovereign Substrate Essay", "doctrine"),
    (r"sovereign canon volume 17.*adr-0028", "Ratified Intergraph BPv7 DTN over Iroh Mesh (ADR-0028)", "Intergraph DTN (ADR-0028)", "doctrine"),
    (r"adr-0016.*7-layer dip kv radix permutation engine", "Invented 7-Layer Dip KV Radix Permutation Engine (ADR-0016)", "7-Layer KV Radix (ADR-0016)", "invention"),
    (r"multi-dimensional social hypergraph engine", "Architected Multi-Dimensional Social Hypergraph Engine", "Social Hypergraph Engine", "invention"),
    (r"runestack v0\.1\.0 sovereign runtime daemon.*axiom-zero/v1", "Shipped Runestack v0.1.0 & axiom-zero/v1 Iroh/Bao Mesh", "Runestack v0.1.0 & Iroh Mesh", "invention"),
    (r"celestial realm particle states of matter", "Engineered Celestial Particle States of Matter & GPU Batching", "Celestial Particle Physics", "invention")
]

def check_milestones(shipped, impact):
    text = (shipped + " " + impact).lower()
    matches = []
    for pat, title, short, kind in INVENTIONS_AND_DOCTRINES_CATALOG:
        if re.search(pat, text):
            matches.append({
                "title": title,
                "short": short,
                "kind": kind
            })
    return matches

def classify_win(shipped, impact):
    text = (shipped + " " + impact).lower()
    matched_repos = []
    
    # Check each repository by its explicit regex patterns
    for r_key, r_info in REPOSITORIES.items():
        kws = r_info.get("keywords", [])
        if not kws:
            continue
        if any(re.search(rf"\b{k}\b", text) for k in kws):
            matched_repos.append(r_key)
            
    if not matched_repos:
        matched_repos.append("Ravenhelm Core")
        
    # Derive spheres from matched repos
    spheres = list(set(REPOSITORIES[r]["sphere"] for r in matched_repos))
    return matched_repos, spheres

def parse_wins():
    with open(SOURCE_MD, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    current_week = None
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("## Week of"):
            current_week = line.replace("## Week of", "").strip()
        elif line.startswith("- 2026-"):
            m = re.match(r"- (\d{4}-\d{2}-\d{2})\s*—\s*(.*?)\s*→\s*(.*)", line)
            if m:
                dt_str, shipped, impact = m.groups()
                repos, spheres = classify_win(shipped, impact)
                matches = check_milestones(shipped, impact)
                is_ms = len(matches) > 0
                ms_title = " & ".join(m["title"] for m in matches) if is_ms else ""
                ms_short = " & ".join(m["short"] for m in matches) if is_ms else ""
                ms_kind = matches[0]["kind"] if len(matches) == 1 else ("doctrine" if all(m["kind"] == "doctrine" for m in matches) else "invention")
                entries.append({
                    "id": f"win-{len(entries)+1}",
                    "date": dt_str,
                    "week": current_week,
                    "month": dt_str[:7],
                    "shipped": shipped,
                    "impact": impact,
                    "repos": repos,
                    "spheres": spheres,
                    "isMilestone": is_ms,
                    "milestones": matches,
                    "milestoneTitle": ms_title,
                    "milestoneShort": ms_short,
                    "milestoneKind": ms_kind
                })
    return entries

def build_month_heatmaps(entries):
    months_meta = [
        {"key": "2026-06", "name": "June", "year": 2026, "month": 6, "narrative": "Foundational Networks, ClickHouse Ingestion & Initial Agent Telephony"},
        {"key": "2026-07", "name": "July", "year": 2026, "month": 7, "narrative": "The 'puter Face Sentience Pipeline, Runestack Persistence, Huginn RF & MLX Voice"},
        {"key": "2026-08", "name": "August", "year": 2026, "month": 8, "narrative": "Release Doctrine (Harbor b<N>), Workstation Custody & Fleet Governance"},
        {"key": "2026-09", "name": "September", "year": 2026, "month": 9, "narrative": "Universal System Epoch (USE), Odin OS Theory, Yggdrasil Runtime Engine, MDE & Kanidm Identity"},
        {"key": "2026-10", "name": "October", "year": 2026, "month": 10, "narrative": "DIS 1.8 Launch, Kanidm POSIX Kernel DAC, Got, Ontic Hyperedge, 7-Layer KV Radix & Runestack v0.1.0"},
        {"key": "2026-11", "name": "November", "year": 2026, "month": 11, "narrative": "Ullr Runtime Circuit Breakers, Resilience Contracts & Public Continuum Launch"}
    ]

    by_date = {}
    for e in entries:
        d = e["date"]
        if d not in by_date:
            by_date[d] = []
        by_date[d].append(e)

    result = []
    for m in months_meta:
        y = m["year"]
        mon = m["month"]
        num_days = calendar.monthrange(y, mon)[1]
        if mon == 11:
            num_days = min(num_days, 14)

        days_in_month = []
        for day in range(1, num_days + 1):
            d_obj = date(y, mon, day)
            d_str = d_obj.strftime("%Y-%m-%d")
            wins_here = by_date.get(d_str, [])
            day_milestones = [ms for w in wins_here for ms in w.get("milestones", [])]
            has_ms = len(day_milestones) > 0
            has_inv = any(ms["kind"] == "invention" for ms in day_milestones)
            has_doc = any(ms["kind"] == "doctrine" for ms in day_milestones)
            days_in_month.append({
                "date": d_str,
                "day": day,
                "dayOfWeek": d_obj.weekday(),
                "count": len(wins_here),
                "hasMilestone": has_ms,
                "hasInvention": has_inv,
                "hasDoctrine": has_doc,
                "milestones": day_milestones,
                "wins": [w["id"] for w in wins_here],
                "repos": list(set(r for w in wins_here for r in w["repos"])),
                "spheres": list(set(s for w in wins_here for s in w["spheres"]))
            })

        month_wins = [e for e in entries if e["month"] == m["key"]]
        sphere_dist = {}
        for w in month_wins:
            for s in w["spheres"]:
                sphere_dist[s] = sphere_dist.get(s, 0) + 1

        result.append({
            "key": m["key"],
            "name": m["name"],
            "year": y,
            "narrative": m["narrative"],
            "totalWins": len(month_wins),
            "days": days_in_month,
            "sphereDist": sphere_dist
        })
    return result

def build():
    entries = parse_wins()
    month_heatmaps = build_month_heatmaps(entries)

    total_wins = len(entries)
    active_days = len(set(e["date"] for e in entries))
    total_inventions = sum(len([m for m in e["milestones"] if m["kind"] == "invention"]) for e in entries)
    total_doctrines = sum(len([m for m in e["milestones"] if m["kind"] == "doctrine"]) for e in entries)
    total_milestones = total_inventions + total_doctrines
    total_repos_count = len(REPOSITORIES)
    
    # Calculate repository ship counts
    repo_counts = {}
    for e in entries:
        for r in e["repos"]:
            repo_counts[r] = repo_counts.get(r, 0) + 1

    # Client-ready metadata
    client_repos = {}
    for r_key, r_info in REPOSITORIES.items():
        client_repos[r_key] = {
            "name": r_key,
            "sphere": r_info["sphere"],
            "rune": r_info["rune"],
            "runeName": r_info["runeName"],
            "desc": r_info["desc"],
            "iconHtml": render_repo_icon_html(r_key),
            "count": repo_counts.get(r_key, 0)
        }

    wins_json = json.dumps(entries)
    month_heatmaps_json = json.dumps(month_heatmaps)
    repos_json = json.dumps(client_repos)
    spheres_json = json.dumps(SPHERES)

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nathan Walker · Done Log & Capability Continuum</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
/* Estate Marks & Palette Doctrine */
:root {{
    --bg: #000000;
    --obsidian: #0B0C0E;
    --surface: #0B0C0E;
    --surface-elevated: #13151A;
    --surface-card: #171920;
    --rule: #23262C;
    --rule-subtle: #191B20;
    
    --bone: #EDE8DC;
    --ink: #EDE8DC;
    --silver: #B8BCC4;
    --ash: #8E939B;
    --ink-muted: #8E939B;
    --ink-dim: #545861;
    
    --garnet: #A3222F; /* Witness Red — One per composition */
    --blue: #3D5F8F;   /* Instrumentation Blue — live state (.ai) */
    --brass: #8C6A3F;  /* Brass — provenance & custody (.co) */
    --brass-bright: #D2A93B;
    --emerald: #17C97B; /* Flight deck signal green */
    --emerald-dim: #0E472D;
    --emerald-glow: rgba(23, 201, 123, 0.18);
    
    --fp: "Source Serif 4", Georgia, serif;
    --fs: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, sans-serif;
    --fm: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    background-color: var(--bg);
    color: var(--bone);
    font-family: var(--fs);
    font-size: 15px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    padding-bottom: 120px;
}}

.wrap {{
    max-width: 1260px;
    margin: 0 auto;
    padding: 0 24px;
}}

/* Header & Telemetry */
header {{
    padding: 60px 0 36px;
    border-bottom: 1px solid var(--rule);
    position: relative;
}}

.brand-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
}}

.brand-badge {{
    display: inline-flex;
    align-items: center;
    gap: 14px;
    font-family: var(--fm);
    font-size: 11px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--silver);
}}

.brand-badge img {{
    width: 28px;
    height: 28px;
    border-radius: 6px;
}}

.view-controls {{
    display: flex;
    gap: 6px;
    background: var(--surface);
    padding: 4px;
    border-radius: 8px;
    border: 1px solid var(--rule);
}}

.view-btn {{
    background: transparent;
    border: none;
    color: var(--ash);
    font-family: var(--fm);
    font-size: 11px;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}

.view-btn:hover {{
    color: var(--bone);
    background: var(--surface-elevated);
}}

.view-btn.active {{
    background: var(--rule);
    color: var(--bone);
    font-weight: 600;
}}

h1 {{
    font-family: var(--fp);
    font-size: 46px;
    font-weight: 600;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 16px;
}}

h1 span.accent {{
    color: var(--bone);
    border-bottom: 2px solid var(--brass);
}}

.subtitle {{
    font-family: var(--fs);
    font-size: 17px;
    color: var(--ash);
    max-width: 860px;
    margin-bottom: 32px;
    line-height: 1.5;
}}

/* Executive Summary Box */
.story-box {{
    background: var(--surface);
    border: 1px solid var(--rule);
    border-left: 3px solid var(--brass);
    border-radius: 8px;
    padding: 24px 28px;
    margin-bottom: 36px;
}}

.story-box-title {{
    font-family: var(--fm);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--brass-bright);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.story-text {{
    font-size: 15.5px;
    color: var(--bone);
    line-height: 1.65;
}}

.story-text p + p {{
    margin-top: 10px;
}}

/* KPI Telemetry Ribbon */
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}}

.kpi-card {{
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 8px;
    padding: 18px 22px;
    position: relative;
    overflow: hidden;
}}

.kpi-label {{
    font-family: var(--fm);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ash);
    margin-bottom: 6px;
}}

.kpi-val {{
    font-family: var(--fm);
    font-size: 34px;
    font-weight: 600;
    color: var(--bone);
    line-height: 1.1;
}}

.kpi-meta {{
    font-family: var(--fm);
    font-size: 11.5px;
    color: var(--silver);
    margin-top: 4px;
}}

/* Month-by-Month Heatmap Section */
.heatmap-section {{
    padding: 36px 0;
    border-bottom: 1px solid var(--rule);
}}

.section-head {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 24px;
}}

.section-title {{
    font-family: var(--fp);
    font-size: 26px;
    font-weight: 600;
    letter-spacing: -0.01em;
}}

.section-meta {{
    font-family: var(--fm);
    font-size: 12px;
    color: var(--ash);
}}

.months-heatmap-row {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 14px;
}}

.month-block {{
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 10px;
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: border-color 0.15s ease, transform 0.15s ease;
    cursor: pointer;
}}

.month-block:hover {{
    border-color: var(--silver);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}}

.month-block-head {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--rule-subtle);
    padding-bottom: 8px;
}}

.month-title {{
    font-family: var(--fm);
    font-size: 13px;
    font-weight: 600;
    color: var(--bone);
    letter-spacing: 0.06em;
    text-transform: uppercase;
}}

.month-count-pill {{
    font-family: var(--fm);
    font-size: 12px;
    font-weight: 600;
    color: var(--brass-bright);
}}

.month-grid-wrap {{
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
}}

.day-legend-col {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    font-family: var(--fm);
    font-size: 8.5px;
    color: var(--ink-dim);
    width: 18px;
    height: 122px;
}}

.month-cells-grid {{
    display: grid;
    grid-template-rows: repeat(7, 14px);
    grid-auto-flow: column;
    grid-auto-columns: 14px;
    gap: 4px;
}}

.cell {{
    width: 14px;
    height: 14px;
    border-radius: 2px;
    background: #111317;
    border: 1px solid rgba(255, 255, 255, 0.03);
    cursor: pointer;
    transition: transform 0.1s ease, outline 0.1s ease;
}}

.cell:hover {{
    transform: scale(1.4);
    z-index: 10;
    outline: 2px solid var(--bone);
}}

.cell.empty {{
    background: transparent;
    border-color: transparent;
    cursor: default;
    pointer-events: none;
}}

.cell.lvl-1 {{ background: #0E3E26; border-color: #145937; }}
.cell.lvl-2 {{ background: #13693F; border-color: #17C97B; }}
.cell.lvl-3 {{ background: #17C97B; border-color: #5AD8A6; box-shadow: 0 0 6px var(--emerald-glow); }}
.cell.lvl-4 {{ background: #D2A93B; border-color: #FFE58F; box-shadow: 0 0 8px rgba(210, 169, 59, 0.4); }}

.month-narrative {{
    font-size: 11.5px;
    color: var(--ash);
    line-height: 1.4;
    margin-bottom: 12px;
    min-height: 34px;
}}

/* Mini Sphere Distribution Bar */
.domain-bar {{
    display: flex;
    height: 4px;
    border-radius: 2px;
    overflow: hidden;
    background: var(--surface-elevated);
    gap: 1px;
}}

.domain-bar-seg {{
    height: 100%;
    transition: width 0.3s ease;
}}

/* Heatmap Legend Bar */
.heatmap-legend {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
    font-family: var(--fm);
    font-size: 11px;
    color: var(--ash);
    margin-top: 18px;
}}

.legend-cells {{
    display: flex;
    gap: 4px;
}}

/* Controls Bar: Search, Sphere Selector & Repository Deck */
.controls-bar {{
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(0, 0, 0, 0.94);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 16px 0;
    border-bottom: 1px solid var(--rule);
    margin-bottom: 32px;
}}

.search-row {{
    display: flex;
    gap: 12px;
    margin-bottom: 14px;
}}

.search-input {{
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 8px;
    color: var(--bone);
    font-family: var(--fs);
    font-size: 14px;
    padding: 10px 16px;
    outline: none;
    transition: border-color 0.15s ease;
}}

.search-input:focus {{
    border-color: var(--silver);
}}

.reset-btn {{
    background: var(--surface);
    border: 1px solid var(--rule);
    color: var(--ash);
    font-family: var(--fm);
    font-size: 12px;
    padding: 0 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
}}

.reset-btn:hover {{
    color: var(--bone);
    border-color: var(--silver);
}}

/* Sphere Selector Tabs */
.spheres-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--rule-subtle);
}}

.sphere-btn {{
    background: transparent;
    border: 1px solid var(--rule);
    color: var(--ash);
    border-radius: 6px;
    padding: 5px 12px;
    font-family: var(--fm);
    font-size: 11.5px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}

.sphere-btn:hover {{
    color: var(--bone);
    border-color: var(--silver);
}}

.sphere-btn.active {{
    background: var(--surface-card);
    border-color: var(--brass-bright);
    color: var(--bone);
    font-weight: 600;
}}

.sphere-lead-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}}

/* 46 Repositories Deck */
.repo-deck {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    max-height: 160px;
    overflow-y: auto;
    padding-right: 4px;
}}

.repo-deck::-webkit-scrollbar {{
    width: 4px;
}}
.repo-deck::-webkit-scrollbar-thumb {{
    background: var(--rule);
    border-radius: 2px;
}}

.repo-btn {{
    background: var(--surface);
    border: 1px solid var(--rule);
    color: var(--ash);
    border-radius: 6px;
    padding: 4px 10px;
    font-family: var(--fm);
    font-size: 11.5px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
}}

.repo-btn:hover {{
    border-color: var(--silver);
    color: var(--bone);
    transform: translateY(-1px);
}}

.repo-btn.active {{
    background: var(--surface-card);
    border-color: var(--brass);
    color: var(--bone);
    font-weight: 600;
    box-shadow: 0 0 10px rgba(140, 106, 63, 0.3);
}}

.icon-wrap {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.app-squircle-img {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    display: block;
}}

.app-squircle {{
    width: 18px;
    height: 18px;
    display: block;
}}

.repo-count {{
    background: var(--surface-elevated);
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 9.5px;
    color: var(--ink-dim);
    margin-left: 2px;
}}

.repo-btn.active .repo-count {{
    color: var(--brass-bright);
    background: rgba(255, 255, 255, 0.08);
}}

/* Timeline & Win Cards */
.timeline {{
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.month-group {{
    position: relative;
}}

.month-divider {{
    position: sticky;
    top: 210px;
    z-index: 20;
    background: rgba(0, 0, 0, 0.96);
    padding: 12px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--rule-subtle);
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}}

.month-name {{
    font-family: var(--fp);
    font-size: 26px;
    font-weight: 600;
    color: var(--bone);
}}

.month-meta {{
    font-family: var(--fm);
    font-size: 12px;
    color: var(--silver);
}}

.cards-stream {{
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

.win-card {{
    background: var(--surface);
    border: 1px solid var(--rule);
    border-radius: 10px;
    padding: 20px 24px;
    transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    display: grid;
    grid-template-columns: 180px 1fr;
    gap: 24px;
}}

.win-card:hover {{
    border-color: var(--silver);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    transform: translateY(-1px);
}}

.card-left {{
    border-right: 1px solid var(--rule-subtle);
    padding-right: 16px;
    display: flex;
    flex-direction: column;
}}

.card-date {{
    font-family: var(--fm);
    font-size: 13px;
    font-weight: 600;
    color: var(--bone);
    letter-spacing: 0.05em;
}}

.card-dayname {{
    font-family: var(--fm);
    font-size: 11px;
    color: var(--ash);
    text-transform: uppercase;
    margin-top: 2px;
}}

.card-badges {{
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-top: 14px;
}}

.card-repo-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--fm);
    font-size: 11px;
    color: var(--bone);
    background: var(--surface-elevated);
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid var(--rule);
    cursor: pointer;
    transition: border-color 0.1s ease;
    width: fit-content;
}}

.card-repo-badge:hover {{
    border-color: var(--brass-bright);
}}

.card-repo-badge .app-squircle-img,
.card-repo-badge .app-squircle {{
    width: 16px;
    height: 16px;
}}

.card-sphere-tag {{
    font-family: var(--fm);
    font-size: 9.5px;
    color: var(--ash);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
}}

.card-content {{
    display: flex;
    flex-direction: column;
    gap: 10px;
}}

.card-shipped {{
    font-size: 16px;
    font-weight: 500;
    color: var(--bone);
    line-height: 1.45;
}}

.card-impact {{
    font-size: 14px;
    color: var(--bone);
    background: var(--surface-elevated);
    padding: 10px 14px;
    border-radius: 6px;
    border-left: 2px solid var(--brass);
    line-height: 1.5;
}}

.card-impact strong {{
    color: var(--brass-bright);
}}

.inline-code {{
    font-family: var(--fm);
    font-size: 0.88em;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 1px 5px;
    border-radius: 4px;
    color: var(--bone);
}}

/* Milestone Card & Badge Styling */
.win-card.milestone-card {{
    position: relative;
}}

.win-card.invention-card {{
    border: 1.5px solid var(--brass-bright);
    background: linear-gradient(135deg, rgba(210, 169, 59, 0.09) 0%, #13151D 100%);
    box-shadow: 0 0 32px rgba(210, 169, 59, 0.16);
}}

.win-card.invention-card:hover {{
    border-color: #FFE58F;
    box-shadow: 0 0 45px rgba(210, 169, 59, 0.28);
    transform: translateY(-2px);
}}

.win-card.doctrine-card {{
    border: 1.5px solid #8C6A3F;
    background: linear-gradient(135deg, rgba(163, 34, 47, 0.08) 0%, #13151D 100%);
    box-shadow: 0 0 28px rgba(163, 34, 47, 0.12);
}}

.win-card.doctrine-card:hover {{
    border-color: var(--bone);
    box-shadow: 0 0 40px rgba(163, 34, 47, 0.24);
    transform: translateY(-2px);
}}

.milestones-container {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 10px;
}}

.milestone-badge-row {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-radius: 6px;
    padding: 3px 10px;
    width: fit-content;
}}

.milestone-badge-row.invention-badge-row {{
    background: rgba(210, 169, 59, 0.14);
    border: 1px solid var(--brass);
}}

.milestone-badge-row.doctrine-badge-row {{
    background: rgba(163, 34, 47, 0.14);
    border: 1px solid var(--garnet);
}}

.milestone-star {{
    color: var(--brass-bright);
    font-size: 13px;
    line-height: 1;
}}

.doctrine-icon {{
    color: #E24B58;
    font-size: 11px;
    line-height: 1;
}}

.milestone-pill {{
    font-family: var(--fm);
    font-size: 10px;
    font-weight: 700;
    color: var(--brass-bright);
    letter-spacing: 0.12em;
    text-transform: uppercase;
}}

.milestone-pill.doctrine-pill {{
    color: #FF808C;
}}

.milestone-title-tag {{
    font-family: var(--fm);
    font-size: 11px;
    color: var(--silver);
    font-weight: 500;
}}

.milestone-title-text {{
    font-family: var(--fp);
    font-size: 21px;
    font-weight: 600;
    color: var(--bone);
    line-height: 1.25;
    margin-top: 2px;
    letter-spacing: -0.01em;
}}

.card-milestone-pill {{
    font-family: var(--fm);
    font-size: 9px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 8px;
    width: fit-content;
}}

.card-milestone-pill.invention-pill {{
    color: #0B0C0E;
    background: var(--brass-bright);
}}

.card-milestone-pill.doctrine-pill {{
    color: #EDE8DC;
    background: var(--garnet);
    border: 1px solid rgba(255, 255, 255, 0.15);
}}

.milestones-toggle-btn {{
    background: var(--surface);
    border: 1px solid var(--brass);
    color: var(--brass-bright);
    font-family: var(--fm);
    font-size: 12px;
    padding: 0 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
}}

.milestones-toggle-btn:hover {{
    background: rgba(210, 169, 59, 0.15);
    border-color: #FFE58F;
    color: #FFE58F;
}}

.milestones-toggle-btn.active {{
    background: var(--brass-bright);
    color: #000;
    font-weight: 700;
    border-color: var(--brass-bright);
    box-shadow: 0 0 18px rgba(210, 169, 59, 0.4);
}}

.cell.has-invention {{
    outline: 2px solid var(--brass-bright);
    outline-offset: -1px;
}}

.cell.has-doctrine:not(.has-invention) {{
    outline: 2px solid var(--garnet);
    outline-offset: -1px;
}}

/* Floating Tooltip */
#tooltip {{
    position: fixed;
    display: none;
    z-index: 1000;
    background: #0B0C0E;
    border: 1px solid var(--silver);
    border-radius: 8px;
    padding: 12px 16px;
    font-family: var(--fs);
    font-size: 13px;
    color: var(--bone);
    max-width: 380px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.8);
    pointer-events: none;
}}

#tooltip .tt-date {{
    font-family: var(--fm);
    font-size: 11px;
    font-weight: 600;
    color: var(--brass-bright);
    margin-bottom: 6px;
    text-transform: uppercase;
}}

#tooltip .tt-count {{
    color: var(--bone);
    font-weight: 600;
}}

#tooltip ul {{
    list-style: none;
    margin-top: 6px;
}}

#tooltip li {{
    font-size: 12px;
    line-height: 1.4;
    margin-bottom: 6px;
    color: var(--ash);
    border-left: 2px solid var(--rule);
    padding-left: 8px;
}}

#tooltip li .tt-repo {{
    color: var(--bone);
    font-weight: 600;
    font-family: var(--fm);
    font-size: 11px;
}}

/* Responsive */
@media (max-width: 1080px) {{
    .months-heatmap-row {{
        grid-template-columns: repeat(3, 1fr);
    }}
}}

@media (max-width: 760px) {{
    .months-heatmap-row {{
        grid-template-columns: 1fr;
    }}
    .win-card {{
        grid-template-columns: 1fr;
        gap: 12px;
    }}
    .card-left {{
        border-right: none;
        border-bottom: 1px solid var(--rule-subtle);
        padding-right: 0;
        padding-bottom: 10px;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }}
    .card-badges {{
        margin-top: 0;
        flex-direction: row;
        flex-wrap: wrap;
    }}
    h1 {{
        font-size: 32px;
    }}
}}
</style>
</head>
<body>

<div class="wrap">
    <header>
        <div class="brand-row">
            <div class="brand-badge">
                <img src="{ICONS['ravenhelm']}" alt="Ravenhelm">
                <span>Ravenhelm Sovereign Estate · Done Log</span>
            </div>
            <div class="view-controls">
                <button class="view-btn active" data-view="balanced">Full Deck</button>
                <button class="view-btn" data-view="heatmap-only">Heatmap Focus</button>
                <button class="view-btn" data-view="stream-only">Cards Stream</button>
            </div>
        </div>

        <h1>Shipped Capability <span class="accent">Continuum</span></h1>
        <p class="subtitle">
            An immutable, factual record of {total_repos_count} sovereign repositories, autonomous infrastructure, declarative governance schemas, POSIX kernel identities, and mathematical execution ledgers shipped by Nathan Walker.
        </p>

        <!-- Executive Narrative -->
        <div class="story-box">
            <div class="story-box-title">
                <span>The 6-Month Trajectory · Executive Summary</span>
                <span>June – November 2026</span>
            </div>
            <div class="story-text">
                <p>
                    <strong>A unified intellectual practice across three altitudes:</strong> Nathan Walker's work is not a scattered collection of scripts or apps—it is a coherent body of computer science, formal mathematics, and systems engineering spanning theoretical foundations, cryptographic protocols, and production-hardened sovereign infrastructure.
                </p>
                <p>
                    <strong>Theoretical & Mathematical Formalisms:</strong> Formalized computational execution as the <em>Ontic Hyperedge</em> (<em>e</em><sub>exec</sub> = ⟨<em>V</em><sub>C</sub>, <em>V</em><sub>T</sub>, <em>V</em><sub>S</sub>, <em>V</em><sub>E</sub>, <em>V</em><sub>X</sub>, <em>V</em><sub>I</sub>, <em>V</em><sub>W</sub>, <em>V</em><sub>Q</sub>⟩), demonstrating 0.00% false attribution under concurrency versus 75.00% decay in relational joins; authored <em>Agentropy</em> (registered Zenodo DOI) establishing informational forgetting as anti-equilibrium; authored <em>The Odin Project</em> operating system treatise inverting 50 years of ambient Unix authority (<em>"State that cannot prove its right to exist cannot be committed to memory or disk"</em>); and ratified the <em>Mímir Grammar</em> and <em>Yggdrasil Workflow Nets</em> with discrete monotonic integer clocks.
                </p>
                <p>
                    <strong>Cryptographic Protocols & Sovereign Infrastructure:</strong> Invented <em>Got (Git Ontic Trace)</em>, repurposing Git Merkle DAGs and CAS object storage as a tamper-evident computational ledger; architected <em>Universal System Epoch (USE)</em> anchoring agent execution to Stratum 1 Galileo OSNMA cryptographic time and NetHSM Ed25519 signing; architected <em>The Yggdrasil Attributable Runtime Engine</em> (Four-Authority Architecture) and <em>Per-File Version Control on Shared Filesystems (MDE)</em>; architected <em>Týr</em> for zero-leakage out-of-band outcome verification; and operationalized <em>Kanidm</em> POSIX LDAPv3 kernel DAC agent fencing with zero libc overhead.
                </p>
                <p>
                    <strong>A Federated Fleet of {total_repos_count} Engines Across 6 Strategic Spheres:</strong> Conversational presence is orchestrated through Puter, The 'puter Face (<em>"Emergent intelligence from the signal"</em>), Erwin (3D avatar), Ullr (sub-second turn detection), Vitki, Qwen3-TTS, and Mœðr; observability and telemetry through Heimdall, Huginn, and Muninn; flight deck custody through Doomstadt and Doomcourt; governed by the ratified <em>Checkout Custody Standard</em>, <em>Release Doctrine</em> (ADR-0007), <em>Cutover Doctrine</em> (ADR-011), <em>Sovereign Identity Standard</em>, and <em>Domain Intelligence Schema (DIS 1.8)</em>.
                </p>
            </div>
        </div>

        <!-- Telemetry KPIs -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Capabilities Shipped</div>
                <div class="kpi-val" id="kpi-total">{total_wins}</div>
                <div class="kpi-meta">100% In-House Verified</div>
            </div>
            <div class="kpi-card" id="kpi-milestones-card" style="cursor:pointer;" title="Click to filter by Inventions & Ratified Doctrines">
                <div class="kpi-label">Inventions & Doctrines</div>
                <div class="kpi-val" id="kpi-milestones" style="color:var(--brass-bright);">{total_milestones}</div>
                <div class="kpi-meta" id="kpi-milestones-meta">{total_inventions} Inventions · {total_doctrines} Doctrines</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Active Sovereign Repositories</div>
                <div class="kpi-val" id="kpi-repos">{total_repos_count}</div>
                <div class="kpi-meta" id="kpi-repos-meta">Across 6 Strategic Spheres</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Active Shipping Days</div>
                <div class="kpi-val">{active_days}</div>
                <div class="kpi-meta">Across 20 Active Weeks</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Current Momentum</div>
                <div class="kpi-val">2.0 / day</div>
                <div class="kpi-meta">October Acceleration</div>
            </div>
        </div>
    </header>

    <!-- Interactive Heatmap Section (Month-by-Month Blocks) -->
    <section class="heatmap-section" id="heatmap-view">
        <div class="section-head">
            <h2 class="section-title">Temporal Activity Heatmap</h2>
            <div class="section-meta">Click any day or month to jump directly into the cards stream</div>
        </div>

        <div class="months-heatmap-row" id="months-heatmap-container">
            <!-- Rendered by client script -->
        </div>

        <div class="heatmap-legend">
            <span>Velocity</span>
            <div class="legend-cells">
                <div class="cell"></div>
                <div class="cell lvl-1"></div>
                <div class="cell lvl-2"></div>
                <div class="cell lvl-3"></div>
                <div class="cell lvl-4"></div>
            </div>
            <span>5+ / day</span>
        </div>
    </section>

    <!-- Controls Bar: Search, Spheres & Repository Deck -->
    <div class="controls-bar">
        <div class="search-row">
            <input type="text" class="search-input" id="search-box" placeholder="Search across all {total_repos_count} repos, inventions, doctrines, technologies, PR #, or keywords (e.g. 'ontic', 'got', 'ullr', 'kanidm', 'merkle', 'qwen', 'huginn')...">
            <button class="milestones-toggle-btn" id="milestones-toggle">
                <span class="milestone-star">★</span>
                <span>Inventions & Doctrines (<span id="milestone-count">{total_milestones}</span>)</span>
            </button>
            <button class="reset-btn" id="reset-btn">Reset All</button>
        </div>
        
        <!-- Strategic Sphere Tabs -->
        <div class="spheres-bar" id="spheres-filter">
            <!-- Rendered by client script -->
        </div>

        <!-- 46 Repositories Deck -->
        <div class="repo-deck" id="repo-deck">
            <!-- Rendered by client script -->
        </div>
    </div>

    <!-- Cards Stream Section -->
    <main class="timeline" id="cards-stream">
        <!-- Rendered by client script -->
    </main>
</div>

<!-- Floating Tooltip -->
<div id="tooltip"></div>

<script>
const WINS = {wins_json};
const MONTH_HEATMAPS = {month_heatmaps_json};
const REPOS = {repos_json};
const SPHERES = {spheres_json};

let activeSphere = "all";
let activeRepo = null;
let searchQuery = "";
let milestonesOnly = false;

const MONTH_NAMES = {{
    "2026-06": "June 2026",
    "2026-07": "July 2026",
    "2026-08": "August 2026",
    "2026-09": "September 2026",
    "2026-10": "October 2026",
    "2026-11": "November 2026"
}};

function init() {{
    renderSpheres();
    renderRepoDeck();
    renderMonthHeatmaps();
    renderCards();
    attachEvents();
}}

function renderSpheres() {{
    const bar = document.getElementById("spheres-filter");
    bar.innerHTML = "";

    Object.values(SPHERES).forEach(s => {{
        const btn = document.createElement("button");
        btn.className = "sphere-btn" + (activeSphere === s.id ? " active" : "");
        btn.dataset.sphere = s.id;
        
        // Count total wins in sphere
        let count = 0;
        if (s.id === "all") {{
            count = WINS.length;
        }} else {{
            count = WINS.filter(w => w.spheres.includes(s.id)).length;
        }}

        btn.innerHTML = `
            <span class="sphere-lead-dot" style="background:${{s.leadColor}}"></span>
            <span>${{s.short}}</span>
            <span class="repo-count">${{count}}</span>
        `;

        btn.addEventListener("click", () => {{
            activeSphere = s.id;
            activeRepo = null;
            document.querySelectorAll(".sphere-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            renderRepoDeck();
            renderMonthHeatmaps();
            renderCards();
        }});

        bar.appendChild(btn);
    }});
}}

function renderRepoDeck() {{
    const deck = document.getElementById("repo-deck");
    deck.innerHTML = "";

    const visibleRepos = Object.entries(REPOS).filter(([k, r]) => {{
        if (activeSphere === "all") return true;
        return r.sphere === activeSphere;
    }}).sort((a, b) => b[1].count - a[1].count);

    visibleRepos.forEach(([rKey, rInfo]) => {{
        if (rInfo.count === 0) return;
        const btn = document.createElement("button");
        btn.className = "repo-btn" + (activeRepo === rKey ? " active" : "");
        btn.dataset.repo = rKey;
        btn.title = rInfo.desc;

        btn.innerHTML = `
            <span class="icon-wrap">${{rInfo.iconHtml}}</span>
            <span>${{rKey}}</span>
            <span class="repo-count">${{rInfo.count}}</span>
        `;

        btn.addEventListener("click", () => {{
            if (activeRepo === rKey) {{
                activeRepo = null;
                btn.classList.remove("active");
            }} else {{
                document.querySelectorAll(".repo-btn").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                activeRepo = rKey;
            }}
            renderMonthHeatmaps();
            renderCards();
        }});

        deck.appendChild(btn);
    }});
}}

function renderMonthHeatmaps() {{
    const container = document.getElementById("months-heatmap-container");
    container.innerHTML = "";

    MONTH_HEATMAPS.forEach(m => {{
        const block = document.createElement("div");
        block.className = "month-block";
        block.dataset.month = m.key;

        const matchingMonthWins = WINS.filter(w => {{
            const inMonth = w.month === m.key;
            const matchesMilestone = !milestonesOnly || w.isMilestone;
            const matchesSphere = activeSphere === "all" || w.spheres.includes(activeSphere);
            const matchesRepo = !activeRepo || w.repos.includes(activeRepo);
            return inMonth && matchesMilestone && matchesSphere && matchesRepo;
        }});

        // Header
        const head = document.createElement("div");
        head.className = "month-block-head";
        head.innerHTML = `
            <div class="month-title">${{m.name}} ${{m.year}}</div>
            <div class="month-count-pill">${{matchingMonthWins.length}} ships</div>
        `;
        block.appendChild(head);

        // Grid of cells
        const gridWrap = document.createElement("div");
        gridWrap.className = "month-grid-wrap";

        const legendCol = document.createElement("div");
        legendCol.className = "day-legend-col";
        legendCol.innerHTML = `<div>M</div><div>W</div><div>F</div><div>S</div>`;
        gridWrap.appendChild(legendCol);

        const cellsGrid = document.createElement("div");
        cellsGrid.className = "month-cells-grid";

        // First day padding
        const firstDayOfWeek = m.days[0].dayOfWeek;
        for (let p = 0; p < firstDayOfWeek; p++) {{
            const emptyCell = document.createElement("div");
            emptyCell.className = "cell empty";
            cellsGrid.appendChild(emptyCell);
        }}

        m.days.forEach(day => {{
            const cell = document.createElement("div");
            cell.className = "cell";
            cell.dataset.date = day.date;

            const matchingDayWins = WINS.filter(w => {{
                const onDay = w.date === day.date;
                const matchesMilestone = !milestonesOnly || w.isMilestone;
                const matchesSphere = activeSphere === "all" || w.spheres.includes(activeSphere);
                const matchesRepo = !activeRepo || w.repos.includes(activeRepo);
                return onDay && matchesMilestone && matchesSphere && matchesRepo;
            }});

            const count = matchingDayWins.length;
            if (count >= 5) cell.classList.add("lvl-4");
            else if (count >= 3) cell.classList.add("lvl-3");
            else if (count >= 2) cell.classList.add("lvl-2");
            if (count >= 1) cell.classList.add("lvl-1");

            if (day.hasInvention) {{
                cell.classList.add("has-invention");
            }} else if (day.hasDoctrine) {{
                cell.classList.add("has-doctrine");
            }}

            cell.addEventListener("mouseenter", (e) => showTooltip(e, day, matchingDayWins));
            cell.addEventListener("mouseleave", hideTooltip);

            cell.addEventListener("click", (e) => {{
                e.stopPropagation();
                const target = document.getElementById("day-" + day.date);
                if (target) {{
                    target.scrollIntoView({{ behavior: "smooth", block: "center" }});
                    target.style.outline = "2px solid var(--brass)";
                    setTimeout(() => target.style.outline = "none", 2000);
                }}
            }});

            cellsGrid.appendChild(cell);
        }});

        gridWrap.appendChild(cellsGrid);
        block.appendChild(gridWrap);

        // Narrative
        const narrative = document.createElement("div");
        narrative.className = "month-narrative";
        narrative.innerText = m.narrative;
        block.appendChild(narrative);

        // Mini sphere distribution bar
        const domainBar = document.createElement("div");
        domainBar.className = "domain-bar";
        let barHtml = "";
        const totalSpheresInMonth = Object.values(m.sphereDist).reduce((a, b) => a + b, 0) || 1;
        for (const [sKey, count] of Object.entries(m.sphereDist)) {{
            const sCfg = SPHERES[sKey] || {{ leadColor: "#8E939B", short: sKey }};
            const pct = (count / totalSpheresInMonth) * 100;
            barHtml += `<div class="domain-bar-seg" style="width:${{pct}}%;background:${{sCfg.leadColor}};" title="${{sCfg.short}}: ${{count}}"></div>`;
        }}
        domainBar.innerHTML = barHtml;
        block.appendChild(domainBar);

        // Click whole month block
        block.addEventListener("click", () => {{
            const target = document.getElementById("month-divider-" + m.key);
            if (target) {{
                target.scrollIntoView({{ behavior: "smooth", block: "start" }});
            }}
        }});

        container.appendChild(block);
    }});
}}

function showTooltip(e, day, matchingWins) {{
    const tt = document.getElementById("tooltip");
    const dObj = new Date(day.date + "T12:00:00");
    const dayName = dObj.toLocaleDateString("en-US", {{ weekday: "short", month: "short", day: "numeric" }});
    
    let html = `<div class="tt-date">${{dayName}}</div>`;
    html += `<div><span class="tt-count">${{matchingWins.length}}</span> capability ships logged</div>`;
    
    if (day.hasMilestone && day.milestones && day.milestones.length > 0) {{
        let msHtml = day.milestones.map(m => {{
            const isInv = m.kind === "invention";
            const icon = isInv ? "★" : "◆";
            const label = isInv ? "ESTATE INVENTION" : "RATIFIED DOCTRINE";
            const color = isInv ? "var(--brass-bright)" : "#FF808C";
            const border = isInv ? "rgba(210,169,59,0.3)" : "rgba(163,34,47,0.4)";
            const bg = isInv ? "rgba(210,169,59,0.12)" : "rgba(163,34,47,0.15)";
            return `<div style="margin:4px 0;padding:5px 8px;background:${{bg}};border:1px solid ${{border}};border-radius:4px;font-family:var(--fm);font-size:11px;color:${{color}};font-weight:600;"><span style="margin-right:4px;">${{icon}}</span> <span style="font-size:9.5px;letter-spacing:0.08em;text-transform:uppercase;color:var(--ash);margin-right:6px;">${{label}}:</span> ${{escapeHtml(m.title)}}</div>`;
        }}).join("");
        html += msHtml;
    }}

    if (matchingWins.length > 0) {{
        html += `<ul>`;
        matchingWins.slice(0, 4).forEach(w => {{
            const repoList = w.repos.slice(0, 2).map(r => `<span class="tt-repo">[${{r}}]</span>`).join(" ");
            const msPrefix = w.isMilestone ? '<strong style="color:var(--brass-bright);">★ </strong>' : '';
            html += `<li>${{msPrefix}}${{repoList}} ${{w.shipped.slice(0, 85)}}${{w.shipped.length > 85 ? '...' : ''}}</li>`;
        }});
        if (matchingWins.length > 4) {{
            html += `<li>+ ${{matchingWins.length - 4}} more ships...</li>`;
        }}
        html += `</ul>`;
    }}

    tt.innerHTML = html;
    tt.style.display = "block";
    
    const x = e.clientX + 16;
    const y = e.clientY + 16;
    tt.style.left = Math.min(x, window.innerWidth - 400) + "px";
    tt.style.top = y + "px";
}}

function hideTooltip() {{
    document.getElementById("tooltip").style.display = "none";
}}

function renderCards() {{
    const stream = document.getElementById("cards-stream");
    stream.innerHTML = "";

    const filtered = WINS.filter(w => {{
        const matchesMilestone = !milestonesOnly || w.isMilestone;
        const matchesSphere = activeSphere === "all" || w.spheres.includes(activeSphere);
        const matchesRepo = !activeRepo || w.repos.includes(activeRepo);
        const matchesSearch = !searchQuery || 
            w.shipped.toLowerCase().includes(searchQuery) || 
            w.impact.toLowerCase().includes(searchQuery) ||
            w.repos.some(r => r.toLowerCase().includes(searchQuery)) ||
            (w.isMilestone && w.milestoneTitle.toLowerCase().includes(searchQuery)) ||
            w.date.includes(searchQuery);
        return matchesMilestone && matchesSphere && matchesRepo && matchesSearch;
    }});

    const activeReposInFiltered = new Set();
    filtered.forEach(w => w.repos.forEach(r => activeReposInFiltered.add(r)));
    document.getElementById("kpi-total").innerText = filtered.length;
    document.getElementById("kpi-repos").innerText = activeReposInFiltered.size;
    if (activeRepo) {{
        document.getElementById("kpi-repos-meta").innerText = `Isolated: ${{activeRepo}}`;
    }} else if (activeSphere !== "all") {{
        document.getElementById("kpi-repos-meta").innerText = `In ${{SPHERES[activeSphere].short}}`;
    }} else {{
        document.getElementById("kpi-repos-meta").innerText = "Across 6 Strategic Spheres";
    }}

    if (filtered.length === 0) {{
        stream.innerHTML = `<div style="padding:60px 0;text-align:center;color:var(--ash);font-family:var(--fm);">No capabilities matching criteria.</div>`;
        return;
    }}

    // Group by month
    const byMonth = {{}};
    filtered.forEach(w => {{
        if (!byMonth[w.month]) byMonth[w.month] = [];
        byMonth[w.month].push(w);
    }});

    const sortedMonths = Object.keys(byMonth).sort().reverse();

    sortedMonths.forEach(mKey => {{
        const group = document.createElement("div");
        group.className = "month-group";

        const divider = document.createElement("div");
        divider.className = "month-divider";
        divider.id = "month-divider-" + mKey;
        divider.innerHTML = `
            <div class="month-name">${{MONTH_NAMES[mKey] || mKey}}</div>
            <div class="month-meta">${{byMonth[mKey].length}} ships</div>
        `;
        group.appendChild(divider);

        const cardStream = document.createElement("div");
        cardStream.className = "cards-stream";

        const monthWinsDesc = [...byMonth[mKey]].sort((a, b) => b.date.localeCompare(a.date));

        monthWinsDesc.forEach(w => {{
            const isMs = !!w.isMilestone;
            const hasInv = w.milestones && w.milestones.some(m => m.kind === "invention");
            const hasDoc = w.milestones && w.milestones.some(m => m.kind === "doctrine");
            
            let cardExtraClass = "";
            if (isMs) {{
                cardExtraClass = hasInv ? " milestone-card invention-card" : " milestone-card doctrine-card";
            }}
            const card = document.createElement("div");
            card.className = "win-card" + cardExtraClass;
            card.id = "day-" + w.date;

            const dObj = new Date(w.date + "T12:00:00");
            const dayOfWeek = dObj.toLocaleDateString("en-US", {{ weekday: "short" }});

            let badgesHtml = "";
            w.repos.forEach(rKey => {{
                const rInfo = REPOS[rKey] || {{ iconHtml: "", sphere: "platform" }};
                badgesHtml += `
                <div class="card-repo-badge" data-repo="${{rKey}}">
                    ${{rInfo.iconHtml}}
                    <span>${{rKey}}</span>
                </div>`;
            }});

            const primarySphereKey = w.spheres[0] || "platform";
            const sphereCfg = SPHERES[primarySphereKey] || {{ short: "Platform" }};

            let milestoneBadgesHtml = "";
            if (isMs && w.milestones && w.milestones.length > 0) {{
                milestoneBadgesHtml = `<div class="milestones-container">` + w.milestones.map(m => {{
                    const isInv = m.kind === "invention";
                    const rowClass = isInv ? "invention-badge-row" : "doctrine-badge-row";
                    const icon = isInv ? `<span class="milestone-star">★</span>` : `<span class="doctrine-icon">◆</span>`;
                    const pillClass = isInv ? "milestone-pill" : "milestone-pill doctrine-pill";
                    const label = isInv ? "ESTATE INVENTION" : "RATIFIED DOCTRINE";
                    return `
                        <div class="milestone-badge-row ${{rowClass}}">
                            ${{icon}}
                            <span class="${{pillClass}}">${{label}}</span>
                            <span class="milestone-title-tag">${{escapeHtml(m.short || m.title)}}</span>
                        </div>
                        <div class="milestone-title-text">${{escapeHtml(m.title)}}</div>
                    `;
                }}).join("") + `</div>`;
            }}

            let cardMilestonePill = "";
            if (isMs) {{
                if (hasInv) {{
                    cardMilestonePill = `<div class="card-milestone-pill invention-pill">★ INVENTION</div>`;
                }} else {{
                    cardMilestonePill = `<div class="card-milestone-pill doctrine-pill">◆ DOCTRINE</div>`;
                }}
            }}

            card.innerHTML = `
                <div class="card-left">
                    <div class="card-date">${{w.date}}</div>
                    <div class="card-dayname">${{dayOfWeek}}</div>
                    ${{cardMilestonePill}}
                    <div class="card-badges">${{badgesHtml}}</div>
                    <div class="card-sphere-tag">${{sphereCfg.short}}</div>
                </div>
                <div class="card-content">
                    ${{milestoneBadgesHtml}}
                    <div class="card-shipped">${{formatText(w.shipped)}}</div>
                    <div class="card-impact">→ <strong>Impact:</strong> ${{formatText(w.impact)}}</div>
                </div>
            `;

            // Click badge on card to filter
            card.querySelectorAll(".card-repo-badge").forEach(badge => {{
                badge.addEventListener("click", (e) => {{
                    e.stopPropagation();
                    const clickedRepo = badge.dataset.repo;
                    activeRepo = clickedRepo;
                    const rInfo = REPOS[clickedRepo];
                    if (rInfo) {{
                        activeSphere = rInfo.sphere;
                        renderSpheres();
                    }}
                    renderRepoDeck();
                    renderMonthHeatmaps();
                    renderCards();
                }});
            }});

            cardStream.appendChild(card);
        }});

        group.appendChild(cardStream);
        stream.appendChild(group);
    }});
}}

function escapeHtml(str) {{
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}}

function formatText(str) {{
    if (!str) return "";
    let s = escapeHtml(str);
    // LaTeX math for ontic hyperedge
    s = s.replace(/\\(\\$e_.*?=\\s*\\\\langle\\s*(.*?)\\s*\\\\rangle\\$\\)/g, 
        '(<em>e</em><sub>exec</sub> = ⟨$1⟩)');
    s = s.replace(/V_([A-Z])/g, '<em>V</em><sub>$1</sub>');
    // Backticks to inline code
    s = s.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    return s;
}}

function attachEvents() {{
    const search = document.getElementById("search-box");
    search.addEventListener("input", (e) => {{
        searchQuery = e.target.value.toLowerCase().trim();
        renderCards();
    }});

    const msToggle = document.getElementById("milestones-toggle");
    if (msToggle) {{
        msToggle.addEventListener("click", () => {{
            milestonesOnly = !milestonesOnly;
            if (milestonesOnly) {{
                msToggle.classList.add("active");
            }} else {{
                msToggle.classList.remove("active");
            }}
            renderMonthHeatmaps();
            renderCards();
        }});
    }}

    const kpiMs = document.getElementById("kpi-milestones-card");
    if (kpiMs) {{
        kpiMs.addEventListener("click", () => {{
            milestonesOnly = !milestonesOnly;
            if (msToggle) {{
                if (milestonesOnly) msToggle.classList.add("active");
                else msToggle.classList.remove("active");
            }}
            renderMonthHeatmaps();
            renderCards();
        }});
    }}

    document.getElementById("reset-btn").addEventListener("click", () => {{
        activeSphere = "all";
        activeRepo = null;
        milestonesOnly = false;
        searchQuery = "";
        search.value = "";
        if (msToggle) msToggle.classList.remove("active");
        renderSpheres();
        renderRepoDeck();
        renderMonthHeatmaps();
        renderCards();
    }});

    document.querySelectorAll(".view-btn").forEach(btn => {{
        btn.addEventListener("click", () => {{
            document.querySelectorAll(".view-btn").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            const view = btn.dataset.view;
            const heatmapSection = document.getElementById("heatmap-view");
            const cardsStream = document.getElementById("cards-stream");

            if (view === "heatmap-only") {{
                heatmapSection.style.display = "block";
                cardsStream.style.display = "none";
            }} else if (view === "stream-only") {{
                heatmapSection.style.display = "none";
                cardsStream.style.display = "flex";
            }} else {{
                heatmapSection.style.display = "block";
                cardsStream.style.display = "flex";
            }}
        }});
    }});
}}

window.addEventListener("DOMContentLoaded", init);
</script>

</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"✓ Generated {OUTPUT_HTML} ({len(html_template)} bytes, {len(entries)} wins across {len(REPOSITORIES)} repos, {total_milestones} milestones)")

if __name__ == "__main__":
    build()
