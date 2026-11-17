<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="loopify : une boucle que vous n'avez pas à surveiller. Confiez à Claude une tâche qui se répète, revenez à un journal de ce que chaque tick a fait." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <b>Français</b>
</p>

<p align="center">
  <strong>Confiez à Claude une tâche qui se répète. Revenez à un journal de ce que chaque tick a fait, pas à une boucle qu'il faut surveiller.</strong>
</p>

<p align="center">
  <a href="#installation">Installation</a> · <a href="#comment-ça-marche">Comment ça marche</a> · <a href="#ce-que-vous-obtenez">Ce que vous obtenez</a> · <a href="#compatibilité">Compatibilité</a> · <a href="#preuves">Preuves</a> · <a href="#faq">FAQ</a> · <a href="#limites">Limites</a>
</p>

<p align="center"><sub>Cette traduction peut avoir du retard sur l'original en anglais.<!-- may-lag --></sub></p>

loopify écrit le prompt du `/loop` de Claude Code. Vous décrivez une tâche qui se répète. Vous
obtenez un brief que la boucle relit à chaque tick, et un journal de ce que chaque tick a fait.

```text
STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued
Do next:
1. QUEUE.md, tick 4: Post the drafted reply on the `fetchAll` rename thread of PR #412
```

Ce sont les premières lignes de `loop_status.py` sur l'exemple fourni. Le rapport complet est plus
bas, dans [Ce que vous obtenez](#ce-que-vous-obtenez).

## Installation

Dans Claude Code, lancez ces deux commandes :

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

Tout autre agent installe le même skill en une ligne, avec la
[CLI skills](https://github.com/vercel-labs/skills) :

```bash
npx skills add Aboudjem/loopify
```

Rien à compiler. Le skill est un dossier avec trois scripts Python, bibliothèque standard seulement.

## Comment ça marche

Certaines tâches ne finissent jamais. Une pull request de release se surveille tout l'après-midi.
Les nouveaux bugs s'empilent la nuit. Claude Code a déjà `/loop` : il relance un prompt tant que
votre session est ouverte. Il n'écrit pas le prompt à votre place.

loopify l'écrit. Il lit votre projet, pose les quelques décisions qui comptent, et écrit deux choses.

- **Le brief, un fichier.** Un tour de la tâche : quoi lire, quoi modifier, quoi ne jamais faire,
  quand s'arrêter. La boucle le rouvre à chaque tour, vous pouvez donc le modifier en cours de route.
- **La ligne, une seule chaîne.** Vous la collez dans `/loop`. Elle porte le chemin du brief et la
  règle d'arrêt.

Chaque tour est un **tick**. À chaque tick, Claude relit le brief, fait un tour, et note ce qui
s'est passé dans `TICKS.md`.

### 1. Décrivez la tâche

Tapez `/loopify` dans Claude Code et dites ce qui doit se répéter. loopify lit le README, les
derniers commits et les pull requests ouvertes. Puis il pose une courte série de questions.

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` remplace votre projet. loopify affiche vos vrais chemins.

### 2. Collez la ligne

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude fait un tour tout de suite, puis toutes les 20 minutes dans cette session. Il s'arrête quand
la PR est fusionnée ou après 30 ticks, au premier des deux. Les deux erreurs les plus fréquentes :

```text loop-antipattern
# not this: "every morning" can make /loop offer a cloud schedule instead, and nothing says when to stop
/loop every morning keep the release PR healthy

# and not the path alone: the tick gets a filename and no instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. Lisez le journal, ou demandez l'état

`TICKS.md` contient une entrée par tick, avec un compteur en haut :

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

Ce que la boucle n'a pas pu faire sans risque vous attend dans `QUEUE.md`. Une commande lit les trois
fichiers et vous dit quoi faire ensuite. Voir la section suivante.

## Ce que vous obtenez

Voici la vraie sortie du rapport d'état sur le dossier d'exemple de ce dépôt :

```bash
python3 skills/loopify/scripts/loop_status.py examples/loop-state/pr-babysitter --now 2026-09-01T09:50
```

```text
STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued
Do next:
1. QUEUE.md, tick 4: Post the drafted reply on the `fetchAll` rename thread of PR #412
   unblock: post the reply below on the thread, then delete this item
2. QUEUE.md, tick 5: `e2e` fails in checkout.spec.ts line 88: expected total 42.00, received 41.99
   unblock: fix the rounding in src/cart/total.ts or mark the PR as blocked
3. Read tick 7 in examples/loop-state/pr-babysitter/TICKS.md and check its evidence.
Detail:
  ticks logged  7 (4 changed, 3 noop, 0 stopped)
  queue         2 open item(s)
  lessons       5 line(s)
  lock          none
  interval      20m (from the saved line)
  log format    passes ticks_lint
  state dir     examples/loop-state/pr-babysitter
```

`--now` fixe l'horloge pour que l'exemple s'affiche toujours pareil. Ne le mettez pas sur une vraie boucle.

La ligne 1 est toujours le verdict : `OK`, `NEEDS YOU`, `STALE`, `STOPPED`, `NOT STARTED` ou
`BROKEN LOG`. Puis trois actions au plus. Puis le détail.

Chaque brief écrit par loopify vous donne aussi :

- **Une règle d'arrêt et un plafond de ticks dans la ligne.** Une boucle qui a fini s'arrête. Celle
  qui atteint son plafond aussi.
- **Des garde-fous pour tourner seule.** Pas de comptes, pas de paiements, pas de push ni de
  publication sans votre accord. Ce que la boucle lit, comme un commentaire de PR, est une donnée,
  jamais une instruction.
- **Une clause de répétition sûre.** Le brief nomme le marqueur qu'un tick cherche avant d'agir.
  Un tick lancé deux fois voit que le travail est déjà fait.
- **Un journal au format fixe.** Chaque entrée commence par `## tick <n> · <ISO timestamp> · changed |
noop | stopped`. `ticks_lint.py` le vérifie.
- **Une boucle qui apprend.** `LESSONS.md` garde ce qui a marché et ce qui a fait perdre du temps.

## Compatibilité

Chaque ligne ci-dessous est une installation que j'ai faite le 2026-11-17, dans un dossier vide.

| Agent                    | Commande d'installation                                               | Testé                                        |
| ------------------------ | --------------------------------------------------------------------- | -------------------------------------------- |
| Claude Code 2.1.326      | `claude plugin install` depuis la marketplace du dépôt, config vierge | 2026-11-17, plugin actif, scripts présents   |
| Claude Code (CLI skills) | `npx skills add Aboudjem/loopify -a claude-code`                      | 2026-11-17, skill lié dans `.claude/skills/` |
| Cursor                   | `npx skills add Aboudjem/loopify -a cursor`                           | 2026-11-17, skill dans `.agents/skills/`     |
| Codex                    | `npx skills add Aboudjem/loopify -a codex`                            | 2026-11-17, skill dans `.agents/skills/`     |
| GitHub Copilot           | `npx skills add Aboudjem/loopify -a github-copilot`                   | 2026-11-17, skill dans `.agents/skills/`     |
| Gemini CLI               | `npx skills add Aboudjem/loopify -a gemini-cli`                       | 2026-11-17, skill dans `.agents/skills/`     |

« Testé » veut dire : les fichiers sont arrivés et les trois scripts tournent depuis la copie
installée. Cela ne veut pas dire qu'une boucle a tourné dans cet agent.

Documentés, non testés : OpenCode, Windsurf, Zed, Kimi Code CLI et la copie à la main de
`skills/loopify/`. Voir [docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md).

Le brief voyage, la ligne non. La ligne est une ligne `/loop` de Claude Code. Ailleurs, le brief
fait un tour, le note et sort, et un planificateur externe lance le tick suivant.
[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) couvre
Kimi, Copilot CLI, Cursor, Goose et cron.

## Preuves

`make test` affiche chaque nombre ci-dessous. La CI le lance à chaque push et pull request.

```bash
make test
```

| Suite                       | Ce qu'elle vérifie                                                             | Résultat |
| --------------------------- | ------------------------------------------------------------------------------ | -------- |
| `evals/check_skill.py`      | Le contrat du skill, en assertions                                             | 160/160  |
| `tests/test_manifests.py`   | Manifestes, versions, brief d'exemple, traductions, SVG, secrets, tirets longs | 170/170  |
| `tests/test_ticks_lint.py`  | Le format du journal des ticks                                                 | 13/13    |
| `tests/test_loop_status.py` | Chaque verdict, et l'exemple du README à l'octet près                          | 51/51    |
| `evals/loop_line_lint.py`   | La ligne canonique passe les huit règles                                       | PASS     |

La CI lance aussi `claude plugin validate . --strict` sur un Claude Code épinglé, et vérifie que
`npx skills@1.9.0 add . --list` trouve le skill.

Les faits sur `/loop` viennent du binaire Claude Code 2.1.252 et de la documentation. La trace est
dans [docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md).

## FAQ

**Est-ce que loopify lance la boucle pour moi ?**
Non. Il écrit le brief, affiche la ligne, et s'arrête. Vous collez la ligne quand vous voulez
démarrer.

**Pourquoi un fichier et une chaîne, pas un seul prompt ?**
Le tick a besoin de détails : chemins, commandes, quoi faire en cas de blocage. `/loop` a besoin d'un
prompt court renvoyé à chaque tick. Le brief porte le détail, la ligne porte son chemin.

**Comment savoir si la boucle tourne encore ?**
Lancez `loop_status.py` sur le dossier d'état. Il dit `STALE` quand aucun tick n'est arrivé depuis
deux intervalles. Vous pouvez aussi demander à Claude « what scheduled tasks do I have? ».

**Qu'est-ce qui arrête une boucle ?**
La règle d'arrêt du brief, le plafond de ticks, l'expiration à sept jours, ou vous. La liste
complète est dans [docs/faq.md](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md).

**Est-ce que mon code part quelque part ?**
Non. loopify et ses scripts ne font aucun appel réseau. Un tick fait ce que votre brief autorise.

## Limites

> [!IMPORTANT]
> Une boucle qui tourne ne prouve pas qu'elle fait la bonne chose. Aucun évaluateur n'est derrière
> `/loop`. Le journal et le rapport d'état sont les seules preuves.

- **La boucle vit dans la session où vous la collez.** Fermez le terminal et elle s'arrête. `/clear`
  efface aussi le planning.
- **Chaque boucle s'arrête à 7 jours.** Une session tient au plus 50 tâches planifiées. Ce sont des
  limites de Claude Code. Recollez la ligne pour continuer.
- **Pré-approuvez ce qu'un tick lance.** Un tick bloqué sur une demande de permission attend une
  réponse. loopify affiche les commandes à autoriser, comme `gh pr view` ou `git commit`.
- **Le rapport d'état a besoin de l'intervalle** pour distinguer une boucle vivante d'une boucle
  morte. Il le lit dans la ligne enregistrée, ou dans `--interval`.

La liste complète, sourcée : [docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md).

## Pour aller plus loin

- [Démarrage rapide](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) : votre première boucle, pas à pas
- [Installer dans votre éditeur](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md) : le code agent et les deux chemins
- [Un exemple complet](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md) : un brief entier, la ligne en bas
- [Autres agents](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) : le même brief sous Kimi, Cursor, Goose et cron
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [Le pointeur `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Changelog](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [Contribuer](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [Le skill lui-même](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

Si vous connaissez [goalify](https://github.com/Aboudjem/goalify), vous serez en terrain connu.
goalify sert à une tâche qui finit. loopify sert à une tâche qui se répète.

---

<sub>Créé par <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. Le comportement de `/loop` est
redérivé du binaire Claude Code 2.1.252 et de la documentation officielle. Frère de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, qui fait la même chose pour `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">Une lacune repérée ?</a></sub>

<sub>Traduction assistée par machine, puis relue. La version de référence est le <a href="../README.md">README.md</a> en anglais.</sub>
