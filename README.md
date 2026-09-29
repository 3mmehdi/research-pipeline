# research-pipeline

**Une skill Claude Code de 14 phases qui transforme un sujet en dossier classé.** Recherche web,
constitution d'un carnet NotebookLM persistant, briefing en français avec citations, ingestion
dans un coffre Obsidian, détection des contradictions, protocole d'expérimentation, carte visuelle,
puis un menu de livrables à la demande — quiz, cartes mémoire, résumé audio, infographie.

> *A 14-phase Claude Code skill that turns a topic into a filed, cited dossier: web research →
> persistent NotebookLM notebook → French briefing → Obsidian ingest → contradiction lint →
> experiment protocol → canvas map → on-demand deliverables. Written in English, produces French.*

---

## Ce qu'elle produit, à chaque passage

1. Un briefing en français, sourcé, déposé dans le coffre
2. L'ingestion dans le wiki, avec entités, concepts, index et journal mis à jour
3. Une passe de détection des **contradictions** avec ce que le coffre contenait déjà
4. Un protocole d'expérimentation : hypothèse, cases à cocher, critère de réfutation
5. Une carte visuelle des concepts
6. Un menu interactif : quiz, cartes mémoire, résumé audio, infographie
7. Un carnet NotebookLM **gardé vivant**, réutilisable pour tout artefact ultérieur
8. Une passe autonome de comblement des angles morts

**Chaque phase est non fatale pour les suivantes.** Si la carte échoue, le briefing et le protocole
arrivent quand même. C'est une orchestration longue et non surveillée : la tolérance aux pannes
partielles est un choix de conception, pas un accident.

## Six modes d'entrée

| Mode | Déclencheur | Ce qu'il fait |
|---|---|---|
| Pipeline complet | `/research-pipeline <sujet>` | Les 14 phases |
| Aide | `help research` | Aide-mémoire, aucune exécution |
| Reprise | `resume research on [[X]]` | Rouvre le menu d'un sujet existant |
| Ajout d'URL | `add this URL to my X research` | Étend un carnet sans passer par le menu |
| Réconciliation | `reconcile contradictions` | Résout les contradictions repérées |
| Fraîcheur | `research freshness check` | Signale les sujets de plus de 6 mois |

## Deux garde-fous qui comptent plus que les phases

**La phase 0 refuse de créer un silo.** Avant tout travail, elle mesure le recouvrement avec les
sujets déjà présents dans le coffre. Au-delà de **60 %**, elle propose d'étendre le carnet existant
au lieu d'en ouvrir un nouveau. Sans ça, un second cerveau accumule des pages parallèles sur le
même sujet et devient inutilisable.

**La phase 1 regarde d'abord à l'intérieur.** Elle parcourt les sources déjà ingérées et les
présente à côté des résultats du web, avant la porte de validation. Chercher dehors ce qu'on a
déjà dedans est l'erreur la plus coûteuse d'un outil de recherche.

## `EVALUATION.md` — la description a été mesurée, pas devinée

Une skill ne sert à rien si elle ne se déclenche pas. J'ai donc fait un **A/B sur la description**
elle-même : 26 requêtes (14 devant déclencher, 12 ne devant pas), 2 passages chacune, **52 appels
par version**.

| Mesure | v1 | v2 |
|---|---|---|
| Positifs déclenchés | 0/14 | 1/14 |
| Négatifs correctement ignorés | 12/12 | 12/12 |
| Faux positifs | 0 | 0 |

⚠️ **Et la conclusion honnête est dans le fichier** : la simulation utilisée par le banc d'essai est
systématiquement plus sévère que l'usage réel — elle rate même des appels littéraux qui, eux,
déclenchent en session. **Les valeurs absolues ne sont pas exploitables, seul le sens de l'écart
l'est.** Un banc d'essai dont on ne connaît pas le biais produit des chiffres pires qu'aucun
chiffre, parce qu'on les croit.

## Contenu du dépôt

| Fichier | Quoi |
|---|---|
| `SKILL.md` | La skill entière — 14 phases, 6 modes, les portes de validation |
| `scripts/finalize_note.py` | Dépose le briefing dans l'arbre des sources brutes |
| `scripts/finalize_protocol.py` | Écrit le protocole d'expérimentation |
| `evals/` | Les jeux d'évaluation de déclenchement |
| `EVALUATION.md` | Le compte rendu de l'A/B, avec ses limites |

## Dépendances et portée

Claude Code, un coffre Obsidian, la CLI `notebooklm-py`, et les skills compagnes
`claude-obsidian:*` pour l'ingestion et la détection de contradictions.

**Les chemins ont été remplacés par `$VAULT`, `$SKILL_DIR` et `$TMP`** au moment de la publication :
la version qui tourne chez moi les a en dur. Ce dépôt se lit comme un cas réel, pas comme un paquet
prêt à installer.

## Licence

MIT. Voir [LICENSE](LICENSE).
