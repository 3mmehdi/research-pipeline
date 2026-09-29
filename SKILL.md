---
name: research-pipeline
description: 'Mehdi''s "super skill" / God Mode topic research — a 14-phase NotebookLM-backed orchestration. WebSearch → NotebookLM notebook + source upload → French briefing-doc → auto-ingest (claude-obsidian:wiki-ingest) → auto-lint for contradictions (claude-obsidian:wiki-lint) → French Protocole d''Expérimentation (Zhutov-style hypothesis + checkboxes) → mind-map → visual canvas (claude-obsidian:canvas) → interactive deliverables menu (quiz / flashcards / audio overview / infographic) → final report → autonomous gap-filling pass (claude-obsidian:autoresearch). ONLY skill that produces a NotebookLM-backed, citation-rich French brief PLUS protocol PLUS canvas map PLUS on-demand podcast/quiz/flashcards PLUS an automatic autoresearch sweep of the remaining blind spots, all filed into the Obsidian vault. MUST trigger on any of: "/research-pipeline", "/research-pipeline [topic]", "super skill", "god mode", "research X using notebooklm", "send these sources to notebooklm", "build me a research notebook on X", "deep-dive X using notebooklm", "audio overview of X" (when sources still need curating), "french briefing on X", "experiments protocol on X", "canvas map of X research", "research X and file it", "full research pipeline on X", "gap-fill research on X", or any topic-in → filed-brief-out request that mentions NotebookLM, wants French output, or asks for a synthesized-and-filed artifact. NOT the same as a bare call to claude-obsidian:autoresearch — this skill curates sources into a PERSISTENT NotebookLM notebook, produces a French briefing, protocol file, and canvas, optionally spins up podcasts/quizzes/flashcards, and THEN invokes autoresearch as a final gap-filling pass (the two are composed, not competitors). Prefer this skill whenever NotebookLM, French output, God Mode, a full research pipeline, or any mention of protocol/canvas/deliverables/gap-filling tied to research is involved. Multi-phase, long-running orchestration — do NOT attempt inline; delegate to the skill. ALSO triggers on help / cheat-sheet queries — phrases like "help research", "how does this work", "list commands", "list research commands", "research cheat sheet", "what can research-pipeline do", "/research-pipeline help" — in HELP MODE the skill prints a Markdown cheat sheet covering the 14-phase workflow AND the companion commands for both plugins (claude-obsidian: /wiki, ingest [file], /save, /autoresearch [topic], /canvas, lint the wiki ; notebooklm-py: create notebook, source add URL / YouTube / PDF, generate report / audio / mind-map / quiz / flashcards / infographic, artifact wait, download), then stops — NO pipeline run in help mode. ALSO supports an iterative update loop: Phase 12 menu includes option 6 ("Add new links/sources") that re-uses the existing NotebookLM notebook to ingest fresh URLs, regenerate the briefing, re-ingest into Obsidian without breaking existing wikilinks, and lint for contradictions between old and new data — the menu then re-displays so the user can keep iterating. ALSO supports 4 additional entry modes beyond the full pipeline: (a) RESUME MODE — triggers "resume research on [[X]]", "/research-pipeline resume [[X]]", "extend my X research" — skips Phases 1-11 and jumps directly to the Phase 12 menu against an existing notebook (looked up via the wiki/meta/notebooks.md registry) ; (b) ADD-URL MODE — triggers "add this URL to my X research", "add these sources to [[X]]", "étends ma recherche X avec" — resolves the notebook_id from the registry and runs Phase 12b.2-9 directly without any menu ceremony ; (c) RECONCILE MODE — triggers "reconcile contradictions", "/research-pipeline reconcile", "resolve open contradictions in wiki" — walks through every [!contradiction] callout in the wiki and offers a structured resolution workflow ; (d) FRESHNESS MODE — triggers "research freshness check", "which topics need refresh", "/research-pipeline freshness" — scans the notebooks registry and flags topics > 6 months old for update. Phase 0 runs a vault-state pre-check on every full-pipeline call to detect topic overlap with existing research (≥ 60 % overlap → asks user to extend an existing notebook instead of creating a new silo). Phase 1 is vault-aware: scans wiki/sources/ for already-ingested URLs relevant to the topic and surfaces them alongside WebSearch results in the approval gate.'
---

# Research Pipeline — God Mode

End-to-end 14-phase orchestration. The user supplies a topic; the skill returns:

1. A filed French briefing-doc in `.raw/Projets/`
2. The briefing ingested into `wiki/` with entities/concepts/index/log updated
3. Contradiction lint pass against the existing wiki
4. A French "Protocole d'Expérimentation" file (hypothesis + checkboxes, Zhutov-style)
5. A visual canvas map of the research concepts
6. An interactive menu offering a quiz / flashcards / audio overview / infographic on demand
7. A reusable NotebookLM notebook kept alive for any further artifact the user wants later
8. An autonomous gap-filling autoresearch pass that sweeps the wider web for anything the curated NotebookLM corpus missed, filed straight into `wiki/` by the `claude-obsidian:autoresearch` sibling skill

Each phase is non-fatal for the ones after: if the canvas fails, the briefing + protocol still land; if the gap-fill pass fails, the primary deliverables still stand. The skill is tolerant by design because this is an unattended workflow.

## Help / Cheat Sheet Mode

If the user message is a help / discovery query (not an actual research request), output the cheat sheet **verbatim** and stop. **Do NOT start a pipeline. Do NOT prompt for a topic.**

**Triggers for help mode:**
- "help research" / "research help"
- "how does this work" / "how do I use research-pipeline"
- "list commands" / "list research commands"
- "research cheat sheet" / "cheat sheet"
- "what can research-pipeline do"
- "/research-pipeline help" (bare slash with `help` as argument)
- "show me the commands"

If the same message also contains a concrete research topic ("help, research transformers"), treat it as a real pipeline run rather than help mode — the help trigger should only activate for pure discovery queries.

---

### Cheat sheet (emit verbatim in HELP MODE)

```markdown
# 🧭 research-pipeline — Cheat Sheet

## Ce que fait ce skill

Gère **TOUT le cycle de vie** d'une recherche dans ton vault, en pont entre Claude, NotebookLM et Obsidian :

1. **Création** — WebSearch → notebook NotebookLM → briefing FR → ingest Obsidian → lint → protocole → canvas → livrables → autoresearch
2. **Mise à jour** — ajoute des sources à un notebook existant, met à jour le wiki en mode delta sans casser les wikilinks
3. **Reprise** — rouvre le menu des livrables sur n'importe quelle recherche déjà faite
4. **Maintenance** — résout les contradictions accumulées, audite la fraîcheur des topics, archive les obsolètes

Tous les livrables atterrissent dans le vault en **français**. Les notebooks NotebookLM restent vivants et sont centralisés dans `wiki/meta/notebooks.md`.

## Les 6 modes opérationnels

Le skill détecte le mode selon la phrase d'entrée :

| # | Mode | Quand | Triggers |
|---|---|---|---|
| **1** | **Full pipeline** | Nouveau sujet | `/research-pipeline <sujet>`, « research X using NotebookLM », « deep-dive X and file it » |
| **2** | **Help** | Découverte | « help research », « how does this work », « list commands », « /research-pipeline help » |
| **3** | **Resume** | Rouvrir le menu | « resume research on [[X]] », « extend my X research », « /research-pipeline resume [[X]] » |
| **4** | **Add URL** | Étendre un sujet | « add this URL to my X research », « étends ma recherche X avec <url1>, <url2> » |
| **5** | **Reconcile** | Résoudre contradictions | « reconcile contradictions », « resolve open contradictions », « walk me through contradictions » |
| **6** | **Freshness** | Auditer la fraîcheur | « research freshness check », « which topics need refresh », « list stale research » |

## Les phases (ce qui est produit, par mode)

### Pipeline complet (Mode 1)

| Phase | Artefact | Emplacement |
|---|---|---|
| **0** | **Vault state check** — détecte overlap ≥ 60 % avec un topic existant, porte 4 choix (extend / resume / new / cancel) | chat |
| **1** | **Phase 1 vault-aware** — scan `wiki/sources/` puis WebSearch, porte d'approbation mixte | chat |
| 2–4 | Notebook NotebookLM + sources indexées | sauvegardé dans NotebookLM |
| 5–7 | Briefing-doc français | `.raw/Projets/<date>-<slug>.md` |
| 8 | Pages wiki (entités, concepts, cross-refs) | `wiki/entités/`, `wiki/concepts/`, `wiki/cours/ia/`… |
| 9 | Rapport de lint scopé | `wiki/meta/lint-report-<date>.md` |
| 10 | Protocole d'Expérimentation (FR, hypothèses + cases à cocher) | `.raw/Projets/<date>-<slug>-protocole.md` |
| 11 | Carte canvas (mind-map → .canvas) | `wiki/meta/canvas/<date>-<slug>-map.canvas` |
| 12 | Menu interactif : quiz / flashcards / audio / infographic / **add sources** / none | `.raw/Projets/…` |
| **12b** | *(option 6)* Nouvelles URL → notebook + briefing + wiki mis à jour + lint | `.raw/Projets/<date>-<slug>-update-<timestamp>.md` |
| 13 | Résumé + **mise à jour du registre `wiki/meta/notebooks.md` et de `hot.md`** | chat + registre |
| 14 | Rattrapage autoresearch (nouvelles pages wiki) | via `claude-obsidian:autoresearch` |
| **17** | *(post-Phase-12 option 3)* Hook transcription podcast → source wiki | `.raw/Projets/audio/<slug>-transcript.md` |

### Phases alternes (Modes 3-6)

| Mode | Phase | Ce qui se passe |
|---|---|---|
| **3 Resume** | **Phase R** | Lit `notebooks.md` → résout `notebook_id` → jump direct au menu Phase 12 (sans 1-11) |
| **4 Add URL** | **Phase A** | Lit `notebooks.md` → exécute Phase 12b.2-9 directement, pas de menu |
| **5 Reconcile** | **Phase 15** | Parcours de chaque `[!contradiction]` avec 6 options de résolution (keep-initial / keep-alt / both-valid / defer / skip / stop) |
| **6 Freshness** | **Phase 16** | Buckets vert/jaune/orange/rouge selon âge → propose update/autoresearch/archive per topic |

## Le registre central : `wiki/meta/notebooks.md`

**Source de vérité** pour tous les notebooks NotebookLM vivants. Centralise le pont wiki ↔ NotebookLM.

Contient :
- Tableau des **notebooks actifs** : topic, `notebook_id`, créé, dernière MAJ, sources, contradictions, page wiki principale, briefing
- Queries **Dataview** pour freshness tracking et liste des contradictions actives
- **Commandes de reprise rapide** (Modes 3 et 4)
- Section **« notebooks archivés »** pour les topics clos

**Mis à jour automatiquement par** :
- Phase 13 (nouveau topic créé)
- Phase 12b.9 (après chaque update pass)
- Phase 16 (archivage manuel en freshness audit)

## Commandes compagnons

### 🗂 claude-obsidian — opérations sur le wiki Obsidian

| Commande | Ce qu'elle fait |
|---|---|
| `/wiki` | Bootstrap ou health-check du vault |
| `ingest <fichier>` ou `/claude-obsidian:wiki-ingest <fichier>` | Lit une source, extrait entités/concepts, crée/met à jour les pages wiki avec cross-refs |
| `/save` ou « save this » | Archive la conversation courante comme note wiki |
| `/autoresearch <sujet>` ou « research <sujet> and file it » | Boucle web autonome → pages wiki synthétisées |
| `/canvas` ou « create canvas » | Crée/édite un canvas Obsidian (fichiers `.canvas`) |
| `lint the wiki` ou `/claude-obsidian:wiki-lint` | Health check : pages orphelines, liens morts, contradictions, frontmatter incomplet |

### 🎙 notebooklm-py — CLI NotebookLM (commandes directes)

**Création de notebook**
```bash
notebooklm create "<titre>" --json
```

**Ajout de sources** (l'une des trois formes selon la nature de la source)
```bash
# Page web
notebooklm source add "https://example.com/article" -n <notebook_id> --json

