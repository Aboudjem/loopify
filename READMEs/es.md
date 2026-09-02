<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-dark.svg">
    <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero-light.svg" alt="loopify: un bucle que no tienes que vigilar. Dale a Claude un trabajo que se repite y vuelve a un registro de lo que hizo cada tick." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <a href="https://github.com/Aboudjem/loopify/stargazers"><img src="https://img.shields.io/github/stars/Aboudjem/loopify?color=2BE8C8&labelColor=0A0F1C" alt="stars"></a>
</p>

<p align="center">
  <a href="../README.md">English</a> · <a href="zh-CN.md">简体中文</a> · <a href="ja.md">日本語</a> · <b>Español</b> · <a href="fr.md">Français</a>
</p>

<p align="center">
  <strong>Dale a Claude un trabajo que se repite. Vuelve a un registro de lo que hizo cada tick, no a un bucle que tienes que vigilar.</strong>
</p>

<p align="center">
  <a href="#qué-hace">Qué hace</a> · <a href="#instalación">Instalación</a> · <a href="#cómo-usarlo">Cómo usarlo</a> · <a href="#en-tu-editor">En tu editor</a> · <a href="#conviene-saber">Conviene saber</a> · <a href="#más-información">Más información</a>
</p>

<p align="center"><sub>Esta traducción puede ir por detrás del original en inglés.<!-- may-lag --></sub></p>

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

## Qué hace

Algunos trabajos nunca terminan del todo. Una pull request de release hay que vigilarla toda la
tarde; los informes de fallos se acumulan durante la noche y piden un primer vistazo antes de que
nadie los lea. Claude Code ya tiene un comando para repetir trabajo, `/loop`: le das un prompt y un
intervalo, y ejecuta ese prompt una y otra vez mientras tu sesión siga abierta. Lo que no te da es el
prompt.

loopify escribe ese prompt. Describes el trabajo una vez, en palabras llanas. loopify lee tu proyecto
mientras Claude todavía tiene tu contexto, te plantea las pocas decisiones que importan (con qué
frecuencia, cuándo parar, qué puede tocar) y escribe dos cosas.

- **El brief, un archivo.** Una ronda del trabajo: qué leer, qué puede cambiar, qué no debe hacer
  nunca, cuándo parar y dónde anotar lo que pasó. El bucle lo abre de nuevo al principio de cada
  ejecución, así que nada se pierde entre ejecuciones, y puedes editarlo con el bucle en marcha.
- **La línea, una sola cadena.** La pegas en `/loop`. La ruta del brief va dentro, así que cada
  ejecución sabe dónde mirar. La regla de parada también, así que el bucle termina en tus términos.

Cada ejecución es un **tick**. En cada tick, Claude relee el brief, hace una ronda del trabajo y
escribe lo que pasó en un registro llamado `TICKS.md`. No tienes que quedarte despierto; sí tienes
que leer el registro.

