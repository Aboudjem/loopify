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

Certaines tâches ne se terminent jamais vraiment. Une pull request de release a besoin que quelqu'un
surveille ses vérifications et réponde aux relecteurs pendant tout l'après-midi. Un déploiement doit
être vérifié toutes les quelques minutes jusqu'à ce qu'il se stabilise. De nouveaux rapports de bugs
s'accumulent pendant la nuit et méritent un premier coup d'œil avant que quiconque ne les lise. Vous
pouvez demander à Claude de faire chacune de ces choses une fois. Lui demander de continuer à les
faire, selon un rythme, sans que vous restiez là à surveiller, c'est là que ça se complique.

Claude Code dispose d'une commande pour répéter une tâche : `/loop`. Vous lui donnez un prompt et un
intervalle, et elle relance ce prompt encore et encore tant que votre session reste ouverte. Ce qu'elle
ne vous donne pas, c'est le prompt. Écrivez-en un court, et la boucle oublie ce qu'elle a décidé la
dernière fois. Écrivez-en un long, et elle pousse des choses que vous ne vouliez jamais pousser, ou
continue de tourner bien après que la tâche est terminée, parce que rien ne lui a dit quand s'arrêter.

loopify est un skill Claude Code qui écrit ce prompt à votre place, correctement. Vous décrivez la
tâche une fois, en langage clair. loopify lit votre projet pendant que Claude a encore votre contexte,
vous pose les quelques questions qui comptent vraiment (à quelle fréquence, quand s'arrêter, ce qu'il
peut toucher), et écrit deux choses.

La première est le **brief** : un fichier qui décrit un tour de la tâche. Ce qu'il faut lire, ce qu'il
peut changer, ce qu'il ne doit jamais faire, quand s'arrêter, et où consigner ce qui s'est passé. La
boucle rouvre ce fichier à neuf au début de chaque exécution, pour que rien ne se perde d'une exécution
à l'autre, et vous pouvez le modifier pendant que la boucle tourne.

La seconde est la **ligne** : une courte chaîne que vous collez dans `/loop`. Le chemin du brief s'y
trouve, pour que chaque exécution sache où regarder. La règle d'arrêt aussi, pour que la boucle se
termine selon vos règles.

Chaque exécution est un **tick**. À chaque tick, Claude relit le brief, effectue un tour de la tâche,
et consigne ce qui s'est passé dans un journal appelé `TICKS.md`. Pensez à un veilleur de nuit avec un
carnet : le brief est la feuille de ronde affichée au mur, la ligne est le poste que vous programmez,
et le journal est le carnet que vous lisez le matin. Vous n'avez pas besoin de veiller. Vous devez en
revanche lire le carnet.

## Ce que vous obtenez

- ⚡ **Une ligne à transmettre.** Collez-la une fois, dans cette session ou n'importe quelle session
  ouverte dans ce projet. Le chemin du brief voyage à l'intérieur.
- 📋 **Un brief qui reste en place.** C'est un fichier permanent : relu à chaque tick, jamais archivé,
  jamais réécrit par la boucle. Vous pouvez l'ouvrir et changer une décision entre deux ticks.
- 🧭 **Les quelques vrais choix réglés d'abord.** À quelle fréquence la boucle tourne, quand elle
  s'arrête, et ce qu'elle peut toucher : ces questions vous sont posées une fois, avant le premier
  tick, pas devinées au tick 12.
- 🛑 **Une règle d'arrêt et un plafond de ticks dans la ligne elle-même.** Une boucle qui termine sa
  tâche s'arrête. Une boucle qui atteint son plafond s'arrête. Rien ne tourne accidentellement
  jusqu'à la limite de 7 jours.
- 🔒 **Des garde-fous pour une exécution sans surveillance.** Aucun compte, aucun paiement, aucun push
  ni aucune publication sauf si vous le dites. Tout ce que la boucle lit en chemin, comme un
  commentaire de PR ou une issue, est une donnée, jamais une instruction.
- 🗒️ **Un journal lisible.** `TICKS.md` compte chaque tick et cite les preuves de ce qu'elle a fait.
  `QUEUE.md` conserve ce que la boucle n'a pas pu faire en toute sécurité et vous a laissé.
- 🧠 **Une boucle qui apprend.** `LESSONS.md` garde ce qui a fonctionné et ce qui a fait perdre du
  temps, et la boucle le relit à chaque tick.
- 🔁 **Redémarrage en un seul collage.** Le brief garde sa forme. Quand la boucle se termine, collez
  la ligne à nouveau.

## Trois étapes

### 1. Installez une fois

Ouvrez un terminal et ajoutez le marketplace 10x, puis installez le plugin. loopify a été vérifié avec
Claude Code 2.1.252 ; le [guide de démarrage](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)
présente les autres façons de l'installer.

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