# Vidéo YouTube (URL directe)
notebooklm source add "https://www.youtube.com/watch?v=XXXXXX" -n <notebook_id> --json

# PDF local
notebooklm source add "/chemin/vers/fichier.pdf" -n <notebook_id> --json
```

**Gestion des sources**
```bash
notebooklm source list -n <notebook_id> --json          # Liste des sources
notebooklm source wait <source_id> -n <nb> --timeout 600  # Attend l'indexation
```

**Génération de livrables** (toujours `--language fr` dans ce vault)
```bash
# Briefing-doc / note de synthèse
notebooklm generate report --format briefing-doc --language fr -n <id> --json

# Audio Overview (podcast FR, format deep-dive)
notebooklm generate audio "<consignes en français>" --language fr -n <id> --json

# Mind-map (JSON hiérarchique)
notebooklm generate mind-map -n <id> --json

# Quiz (Markdown)
notebooklm generate quiz --language fr -n <id> --json

# Flashcards (Markdown, import spaced-repetition)
notebooklm generate flashcards --language fr -n <id> --json

# Infographic (PNG)
notebooklm generate infographic --language fr --orientation portrait -n <id> --json

# Vidéo explicative
notebooklm generate video "<consignes FR>" --language fr -n <id> --json
```

**Cycle attendre + télécharger**
```bash
notebooklm artifact wait <task_id> -n <nb> --timeout 1200
notebooklm download <type> "<chemin_sortie>" -a <task_id> -n <nb>
```

où `<type>` ∈ `report`, `audio`, `mind-map`, `quiz`, `flashcards`, `infographic`, `video`.

**Gestion générale**
```bash
notebooklm list --json               # Tous vos notebooks
notebooklm artifact list -n <id>     # État des tâches du notebook
notebooklm login                     # Re-authentifier si AUTH_REQUIRED
notebooklm --help                    # Référence CLI complète
```

## Recettes courantes

### Étendre un sujet existant (Mode 4 — le plus rapide)

Depuis n'importe quel contexte :
```
« add this URL to my Claude Design research: https://nouveau.com/article »
« étends ma recherche Claude Code avec https://url1 et https://url2 »
```
Le skill résout `notebook_id` depuis `notebooks.md` → Phase 12b.2-9 directement. Pas de menu, pas de briefing complet à refaire. Jusqu'à 3 passes par session.

### Rouvrir le menu livrables (Mode 3 — Resume)

```
« resume research on [[Claude Code]] »
« extend my Claude Design research »
```
Jump direct au menu Phase 12 contre le notebook existant. Idéal pour générer un quiz, des flashcards ou un podcast sur un topic déjà filé.

### Depuis le menu Phase 12 (option 6)

Après un pipeline complet, picke **6** dans le menu pour déclencher la Phase 12b (même flux que Mode 4). Le menu se ré-affiche après chaque passe, jusqu'à 3 max.

### Résoudre les contradictions accumulées (Mode 5)

```
« reconcile contradictions »
```
Walk interactif de chaque `[!contradiction]` dans le wiki, avec 6 options par conflit.

### Audit trimestriel de fraîcheur (Mode 6)

```
« research freshness check »
```
Liste les topics > 6 mois → propose update/autoresearch/archive pour chacun.

### Équivalent CLI brut (hors skill)

Si tu veux court-circuiter le skill :
```bash
notebooklm source add "<url>" -n <notebook_id> --json
notebooklm generate report --format briefing-doc --language fr -n <notebook_id> --json
# puis Skill(claude-obsidian:wiki-ingest, <briefing>) + Skill(claude-obsidian:wiki-lint, ...)
```

## Manuel complet

Pour le fonctionnement détaillé du skill, ouvre [[00_manuel/research-pipeline|le manuel complet]] — philosophie, architecture, chaque phase en profondeur, FAQ.

## Règle de langue

Tout livrable écrit dans le vault est en français. Toujours passer `--language fr` explicitement à chaque `notebooklm generate …`. Ne JAMAIS utiliser `notebooklm language set fr` (paramètre global fragile qui affecte d'autres skills).

## Dépannage

| Symptôme | Remède |
|---|---|
| `AUTH_REQUIRED` sur `notebooklm create` | `notebooklm login` dans un terminal interactif |
| `source add` timeout 30 s | La source est souvent ajoutée côté serveur malgré l'erreur — vérifier avec `notebooklm source list` |
| Rate-limit sur `generate audio/quiz/flashcards` | Retry après 5 min |
| Wiki-ingest crée des doublons | Relire le prompt ingest : rappeler qu'il s'agit d'un update et pointer vers la page existante |
| Le canvas ne s'ouvre pas | Le JSON mind-map est préservé dans `AppData/Local/Temp/` — relancer la création de canvas manuellement |
```

---

## Operational modes

The skill routes the user's message to one of **6 modes** based on trigger phrasing. Detect the mode BEFORE doing anything — different modes skip different phases.

| # | Mode | Triggers | Phases executed |
|---|---|---|---|
| 1 | **Full pipeline** (default) | `/research-pipeline <topic>`, « research X using NotebookLM », « deep-dive X and file it », etc. | 0 → 14 |
| 2 | **Help / cheat sheet** | « help research », « how does this work », « list commands », « research cheat sheet », « /research-pipeline help » | Cheat sheet only |
| 3 | **Resume** — re-enter the menu for an existing notebook | « resume research on [[X]] », « /research-pipeline resume [[X]] », « extend my X research », « continue research on X » | Skip 1-11 → **Phase 12 menu** against existing notebook |
| 4 | **Add URL** — append sources to an existing notebook without menu | « add this URL to my X research », « add these sources to [[X]] », « étends ma recherche X avec … », « expand X with <URLs> » | **Phase 12b.2 → 12b.9** directly, max 3 passes/session |
| 5 | **Reconcile** — resolve open contradictions interactively | « reconcile contradictions », « /research-pipeline reconcile », « resolve open contradictions in wiki », « walk me through contradictions » | **Phase 15** (reconcile workflow) |
| 6 | **Freshness** — audit outdated research topics | « research freshness check », « which topics need refresh », « /research-pipeline freshness », « list stale research » | **Phase 16** (freshness audit) |

Modes 3 and 4 require a `notebook_id` resolution. **Always resolve via `wiki/meta/notebooks.md`** first (the registry), with a fallback to reading the `notebook_id` field from the frontmatter of the wiki page mentioned in the trigger (e.g. `[[Claude Code]]`). If no match is found, emit `✗ No existing notebook found for "<topic>". Did you mean "<closest_match>"? Or run /research-pipeline <topic> to start fresh.` and stop.

