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

Hay trabajos que nunca terminan del todo. Una pull request de release necesita que alguien vigile
sus checks y responda a los revisores durante toda la tarde. Un deploy hay que revisarlo cada pocos
minutos hasta que se estabiliza. Los bug reports nuevos se acumulan durante la noche y conviene
echarles un primer vistazo antes de que nadie los lea. Puedes pedirle a Claude que haga cualquiera
de estas cosas una vez. Pedirle que las siga haciendo, con un horario, sin que tú estés ahí sentado,
es la parte que se complica.

Claude Code tiene un comando para el trabajo que se repite: `/loop`. Le das un prompt y un
intervalo, y vuelve a ejecutar ese prompt una y otra vez mientras tu sesión sigue abierta. Lo que no
te da es el prompt. Si escribes uno corto, el loop olvida lo que decidió la última vez. Si escribes
uno largo, acaba haciendo push de cosas que nunca quisiste subir, o sigue corriendo mucho después de
que el trabajo termine, porque nada le dijo cuándo detenerse.

loopify es una skill de Claude Code que te escribe ese prompt como es debido. Describes el trabajo
una vez, con tus propias palabras. loopify lee tu proyecto mientras Claude todavía tiene tu
contexto, te pregunta por las pocas decisiones que importan (con qué frecuencia, cuándo detenerse,
qué puede tocar), y escribe dos cosas.

La primera es el **brief**: un archivo que describe una ronda del trabajo. Qué leer, qué puede
cambiar, qué no debe hacer nunca, cuándo detenerse, y dónde anotar lo que pasó. El loop abre este
archivo de nuevo al empezar cada ejecución, así que no se pierde nada entre una ronda y otra, y
puedes editarlo mientras el loop está corriendo.

La segunda es la **línea**: una cadena corta que pegas en `/loop`. La ruta del brief va dentro de
ella, así que cada ejecución sabe dónde mirar. También va la regla de parada, para que el loop
termine en tus términos.

Cada ejecución es un **tick**. En cada tick, Claude vuelve a leer el brief, hace una ronda del
trabajo, y escribe lo que pasó en un registro llamado `TICKS.md`. Piénsalo como un vigilante
nocturno con un portapapeles: el brief es la hoja de ronda pinchada en la pared, la línea es el
turno que dejas programado, y el registro es el portapapeles que lees por la mañana. Tú no tienes
que quedarte despierto. Sí tienes que leer el portapapeles.

## Lo que obtienes

- ⚡ **Una línea para entregar.** Pégala una vez, en esta sesión o en cualquier sesión abierta en ese
  proyecto. La ruta del brief viaja dentro de ella.
- 📋 **Un brief que se queda quieto.** Es un archivo fijo: se relee en cada tick, nunca se archiva,
  el loop nunca lo reescribe. Puedes abrirlo y cambiar una decisión entre un tick y otro.
- 🧭 **Las pocas decisiones que de verdad importan, resueltas primero.** Con qué frecuencia corre,
  cuándo se detiene y qué puede tocar se preguntan una vez, antes del primer tick, no se adivinan en
  el tick 12.
- 🛑 **Una regla de parada y un tope de ticks en la propia línea.** Un loop que termina su trabajo se
  detiene. Un loop que llega a su tope se detiene. Nada corre hasta el límite de 7 días por
  accidente.
- 🔒 **Límites de seguridad para una ejecución sin supervisión.** Sin cuentas, sin pagos, sin hacer
  push ni publicar salvo que tú lo digas. Cualquier cosa que el loop lea por el camino, como un
  comentario de PR o un issue, es información, nunca una instrucción.
- 🗒️ **Un registro que puedes leer.** `TICKS.md` cuenta cada tick y cita la evidencia de lo que hizo.
  `QUEUE.md` guarda lo que no pudo hacer con seguridad y te dejó pendiente.
- 🧠 **Un loop que aprende.** `LESSONS.md` guarda lo que funcionó y lo que fue una pérdida de tiempo,
  y el loop lo relee en cada tick.
- 🔁 **Reinicia con una sola pegada.** El brief conserva su forma. Cuando el loop termina, vuelve a
  pegar la línea.

## Tres pasos

### 1. Instálalo una vez

Abre una terminal y añade el marketplace 10x, luego instala el plugin. loopify se verificó contra
Claude Code 2.1.252; la [guía rápida](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md)
tiene las demás formas de instalarlo.

```bash
claude plugin marketplace add Aboudjem/10x
claude plugin install loopify@10x
```

