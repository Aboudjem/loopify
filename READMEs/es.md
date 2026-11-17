<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="Banner de loopify: el titular Your loop, in one line; tres etiquetas No babysitting, Fewer stuck ticks, Stops by itself; un anillo de 30 puntos de tick con 7 hechos; el comando de instalación y la línea de estado STATUS: NEEDS YOU, tick 7/30." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <a href="ja.md">日本語</a> · <b>Español</b> · <a href="fr.md">Français</a>
</p>

<p align="center"><strong>Revisa un trabajo de agente que se repite, en una línea.</strong></p>

<p align="center">
  <a href="#instalación">Instalación</a> · <a href="#cómo-funciona">Cómo funciona</a> · <a href="#qué-obtienes">Qué obtienes</a> · <a href="#compatibilidad">Compatibilidad</a> · <a href="#pruebas">Pruebas</a> · <a href="#preguntas-frecuentes">Preguntas frecuentes</a> · <a href="#límites">Límites</a>
</p>

<p align="center"><sub>Esta traducción puede ir por detrás del original en inglés.<!-- may-lag --></sub></p>

loopify escribe la línea de `/loop` y el brief. Después, un comando lee el registro por ti.

| Sin vigilar | Menos ticks atascados | Se detiene solo |
|:--|:--|:--|
| `loop_status.py` muestra uno de seis veredictos y hasta tres cosas que hacer. | loopify muestra primero los comandos que debes permitir, como `gh pr view`. | La línea lleva una regla de parada. Cada `/loop` termina a los 7 días. |

Un tick es una ejecución del trabajo que se repite. `make test` comprueba cada veredicto y cada código de salida.

**Funciona con:** el `/loop` de Claude Code. El skill se instala en cualquier agente que lea skills. Instalación probada: Claude Code, Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode. No depende de un modelo: es Markdown y tres scripts sencillos de Python.

```bash
npx skills add Aboudjem/loopify -g -a claude-code
# then, in Claude Code: /loopify keep our release PR healthy, every 20 minutes
```

El comando de estado, ejecutado sobre el ejemplo que trae este repositorio:

```bash
python3 skills/loopify/scripts/loop_status.py examples/loop-state/pr-babysitter --now 2026-09-01T09:50
```

```text
STATUS: NEEDS YOU · tick 7/30 · last tick 2026-09-01T09:40 (changed, 10 min ago) · 2 queued
Do next:
1. QUEUE.md, tick 4: Post the drafted reply on the `fetchAll` rename thread of PR #412
```

`--now` fija el reloj, así que el ejemplo muestra `NEEDS YOU` siempre.

**Qué es:** un skill que escribe el brief y la línea para el `/loop` de Claude Code.
**Cuándo usarlo:** para un trabajo que se repite, como vigilar una pull request toda la tarde.
**Qué obtienes:** una línea de estado que dice si el bucle te necesita.

El bucle vive en tu sesión abierta y termina a los 7 días.

## Instalación


**Recomendado: el CLI de skills de Vercel.** `npx skills` es el instalador abierto de Vercel para skills de agentes.

```bash
npx skills add Aboudjem/loopify -g
```