## The notebooks registry — `wiki/meta/notebooks.md`

Single source of truth for all living NotebookLM notebooks created by this skill. Every full-pipeline run and every update pass MUST update this file (see Phase 13 and Phase 12b.9).

**Schema** (respect it — the skill reads the table programmatically via grep):

```markdown
| Sujet | Notebook ID | Créé | Dernière MAJ | Sources | Contradictions ouvertes | Page wiki principale | Dernier briefing |
|---|---|---|---|---|---|---|---|
| <Topic> | `<uuid>` | YYYY-MM-DD | YYYY-MM-DD | <N> | <K> (<pages>) | [[<Entity page>]] | [[<Source summary>]] |
```

The registry lives at `$VAULT/wiki/meta/notebooks.md`. Bootstrap it on first use if it doesn't exist — template is in the file itself (it already seeds Dataview queries for freshness and contradictions).

---

## When to trigger

- Slash form: `/research-pipeline <topic>` or `/research-pipeline [folder] <topic>`
- Natural phrasing: "research X using NotebookLM", "build me a research notebook on X", "deep-dive X and file it"
- Whenever the goal is "gather sources + synthesize into a filed brief" rather than a one-shot answer

## Language rule (important)

**All generated artifacts must be in French.** This is a standing requirement for this vault. Every `notebooklm generate *` call in this skill — report, audio, video, quiz, flashcards, slide deck, infographic — must pass `--language fr` explicitly. Do not rely on the global `notebooklm language get` setting: it affects all notebooks in the account and is brittle. Always pass the flag.

When the user later returns to a notebook created by this skill and asks for, e.g., a podcast or quiz, reuse the same rule:

- Podcast: `notebooklm generate audio "<instructions en français>" --language fr --notebook <id>`
- Quiz: `notebooklm generate quiz --language fr --notebook <id>`
- Video: `notebooklm generate video "<instructions en français>" --language fr --notebook <id>`
- Slide deck / infographic: same pattern, always `--language fr`

The steering prompts passed via `--append` or as the positional instructions should also be written in French — models follow the language of the instructions they're given.

## Defaults (override by asking)

| Setting | Default | Override by |
|---|---|---|
| Articles to search | 8 | Asking for more/fewer |
| YouTube videos to search | 4 | Asking for more/fewer |
| Output folder | `.raw/Projets/` | `/research-pipeline [Cours/ai] <topic>` |
| Report format | `briefing-doc` | Asking for `study-guide` or `blog-post` |
| Language | `fr` | Non-negotiable for this vault |
| Keep notebook after | yes | User can delete manually if they want |

Vault root: `$VAULT/` (Windows path with forward slashes works in bash).

## Pre-flight

None. Skip straight to Phase 1.

The NotebookLM CLI is persistently authenticated on this machine via `C:\Users\mehdi\.notebooklm\storage_state.json`, and a gratuitous pre-flight check (e.g., `notebooklm list --json`) just adds latency and a failure surface when the auth is in fact fine. If auth ever *does* expire (Google session cookies eventually roll), `notebooklm create` will fail loudly with `AUTH_REQUIRED` — handle that the same way as any other Phase 2 failure: stop, tell the user to refresh login in their own terminal, don't retry blindly.

In other words: trust the happy path; let the first real CLI call double as the auth check.

## The pipeline

### Phase 0 — Vault state check (full pipeline only)

Runs ONLY on **Mode 1** (full pipeline). Modes 2-6 skip this.

Goal : avant de créer un nouveau notebook et de brûler 20 min de pipeline, vérifier si le sujet overlap avec un topic de recherche existant. Évite les silos.

1. **Read the registry.** `wiki/meta/notebooks.md` — extract the list of active topics + their `notebook_id`s.

1b. **QMD semantic pre-check (NEW, added 2026-04-24).** Before the registry overlap heuristic, run `qmd query "<user_topic>" -c mehdi-vault` to detect vault coverage that might not yet be tracked in the notebooks registry (ex : content ingested via `/claude-obsidian:wiki-ingest` without a NotebookLM notebook, early research filed manually, legacy pages from before the registry). This broadens overlap detection beyond "topics with an active notebook".

   - **Run the query** : `qmd query "<user_topic>" -c mehdi-vault` (hybride BM25 + vecteur + rerank, expansion auto). Fallback `qmd search "<user_topic>" -c mehdi-vault` si la première rend vide.
   - **Count and inspect top results.** If **≥ 5 pertinent hits** land in `wiki/entités/`, `wiki/concepts/`, `wiki/cours/*/`, or `wiki/sources/` (not just `wiki/log.md` or `wiki/index.md` which match everything), treat this as **vault coverage detected**.
   - **Augment the gate** : when Phase 0 would otherwise say "No overlap" (< 30 % from the registry alone) BUT QMD surfaced ≥ 5 pertinent pages, upgrade the decision to a soft gate :
     > Aucun notebook NotebookLM existant ne couvre « <user_topic> », mais le vault contient déjà **<N> pages pertinentes** (aperçu : <top_3_titles>). Tu préfères :
     >   1. **Pipeline complet** (nouveau notebook, briefing frais, ingest qui croisera les pages existantes)
     >   2. **Autoresearch gap-fill** (`/claude-obsidian:autoresearch <user_topic>` — moins lourd, file uniquement les blind spots)
     >   3. **Résumer ce que j'ai déjà** (lecture des N pages + synthèse en chat, zéro fichier créé)
     >   4. **Continuer pipeline complet sans crédit aux pages existantes**
     >
     > Ta réponse ?
   - **If QMD returns < 5 pertinent hits** → silent, proceed to step 2 (registry overlap heuristic) as before.
   - **If `qmd` binary is unavailable or returns an error** → log a one-line warning and skip to step 2.

2. **Overlap heuristic.** For each active topic, compute a naive overlap score against the user's topic :
   - **Strong overlap (≥ 60 %)** : same primary entity (e.g. « Claude Code » vs « Claude Code best practices 2026 »), or ≥ 3 shared key terms.
   - **Partial overlap (30–59 %)** : shared sub-domain (e.g. « Claude Design » vs « Figma alternatives »).
   - **No overlap (< 30 %)** : unrelated topics, proceed normally.
3. **Decision gate** :
   - **Strong overlap detected** → ask verbatim :
     > Le sujet « <user_topic> » recouvre significativement une recherche existante : « <existing_topic> » (notebook `<notebook_id>`, dernière MAJ <date>, <N> sources, page wiki [[<entity_page>]]).
     >
     > Préfères-tu :
     >   1. **Étendre** le notebook existant (je lance le Mode 4 / Add-URL, tu me donnes les nouvelles URL)
     >   2. **Reprendre** le menu deliverables sur le notebook existant (Mode 3 / Resume)
     >   3. **Créer un nouveau thread** (je continue avec Phase 1 — nouveau notebook, nouveau briefing)
     >   4. **Annuler**
     >
     > Ta réponse ?

   - **Partial overlap detected** → info-only, no gate :
     > Ce sujet touche partiellement à la recherche existante « <existing_topic> » (notebook `<notebook_id>`). Je continue avec un nouveau notebook, mais je vais scanner ses sources en Phase 1 pour éviter les doublons.

   - **No overlap** → silent, proceed directly to Phase 1.

4. **If the registry file doesn't exist yet** (first run of the skill on this vault) : bootstrap it using the template embedded in `wiki/meta/notebooks.md` (the template was seeded during skill install). Continue to Phase 1 with no overlap detection.

5. **On user decision** :
   - « 1 » → go to Mode 4 (Add-URL) with the existing `notebook_id`
   - « 2 » → go to Mode 3 (Resume) with the existing `notebook_id`
   - « 3 » → proceed to Phase 1 as normal
   - « 4 » → stop the skill, emit `✗ Pipeline cancelled by user.`

**Non-fatal.** If the overlap check itself fails (e.g. registry malformed, grep error), log a one-line warning and proceed to Phase 1 as a fresh pipeline. Never block on a state-check failure.

### Phase 1 — Discover sources (WebSearch + vault scan)

Goal: land a mixed list of authoritative articles and relevant YouTube videos. Quality over quantity.

#### 1a — Vault scan (cheap, runs first)

Before WebSearch, scan `wiki/sources/` for URLs that are already in the vault and relevant to this topic. Useful when Phase 0 flagged a partial overlap — those sources can be surfaced in the approval gate alongside new web results.

```bash
# Extract all URLs + titles already in wiki sources, with the topic of each
grep -rE '^(source_url|url):|^- url:' "$VAULT/wiki/sources/" 2>/dev/null | head -200
```

Build a mental map `{url → (source_page, topic)}`. When a vault URL keyword-matches the new topic (shared primary entity, ≥ 2 shared nouns), mark it as a **"déjà dans le vault"** candidate.

#### 1b — WebSearch

- Run 2–3 `WebSearch` queries. Vary phrasing: one literal, one with "best practices" / "guide" / "2026", one with "youtube" or "site:youtube.com" to bias toward video results.
- For any URL that looks like a YouTube shorts/playlist/channel rather than a concrete video, drop it — NotebookLM ingests single video URLs best.
- Prefer sources from the last 24 months unless the topic is intrinsically historical.
- Deduplicate by domain where possible (max 2 per domain) to diversify perspectives.
- **Auto-deduplicate against the vault.** If a WebSearch result URL is already flagged as a vault source, merge it — keep the URL, add a tag `(déjà dans [[<source_page>]])` to its entry in the approval list.

