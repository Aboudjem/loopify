<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="loopify : une boucle que vous n'avez pas à surveiller. Confiez à Claude une tâche qui se répète, revenez à un journal de ce que chaque tick a fait." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <a href="https://github.com/Aboudjem/loopify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/loopify?color=2BE8C8&labelColor=0A0F1C" alt="stars"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <a href="ja.md">日本語</a> · <a href="es.md">Español</a> · <b>Français</b>
</p>

<p align="center">
  <strong>Confiez à Claude une tâche qui se répète. Revenez à un journal de ce que chaque tick a fait, pas à une boucle qu'il faut surveiller.</strong>
</p>

<p align="center">
  <a href="#ce-que-ça-fait">Ce que ça fait</a> · <a href="#installation">Installation</a> · <a href="#utilisation">Utilisation</a> · <a href="#dans-votre-éditeur">Dans votre éditeur</a> · <a href="#bon-à-savoir">Bon à savoir</a> · <a href="#pour-aller-plus-loin">Pour aller plus loin</a>
</p>

<p align="center"><sub>Cette traduction peut avoir du retard sur l'original en anglais.<!-- may-lag --></sub></p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

## Ce que ça fait

Certaines tâches ne se terminent jamais vraiment. Une pull request de release demande à être
surveillée tout l'après-midi ; de nouveaux rapports de bugs s'accumulent pendant la nuit et méritent
un premier coup d'œil avant que quiconque ne les lise. Claude Code dispose déjà d'une commande pour
répéter une tâche, `/loop` : vous lui donnez un prompt et un intervalle, et elle relance ce prompt
encore et encore tant que votre session reste ouverte. Ce qu'elle ne vous donne pas, c'est le prompt.

loopify écrit ce prompt. Vous décrivez la tâche une fois, en mots simples. loopify lit votre projet
pendant que Claude a encore votre contexte, vous pose les rares décisions qui comptent (à quelle
fréquence, quand s'arrêter, ce qu'elle peut toucher), et écrit deux choses.

- **Le brief, un fichier.** Un tour de la tâche : quoi lire, ce qu'il peut modifier, ce qu'il ne doit
  jamais faire, quand s'arrêter, et où noter ce qui s'est passé. La boucle l'ouvre à neuf au début de
  chaque exécution, donc rien ne se perd d'une exécution à l'autre, et vous pouvez le modifier
  pendant que la boucle tourne.
- **La ligne, une seule chaîne.** Vous la collez dans `/loop`. Le chemin du brief est dedans, donc
  chaque exécution sait où regarder. La règle d'arrêt aussi, donc la boucle se termine à vos
  conditions.

Chaque exécution est un **tick**. À chaque tick, Claude relit le brief, fait un tour de la tâche, et
écrit ce qui s'est passé dans un journal appelé `TICKS.md`. Vous n'avez pas à veiller ; vous devez
lire le journal.