Si prefieres la [CLI de skills](https://skills.sh), un solo comando hace lo mismo:
`npx skills add Aboudjem/loopify`

### 2. Describe el trabajo, y luego pega la línea

En el chat de Claude Code, escribe `/loopify` y di qué debe repetirse. Así es como se ve para una
pull request de release que necesita que alguien la vigile:

```text
/loopify keep our release PR healthy, check it every 20 minutes
    brief      /Users/you/acme/.loop/pr-babysitter.md     a file — re-read every tick
    state      /Users/you/acme/.loop/pr-babysitter/       TICKS.md · LESSONS.md · QUEUE.md
    line       144 chars                                  one string — you paste it below

/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.
```

loopify lee tu proyecto primero. Mira el README, los commits recientes, las pull requests abiertas,
y te hace una tanda corta de preguntas: con qué frecuencia, cuándo detenerse, qué puede cambiar el
loop. Luego escribe el brief e imprime la línea. `/Users/you/acme/` representa tu proyecto; loopify
imprime tus rutas reales.

Pega la línea en el chat. En el ejemplo de arriba, Claude ejecuta una ronda enseguida y luego cada
20 minutos, en esa sesión, hasta que la PR se fusiona o pasan 30 ticks, lo que ocurra primero. Si
dejas el intervalo fuera de la línea, Claude elige el ritmo por sí mismo, esperando más cuando no
pasa nada.

### 3. Lee el registro

Vuelve cuando quieras. `TICKS.md` tiene una entrada por tick con lo que cambió y la evidencia de
ello, y un contador arriba para que veas cómo va el loop:

```text
tick: 7/30

## tick 7 · 2026-09-01T09:40 · changed
- CI: lint falló en src/api.ts → arreglado el import sin usar, commit 4f2a1c9, npm test 12/12
- reviews: 1 hilo nuevo respondido (rename), respuesta redactada en QUEUE.md
```

Lo que el loop no pudo hacer con seguridad, como una respuesta de review que no debía publicar por
su cuenta, te espera en `QUEUE.md`.

### La línea, bien y mal

La línea correcta lleva la ruta del brief y la regla de parada. Las dos incorrectas de abajo son los
errores más comunes: una frase con periodicidad diaria, que puede hacer que `/loop` ofrezca un
horario en la nube en vez de un loop local, y una ruta sola, que no le da al tick ninguna
instrucción.

```text loop-antipattern
# la línea en sí — la cadena exacta que imprimió loopify (144 caracteres)
/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, obey its stop rule (30 ticks or the PR merges), log the tick.

# esto no — "every morning" puede hacer que /loop ofrezca un horario en la nube en su lugar, y no hay regla de parada
/loop every morning keep the release PR healthy

# y tampoco la ruta sola — el tick recibe un nombre de archivo y ninguna instrucción
/loop 20m /Users/you/acme/.loop/pr-babysitter.md
```

### Cosas que conviene saber antes de tu primer loop

- **El loop vive en la sesión en la que lo pegas.** Solo se dispara mientras esa sesión está
  abierta. Cierra la terminal y se detiene; `/clear` también borra el horario. Ejecutar Claude Code
  en segundo plano lo mantiene vivo sin necesidad de una ventana.
- **Preaprueba lo que ejecuta un tick.** loopify imprime los comandos que necesita el loop, como
  `gh pr view` o `git commit`. Añádelos a tu allowlist antes de pegar la línea. Si un tick se
  encuentra con un permission prompt, se queda esperando ahí hasta que alguien responda.
- **Todo loop termina a los 7 días.** Es una regla de Claude Code para el trabajo programado, en los
  dos modos. Vuelve a pegar la línea y el loop retoma donde diga el brief.
- **Para detenerlo antes**, pulsa `Esc` mientras un loop de ritmo propio espera, o di "cancela el
  job pr-babysitter" para uno fijo. Pregunta "¿qué tareas programadas tengo?" para confirmar que ya
  no está.

> [!IMPORTANT]
> Que un loop esté corriendo no es prueba de que esté haciendo lo correcto — lee el registro de
> ticks. Nada juzga un `/loop`; la checklist por tick del brief y `TICKS.md` son la única prueba
> que existe. El loop se ejecuta dentro de la sesión de Claude Code en la que lo pegaste: solo se
> dispara mientras esa sesión está abierta. Todo loop se detiene a los 7 días; vuelve a pegar la
> línea.

## Más información

- [Guía rápida](https://github.com/Aboudjem/loopify/blob/main/docs/quickstart.md) — tu primer loop
  paso a paso, otras formas de instalarlo, y cómo ejecutar un loop sin tener una terminal abierta
- [Un ejemplo resuelto](https://github.com/Aboudjem/loopify/blob/main/examples/sample-loop-brief.md)
  — un brief completo para el trabajo de la PR de release, con la línea al final
- [Límites honestos](https://github.com/Aboudjem/loopify/blob/main/docs/limits.md) — todo lo que
  loopify no promete, cada uno rastreado hasta el binario de Claude Code o su documentación
- [Otros agentes](https://github.com/Aboudjem/loopify/blob/main/docs/other-agents.md) — el mismo
  brief bajo Kimi, Copilot CLI, Cursor, Qwen Code, Hermes, Goose, y cron a secas
- [FAQ](https://github.com/Aboudjem/loopify/blob/main/docs/faq.md) ·
  [El puntero `loop.md`](https://github.com/Aboudjem/loopify/blob/main/docs/loop-md.md) ·
  [Registro de cambios](https://github.com/Aboudjem/loopify/blob/main/CHANGELOG.md) ·
  [Contribuir](https://github.com/Aboudjem/loopify/blob/main/CONTRIBUTING.md) ·
  [La skill en sí](https://github.com/Aboudjem/loopify/blob/main/skills/loopify/SKILL.md)

Si has usado [goalify](https://github.com/Aboudjem/goalify), esto te resultará familiar. goalify es
para un trabajo que termina: una tarea grande, una definición de terminado, `/goal`. loopify es para
un trabajo que se repite. Mismo autor, misma costumbre de escribir primero las pruebas, misma
honestidad sobre lo que la herramienta no puede prometer.

---

<sub>Creado por <a href="https://github.com/Aboudjem">Adam Boudjemaa</a> · MIT. El comportamiento de
`/loop` se ha vuelto a derivar del binario de Claude Code 2.1.252 tal como se distribuye y de la
documentación oficial, 2026. Hermano de
<a href="https://github.com/Aboudjem/goalify">goalify</a>, que hace lo mismo para `/goal`.
<a href="https://github.com/Aboudjem/loopify/issues">¿Ves un hueco?</a></sub>