#### 1c — Approval gate (user interaction)

Present to user before uploading. Format as a numbered list grouped :

1. **« Déjà dans ton vault (réutilisables) »** — URLs from step 1a that match the topic. Each entry : `<title> — <url> (actuellement dans [[<source_page>]])`.
2. **« Articles web »** — new articles from 1b.
3. **« Vidéos YouTube »** — new YouTube videos from 1b.

Ask verbatim :

> J'ai trouvé <N_vault> URL déjà dans ton vault et <N_new> nouvelles URL sur le web. Voici la liste complète. Je peux :
>   - Ingérer **tout** dans le nouveau notebook (les URL déjà dans ton vault seront re-référencées côté notebook)
>   - **Exclure** certaines (donne les numéros à retirer)
>   - **Swap** des URL (ex: « remplace 3 par <nouvelle_url> »)
>
> Prêt à procéder, ou tu veux changer quelque chose ?

This is the only interactive gate in the full-pipeline flow — everything after is fire-and-forget via subagents.

### Phase 2 — Create the notebook

Slugify the topic for the title-tail (see `scripts/finalize_note.py` slug rules) and create:

```bash
notebooklm create "Research: <topic>" --json
```

Parse `id` from the JSON output. Store as `$NOTEBOOK_ID`. Also save a local sources manifest — a JSON file at `/tmp/research-<slug>-sources.json` containing `[{"url": "...", "title": "..."}, ...]`. `finalize_note.py` reads this later.

### Phase 3 — Add sources

For each approved URL, call:

```bash
notebooklm source add "<url>" --notebook "$NOTEBOOK_ID" --json
```

Capture `source_id` from each. If one source fails (404, paywall, anti-bot), log a one-line warning and continue — a single bad URL should not kill the run. Collect successful `source_id`s into a list for the wait phase.

**Serialize these adds, do not parallelize.** Parallel `source add` calls trigger 30-second RPC timeouts on NotebookLM's side (observed on CLI 0.3.4). Even when the RPC reports an error, the source often ends up added server-side, producing duplicates or confusing state. Run them one after another in a single chained bash loop with a generous `timeout` on the Bash tool (e.g., 600000ms for 10 sources):

```bash
NB=<notebook_id>
for url in "<url1>" "<url2>" ... ; do
  echo "=== adding: $url ==="
  notebooklm source add "$url" --notebook "$NB" --json 2>&1 | head -5 || echo "(continuing)"
done
notebooklm source list -n "$NB" --json
```

YouTube sources show `"url": null` in `source list` output — they're stored as YouTube-typed sources rather than web-page URLs. That's expected; don't treat it as a failure.

### Phase 4 — Wait for source processing (subagent)

Processing takes 30s–10min per source. Spawn a `general-purpose` subagent:

```
Task(
  description="Wait for NotebookLM sources to index",
  prompt="Wait for all of these source_ids in notebook <NOTEBOOK_ID> to reach status=ready.
          For each id in [<list>]: run `notebooklm source wait <id> -n <NOTEBOOK_ID> --timeout 600`.
          If any source returns exit code 1 (failed), note it but continue waiting for the rest.
          Report back: list of ready source_ids and list of failed source_ids. Under 100 words.",
  subagent_type="general-purpose"
)
```

If more than half the sources fail, stop and ask the user how to proceed — the report won't be useful on a thin corpus.

### Phase 5 — Generate the French briefing report

```bash
notebooklm generate report \
  --format briefing-doc \
  --language fr \
  --append "$STEERING_PROMPT" \
  --notebook "$NOTEBOOK_ID" \
  --json
```

Parse `task_id` from the output.

**Steering prompt template** (write it in French — models align to the instruction language):

```
Rédige ce document entièrement en français. N'utilise l'anglais que pour les
noms propres, les termes techniques intraduisibles et les citations textuelles
sourcées. Structure attendue :
1. Introduction et contexte du sujet.
2. Synthèse transversale des idées principales présentes dans les sources.
3. Sections thématiques détaillées, chacune avec citations entre crochets
   renvoyant aux sources numérotées de NotebookLM.
4. Points de désaccord ou de débat entre les sources, s'il y en a.
5. Recommandations pratiques et pistes d'approfondissement.
6. Conclusion.
Style : rigoureux, dense, factuel. Cite systématiquement les sources.
```

Substitute this into `$STEERING_PROMPT` as a single-line bash variable (escape quotes with `\"` or use a heredoc-fed env var).

### Phase 6 — Wait + download (subagent)

Artifacts take 5–20 min. Spawn a subagent:

```
Task(
  description="Wait for report and download",
  prompt="Wait for NotebookLM artifact <task_id> in notebook <NOTEBOOK_ID> to complete,
          then download the report markdown.
          Step 1: `notebooklm artifact wait <task_id> -n <NOTEBOOK_ID> --timeout 1200`
          Step 2: `notebooklm download report /tmp/research-<slug>-raw.md -a <task_id> -n <NOTEBOOK_ID>`
          If step 1 times out (exit code 2), run `notebooklm artifact list -n <NOTEBOOK_ID>` and report the current status instead of failing.
          Report: final file path if successful, or status if still pending.",
  subagent_type="general-purpose"
)
```

### Phase 7 — Finalize to vault (script)

Run the bundled finalizer to prepend vault-compliant frontmatter and place the file:

```bash
python $SKILL_DIR/scripts/finalize_note.py \
  --input "/tmp/research-<slug>-raw.md" \
  --topic "<topic>" \
  --slug "<slug>" \
  --notebook-id "$NOTEBOOK_ID" \
  --sources-json "/tmp/research-<slug>-sources.json" \
  --output-dir "$VAULT/.raw/Projets/" \
  --language fr
```

The script writes to `<output-dir>/<YYYY-MM-DD>-<slug>.md` and prints the final path. Capture that stdout line — it's the canonical path for Phase 8.

### Phase 8 — Auto-ingest into the wiki

This is not optional. Immediately after `finalize_note.py` prints the final path, invoke the sibling skill `claude-obsidian:wiki-ingest` on that exact file so the new briefing is promoted into `wiki/` with entities, concepts, cross-references, and log entry in one pass.

Invocation:

```
Skill(skill="claude-obsidian:wiki-ingest", args="<FINAL_PATH_OR_FILENAME>")
```

- Pass the **full path** that `finalize_note.py` printed (e.g. `$VAULT/.raw/Projets/2026-04-20-claude-code-best-practices-optimization-workflow.md`). If the ingest skill only accepts bare filenames, fall back to just `<YYYY-MM-DD>-<slug>.md` — both should resolve because the file now lives in the canonical `.raw/` tree the wiki skill scans.
- Do not ask the user to confirm before ingesting. The whole point of this skill is an autonomous topic-in, wiki-entry-out flow.
- If the wiki-ingest call fails, surface the error in Phase 9 so the user knows the file is filed but not yet promoted — do not treat this as a fatal error for the pipeline overall, since the raw file is still intact in `.raw/Projets/`.

### Phase 9 — Auto-lint for contradictions

Right after the wiki-ingest step succeeds, run a contradiction check so that any claim in the new briefing that conflicts with existing wiki pages gets flagged with a `[!contradiction]` callout on both sides.

Invocation:

```
Skill(skill="claude-obsidian:wiki-lint",
      args="contradiction check on pages created/updated by the 2026-MM-DD ingest of <slug>. Compare new claims against existing wiki pages; on any conflict add a > [!contradiction] callout on both the new source summary AND the pre-existing page. Do not silently overwrite. Pages to check: <pipe-separated list of pages_created + pages_updated from the manifest entry that finalize + ingest just wrote>.")
```

Why we scope the lint to just the new pages rather than a full wiki sweep: full-vault lint is a larger operation that the user runs deliberately (`lint the wiki`). Here we only care about *new* contradictions introduced by this ingest.

Capture the lint report (which pages got contradiction callouts, if any) for the final Phase 13 summary.

**Non-fatal.** If lint fails or produces no contradictions, proceed to Phase 10.

### Phase 10 — Protocole d'Expérimentation (Zhutov-style action plan)

Read the briefing at `<final_briefing_path>` and generate a companion **action plan** in French. Purpose: turn the briefing's synthesis into concrete hypotheses the user can test, with checkboxes to track progress. Inspired by the Zhutov method's hypothesis → experiment → verification loop.

Structure — produce the body in French, then run the bundled finalizer:

```markdown
# Protocole d'Expérimentation — <topic>

## Contexte
<1-2 phrases reliant le briefing à une question pratique ou une décision à prendre.>

## Hypothèse principale
> <Énoncé testable et falsifiable, tiré de la synthèse du briefing.>

## Sous-hypothèses
- **H1.** ...
- **H2.** ...

## Expériences
### E1 — <titre>
- [ ] Étape 1 : ...
- [ ] Étape 2 : ...
- [ ] Étape 3 : ...
**Résultat attendu :** ...
**Métrique de succès :** ...
**Contre-preuve (ce qui invaliderait l'hypothèse) :** ...

### E2 — <titre>
... (pareil)

## Décisions à prendre
- [ ] ...
- [ ] ...

## Échéance estimée
<1 semaine / 1 mois / etc.>

## Prochaines actions immédiates
- [ ] ...
- [ ] ...
```