Si has usado [goalify](https://github.com/Aboudjem/goalify), esto te resultará familiar. goalify es
para un trabajo que termina: una tarea grande, una definición de qué es "terminado", `/goal`.
loopify es para un trabajo que se repite.

## Instalación

Los dos comandos de arriba añaden el marketplace 10x e instalan el plugin en Claude Code, contra el
que loopify se verificó en la versión 2.1.252. Cualquier otro agente instala el mismo directorio de
skill en una línea, con el [CLI de skills](https://github.com/vercel-labs/skills):

```bash
npx skills add Aboudjem/loopify
```

## Cómo usarlo

### 1. Describe el trabajo

Escribe `/loopify` en el chat de Claude Code y di qué debe repetirse. loopify lee el README, los
commits recientes y las pull requests abiertas, y luego hace una sola tanda corta de preguntas.

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file, re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string, you paste it below
```

`/Users/you/acme/` está en lugar de tu proyecto; loopify imprime tus rutas reales.

### 2. Pega la línea

```text
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

Claude hace una ronda enseguida y luego cada 20 minutos, en esa sesión, hasta que la pull request se
fusione o pasen 30 ticks, lo que ocurra primero. Quita el intervalo y Claude marca el ritmo por su
cuenta. Los dos errores más frecuentes:

```text loop-antipattern
# esto no: "every morning" puede hacer que /loop ofrezca un horario en la nube, y nada dice cuándo parar
/loop every morning keep the release PR healthy

# ni la ruta sola: el tick recibe un nombre de archivo y ninguna instrucción
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### 3. Lee el registro

`TICKS.md` tiene una entrada por tick, con lo que cambió y la evidencia de ello, y un contador
arriba:

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint failed on src/api.ts → fixed the unused import, committed 4f2a1c9, npm test 12/12
- reviews: 1 new thread answered (rename), reply drafted in QUEUE.md
```

Todo lo que el bucle no pudo hacer con seguridad te espera en `QUEUE.md`.

## Qué obtienes

- **Un brief que se queda donde está.** Releído en cada tick, nunca archivado, nunca reescrito por el
  bucle. Con qué frecuencia corre, cuándo para y qué puede tocar se deciden antes del primer tick.
- **Una regla de parada y un tope de ticks dentro de la línea.** Un bucle que termina su trabajo
  se detiene, y uno que llega a su tope también.
- **Barandillas para una ejecución sin vigilancia.** Sin cuentas, sin pagos, sin push ni
  publicaciones salvo que lo digas. Todo lo que el bucle lee, por ejemplo un comentario de una pull
  request, es dato, nunca instrucción.
- **Una cláusula de seguridad ante la repetición en cada brief.** El brief nombra la marca que un
  tick busca antes de actuar, para que un tick repetido vea que el trabajo ya ocurrió.
- **Un registro con forma.** Cada entrada de `TICKS.md` empieza con la misma cabecera,
  `## tick <n> · <ISO timestamp> · changed | noop | stopped`, comprobable con
  `skills/loopify/scripts/ticks_lint.py`. Los elementos bloqueados en `QUEUE.md` llevan una línea
  `reason:` y una línea `unblock:`.
- **Un bucle que aprende.** `LESSONS.md` guarda lo que funcionó y lo que hizo perder tiempo, y el
  bucle lo relee en cada tick.

## En tu editor

Funciona en Claude Code, Cursor, Codex, Copilot, Gemini CLI y más de otros 70 agentes a través de
`npx skills add`.

| Dónde | Cómo |
| --- | --- |
| Claude Code | `claude plugin install loopify@10x` |
| Cursor, Codex, Gemini CLI, OpenCode, Windsurf, Zed, Kimi Code CLI | `npx skills add Aboudjem/loopify -a <agent>` |
| VS Code y GitHub Copilot | `npx skills add Aboudjem/loopify -a github-copilot` |
| Todo lo demás | copia `skills/loopify/` en el directorio de skills de tu agente |

loopify es un solo directorio de skill con dos scripts de Python de la biblioteca estándar al lado,
así que no hay servidor que levantar ni nada que compilar. El código `-a`, las dos rutas de
instalación por agente y la copia manual están en
[docs/editors.md](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md).

El brief viaja; la línea no. La línea es una línea `/loop` de Claude Code, y el paso de planificación
del brief nombra herramientas de Claude Code. El brief ya contempla ese caso: haz una ronda,
regístrala, sal y deja que un planificador externo dispare el siguiente tick.
[docs/other-agents.md](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) cubre
Kimi, Copilot CLI, Cursor, Qwen Code, Hermes, Goose y cron a secas.

## Conviene saber

> [!IMPORTANT]
> Un bucle en marcha no demuestra que esté haciendo lo correcto. Lee el registro de ticks. No hay
> ningún evaluador detrás de `/loop`: la lista de comprobación por tick del brief y `TICKS.md` son la
> única prueba que existe.

- **El bucle vive en la sesión donde lo pegas.** Solo se dispara mientras esa sesión sigue abierta.
  Cierra el terminal y se detiene; `/clear` también borra la planificación. Ejecutar Claude Code en segundo
  plano lo mantiene vivo sin ventana.
- **Todo bucle acaba a los 7 días**, y una sesión admite como mucho 50 tareas planificadas. Ambos son
  límites de Claude Code sobre el trabajo planificado, no de loopify. Vuelve a pegar la línea para
  seguir.
- **Preautoriza lo que ejecuta un tick.** loopify imprime los comandos que el bucle necesita, como
  `gh pr view` o `git commit`. Un tick que se topa con una petición de permiso se queda ahí esperando
  respuesta.

## Más información

- [Guía rápida](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md), tu primer bucle
  paso a paso, y sin terminal abierto
- [Instalar en tu editor](https://github.com/Aboudjem/loopify/blob/main/docs/editors.md), el código
  de agente y las dos rutas del CLI de skills
- [Un ejemplo completo](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md),
  un brief entero con la línea al final
- [Límites honestos](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md), lo que loopify no
  promete, con su origen en el binario o en la documentación
- [Otros agentes](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md), el mismo brief
  en Kimi, Cursor, Goose y cron a secas
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [El puntero `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Changelog](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [Contribuir](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [El skill en sí](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>Creado por <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. El comportamiento de `/loop` se
volvió a derivar del binario de Claude Code 2.1.252 publicado y de la documentación oficial, 2026. Hermano de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, que hace lo mismo para `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">¿Ves algo que falta?</a></sub>

<sub>Traducción asistida por máquina y revisada. La versión de referencia es el <a href="../README.md">README.md</a> en inglés.</sub>