Si vous avez déjà utilisé [goalify](https://github.com/Aboudjem/goalify), ceci vous sera familier.
goalify est fait pour une tâche qui se termine : une grande tâche, une seule définition de « fait »,
`/goal`. loopify est fait pour une tâche qui se répète.

## Installation

Les deux commandes en haut ajoutent le marketplace 10x et installent le plugin dans Claude Code,
contre lequel loopify a été vérifié en version 2.1.252. Tout autre agent installe le même dossier de
skill en une ligne, via le [CLI skills](https://github.com/vercel-labs/skills) :

```bash
npx skills add Aboudjem/loopify
```

## Utilisation

### 1. Décrivez la tâche

Tapez `/loopify` dans le chat de Claude Code et dites ce qui doit se répéter. loopify lit le README,
les commits récents et les pull requests ouvertes, puis pose une seule courte série de questions.

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` remplace votre projet ; loopify affiche vos vrais chemins.

### 2. Collez la ligne

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude fait un tour tout de suite, puis toutes les 20 minutes, dans cette session, jusqu'à ce que la
pull request soit fusionnée ou que 30 ticks soient passés, selon ce qui arrive en premier. Retirez
l'intervalle et Claude choisit lui-même le rythme. Les deux erreurs les plus fréquentes :

```text loop-antipattern
# pas ceci : « every morning » peut pousser /loop à proposer une planification cloud, et rien ne dit quand s'arrêter
/loop every morning keep the release PR healthy

# ni le chemin seul : le tick reçoit un nom de fichier et aucune instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. Lisez le journal

`TICKS.md` contient une entrée par tick, avec ce qui a changé et la preuve correspondante, et un
compteur en haut :

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

Tout ce que la boucle n'a pas pu faire sans risque vous attend dans `QUEUE.md`.

## Ce que vous obtenez

- **Un brief qui reste en place.** Relu à chaque tick, jamais archivé, jamais réécrit par la boucle.
  La fréquence, le moment de l'arrêt et ce qu'elle peut toucher sont réglés avant le premier tick.
- **Une règle d'arrêt et un plafond de ticks dans la ligne.** Une boucle qui finit sa tâche s'arrête,
  et une boucle qui atteint son plafond aussi.
- **Des garde-fous pour une exécution sans surveillance.** Pas de comptes, pas de paiements, aucun
  push ni publication sauf si vous le dites. Tout ce que la boucle lit, par exemple un commentaire de
  pull request, est une donnée, jamais une instruction.
- **Une clause « sûr en cas de répétition » dans chaque brief.** Le brief nomme le marqueur qu'un
  tick cherche avant d'agir, pour qu'un tick relancé puisse voir que le travail a déjà eu lieu.
- **Un journal qui a une forme.** Chaque entrée de `TICKS.md` commence par le même en-tête,
  `## tick <n> · <ISO timestamp> · changed | noop | stopped`, vérifiable avec
  `skills/loopify/scripts/ticks_lint.py`. Les éléments bloqués dans `QUEUE.md` portent une ligne
  `reason:` et une ligne `unblock:`.
- **Une boucle qui apprend.** `LESSONS.md` garde ce qui a marché et ce qui a fait perdre du temps, et
  la boucle le relit à chaque tick.

## Dans votre éditeur

Fonctionne dans Claude Code, Cursor, Codex, Copilot, Gemini CLI, et plus de 70 autres agents via
`npx skills add`.

| Où | Comment |
| --- | --- |
| Claude Code | `claude plugin install loopify@10x` |
| Cursor, Codex, Gemini CLI, OpenCode, Windsurf, Zed, Kimi Code CLI | `npx skills add Aboudjem/loopify -a <agent>` |
| VS Code et GitHub Copilot | `npx skills add Aboudjem/loopify -a github-copilot` |
| Tout le reste | copiez `skills/loopify/` dans le dossier de skills de votre agent |

loopify est un seul dossier de skill avec deux scripts Python de la bibliothèque standard à côté,
donc il n'y a aucun serveur à lancer ni rien à compiler. Le code `-a`, les deux chemins
d'installation par agent et la méthode de copie manuelle sont dans
[docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md).

Le brief voyage ; la ligne non. La ligne est une ligne `/loop` propre à Claude Code, et l'étape de
planification du brief nomme des outils Claude Code. Le brief prévoit ce cas : faire un tour,
l'enregistrer, sortir, et laisser un planificateur extérieur déclencher le tick suivant.
[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) couvre
Kimi, Copilot CLI, Cursor, Qwen Code, Hermes, Goose et le cron classique.

## Bon à savoir

> [!IMPORTANT]
> Une boucle qui tourne ne prouve pas qu'elle fait la bonne chose. Lisez le journal de ticks. Aucun
> évaluateur ne se cache derrière `/loop` : la checklist par tick du brief et `TICKS.md` sont les
> seules preuves qui existent.

- **La boucle vit dans la session où vous la collez.** Elle ne se déclenche que tant que cette
  session est ouverte. Fermez le terminal et elle s'arrête ; `/clear` efface aussi la planification.
  Lancer Claude Code en arrière-plan la garde en vie sans fenêtre.
- **Toute boucle s'arrête à 7 jours**, et une session ne contient au plus que 50 tâches planifiées.
  Ce sont deux limites de Claude Code sur le travail planifié, pas de loopify. Recollez la ligne pour
  continuer.
- **Pré-autorisez ce qu'un tick exécute.** loopify affiche les commandes dont la boucle a besoin,
  comme `gh pr view` ou `git commit`. Un tick qui tombe sur une demande d'autorisation y attend une
  réponse.

## Pour aller plus loin

- [Guide de démarrage](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md), votre
  première boucle pas à pas, et sans terminal ouvert
- [Installer dans votre éditeur](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md), le
  code agent et les deux chemins du CLI skills
- [Un exemple complet](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md),
  un brief entier avec la ligne à la fin
- [Limites honnêtes](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md), ce que loopify ne
  promet pas, tracé jusqu'au binaire ou à la documentation
- [Autres agents](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md), le même brief
  sous Kimi, Cursor, Goose et le cron classique
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [Le pointeur `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Changelog](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [Contribuer](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [Le skill lui-même](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>Créé par <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. Le comportement de `/loop` a été
redérivé à partir du binaire Claude Code 2.1.252 diffusé et de la documentation officielle, 2026. Frère de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, qui fait la même chose pour `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">Une lacune repérée ?</a></sub>