Then run:

```bash
python $SKILL_DIR/scripts/finalize_protocol.py \
  --body-file "<tmp path with the body Claude just produced>" \
  --topic "<topic>" \
  --slug "<slug>" \
  --briefing-filename "<YYYY-MM-DD-<slug>.md>" \
  --output-dir "$VAULT/.raw/Projets/" \
  --language fr
```

The script prepends vault frontmatter and writes to `.raw/Projets/<YYYY-MM-DD>-<slug>-protocole.md`. Capture the printed path.

**Non-fatal.** If the model can't produce a sensible protocol (e.g., the briefing topic is non-actionable), skip with a warning in the final report rather than blocking the rest of the pipeline.

### Phase 11 — Mind-map → Visual canvas

Step 1 — generate the mind-map JSON (sync, ~instant per notebooklm docs):

```bash
notebooklm generate mind-map --notebook "$NOTEBOOK_ID" --json
# may return a task_id; mind-map is usually sync so it's ready immediately
notebooklm download mind-map "$TMP/research-<slug>-mindmap.json" -n "$NOTEBOOK_ID"
```

Step 2 — hand the JSON to the canvas skill:

```
Skill(skill="claude-obsidian:canvas",
      args="create a new canvas 'Research Map — <topic>' under wiki/meta/canvases/. Read the NotebookLM mind-map JSON at $TMP/research-<slug>-mindmap.json and materialize it as a canvas: one text card per node, hierarchical tree layout (root centered, children fanning out), edges following the parent-child structure. Where a node label matches an existing wiki page title (case-insensitive), add it as a wiki-page card (embedded) instead of a plain text card so the canvas becomes navigable. Canvas file should be saved as wiki/meta/canvases/<YYYY-MM-DD>-<slug>-map.canvas.")
```

If the canvas skill's API is simpler than this (e.g., it only accepts "add text X to canvas Y"), fall back to: Claude reads the mind-map JSON itself, walks the node tree, and invokes canvas once per node with an `add text` or `add note` operation. The important output is a `.canvas` file under `wiki/meta/canvases/` with the research topology visualized.

**Non-fatal.** Mind-map generation is reliable per notebooklm docs, but canvas skill behavior is less predictable. If the canvas step fails, capture the mind-map JSON path for the final report so the user can retry manually.

### Phase 12 — Interactive Deliverable Menu

All autonomous work is now done. Pause and display **one message** to the user with a numbered menu. Wait for their numeric reply before acting.

Menu text (write this verbatim):

```
Research, ingestion, linting, action plan, and canvas map complete!

The NotebookLM notebook is still alive (ID: <NOTEBOOK_ID>) and can produce one more deliverable in French, OR be expanded with new sources. Pick a number:

  1. Quiz (Markdown, for review)
  2. Flashcards (Markdown, for spaced-repetition import)
  3. Audio Overview (French podcast, 10–20 min to generate)
  4. Infographic (PNG, visual one-pager)
  5. None — I'm done for now.
  6. Add new links/sources to expand this topic (updates the briefing + wiki in place).
```

Map the numeric reply to a notebooklm command. **Always pass `--language fr`** and place the steering prompt (if any) in French.

| Choice | Command | Output path |
|---|---|---|
| 1 Quiz | `notebooklm generate quiz --language fr --notebook "$NOTEBOOK_ID" --json` → subagent waits → `notebooklm download quiz --format markdown ".raw/Projets/<slug>-quiz.md" -a <task_id> -n "$NOTEBOOK_ID"` | `.raw/Projets/<slug>-quiz.md` |
| 2 Flashcards | `notebooklm generate flashcards --language fr --notebook "$NOTEBOOK_ID" --json` → wait → `notebooklm download flashcards --format markdown ".raw/Projets/<slug>-flashcards.md" -a <task_id> -n "$NOTEBOOK_ID"` | `.raw/Projets/<slug>-flashcards.md` |
| 3 Audio | `notebooklm generate audio "<consignes en français : format deep-dive, deux experts, ton clair et dense>" --language fr --notebook "$NOTEBOOK_ID" --json` → wait → `notebooklm download audio ".raw/Projets/audio/<slug>.mp3" -a <task_id> -n "$NOTEBOOK_ID"` | `.raw/Projets/audio/<slug>.mp3` |
| 4 Infographic | `notebooklm generate infographic --language fr --orientation portrait --detail standard --notebook "$NOTEBOOK_ID" --json` → wait → `notebooklm download infographic ".raw/Projets/infographics/<slug>.png" -a <task_id> -n "$NOTEBOOK_ID"` | `.raw/Projets/infographics/<slug>.png` |
| 5 None | Skip to Phase 13. | — |
| 6 Add sources | Go to **Phase 12b** (update loop — prompt for URLs, add to existing notebook, regenerate briefing, re-ingest, lint, return to this menu). | See Phase 12b output paths |

For choices 1–4, spawn a `general-purpose` subagent to run the `artifact wait` (timeout: 1200s for quiz/flashcards, 1800s for audio, 1500s for infographic) and then the download, per the long-wait pattern already established in Phase 6. Audio, quiz, flashcards, and infographic generation are rate-limit-prone per the notebooklm docs — if generation fails with a rate-limit error, retry once after 5 min, then report the failure.

**Post-option-3 hook.** If the user picked **3 (Audio)** and the download succeeded, automatically proceed to **Phase 17 (podcast transcription hook)** before continuing to Phase 13. Phase 17 offers to transcribe the MP3 and file the transcript as a wiki source — non-fatal, user can decline.

If the user types something other than 1-6 (e.g., "actually just give me a podcast about the RAG chapters"), treat it as a natural-language override: parse intent, pick the closest command, confirm once, proceed. If the user says things like "add these URLs" or pastes URLs directly, treat as option 6.

**Loop behavior.** Choices 1–4 complete a single deliverable and then move directly to Phase 13 (no re-prompt of the menu — the user can run `notebooklm` directly against the retained notebook ID for further artifacts). Choice 6 (update loop) is the ONE re-entry point: after Phase 12b completes, the menu is re-displayed for another pass. Cap at **3 update passes per session** to prevent runaway — after the 3rd, force-close with a reminder that further expansion should be a new research thread.

### Phase 12b — Update loop (menu option 6)

Triggered only when the user picks **6** in the Phase 12 menu (or pastes URLs in response to the menu). Goal: absorb new sources into the existing NotebookLM notebook, regenerate the French briefing with an update-oriented steering prompt, re-ingest into the Obsidian wiki in **delta mode** (update existing pages, do not duplicate, do not break existing wikilinks), lint for new contradictions between old and new data, then redisplay the menu.

#### 12b.1 — Collect new URLs from the user

Prompt verbatim:

> Paste one or more new URLs (articles, YouTube videos, or file paths for local PDFs), one per line. I'll add them to the existing notebook and regenerate the briefing. Send an empty message to cancel.

Parsing rules:
- One URL per line — strip any numbering (`1. `, `- `, `* `).
- Also accept comma-separated on one line.
- Accept `http://`, `https://`, `www.` (normalize to `https://`), and absolute Windows paths ending in `.pdf`.
- Skip any line that isn't a URL or a `.pdf` path.
- If zero valid entries are parsed, emit `✗ No valid URLs parsed — returning to menu.` and loop back to the Phase 12 menu without consuming an update pass.

#### 12b.2 — Add new sources to the existing notebook (serialized)

Reuse the same serialized pattern as Phase 3 — never parallelize `source add`:

```bash
NB="$NOTEBOOK_ID"
for url in "<new_url_1>" "<new_url_2>" ... ; do
  echo "=== adding: $url ==="
  notebooklm source add "$url" --notebook "$NB" --json 2>&1 | head -5 || echo "(continuing)"
done
notebooklm source list -n "$NB" --json
```

Collect the new `source_id`s from each response. Show the new source count to the user (e.g., `+3 sources added, total now 14`).

If MORE THAN HALF of the new URLs fail, stop the update pass and emit `✗ Most URLs failed to add — update skipped. Returning to menu.` Do not consume a pass-count.

#### 12b.3 — Wait for the NEW sources to index (subagent)

Scope the wait to only the new `source_id`s — don't re-wait on sources already indexed from the original run.

```
Task(
  description="Wait for NEW NotebookLM sources to index",
  prompt="Wait for these newly-added source_ids in notebook <NOTEBOOK_ID> to reach status=ready.
          For each id in [<new_ids>]: run `notebooklm source wait <id> -n <NOTEBOOK_ID> --timeout 600`.
          Report: list of ready ids and list of failed ids. Under 80 words.",
  subagent_type="general-purpose"
)
```

#### 12b.4 — Regenerate the briefing (update-framed)

```bash
notebooklm generate report \
  --format briefing-doc \
  --language fr \
  --append "$UPDATE_STEERING_PROMPT" \
  --notebook "$NOTEBOOK_ID" \
  --json
```