Si vous préférez la [CLI skills](https://skills.sh), une seule commande fait la même chose :
`npx skills add Aboudjem/loopify`

### 2. Décrivez la tâche, puis collez la ligne

Dans le chat Claude Code, tapez `/loopify` et dites ce qui doit se répéter. Voici à quoi cela ressemble
pour une pull request de release qui a besoin d'être surveillée :

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

loopify commence par lire votre projet. Il regarde le README, les commits récents, les pull requests
ouvertes, et vous pose une courte série de questions : à quelle fréquence, quand s'arrêter, ce que la
boucle peut changer. Il écrit ensuite le brief et affiche la ligne. `/Users/you/acme/` représente votre
projet ; loopify affiche vos vrais chemins.

Collez la ligne dans le chat. Dans l'exemple ci-dessus, Claude effectue un tour tout de suite, puis
toutes les 20 minutes, dans cette session, jusqu'à ce que la PR soit fusionnée ou que 30 ticks se
soient écoulés, selon ce qui arrive en premier. Laissez l'intervalle de côté dans la ligne et Claude
choisit le rythme lui-même, en attendant plus longtemps quand rien ne se passe.

### 3. Lisez le journal

Revenez quand vous voulez. `TICKS.md` contient une entrée par tick avec ce qui a changé et les preuves
à l'appui, avec un compteur en haut pour voir où en est la boucle :

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI : lint en échec sur src/api.ts → import inutilisé corrigé, commit 4f2a1c9, npm test 12/12
- revues : 1 nouveau fil répondu (renommage), réponse rédigée dans QUEUE.md
```

Tout ce que la boucle n'a pas pu faire en toute sécurité, comme une réponse de revue qu'elle ne doit
pas publier seule, vous attend dans `QUEUE.md`.

### La ligne, la bonne et les mauvaises

La ligne correcte porte le chemin du brief et la règle d'arrêt. Les deux mauvaises ci-dessous sont les
erreurs les plus fréquentes : une formulation quotidienne, qui peut pousser `/loop` à proposer une
planification cloud au lieu d'une boucle locale, et un chemin seul, qui ne donne rien à faire au tick.

```text loop-antipattern
# la ligne elle-même — la chaîne exacte affichée par loopify (144 caractères)
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# pas ceci — "chaque matin" peut pousser /loop à proposer une planification cloud à la place, et il n'y a aucune règle d'arrêt
/loop every morning keep the release PR healthy

# et pas le chemin seul — le tick reçoit un nom de fichier et aucune instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### Ce qu'il est utile de savoir avant votre première boucle

- **La boucle vit dans la session où vous la collez.** Elle ne se déclenche que tant que cette session
  est ouverte. Fermez le terminal et elle s'arrête ; `/clear` efface aussi la planification. Faire
  tourner Claude Code en arrière-plan la garde active sans fenêtre ouverte.
- **Pré-approuvez ce qu'un tick exécute.** loopify affiche les commandes dont la boucle a besoin,
  comme `gh pr view` ou `git commit`. Ajoutez-les à votre liste d'autorisations avant de coller. Si un
  tick tombe sur une demande de permission, il attend là jusqu'à ce que quelqu'un réponde.
- **Toute boucle se termine au bout de 7 jours.** C'est une règle de Claude Code pour le travail
  planifié, dans les deux modes. Collez la ligne à nouveau et la boucle reprend là où le brief
  l'indique.
- **Pour arrêter plus tôt**, appuyez sur `Esc` pendant qu'une boucle à rythme libre attend, ou dites
  « annule la tâche pr-babysitter » pour une boucle à intervalle fixe. Demandez « quelles tâches
  planifiées ai-je ? » pour confirmer qu'elle a disparu.

> [!IMPORTANT]
> Une boucle qui tourne n'est pas la preuve qu'elle fait ce qu'il faut — lisez le journal des ticks.
> Rien ne juge un `/loop` ; la checklist par tick du brief et `TICKS.md` sont les seules preuves qui
> existent. La boucle tourne à l'intérieur de la session Claude Code où vous la collez : elle ne se
> déclenche que tant que cette session est ouverte. Toute boucle s'arrête au bout de 7 jours ; collez
> la ligne à nouveau.

## En savoir plus

- [Guide de démarrage](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — votre
  première boucle étape par étape, d'autres façons d'installer, et comment faire tourner une boucle
  sans terminal ouvert
- [Un exemple travaillé](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md)
  — un brief complet pour la tâche de PR de release, avec la ligne tout en bas
- [Limites honnêtes](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — tout ce que
  loopify ne promet pas, chaque point remontant au binaire ou à la documentation de Claude Code
- [Autres agents](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — le même brief
  sous Kimi, Copilot CLI, Cursor, Qwen Code, Hermes, Goose, et cron classique
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [Le pointeur `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Journal des modifications](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [Contribuer](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [Le skill lui-même](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

Si vous avez déjà utilisé [goalify](https://github.com/Aboudjem/goalify), ceci vous sera familier.
goalify est fait pour une tâche qui se termine : une grande tâche, une seule définition du « terminé »,
`/goal`. loopify est fait pour une tâche qui se répète. Même auteur, même habitude de tester d'abord,
même honnêteté sur ce que l'outil ne peut pas promettre.

---

<sub>Créé par <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. Le comportement de `/loop` a été
redérivé à partir du binaire Claude Code 2.1.252 diffusé et de la documentation officielle, 2026. Frère de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, qui fait la même chose pour `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">Une lacune repérée ?</a></sub>