Funciona en más de 70 agentes: elige el tuyo en el menú ([agentes compatibles](https://github.com/vercel-labs/skills#supported-agents)). Instala para todos tus proyectos.

En una terminal muestra el menú de agentes. En un script instala en la carpeta de cada agente, así que añade `-a <agent>` ahí.

<a href="https://skills.sh/aboudjem/loopify"><img src="https://img.shields.io/badge/skills.sh-000000?style=flat-square&logo=vercel&logoColor=white" alt="skills.sh" height="24"></a> La página de loopify: [skills.sh/aboudjem/loopify](https://skills.sh/aboudjem/loopify).

**O instala directamente en un agente.** Cada comando instala para todos tus proyectos.

<p align="center">
  <a href="#install-claude-code"><img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat-square&logo=claude&logoColor=white" alt="Claude Code" height="24"></a>
  <a href="#install-codex"><img src="https://img.shields.io/badge/Codex-000000?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyBmaWxsPSJ3aGl0ZSIgcm9sZT0iaW1nIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BPHRpdGxlPk9wZW5BSTwvdGl0bGU%2BPHBhdGggZD0iTTIyLjI4MTkgOS44MjExYTUuOTg0NyA1Ljk4NDcgMCAwIDAtLjUxNTctNC45MTA4IDYuMDQ2MiA2LjA0NjIgMCAwIDAtNi41MDk4LTIuOUE2LjA2NTEgNi4wNjUxIDAgMCAwIDQuOTgwNyA0LjE4MThhNS45ODQ3IDUuOTg0NyAwIDAgMC0zLjk5NzcgMi45IDYuMDQ2MiA2LjA0NjIgMCAwIDAgLjc0MjcgNy4wOTY2IDUuOTggNS45OCAwIDAgMCAuNTExIDQuOTEwNyA2LjA1MSA2LjA1MSAwIDAgMCA2LjUxNDYgMi45MDAxQTUuOTg0NyA1Ljk4NDcgMCAwIDAgMTMuMjU5OSAyNGE2LjA1NTcgNi4wNTU3IDAgMCAwIDUuNzcxOC00LjIwNTggNS45ODk0IDUuOTg5NCAwIDAgMCAzLjk5NzctMi45MDAxIDYuMDU1NyA2LjA1NTcgMCAwIDAtLjc0NzUtNy4wNzI5em0tOS4wMjIgMTIuNjA4MWE0LjQ3NTUgNC40NzU1IDAgMCAxLTIuODc2NC0xLjA0MDhsLjE0MTktLjA4MDQgNC43NzgzLTIuNzU4MmEuNzk0OC43OTQ4IDAgMCAwIC4zOTI3LS42ODEzdi02LjczNjlsMi4wMiAxLjE2ODZhLjA3MS4wNzEgMCAwIDEgLjAzOC4wNTJ2NS41ODI2YTQuNTA0IDQuNTA0IDAgMCAxLTQuNDk0NSA0LjQ5NDR6bS05LjY2MDctNC4xMjU0YTQuNDcwOCA0LjQ3MDggMCAwIDEtLjUzNDYtMy4wMTM3bC4xNDIuMDg1MiA0Ljc4MyAyLjc1ODJhLjc3MTIuNzcxMiAwIDAgMCAuNzgwNiAwbDUuODQyOC0zLjM2ODV2Mi4zMzI0YS4wODA0LjA4MDQgMCAwIDEtLjAzMzIuMDYxNUw5Ljc0IDE5Ljk1MDJhNC40OTkyIDQuNDk5MiAwIDAgMS02LjE0MDgtMS42NDY0ek0yLjM0MDggNy44OTU2YTQuNDg1IDQuNDg1IDAgMCAxIDIuMzY1NS0xLjk3MjhWMTEuNmEuNzY2NC43NjY0IDAgMCAwIC4zODc5LjY3NjVsNS44MTQ0IDMuMzU0My0yLjAyMDEgMS4xNjg1YS4wNzU3LjA3NTcgMCAwIDEtLjA3MSAwbC00LjgzMDMtMi43ODY1QTQuNTA0IDQuNTA0IDAgMCAxIDIuMzQwOCA3Ljg3MnptMTYuNTk2MyAzLjg1NThMMTMuMTAzOCA4LjM2NCAxNS4xMTkyIDcuMmEuMDc1Ny4wNzU3IDAgMCAxIC4wNzEgMGw0LjgzMDMgMi43OTEzYTQuNDk0NCA0LjQ5NDQgMCAwIDEtLjY3NjUgOC4xMDQydi01LjY3NzJhLjc5Ljc5IDAgMCAwLS40MDctLjY2N3ptMi4wMTA3LTMuMDIzMWwtLjE0Mi0uMDg1Mi00Ljc3MzUtMi43ODE4YS43NzU5Ljc3NTkgMCAwIDAtLjc4NTQgMEw5LjQwOSA5LjIyOTdWNi44OTc0YS4wNjYyLjA2NjIgMCAwIDEgLjAyODQtLjA2MTVsNC44MzAzLTIuNzg2NmE0LjQ5OTIgNC40OTkyIDAgMCAxIDYuNjgwMiA0LjY2ek04LjMwNjUgMTIuODYzbC0yLjAyLTEuMTYzOGEuMDgwNC4wODA0IDAgMCAxLS4wMzgtLjA1NjdWNi4wNzQyYTQuNDk5MiA0LjQ5OTIgMCAwIDEgNy4zNzU3LTMuNDUzN2wtLjE0Mi4wODA1TDguNzA0IDUuNDU5YS43OTQ4Ljc5NDggMCAwIDAtLjM5MjcuNjgxM3ptMS4wOTc2LTIuMzY1NGwyLjYwMi0xLjQ5OTggMi42MDY5IDEuNDk5OHYyLjk5OTRsLTIuNTk3NCAxLjQ5OTctMi42MDY3LTEuNDk5N1oiLz48L3N2Zz4%3D" alt="Codex" height="24"></a>
  <a href="#install-cursor"><img src="https://img.shields.io/badge/Cursor-3B3B3B?style=flat-square&logo=cursor&logoColor=white" alt="Cursor" height="24"></a>
  <a href="#install-gemini-cli"><img src="https://img.shields.io/badge/Gemini-1A73E8?style=flat-square&logo=googlegemini&logoColor=white" alt="Gemini CLI" height="24"></a>
  <a href="#install-github-copilot"><img src="https://img.shields.io/badge/Copilot-24292F?style=flat-square&logo=githubcopilot&logoColor=white" alt="GitHub Copilot" height="24"></a>
  <a href="#install-opencode"><img src="https://img.shields.io/badge/OpenCode-4A4A4A?style=flat-square&logo=opencode&logoColor=white" alt="OpenCode" height="24"></a>
</p>

<a id="install-claude-code"></a>**Claude Code**, instalación probada. `/loop` solo existe en Claude Code:

```bash
npx skills add Aboudjem/loopify -g -a claude-code
```

<a id="install-codex"></a>**Codex**, instalación probada:

```bash
npx skills add Aboudjem/loopify -g -a codex
```

<a id="install-cursor"></a>**Cursor**, instalación probada:

```bash
npx skills add Aboudjem/loopify -g -a cursor
```

<a id="install-gemini-cli"></a>**Gemini CLI**, instalación probada:

```bash
npx skills add Aboudjem/loopify -g -a gemini-cli
```

<a id="install-github-copilot"></a>**GitHub Copilot**, instalación probada:

```bash
npx skills add Aboudjem/loopify -g -a github-copilot
```

<a id="install-opencode"></a>**OpenCode**, instalación probada:

```bash
npx skills add Aboudjem/loopify -g -a opencode
```

Solo este proyecto: quita `-g`. Otro agente: su código `-a` está en [docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md).

**O el plugin de Claude Code.** No añade comandos ni hooks al skill. Añade las actualizaciones por el marketplace 10x. Ejecútalo en tu terminal, no dentro de una sesión de Claude:

```bash
claude plugin marketplace add Aboudjem/10x && claude plugin install loopify@10x
```

Luego escribe `/loopify` en Claude Code y di qué debe repetirse.

No hay nada que compilar. El skill es una carpeta con tres scripts de Python de la biblioteca estándar.
`/loop` es un comando de Claude Code. En otros agentes, un planificador externo como cron lanza cada tick.

## Cómo funciona

Claude Code ya tiene `/loop`. Repite un prompt una y otra vez mientras tu sesión está abierta. No
escribe el prompt por ti. loopify escribe dos cosas:

- **El brief, un archivo.** Una vuelta del trabajo: qué leer, qué puede cambiar, qué no debe hacer
  nunca, cuándo parar. El bucle lo abre de nuevo en cada vuelta, así que puedes editarlo mientras corre.
- **La línea, una sola cadena.** La pegas en `/loop`. Lleva la ruta del brief y la regla de parada.

La línea le pide a cada tick que lea el brief, haga una vuelta y anote lo que pasó en `TICKS.md`.

### 1. Describe el trabajo

Escribe `/loopify` en Claude Code y di qué debe repetirse. loopify lee el README, los commits
recientes y las pull requests abiertas. Luego hace una tanda corta de preguntas.

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` representa tu proyecto. loopify muestra tus rutas reales.

### 2. Pega la línea

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude hace una vuelta ahora y luego cada 20 minutos en esa sesión. Se detiene cuando la PR se
fusiona o tras 30 ticks, lo que ocurra primero. Los dos errores más comunes:

```text loop-antipattern
# not this: "every morning" can make /loop offer a cloud schedule instead, and nothing says when to stop
/loop every morning keep the release PR healthy

# and not the path alone: the tick gets a filename and no instruction
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. Lee el registro, o pide el estado

`TICKS.md` tiene una entrada por cada tick que anota, con un contador arriba:

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

Lo que el bucle no pudo hacer con seguridad te espera en `QUEUE.md`. El comando de estado lee los tres
archivos y te dice qué hacer después.

## Qué obtienes

Un informe de estado. Esta es su salida real sobre la carpeta de ejemplo de este repositorio:

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
  lessons       4 entries
  lock          none
  interval      20m (from the saved line)
  log format    passes ticks_lint
  state dir     examples/loop-state/pr-babysitter
```

`--now` fija el reloj para que el ejemplo salga igual siempre. No lo uses en un bucle real.

1. La línea 1 es el veredicto: `OK`, `NEEDS YOU`, `STALE`, `STOPPED`, `NOT STARTED` o `BROKEN LOG`.
2. Luego, como mucho tres cosas que hacer.
3. Luego, el detalle. `lessons` cuenta las entradas de `LESSONS.md`.

Si un tick no anota nada, el estado dice `STALE` tras más de dos intervalos. Lee el tiempo entre
ticks de tu línea guardada, o de `--interval`.

El código de salida lleva el veredicto, para que un script o un cron puedan actuar:

| Salida | Veredicto | Significado |
| ------ | --------- | ----------- |
| `0` | `OK`, `STOPPED`, `NOT STARTED` | Nada te necesita |
| `1` | `NEEDS YOU`, `STALE`, `BROKEN LOG` | Mira el bucle |
| `2` | ninguno | Error de uso, o la carpeta de estado no existe |

`loop_status.py --help` muestra la misma tabla.

Cada brief que escribe loopify también te da:

- **Una regla de parada y un límite de ticks en la línea.** Un bucle que termina su trabajo se
  detiene. También uno que llega a su límite. loopify revisa antes tu línea con ocho reglas (`loop_line_lint.py`).
- **Los comandos que debes permitir antes de empezar.** El mensaje final lista lo que ejecuta un tick,
  como `gh pr view`, para que un tick no se quede esperando un permiso.
- **Barandillas para correr sin nadie.** Nada de cuentas ni pagos, nada de push ni publicaciones
  salvo que lo digas. Lo que el bucle lee, como un comentario de PR, es un dato, nunca una instrucción.
- **Una cláusula segura ante repeticiones.** El brief nombra la marca que un tick busca antes de
  actuar. Un tick que corre dos veces ve que el trabajo ya está hecho.
- **Un registro con forma fija.** Cada entrada empieza con `## tick <n> · <ISO timestamp> · changed |
noop | stopped`. `ticks_lint.py` lo comprueba.
- **Un bucle que aprende.** `LESSONS.md` guarda lo que funcionó y lo que hizo perder tiempo. El brief
  le pide a cada tick que lo lea.

## Compatibilidad

Cada fila es una instalación global (`-g`) que hice el 2026-11-17, en una carpeta personal vacía.

| Agente                   | Comando de instalación                                    | Probado                                      |
| ------------------------ | --------------------------------------------------------- | -------------------------------------------- |
| Claude Code 2.1.326      | `claude plugin install loopify@10x`, configuración limpia | 2026-11-17, plugin activo para el usuario    |
| Claude Code (CLI skills) | `npx skills add Aboudjem/loopify -g -a claude-code`       | 2026-11-17, skill en `~/.claude/skills/`     |
| Codex                    | `npx skills add Aboudjem/loopify -g -a codex`             | 2026-11-17, skill en `~/.agents/skills/`     |
| Cursor                   | `npx skills add Aboudjem/loopify -g -a cursor`            | 2026-11-17, skill en `~/.agents/skills/`     |
| Gemini CLI               | `npx skills add Aboudjem/loopify -g -a gemini-cli`        | 2026-11-17, skill en `~/.agents/skills/`     |
| GitHub Copilot           | `npx skills add Aboudjem/loopify -g -a github-copilot`    | 2026-11-17, skill en `~/.agents/skills/`     |
| OpenCode                 | `npx skills add Aboudjem/loopify -g -a opencode`          | 2026-11-17, skill en `~/.agents/skills/`     |

"Probado" significa que los archivos llegaron y los tres scripts corrieron desde la copia instalada.
No significa que un bucle haya corrido dentro de ese agente.

Documentados, sin probar: Windsurf, Zed, Kimi Code CLI y una copia a mano de `skills/loopify/`.
Mira [docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md).

El brief funciona en cualquier sitio. La línea no: es una línea de `/loop` de Claude Code. En otro
sitio el brief hace una vuelta, la anota y sale, y un planificador externo lanza el siguiente tick.
[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) cubre Kimi, Copilot CLI, Cursor, Goose y cron.

## Pruebas

`make test` imprime cada número de aquí. La CI lo ejecuta en cada push y pull request.

```bash
make test
```

| Suite                       | Qué comprueba                                                                     | Resultado |
| --------------------------- | --------------------------------------------------------------------------------- | --------- |
| `evals/check_skill.py`      | El contrato del skill, como aserciones                                            | 161/161   |
| `tests/test_manifests.py`   | Manifiestos, versiones, el brief de ejemplo, traducciones, SVG, secretos, guiones | 170/170   |
| `tests/test_ticks_lint.py`  | El formato del registro de ticks                                                  | 13/13     |
| `tests/test_loop_status.py` | Cada veredicto, los códigos de salida y la muestra de este README, byte a byte    | 62/62     |
| `tests/test_no_network.py`  | Ningún script incluido importa un módulo de red ni llama a curl o wget            | 18/18     |
| `tests/test_dated_facts.py` | Un dato de `/loop` fechado en una versión antigua nombra esa versión en todas partes | 5/5    |
| `evals/loop_line_lint.py`   | La línea canónica pasa las ocho reglas                                            | PASS      |

La CI también ejecuta `claude plugin validate . --strict` con un Claude Code fijado, y comprueba que
`npx skills@1.9.0 add . --list` encuentra el skill.

Comprobé los datos de `/loop` con Claude Code 2.1.326 y su documentación el 2026-11-17. Un dato no se
pudo volver a comprobar en 2.1.326: que `/clear` borra la programación. Sigue fechado en 2.1.252 (2026-09-01).
La tabla dato por dato está en [docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md#which-version-each-fact-was-checked-on).

## Preguntas frecuentes

**¿loopify inicia el bucle por mí?**
No. Escribe el brief, muestra la línea y se detiene. Tú pegas la línea cuando quieras que empiece.

**¿Por qué un archivo y una cadena, y no un solo prompt?**
El tick necesita detalle: rutas, comandos, qué hacer si se bloquea. `/loop` necesita un prompt corto
que envía de nuevo en cada tick. El brief tiene el detalle y la línea lleva su ruta.

**¿Cómo sé si el bucle sigue vivo?**
Ejecuta `loop_status.py` sobre la carpeta de estado. Dice `STALE` cuando ningún tick ha anotado nada
en más de dos intervalos. También puedes preguntar a Claude "what scheduled tasks do I have?".

**¿Qué detiene un bucle?**
La regla de parada del brief, el límite de ticks, el límite de siete días, o tú. La lista completa
está en [docs/faq.md](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md).

**¿Envía mi código a algún sitio?**
No. Los scripts de loopify no hacen llamadas de red: `tests/test_no_network.py` falla si uno importa
un módulo de red o llama a curl o wget. Un tick hace lo que tu brief permite.

## Límites

> [!IMPORTANT]
> Que un bucle corra no prueba que haga lo correcto. Ningún evaluador revisa `/loop`. El registro
> de ticks y el informe de estado son la única prueba.

- **El bucle vive en la sesión donde lo pegas.** Cierra la terminal y se detiene. En 2.1.252,
  `/clear` también borraba la programación. Pregunta "what scheduled tasks do I have?" para revisarlo.
- **Cada bucle termina a los 7 días.** Una sesión tiene como mucho 50 tareas programadas. Ambos son
  límites de Claude Code. Pega la línea otra vez para seguir.
- **Nada obliga a un tick a anotar.** La línea se lo pide. Un tick que se salta su entrada aparece
  como `STALE` cuando se conoce el intervalo.
- **Permite lo que ejecuta un tick, antes de empezar.** Un tick que encuentra una petición de permiso
  espera ahí una respuesta. loopify muestra los comandos que permitir, como `gh pr view` o `git commit`.
- **El informe de estado necesita el intervalo** para distinguir un bucle vivo de uno muerto. Lo lee
  de la línea guardada, o de `--interval`.

La lista completa, con su fuente: [docs/limits.md](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md).

## Más información

- [Inicio rápido](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md): tu primer bucle, paso a paso
- [Instalar en tu editor](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md): el código del agente y las dos vías de instalación
- [Un ejemplo completo](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md): un brief entero con la línea al final
- [Otros agentes](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md): el mismo brief con Kimi, Cursor, Goose y cron
- [Preguntas frecuentes](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [El puntero `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Changelog](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [Contribuir](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [El skill](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

Si has usado [goalify](https://github.com/Aboudjem/goalify), esto te resultará familiar. goalify es
para un trabajo que termina. loopify es para un trabajo que se repite.

---

<sub>Hecho por <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. El comportamiento de `/loop` se
comprobó con Claude Code 2.1.326 y la documentación oficial el 2026-11-17, salvo `/clear`, comprobado por
última vez en 2.1.252 (2026-09-01). <a href="https://github.com/Aboudjem/loopify/blob/main/docs/limits.md#which-version-each-fact-was-checked-on">Tabla dato por dato</a>. Hermano de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, que hace lo mismo para `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">¿Ves algo que falta?</a></sub>

<sub>Traducción asistida por máquina y revisada. La versión de referencia es el <a href="../README.md">README.md</a> en inglés.</sub>