Update steering prompt (FR — differs from Phase 5: explicit continuity with the previous briefing, emphasis on what's new):

```
Rédige ce document entièrement en français. Il s'agit d'une MISE À JOUR d'une synthèse
précédente sur le même sujet — de nouvelles sources viennent d'être ajoutées au corpus.
Consignes :
1. Maintiens la même structure que la synthèse initiale (Introduction, Synthèse
   transversale, Sections thématiques, Débats, Recommandations, Conclusion).
2. Mets en avant EXPLICITEMENT ce qui change ou se précise grâce aux nouvelles sources :
   nouveaux faits, nuances, contradictions éventuelles avec la littérature antérieure.
3. Conserve les citations croisées aux sources numérotées NotebookLM.
4. Signale toute divergence franche entre une nouvelle source et l'analyse précédente
   dans la section « Débats » ou via une annotation explicite.
5. Style : rigoureux, dense, factuel.
```

Capture the `task_id`.

#### 12b.5 — Wait + download the updated briefing (subagent)

Same subagent pattern as Phase 6. Download to a timestamped temp path so it never collides with the original:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M)
# Subagent runs:
#   notebooklm artifact wait <task_id> -n "$NB" --timeout 1200
#   notebooklm download report "$TMP/research-<slug>-update-$TIMESTAMP-raw.md" -a <task_id> -n "$NB"
```

#### 12b.6 — Finalize to the vault with an update-suffixed filename

Merge the new URLs into the sources manifest, then run `finalize_note.py` with an update-suffixed slug so the output file is distinct from the original briefing:

```bash
# Append new URLs to the sources manifest
python - <<'EOF'
import json, pathlib
manifest_path = pathlib.Path("$TMP/research-<slug>-sources.json")
existing = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
new_entries = [
    {"url": "<new_url_1>", "title": "<title_or_url_1>"},
    # ...
]
manifest_path.write_text(json.dumps(existing + new_entries, indent=2, ensure_ascii=False), encoding="utf-8")
EOF

# Finalize with an update-suffixed slug:
python $SKILL_DIR/scripts/finalize_note.py \
  --input "$TMP/research-<slug>-update-$TIMESTAMP-raw.md" \
  --topic "<topic> — mise à jour $TIMESTAMP" \
  --slug "<slug>-update-$TIMESTAMP" \
  --notebook-id "$NOTEBOOK_ID" \
  --sources-json "$TMP/research-<slug>-sources.json" \
  --output-dir "$VAULT/.raw/Projets/" \
  --language fr
