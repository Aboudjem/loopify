<p align="center">
  <a href="../README.md">English</a> ·
  <a href="zh-CN.md">简体中文</a> ·
  <a href="ja.md">日本語</a> ·
  <b>Español</b> ·
  <a href="fr.md">Français</a>
</p>

<p align="center"><sub>Esta traducción puede ir por detrás del original en inglés.<!-- may-lag --></sub></p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Aboudjem/loopify/main/assets/hero.svg" alt="Cuatro pasos: describe un trabajo que se repite, obtén un brief (un archivo) y una línea (una cadena), pega la línea en /loop, vuelve a un registro de ticks." width="100%">
</p>

<h1 align="center">loopify</h1>

<p align="center">
  <strong>Dale a Claude un trabajo que se repite. Vuelve a un registro de lo que hizo cada tick — no a un loop que tengas que estar vigilando.</strong>
</p>

<p align="center">
  <a href="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml"><img src="https://github.com/Aboudjem/loopify/actions/workflows/validate.yml/badge.svg" alt="validate"></a>
  <a href="https://github.com/Aboudjem/loopify/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT license"></a>
  <img src="https://img.shields.io/badge/Claude%20Code-skill-d97757" alt="Claude Code skill">
  <a href="https://skills.sh/Aboudjem/loopify"><img src="https://skills.sh/b/Aboudjem/loopify" alt="skills.sh"></a>
</p>

loopify es una skill de Claude Code para trabajos que nunca terminan del todo: mantener en buen
estado una pull request de release mientras van llegando las revisiones, vigilar un deploy hasta que se
estabiliza, revisar los bug reports nuevos cada hora, mantener una rama en verde durante toda la
noche. Describes el trabajo una vez. loopify lee tu proyecto, te pregunta por las pocas decisiones
que de verdad importan, y anota cómo es una ronda del trabajo — mientras Claude todavía tiene tu
contexto. Luego te entrega una línea para pegar.

Escribe dos cosas. El **brief** es un archivo: qué hace una ronda, qué no debe hacer nunca, cuándo
detenerse y dónde escribir sus notas. La **línea** es una cadena corta que pegas en `/loop`, el
comando de repetición integrado de Claude Code. `/loop` vuelve a ejecutar un prompt según el horario
que elijas, o uno que elija Claude. Cada ejecución es un **tick**. En cada tick, Claude vuelve a leer
el brief, hace una ronda, y escribe lo que pasó en un registro. Piénsalo como un vigilante nocturno
con un portapapeles: el brief es la hoja de ronda en la pared, la línea es el turno que dejas
programado, y el registro es el portapapeles que lees por la mañana.

## Lo que obtienes

- ⚡ **Una línea para entregar** — la pegas una vez; la ruta del brief viaja dentro de ella.
- 📋 **Un brief que se queda quieto** — un archivo fijo, releído en cada tick, nunca archivado.
- 🧭 **Las pocas decisiones que importan, resueltas primero** — con qué frecuencia, cuándo detenerse, qué puede tocar.
- 🛑 **Una regla de parada y un tope de ticks en la propia línea** — el loop termina en tus términos, no a los 7 días por accidente.
- 🔒 **Límites de seguridad para una ejecución sin supervisión** — sin cuentas, sin pagos, sin hacer push ni publicar salvo que tú lo digas; todo lo que lee es información, nunca órdenes.
- 🗒️ **Un registro que puedes leer** — `TICKS.md` cuenta cada tick y cita su evidencia; `QUEUE.md` guarda lo que dejó pendiente para ti.
- 🧠 **Un loop que aprende** — `LESSONS.md` guarda lo que funcionó y se relee en cada tick.
- 🔁 **Reinicia pegando una sola vez** — el brief conserva su forma; vuelve a pegar la línea.

## Tres pasos

Instálalo una vez, en una terminal (verificado con Claude Code 2.1.252; más en la [guía rápida](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)):

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

O con la [CLI de skills](https://skills.sh): `npx skills add Aboudjem/loopify`

Luego, en el chat de Claude Code:

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

1. **Describe el trabajo.** `/loopify` más lo que debe repetirse. loopify lee tu proyecto, hace las
   pocas preguntas que importan, y luego escribe el brief y la línea.
2. **Pega la línea.** En esta sesión o en cualquier sesión abierta en ese proyecto. La ruta del
   brief está dentro de la línea, porque cada tick abre el archivo de nuevo. `/Users/you/acme/`
   representa tu proyecto; loopify imprime tus rutas reales.
3. **Lee el registro.** Vuelve a `TICKS.md`: una entrada por tick, qué cambió, la evidencia. Lo que
   no pudo hacer con seguridad te espera en `QUEUE.md`.

```text loop-antipattern
# la línea en sí — la cadena exacta que imprimió loopify (144 caracteres)
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md — read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# esto no — "every morning" puede hacer que /loop ofrezca un horario en la nube en su lugar, y no hay regla de parada
/loop every morning keep the release PR healthy

# y tampoco la ruta sola — el tick recibe un nombre de archivo y ninguna instrucción
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

> [!IMPORTANT]
> Que un loop esté corriendo no es prueba de que esté haciendo lo correcto — lee el registro de
> ticks. Nada juzga un `/loop`; la checklist por tick del brief y `TICKS.md` son la única prueba
> que existe. El loop se ejecuta dentro de la sesión de Claude Code en la que lo pegaste: solo se
> dispara mientras esa sesión está abierta. Todo loop se detiene a los 7 días; vuelve a pegar la
> línea.

## Más información

- [Guía rápida](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — tu primer loop, otras formas de instalar, cómo ejecutarlo sin una terminal abierta
- [Un ejemplo resuelto](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md) — un brief real y la línea al final de él
- [Límites honestos](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — todo lo que loopify no promete
- [Otros agentes](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — el mismo brief bajo Kimi, Copilot CLI, Cursor, Qwen Code, Hermes, Goose y cron
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) · [El puntero `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) · [Registro de cambios](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) · [Contribuir](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) · [La skill en sí](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

---

<sub>Creado por <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. El comportamiento de
`/loop` se ha vuelto a derivar del binario de Claude Code 2.1.252 tal como se distribuye y de la
documentación oficial, 2026. Hermano de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, que hace lo mismo para `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">¿Ves un hueco?</a></sub>
