<p align="center">
  <a href="../README.md">English</a> ·
  <a href="zh-CN.md">简体中文</a> ·
  <a href="ja.md">日本語</a> ·
  <a href="es.md">Español</a> ·
  <b>Français</b>
</p>

<p align="center"><sub>Cette traduction peut avoir du retard sur l'original en anglais.<!-- may-lag --></sub></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero.svg" alt="Quatre étapes : décrivez une tâche qui se répète, obtenez un brief (un fichier) et une ligne (une chaîne unique), collez la ligne dans /loop, revenez à un journal de tick." width="100%">
</p>

<h1 align="center">loopify</h1>

<p align="center">
  <strong>Confiez à Claude une tâche qui se répète. Revenez à un journal de ce que chaque tick a fait — pas une boucle qu'il faut surveiller.</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://skills.sh/Aboudjem/loopify"><img src="https://skills.sh/b/Aboudjem/loopify" alt="skills.sh"></a>
</p>

loopify est un skill Claude Code pour les tâches qui ne se terminent jamais tout à fait : maintenir en
bonne santé une pull request de release pendant que les revues arrivent au compte-gouttes, surveiller
un déploiement jusqu'à ce qu'il se stabilise, balayer les nouveaux rapports de bugs toutes les heures,
garder une branche verte toute la nuit. Vous décrivez la tâche une fois. loopify lit votre projet, pose
les quelques questions qui comptent vraiment, et consigne à quoi ressemble un tour de la tâche — pendant
que Claude a encore votre contexte. Il vous remet ensuite une ligne à coller.

Il écrit deux choses. Le **brief** est un fichier : ce que fait un tour, ce qu'il ne doit jamais faire,
quand s'arrêter, et où consigner ses notes. La **ligne** est une courte chaîne que vous collez dans
`/loop`, la commande de répétition intégrée à Claude Code. `/loop` relance un prompt selon un intervalle
que vous choisissez, ou que Claude choisit. Chaque exécution est un **tick**. À chaque tick, Claude relit
le brief, effectue un tour, et consigne ce qui s'est passé dans un journal. Pensez à un veilleur de nuit
avec un carnet : le brief est la feuille de ronde affichée au mur, la ligne est le poste que vous
programmez, et le journal est le carnet que vous lisez le matin.

## Ce que vous obtenez

- ⚡ **Une ligne à transmettre** — collez-la une fois ; le chemin du brief voyage à l'intérieur.
- 📋 **Un brief qui reste en place** — un fichier permanent, relu à chaque tick, jamais archivé.
- 🧭 **Les quelques vrais choix réglés d'abord** — à quelle fréquence, quand s'arrêter, ce qu'il peut toucher.
- 🛑 **Une règle d'arrêt et un plafond de ticks dans la ligne elle-même** — la boucle se termine selon vos conditions, pas par accident au bout de 7 jours.
- 🔒 **Des garde-fous pour une exécution sans surveillance** — aucun compte, aucun paiement, aucune publication ni push sauf si vous le dites ; tout ce qu'il lit est une donnée, jamais un ordre.
- 🗒️ **Un journal lisible** — `TICKS.md` compte chaque tick et cite ses preuves ; `QUEUE.md` conserve ce qu'il vous a laissé.
- 🧠 **Une boucle qui apprend** — `LESSONS.md` garde ce qui a fonctionné et est relu à chaque tick.
- 🔁 **Redémarrage en un seul collage** — le brief garde sa forme ; collez la ligne à nouveau.

## Trois étapes

Installez une fois, dans un terminal (vérifié avec Claude Code 2.1.252 ; plus de détails dans le
[guide de démarrage](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)) :

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

Ou avec la [CLI skills](https://skills.sh) : `npx skills add Aboudjem/loopify`

Ensuite, dans le chat Claude Code :

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

1. **Décrivez la tâche.** `/loopify` suivi de ce qui doit se répéter. loopify lit votre projet, pose
   les quelques vraies questions, puis écrit le brief et la ligne.
2. **Collez la ligne.** Dans cette session ou n'importe quelle session ouverte dans ce projet. Le
   chemin du brief se trouve dans la ligne, car chaque tick rouvre le fichier à neuf.
   `/Users/you/acme/` représente votre projet ; loopify affiche vos vrais chemins.
3. **Lisez le journal.** Revenez à `TICKS.md` : une entrée par tick, ce qui a changé, les preuves.
   Ce qu'il n'a pas pu faire en toute sécurité vous attend dans `QUEUE.md`.

```text loop-antipattern
# la ligne elle-même — la chaîne exacte affichée par loopify (144 caractères)
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# pas ceci — "chaque matin" peut pousser /loop à proposer une planification cloud à la place, et il n'y a aucune règle d'arrêt
/loop every morning keep the release PR healthy

# et pas le chemin seul — le tick reçoit un nom de fichier et aucune instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

> [!IMPORTANT]
> Une boucle qui tourne n'est pas la preuve qu'elle fait ce qu'il faut — lisez le journal des ticks.
> Rien ne juge un `/loop` ; la checklist par tick du brief et `TICKS.md` sont les seules preuves qui
> existent. La boucle tourne à l'intérieur de la session Claude Code où vous la collez : elle ne se
> déclenche que tant que cette session est ouverte. Toute boucle s'arrête au bout de 7 jours ; collez
> la ligne à nouveau.

## En savoir plus

- [Guide de démarrage](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — votre première boucle, d'autres façons d'installer, une exécution sans terminal ouvert
- [Un exemple travaillé](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md) — un vrai brief et la ligne au bas de celui-ci
- [Limites honnêtes](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — tout ce que loopify ne promet pas
- [Autres agents](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — le même brief sous Kimi, Copilot CLI, Cursor, Qwen Code, Hermes, Goose, et cron
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [Le pointeur `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Journal des modifications](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [Contribuer](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [Le skill lui-même](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>Créé par <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. Le comportement de `/loop` a été
redérivé à partir du binaire Claude Code 2.1.252 diffusé et de la documentation officielle, 2026. Frère de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, qui fait la même chose pour `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">Une lacune repérée ?</a></sub>