```

Expected output filename: `<date>-<slug>-update-<timestamp>.md`. Capture that path — it's the input to 12b.7.

#### 12b.7 — Re-ingest into the wiki (DELTA MODE — this is the sensitive step)

Invoke `claude-obsidian:wiki-ingest` with framing that makes delta behavior explicit. The goal is: **update existing entity/concept pages, do not duplicate, do not rename, preserve all existing `[[wikilinks]]`.**

```
Skill(skill="claude-obsidian:wiki-ingest",
      args="DELTA INGEST for topic '<topic>' — this is an UPDATE to an existing research thread, not a fresh ingest. Original briefing: <original_briefing_filename> (<original_date>). Update briefing: <update_briefing_filename> (today, <timestamp>).

      Read the update briefing at <update_briefing_full_path>.

      Delta rules — follow these strictly:
      1. UPDATE existing entity/concept pages in the wiki with any new claims, facts, or nuances from the update briefing. Merge new information into the existing page bodies — do NOT overwrite.
      2. APPEND the new source to the `sources:` frontmatter list of every existing page whose claims are corroborated or extended by the new sources.
      3. CREATE new entity or concept pages ONLY if the update briefing introduces genuinely new concepts not already in the wiki. When in doubt, prefer updating over creating.
      4. DO NOT rename any existing page. DO NOT change any existing filename. Preserve every `[[wikilink]]` as-is.
      5. APPEND a fresh log entry at the TOP of wiki/log.md describing this as an UPDATE pass, referencing both the original ingest's log entry (<original_date>) and this update. Format header: `## [<today>] update-ingest | <topic> — mise à jour depuis le <original_date>`. List pages updated vs pages created.
      6. Update `wiki/hot.md` with a one-line note that an update pass ran today on <topic>.
      7. Update `.raw/.manifest.json` with the update briefing's entry — include the original briefing filename under a new `parent` key so the delta chain is discoverable.

      New sources added to the NotebookLM notebook this pass: <list the new URLs here>.

      After ingest, REPORT BACK: (a) list of pages UPDATED, (b) list of pages CREATED, (c) any contradictions you noticed between old and new claims while merging — those are critical because Phase 12b.8 will lint for them.")
```

Capture:
- The list of pages updated (for Phase 12b.8 lint scope)
- The list of pages created (for the summary)
- Any contradiction hints the ingest skill surfaced

#### 12b.8 — Scoped contradiction lint (old-vs-new)

Critical — this is the whole point of doing lint *again* after an update. We want to know if the new sources disagree with what the original briefing claimed.

```
Skill(skill="claude-obsidian:wiki-lint",
      args="Contradiction check scoped to the '<topic>' update pass (<timestamp>). Compare new claims (from the update briefing) against existing claims (from the original briefing and its derived wiki pages).

      Pages to check (pipe-separated): <list from Phase 12b.7 pages_updated + pages_created>.

      On any conflict:
      - Add a `> [!contradiction] Mise à jour vs version initiale (<original_date>)` callout on the affected page.
      - Inside the callout, cite BOTH the original source (from the old briefing) and the new source (from the update).
      - On the update source summary page ([[<YYYY-MM-DD>-<slug>-update-<timestamp>]]), add a reciprocal callout pointing back.

      Do not silently reconcile. Flag and move on — the user decides.

      Report back: (a) pages where new contradictions were added, (b) `clean` if none.")
```

Capture the result for Phase 12b.9.

**Non-fatal.** If lint fails or the scope is empty, proceed to 12b.9 with a note that lint produced no output.

#### 12b.9 — Update-pass summary + registry update + menu re-display

**First, update `wiki/meta/notebooks.md`** — find the existing row for this `notebook_id` and update in place :
- `Dernière MAJ` → today's date
- `Sources` → new total
- `Contradictions ouvertes` → new count (from Phase 12b.8 lint)
- Append `(update pass <N>/3 on <today>)` to the topic cell OR replace a previous marker if present

Emit a compact summary, then re-display the Phase 12 menu for another round:

```
Update pass <N>/3 complete.

✔ <K> new source(s) added to notebook <NOTEBOOK_ID> (total sources now: <total>)
✔ Updated briefing (FR): <path to .raw/Projets/<date>-<slug>-update-<timestamp>.md>
✔ Wiki: <U> pages updated, <C> pages created — existing wikilinks preserved
✔ Lint: <"no new contradictions" OR "<K> new contradiction(s) on: page-a, page-b">

---

The notebook is still open. Pick another number (or 5 to finish):

  1. Quiz
  2. Flashcards
  3. Audio Overview
  4. Infographic
  5. None — I'm done for now.
  6. Add more links/sources (<remaining_update_passes> passes left)
```

Increment the update-pass counter. When the counter reaches 3, in the next re-display replace option 6 with: `  6. (update limit reached — start a new /research-pipeline thread for further expansion)` and disable the option — any numeric 6 reply now maps to "return to menu, please pick 1–5 or exit".

**Non-fatal.** If any step inside Phase 12b fails, emit a warning naming the failing step and fall back to the menu — the original artifacts from Phases 1–12 remain intact, and the user can try a different option. Do not kill the overall pipeline.

### Phase 13 — Primary deliverables report + registry update

**Step A — Update the notebooks registry.** Before emitting the summary to the user, append a new row (or update an existing one if this was a resume/update) to `wiki/meta/notebooks.md`. Use `Edit` on the `## Notebooks actifs` table :

```markdown
| <Topic from user prompt> | `<NOTEBOOK_ID>` | <YYYY-MM-DD> | <YYYY-MM-DD> | <N> | <contradictions count from Phase 9> | [[<main_entity_page_from_Phase_8>]] | [[<briefing_source_summary_page>]] |
```

Also add a line to the « Freshness tracking » table under the registry.

**Step B — Update `hot.md`.** Ensure the active notebooks table there includes this topic. Insertion logic : if `hot.md`'s notebooks table already has < 5 rows, prepend the new topic at the top; if it has ≥ 5, drop the oldest row to keep the table scannable.

**Step C — Emit the summary** (one short message to the user).

One short message summarizing everything produced by Phases 1–12. This is *not* the end of the pipeline — Phase 14 (gap-filling autoresearch) kicks off immediately after and may run another 10–30 min. Flag this so the user isn't confused when the agent keeps working after seeing the summary.

Format:

```
Primary pipeline complete. Summary:

✔ Briefing (FR): <path to .raw/Projets/YYYY-MM-DD-<slug>.md>
✔ Wiki pages: <N created, M updated> (via claude-obsidian:wiki-ingest)
✔ Lint: <"clean" OR "K contradiction(s) flagged on: page-a, page-b">
✔ Protocole d'Expérimentation: <path to …-protocole.md>
✔ Canvas map: <path to …-map.canvas>   (or ✗ if skipped)
✔ Bonus deliverable: <quiz / flashcards / audio / infographic / none> → <path or "n/a">

Notebook kept alive: <NOTEBOOK_ID>
To add another artifact later in French: notebooklm generate <type> --language fr --notebook <id>

▶ Next: launching claude-obsidian:autoresearch for a gap-filling sweep — will report back when it finishes.
```

If any phase was skipped or failed, mark it with `✗` and a one-line reason. Do not over-explain — the user can drill in if they want.

### Phase 14 — Autonomous gap-filling (claude-obsidian:autoresearch)

After Phase 13's summary is emitted, kick off an autonomous follow-up research loop to cover blind spots the curated NotebookLM corpus didn't reach. This runs unattended — no user gate — because by this point the user has already committed to the topic being depth-worthy.

**Seed selection.** Pick the autoresearch query based on what Phases 6–9 surfaced:

1. **Gap-driven seed (preferred).** Scan the briefing body and the wiki pages Phase 9 touched for:
   - `[!gap]` callouts ("la source est silencieuse sur X")
   - `[!contradiction]` callouts Phase 9 filed
   - Unanswered questions surfaced in the briefing's *Recommandations / Prochaines actions* section

   Compose a seed like:
   ```
   Follow-up research to close blind spots from the <topic> briefing already filed at <briefing_path>. Gaps to address:
   - <gap 1>
   - <gap 2>
   - <contradiction to resolve>
   Prioritize sources the NotebookLM notebook did NOT already cover (the original source list is in that briefing's frontmatter).
   ```

2. **Broadening seed (fallback).** If no explicit gaps surfaced, pass the original topic with a broadening framing:
   ```
   Complementary coverage of <topic> beyond the NotebookLM briefing at <briefing_path>. Prioritize angles not represented in that briefing's source list — recent criticism, counter-arguments, adjacent fields, case studies.
   ```

**Invocation:**

```
Skill(skill="claude-obsidian:autoresearch", args="<selected seed>")
```

The autoresearch skill handles its own loop (search → fetch → synthesize → file into `wiki/`). This skill's responsibility ends at kicking it off with a well-chosen seed; autoresearch records its own log entry for what it added.

**Why Phase 14 runs after Phase 13 rather than instead of it.** Phase 13 gives the user a clean, navigable summary of the primary artifacts *at the moment they land* — if autoresearch dies halfway through, the user already has everything important in hand. Phase 14 is pure bonus: its failure can't roll back the rest of the pipeline, and its success is additive.

**On completion (or failure)**, emit exactly one closing line:

- Success: `✔ Gap-fill auto-research complete — <N> new wiki pages added on follow-up angles: <page-a>, <page-b>, …`
- Failure: `✗ Gap-fill auto-research failed or was interrupted (<short reason>) — primary deliverables are intact; you can retry manually with /claude-obsidian:autoresearch <topic>`

That is the true end of the pipeline.

---

## Alternate-mode phases (Modes 3-6)

### Phase R — Resume mode (Mode 3)

Trigger: « resume research on [[X]] », « /research-pipeline resume [[X]] », « extend my X research », « continue research on X ».

1. **Resolve notebook_id** — read `wiki/meta/notebooks.md` and find the row whose topic matches X or whose « Page wiki principale » equals `[[X]]`. Fallback : open `wiki/entités/X.md` (or `wiki/cours/ia/X.md`, `wiki/concepts/X.md`) and read the `notebook_id` field in frontmatter.
2. **If no match** : emit `✗ No existing notebook found for "<X>". Did you mean "<closest_match>"? Or run /research-pipeline <X> to start a fresh thread.` and stop.
3. **Health-check the notebook** : `notebooklm list --json | jq '.[] | select(.id=="<notebook_id>")'` — if the notebook was deleted server-side, archive the registry row and emit `✗ Notebook <id> no longer exists on NotebookLM (may have been deleted). Archiving registry row. Run /research-pipeline <X> to start fresh.`
4. **Jump to Phase 12 menu** — same menu as the full pipeline, same 6 options, same 3-update-pass cap. No Phase 1-11, no briefing regeneration (user hasn't asked for it), just « pick a deliverable ».

### Phase A — Add-URL mode (Mode 4)

Trigger: « add this URL to my X research », « add these sources to [[X]] », « étends ma recherche X avec … », « expand X with <URLs> ».

1. **Resolve notebook_id** (same as Phase R, step 1). If no match → `✗` and stop.
2. **Extract URLs** from the user message — one per line, or comma-separated, or bullet-listed.
3. **Run Phase 12b.2 → 12b.9 directly** — same update loop as option 6 from the menu, but with no menu prompt before or after. Emit the 12b.9 summary and stop.
4. The 3-update-pass cap per session still applies. If the cap is already hit, emit `✗ Update pass cap reached for this session — start a new /research-pipeline <X> thread or resume manually tomorrow.`

### Phase 15 — Reconcile open contradictions (Mode 5)

Trigger: « reconcile contradictions », « /research-pipeline reconcile », « resolve open contradictions in wiki », « walk me through contradictions ».

Goal : walk the user through every open `[!contradiction]` callout in the wiki and offer a structured resolution.

#### 15.1 — Enumerate contradictions

```bash
grep -rn "> \[!contradiction\]" "$VAULT/wiki/" 2>/dev/null
```

For each hit, capture : file path, line number, the callout title, and the 2-5 lines of body that follow (the actual conflict description).

**Deduplicate reciprocal callouts** — a contradiction between page A and page B usually shows up twice (once on each page). Group these into a single conflict to present to the user.

If no contradictions remain, emit `✓ Wiki is clean — no open [!contradiction] callouts.` and stop.

#### 15.2 — Present + prompt per-conflict

For each conflict, emit :

```
Contradiction <N>/<total> : [[<page_a>]] vs [[<page_b>]]

  Sujet : <callout title>

  Version initiale ([[<page_a>]], source [[<original_source>]]) :
    "<excerpt from the callout>"

  Version alternative ([[<page_b>]], source [[<new_source>]]) :
    "<excerpt from the callout>"

Que veux-tu faire ?
  1. **Garder version initiale** — la nouvelle source est moins fiable ; retirer le callout et restaurer la version initiale sur les deux pages.
  2. **Garder version alternative** — la nouvelle source est plus récente/plus fiable ; mettre à jour la version initiale sur les deux pages, retirer le callout.
  3. **Les deux valent** — contextes différents ; remplacer le callout par un `> [!note]` expliquant en quel contexte chacune s'applique.
  4. **Besoin de plus de recherche** — laisser le callout ouvert pour l'instant, noter la décision attendue (ex : « à re-évaluer après l'expérience E3 »).
  5. **Skip** — passer à la suivante.
  6. **Stop** — arrêter la session de réconciliation.
```

Wait for the user's numeric reply. Parse naturally — « option 3 parce que les contextes diffèrent, ajoute que l'une s'applique au Pro et l'autre au Max » is option 3 with commentary to inject.

#### 15.3 — Apply the decision

Based on the user's choice :

- **Choice 1** (keep initial) → Edit both pages : remove the `> [!contradiction]` callout block entirely ; restore the original claim wording (already there, just the callout goes away).
- **Choice 2** (keep alternative) → Edit both pages : remove the callout, and update any paragraph where the contradicted claim appears to reflect the new source's version. Also update the `sources:` frontmatter to elevate the new source as primary if applicable.
- **Choice 3** (both valid) → Replace `> [!contradiction]` with `> [!note] Nuance contextuelle` on both pages, containing the user's reasoning as the body.
- **Choice 4** (defer) → Leave the callout. Append a line inside the callout : `> **Décision attendue :** <user's note> (flagué le <today>)`.
- **Choice 5** (skip) → do nothing, move to the next.
- **Choice 6** (stop) → exit the loop.

Log every resolved contradiction in `wiki/log.md` under a new entry :

```markdown
## [<today>] reconcile | Résolution de contradictions
- [[<page_a>]] ↔ [[<page_b>]] : <1-sentence summary of the decision>
- …
```

#### 15.4 — Final summary

After the loop (user picked 6 or all contradictions processed), emit :

```
Reconciliation session complete.

✔ <N> contradictions resolved :
    - <M> "garder initiale"
    - <K> "garder alternative"
    - <P> "les deux valent"
    - <Q> "différées pour plus de recherche"
✔ <S> skipped (still open)

Wiki log updated with today's reconciliation entry.
```

**Non-fatal.** If a specific edit fails (e.g. page moved, callout format changed), log `✗ Failed to edit [[<page>]] — <reason>` and continue with the next conflict.

### Phase 16 — Freshness check (Mode 6)

Trigger: « research freshness check », « which topics need refresh », « /research-pipeline freshness », « list stale research ».

Goal : scan the notebooks registry for topics > 6 months old and propose update passes.

#### 16.1 — Read the registry

Read `wiki/meta/notebooks.md`. Parse the `## Notebooks actifs` table. For each row, compute `age = today - updated_date`.

#### 16.2 — Bucket by age

- **Green (< 3 months)** — no action.
- **Yellow (3–6 months)** — note it, suggest « keep an eye on ».
- **Orange (6–12 months)** — strongly recommend an update pass.
- **Red (> 12 months)** — consider archiving or a full re-run.

#### 16.3 — Present + offer action

Emit one message per non-green topic :

```
Research freshness audit :

🟡 <N> topic(s) à surveiller (3-6 mois) :
  - <topic> (MAJ <date>, <age> mois) — [[<wiki_page>]]

🟠 <M> topic(s) à rafraîchir (6-12 mois) :
  - <topic> (MAJ <date>, <age> mois) — [[<wiki_page>]] → notebook `<notebook_id>`

🔴 <K> topic(s) périmés (> 12 mois) :
  - <topic> (MAJ <date>, <age> mois) — [[<wiki_page>]] → considère archiver ou relancer

Pour chaque topic orange/rouge, je peux :
  A. Lancer un update pass (Mode 4 — Add-URL) avec de nouvelles URL que tu me donnes
  B. Lancer une recherche gap-fill via claude-obsidian:autoresearch (trouve automatiquement de nouvelles angles)
  C. Archiver le topic (déplacer vers la section « Notebooks archivés » du registre)
  D. Rien (je note juste la revue dans le log)

Quelle(s) action(s) pour quel(s) topic(s) ? (ex : « A pour Claude Code, C pour Claude Design »)
```

Parse the response and dispatch :
- **A** → jump to Mode 4 (Add-URL) scoped to that notebook
- **B** → `Skill(skill="claude-obsidian:autoresearch", args="freshness-refresh seed for <topic>, looking for sources newer than <registry_updated_date>")`
- **C** → edit the registry : move the row from `## Notebooks actifs` to `## Notebooks archivés` with an archival date + reason
- **D** → log a freshness-review entry in `wiki/log.md`, no other action

**Non-fatal.** If the registry is empty or malformed, emit `✗ Registre des notebooks absent ou vide — démarre d'abord un pipeline via /research-pipeline <topic>.`

### Phase 17 — Podcast transcription hook (post-Phase-12 option 3)

Runs ONLY when the user picked option 3 (Audio Overview) in the Phase 12 menu AND the download succeeded.

After the MP3 lands at `.raw/Projets/audio/<slug>.mp3`, propose verbatim :

> J'ai téléchargé le podcast (<duration> min). Veux-tu que je :
>   1. Le transcrise en français et archive le texte comme source wiki (utile pour la recherche texte future)
>   2. Passe directement au rapport final

If the user picks 1 :
- Launch a transcription subagent with a `general-purpose` type :
  ```
  Task(
    description="Transcribe podcast to French wiki source",
    prompt="Transcribe the audio file at '<mp3_path>' to French text. If the system has whisper.cpp, ffmpeg+OpenAI API, or another transcription tool available, use it. Otherwise report that no transcription tool is available. On success : save the transcript to '.raw/Projets/audio/<slug>-transcript.md' with a YAML frontmatter header (`type: source, source_type: podcast-transcript, parent_audio: <mp3_filename>, language: fr`), then invoke Skill(skill='claude-obsidian:wiki-ingest', args='<transcript_path>') with a hint that this is a DELTA INGEST to the same topic (matching notebook_id <id>) — update existing pages, do not duplicate. Report back : final transcript path + list of pages updated. Under 150 words.",
    subagent_type="general-purpose"
  )
  ```
- If the subagent reports no transcription tool is available, fallback : emit `✗ Pas d'outil de transcription disponible sur cette machine. Le MP3 est conservé à <path> — tu peux le transcrire manuellement avec whisper.cpp ou le service Google et ré-ingérer avec /claude-obsidian:wiki-ingest.`

**Non-fatal.** Phase 17 is a bonus — its failure never affects Phase 13 or Phase 14.

---

## Frontmatter contract (what `finalize_note.py` emits)

Matches the vault convention declared in `CLAUDE.md`:

```yaml
---
type: source
status: raw
created: YYYY-MM-DD
updated: YYYY-MM-DD
topic: "<original topic>"
notebook_id: <uuid>
language: fr
tags: [research-pipeline, notebooklm, lang/fr]
sources:
  - title: "..."
    url: https://...
  - title: "..."
    url: https://...
---
```

This keeps the file discoverable by the vault's ingest/lint skills and makes the source list reusable without re-opening the notebook.

## Error handling

Overall design: **non-fatal-forward**. Each phase after the briefing download (Phase 6) can fail independently and the pipeline continues. The user always gets *something* filed.

- **Auth failure** (AUTH_REQUIRED on `notebooklm create` or any later CLI call) → stop the pipeline, tell the user to refresh login in their own terminal (`notebooklm login`), don't retry silently. We don't pre-flight auth — this is our fallback when the cached session has in fact rolled.
- **A single source add fails** → log, continue. Record it in the Phase 13 report. Watch for the 30-second RPC timeout pattern: even when the CLI reports an error, the source is often already on the NotebookLM side. Re-check with `notebooklm source list --json` before treating it as lost.
- **Report generation rate-limited** → `--retry 2` is already passed on the `generate report` call. If it fails twice, surface `notebooklm artifact list` and ask the user whether to retry later or abandon.
- **Subagent timeout on long wait** → the subagent itself falls back to `artifact list`; main conversation reads that and decides whether to re-spawn.
- **finalize_note.py fails** → inspect the raw downloaded markdown at `$TMP/research-<slug>-raw.md` — it's still there, not lost.
- **wiki-ingest fails** (Phase 8) → non-fatal. The briefing is already filed in `.raw/Projets/`. Continue to Phase 9; flag in Phase 13.
- **wiki-lint fails or returns unclear results** (Phase 9) → non-fatal. Proceed to Phase 10; note it in the final report.
- **Protocol generation fails** (Phase 10) → non-fatal. Briefing + wiki ingest already landed. Skip with a warning.
- **Mind-map / canvas fails** (Phase 11) → non-fatal. Preserve the mind-map JSON path in `$TMP/research-<slug>-mindmap.json` so the user can retry canvas creation manually.
- **Deliverable generation fails** (Phase 12, choices 1–4) → surface the error, suggest retry after 5–10 min, but do NOT loop or block Phase 13. Rate-limits on audio/infographic/quiz/flashcards are common per the notebooklm docs.
- **Autoresearch fails** (Phase 14) → non-fatal by definition. Primary deliverables are already in the user's hand from Phase 13. Emit the closing failure line and stop; suggest the user retry manually with `/claude-obsidian:autoresearch <topic>` if they want.

## What not to do

- Do not translate source URLs or the user's topic — they go in as given.
- Do not set the global language (`notebooklm language set fr`) — always use the per-command `--language fr` flag, so other skills' work isn't affected.
- Do not delete the notebook after the run. The user may want to come back for a podcast, quiz, or follow-up Q&A.
- Do not try to use `yt-dlp` to download videos. NotebookLM ingests YouTube URLs directly via `source add` — that's both simpler and what the Google-side models are tuned for.
- Do not skip the approval gate after Phase 1. The quality of the brief hinges on source quality; 10 seconds of user review is cheaper than a 20-minute bad report.

## Slug and path conventions

- Slug: lowercase, strip non-ASCII + punctuation → hyphenated, max 60 chars.
- Final filename: `<YYYY-MM-DD>-<slug>.md`.
- Default folder: `.raw/Projets/` (matches the "project inputs" role defined in the vault CLAUDE.md).
- If the user passes a folder override like `/research-pipeline [Cours/ai] <topic>`, route to `.raw/Cours/ai/`.

## Files in this skill

- `SKILL.md` — this file (14-phase orchestration + Phase 0 vault state check + Phase 12b update loop + Phases R/A/15/16/17 for alternate modes + HELP MODE cheat sheet + 6 operational modes)
- `scripts/finalize_note.py` — briefing frontmatter + filing (Phase 7 AND Phase 12b.6, reused with an update-suffixed slug for update briefings)
- `scripts/finalize_protocol.py` — protocol frontmatter + filing (Phase 10)
- `evals/evals.json` — integration test prompts
- `evals/trigger-eval.json` — 26-query triggering benchmark (for description tuning)

## Companion file in the vault

- `wiki/meta/notebooks.md` — central registry of active NotebookLM notebooks (topic, id, sources count, contradictions, wiki pages, freshness tracking, Dataview queries). READ by Phase 0 (overlap detection) + Phase R/A (notebook_id resolution) + Phase 16 (freshness audit). WRITTEN by Phase 13 (new topic), Phase 12b.9 (update pass), Phase 16.3 C (archival).

## Revision log (for future readers of this file)

- Initial version — 14 phases (1…14).
- 2026-04-21 — added **HELP MODE** (cheat sheet on triggers like "help research", "how does this work", "list commands") and **Phase 12b** (update loop: menu option 6 adds new URLs to the existing notebook, regenerates the briefing, re-ingests into the wiki in delta mode, lints for old-vs-new contradictions, re-displays the menu). Max 3 update passes per session.
- 2026-04-21 (evening) — **bridge upgrade** making the skill stateful across sessions. Added (a) the `wiki/meta/notebooks.md` registry as single source of truth for all living NotebookLM notebooks ; (b) **Phase 0** — vault state check that detects topic overlap with existing research and offers to extend/resume instead of creating silos ; (c) **Phase 1 vault-aware** — scans existing wiki sources before WebSearch, surfaces them in the approval gate ; (d) **Mode 3 (Resume)** — re-enter the Phase 12 menu on an existing notebook via « resume research on [[X]] » ; (e) **Mode 4 (Add-URL)** — natural-language « add this URL to my X research » jumps directly to Phase 12b without menu ceremony ; (f) **Phase 15 (Reconcile)** — walk through open `[!contradiction]` callouts with a structured resolution workflow (keep-initial / keep-alternative / both-valid / defer / skip) ; (g) **Phase 16 (Freshness)** — audit topics > 6 months old and propose update/autoresearch/archive ; (h) **Phase 17** — post-audio transcription hook that turns the podcast into a wiki-searchable source. Registry update steps added to Phases 13 and 12b.9.
