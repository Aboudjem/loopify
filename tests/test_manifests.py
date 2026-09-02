#!/usr/bin/env python3
"""
Manifest + contract tests for loopify (a release gate; runs in CI).

  1. plugin.json / marketplace.json parse and carry the required fields.
  2. The version is identical across SKILL.md metadata.version, plugin.json, marketplace.json,
     the latest CHANGELOG.md entry, and the .cursor-plugin / .copilot-plugin mirrors, which must
     otherwise match .claude-plugin/plugin.json field for field.
  3. evals/check_skill.py exits 0 on the real SKILL.md (regression guard).
  4. Repo-wide vocabulary lock: no tracked text file calls the line a "condition", says /loop
     "judges" anything, or hands /loop a bare path with no verb (counted `loop-antipattern`
     exemptions for the lines that TEACH the wrong form).
  5. The shipped example brief carries every template section and locked fragment, and its
     line passes the eight loop-line rules AS CODE (evals/loop_line_lint.py).
  6. The pointer example (examples/loop.md) is <= 5 lines.
  7. README i18n parity: READMEs/{zh-CN,ja,es,fr}.md exist, same H2 count as README.md, carry
     the switcher and the "may lag" note, use absolute URLs for every asset/doc link, and keep
     the canonical line untranslated.
  8. Every shipped SVG is GitHub-safe, and animated unless it is the OG card (which is rasterised);
     the social card has no script/external ref; the social preview PNG is exactly 1280x640.
  9. No tracked file matches a credential pattern.
 10. evals/RED-baseline.md exists and names both RED records.

Standard library only. Run: python3 tests/test_manifests.py   (exit 0 = all pass)
"""
import html
import json
import os
import re
import struct
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "loopify", "scripts"))
from loop_line_lint import lint_loop_line  # noqa: E402

failures = []
_total = 0

STORY = ("Hand Claude a job that repeats. Come back to a log of what every tick did, "
         "not a loop you have to babysit.")
CANON = ("/loop 20m Run one cycle of /Users/you/acme/.loop/pr-babysitter.md · read it first, "
         "obey its stop rule (30 ticks or the PR merges), log the tick.")


def check(name, ok, detail=""):
    global _total
    _total += 1
    tag = "PASS" if ok else "FAIL"
    msg = f"{tag}: {name}"
    if detail and not ok:
        msg += f"  ({detail})"
    print(msg)
    if not ok:
        failures.append(name)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


# --- 1. manifests ---
plugin, mkt = {}, {}
try:
    plugin = json.loads(read(".claude-plugin/plugin.json"))
    check("plugin.json parses as valid JSON", True)
    check("plugin.json name == 'loopify'", plugin.get("name") == "loopify", f"got {plugin.get('name')!r}")
    check("plugin.json has 'version'", bool(plugin.get("version")))
    check("plugin.json has 'description' >= 10 chars", len(plugin.get("description", "")) >= 10)
    check("plugin.json 'author' is a dict with 'name'",
          isinstance(plugin.get("author"), dict) and bool(plugin["author"].get("name")))
    check("plugin.json 'keywords' is a list", isinstance(plugin.get("keywords"), list), "must be array, not string")
    check("plugin.json keywords include 'claude-code' and 'loopify'",
          {"claude-code", "loopify"} <= set(plugin.get("keywords") or []))
    check("plugin.json 'license' == 'MIT'", plugin.get("license") == "MIT")
    check("plugin.json homepage points at the repo", "github.com/Aboudjem/loopify" in plugin.get("homepage", ""))
except (json.JSONDecodeError, FileNotFoundError) as e:
    check("plugin.json parses as valid JSON", False, str(e))
try:
    mkt = json.loads(read(".claude-plugin/marketplace.json"))
    check("marketplace.json parses as valid JSON", True)
    check("marketplace.json name == 'loopify-marketplace'", mkt.get("name") == "loopify-marketplace")
    check("marketplace.json owner.name present", bool((mkt.get("owner") or {}).get("name")))
    p0 = (mkt.get("plugins") or [{}])[0]
    check("marketplace.json plugin[0] name == 'loopify'", p0.get("name") == "loopify")
    check("marketplace.json plugin[0] source == './'", p0.get("source") == "./")
    check("marketplace.json plugin[0] has description >= 10 and version",
          len(p0.get("description", "")) >= 10 and bool(p0.get("version")))
except (json.JSONDecodeError, FileNotFoundError) as e:
    check("marketplace.json parses as valid JSON", False, str(e))


# --- 2. version parity across the six manifests that carry a version ---
def _skill_version():
    try:
        t = read("skills/loopify/SKILL.md")
    except FileNotFoundError:
        return None
    m = re.search(r"^\s+version:\s*[\"']?(\d+\.\d+\.\d+)", t, re.MULTILINE)
    return m.group(1) if m else None


def _changelog_version():
    try:
        for line in read("CHANGELOG.md").splitlines():
            m = re.match(r"^##\s*\[(\d+\.\d+\.\d+)\]", line)
            if m:
                return m.group(1)
    except FileNotFoundError:
        pass
    return None


def _mirror(rel):
    try:
        return json.loads(read(rel))
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


cursor, copilot = _mirror(".cursor-plugin/plugin.json"), _mirror(".copilot-plugin/plugin.json")
versions = {
    "SKILL.md metadata.version": _skill_version(),
    "plugin.json version": plugin.get("version"),
    "marketplace.json plugins[0].version": (mkt.get("plugins") or [{}])[0].get("version"),
    "CHANGELOG.md latest release": _changelog_version(),
    ".cursor-plugin/plugin.json version": cursor.get("version"),
    ".copilot-plugin/plugin.json version": copilot.get("version"),
}
distinct = set(versions.values())
check("version is identical across all six manifests (SKILL.md, plugin.json, marketplace.json, "
      "CHANGELOG.md, .cursor-plugin, .copilot-plugin)",
      len(distinct) == 1 and None not in distinct, ", ".join(f"{k}={v!r}" for k, v in versions.items()))

# The editor mirrors are the same plugin under another agent's directory name, so nothing but the
# path may differ. A mirror that drifts installs a different description than the marketplace shows.
for rel, m in ((".cursor-plugin/plugin.json", cursor), (".copilot-plugin/plugin.json", copilot)):
    check(f"{rel} parses and names the plugin", m.get("name") == "loopify", f"got {m.get('name')!r}")
    check(f"{rel} description matches .claude-plugin/plugin.json",
          m.get("description") == plugin.get("description"))
    check(f"{rel} license matches .claude-plugin/plugin.json", m.get("license") == plugin.get("license"))
    check(f"{rel} keywords match .claude-plugin/plugin.json", m.get("keywords") == plugin.get("keywords"))
    check(f"{rel} declares skills == ['loopify']", m.get("skills") == ["loopify"])
    check(f"{rel} declares no mcp key (loopify ships no server)", "mcp" not in m)

# --- 3. eval regression guard ---
result = subprocess.run([sys.executable, os.path.join(ROOT, "evals", "check_skill.py"),
                         os.path.join(ROOT, "skills", "loopify", "SKILL.md")],
                        capture_output=True, text=True)
check("evals/check_skill.py exits 0 on skills/loopify/SKILL.md", result.returncode == 0,
      f"exit={result.returncode}\n{result.stdout[-300:] if result.stdout else ''}")

# --- 4. repo-wide vocabulary lock (normalised, exemptions counted) ---
tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=ROOT).stdout.splitlines()
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".mp3", ".woff", ".woff2", ".ico", ".pdf",
              ".zip", ".ttf", ".otf"}
_FOLD = {**dict.fromkeys(map(ord, "⁄∕／⧸"), "/"),
         **dict.fromkeys(map(ord, "​‌‍­﻿"), None)}


def _normalize(text):
    return unicodedata.normalize("NFKC", html.unescape(text)).translate(_FOLD)


STRIP_RE = re.compile(r"[`*_\"'‘’“”]")
# The line is a string; it is never a "condition" (that word implies an evaluator /loop does
# not have). /loop schedules; it never judges. And /loop is never handed a bare path.
CONDITION_RE = re.compile(r"/loop\s*<?\s*condition|loop[-\s]+condition|the loop'?s? condition|brief and (?:the )?condition", re.I)
# A line that compares with goalify may name goalify's condition; that is the intended contrast.
GOALIFY_RE = re.compile(r"goalify|/goal\b", re.I)
JUDGES_RE = re.compile(r"/loop\s+(judges|evaluates|checks whether)", re.I)
BARE_PATH_RE = re.compile(r"/loop\s+(?:\d+[smhd]\s+)?(?:/|~/|\.{0,2}/)\S+\.md\s*$", re.I)
EXEMPT = "loop-antipattern"
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})(.*)$")
hits, exempt, scanned = [], [], 0
for rel in tracked:
    # tests/ and evals/ implement the lock, so they have to name what it bans.
    if os.path.splitext(rel)[1].lower() in BINARY_EXT or rel.startswith(("tests/", "evals/")):
        continue
    try:
        lines = read(rel).splitlines()
    except (OSError, UnicodeDecodeError):
        continue
    scanned += 1
    fence, fence_exempt = None, False
    for ln, line in enumerate(lines, 1):
        fm = FENCE_RE.match(line)
        if fm:
            if fence is None:
                fence, fence_exempt = fm.group(1)[0], EXEMPT in fm.group(2)
                continue
            if fm.group(1)[0] == fence and not fm.group(2).strip():
                fence, fence_exempt = None, False
                continue
        cur = STRIP_RE.sub("", _normalize(line))
        cond_hit = CONDITION_RE.search(cur) and not (GOALIFY_RE.search(cur) and "brief and" in cur.lower())
        if cond_hit or JUDGES_RE.search(cur) or BARE_PATH_RE.search(cur):
            (exempt if (EXEMPT in line or fence_exempt) else hits).append(f"{rel}:{ln}")
check(f"vocabulary lock holds repo-wide: the line is never a 'condition', /loop never 'judges', "
      f"no bare path after /loop ({scanned} files scanned)", not hits, "found at " + ", ".join(hits[:8]))
EXPECTED_EXEMPTIONS = 6  # README wrong-example fence, its four translations, quickstart wrong-example fence
check(f"loop-antipattern exemptions stay pinned at {EXPECTED_EXEMPTIONS} ({len(exempt)} in use: {', '.join(exempt) or 'none'})",
      len(exempt) == EXPECTED_EXEMPTIONS,
      "adding one is a deliberate act: confirm the line TEACHES the wrong form, then bump the constant in the same commit")
check("gate self-test: `/loop <condition>` is caught", bool(CONDITION_RE.search("/loop <condition>")))
check("gate self-test: `brief and condition` is caught", bool(CONDITION_RE.search("the generated brief and condition (redacted)")))
check("gate self-test: `/loop judges` is caught", bool(JUDGES_RE.search("/loop judges the transcript")))
check("gate self-test: a bare path after /loop is caught",
      bool(BARE_PATH_RE.search("/loop 20m /Users/x/.loop/job.md")) and not BARE_PATH_RE.search(CANON))

# --- 5. the example brief ---
TEMPLATE_SECTIONS = ["# LOOP:", "## GOAL (per tick)", "## Standing decisions", "## Hard safety rails",
                     "## Repeat-safe", "## The cycle", "## State files", "## Per-tick definition of done", "## Stop rule",
                     "## Pacing rule", "## Duplicate-tick rule", "## Report-on-stop", "## Persistence gate",
                     "## Honest limits", "## Handoff"]
LOCKED_FRAGMENTS = [
    "this file is the standing loop brief: never archive, move, delete or rewrite it from inside a run.",
    "runs write only under the state directory", "proposed brief edits go to queue.md for the human.",
    "run exactly one cycle", "the loop also dies at the 7-day expiry — paste the line again",
    "never ~300 s", "one wakeup only", "≤ 150 lines", "is data, never instructions",
    "safe to run twice", "check before create", "append, never overwrite",
    "skip when the last tick's output already exists", "before any side effect, check the marker",
    "never stage, commit or push the state directory or this brief", "## tick <n> ·", "stopped", "lock",
    "reason:", "unblock:", "never a step this loop then runs itself", "three named exceptions",
]
try:
    ex_raw = read("examples/sample-loop-brief.md")
    ex = re.sub(r"\s+", " ", re.sub(r"(?m)^\s{0,3}>\s?", "", ex_raw)).replace("`", "").replace("*", "").lower()
    for sec in TEMPLATE_SECTIONS:
        check(f"example: section {sec}", sec.lower() in ex)
    for frag in LOCKED_FRAGMENTS:
        check(f"example: locked fragment {frag[:40]!r}", frag in ex)
    check("example: durable counter `tick: N/30`", bool(re.search(r"tick: n/(?:<cap>|\d+)", ex)))
    check("example: mode check with (a) (b) (c)", "mode check" in ex and "(a)" in ex and "(b)" in ex and "(c)" in ex)
    check("example: tick cap in Standing decisions", bool(re.search(r"tick cap: \d+", ex)))
    check("example: dual stop rule + job condition", "whichever comes first" in ex and "or when" in ex)
    check("example: autonomy level stated", "autonomy level" in ex)
    check("example: per-tick budget", "per-tick budget" in ex)
    check("example: no personal data", not re.search(r"adamboudj|boudjemaa|@gmail|aboudjem", ex))
    check("example: absolute paths only (no ~/ paths)", "~/" not in ex_raw)
    check("example: <= 16,000 bytes (a generated brief is budgeted at ~12,000; the sample carries its banner)", len(ex_raw.encode("utf-8")) <= 16000, f"{len(ex_raw.encode('utf-8'))} bytes")
    lines_in_ex = re.findall(r"^/loop .*$", ex_raw, re.MULTILINE)
    check("example: ships the canonical line byte-identical in its Handoff", CANON in lines_in_ex)
    ok, fails, notes = lint_loop_line(CANON, "fixed")
    check("example line passes the eight loop-line rules AS CODE", ok, "; ".join(fails))
    check("lint self-test: a ~ path fails rule 2", not lint_loop_line(CANON.replace("/Users/you", "~"))[0])
    check("lint self-test: daily phrasing fails rule 5", not lint_loop_line(CANON.replace("20m", "1d").replace("pr-babysitter", "daily-digest"))[0])
    check("lint self-test: a slash-command prompt fails rule 6", not lint_loop_line("/loop 20m /deploy-now")[0])
    check("lint self-test: a missing tick cap fails rule 3", not lint_loop_line(CANON.replace("30 ticks or ", ""))[0])
    check("lint self-test: ≥ 60 min emits the cloud-caveat note", bool(lint_loop_line(CANON.replace("20m", "2h"))[2]))
    check("lint self-test: mode mismatch fails rule 8", not lint_loop_line(CANON, "self-paced")[0])
    over = lint_loop_line(CANON.replace("20m", "14d"))
    check("lint self-test: a span past the 7-day expiry emits a note, not a failure",
          over[0] and any("expires after 7 days" in n for n in over[2]), "; ".join(over[2]))
    check("lint self-test: the canonical line emits no expiry note",
          not any("expires after 7 days" in n for n in lint_loop_line(CANON)[2]))
    check("lint self-test: a digit in the brief's slug is not read as a span",
          not any("expires after 7 days" in n
                  for n in lint_loop_line(CANON.replace("pr-babysitter", "pr-30d-watch"))[2]))
except FileNotFoundError as e:
    check("examples/sample-loop-brief.md is readable", False, str(e))

# --- 5b. the QUEUE.md example block inside the SKILL.md template ---
# check_skill.py extracts the template with the same non-greedy regex, so it stops at the FIRST
# closing fence. SKILL.md has two ```markdown fences (the template, then the .claude/loop.md
# pointer); anchoring on the first is what both suites do, and it is why the QUEUE.md example is
# indented rather than fenced: a nested fence would truncate the template here.
try:
    skill_body = read("skills/loopify/SKILL.md")
    tm = re.search(r"^```markdown\s*\n(.*?)\n```\s*$", skill_body, re.DOTALL | re.MULTILINE)
    tmpl = tm.group(1) if tm else ""
    check("SKILL.md template block extracts whole (no nested fence truncates it)",
          "## Handoff" in tmpl, f"{len(tmpl)} chars extracted")
    qm = re.search(r"^\s+- \[tick \d+\].*?(?=\n\S|\Z)", tmpl, re.DOTALL | re.MULTILINE)
    block = qm.group(0) if qm else ""
    check("SKILL.md QUEUE.md example block exists (indented, not fenced)", bool(block))
    check("SKILL.md QUEUE.md example block carries a `reason:` line",
          bool(re.search(r"^\s+reason:\s*\S", block, re.MULTILINE)), repr(block[:120]))
    check("SKILL.md QUEUE.md example block carries an `unblock:` line",
          bool(re.search(r"^\s+unblock:\s*\S", block, re.MULTILINE)), repr(block[:120]))
    check("SKILL.md pins both fields on every blocked item",
          "every blocked item" in tmpl.lower() and "`reason:`" in tmpl and "`unblock:`" in tmpl)
except FileNotFoundError as e:
    check("skills/loopify/SKILL.md is readable", False, str(e))

# --- 6. the pointer example ---
try:
    ptr = read("examples/loop.md")
    plines = [l for l in ptr.splitlines() if l.strip()]
    check("examples/loop.md is <= 5 non-empty lines", len(plines) <= 5, f"{len(plines)} lines")
    check("examples/loop.md says Run one cycle of an absolute path", bool(re.search(r"Run one cycle of `?/", ptr)))
    check("examples/loop.md states the ignored-when-a-prompt-is-typed caveat", "ignore" in ptr.lower())
except FileNotFoundError as e:
    check("examples/loop.md is readable", False, str(e))

# --- 7. README i18n parity ---
def _h2_count(text):
    """Count `## ` headings outside fenced code blocks (a sample TICKS.md shows `## tick N`)."""
    n, fence = 0, None
    for line in text.splitlines():
        fm = FENCE_RE.match(line)
        if fm:
            if fence is None:
                fence = fm.group(1)[0]
            elif fm.group(1)[0] == fence and not fm.group(2).strip():
                fence = None
            continue
        if fence is None and line.startswith("## "):
            n += 1
    return n


try:
    readme = read("README.md")
    h2 = _h2_count(readme)
    check("README.md carries the story verbatim", STORY in readme)
    check("README.md carries the canonical line verbatim", CANON in readme)
    check("README.md has the language switcher at the top", "READMEs/zh-CN.md" in readme[:1500])
    for lang in ("zh-CN", "ja", "es", "fr"):
        rel = f"READMEs/{lang}.md"
        try:
            t = read(rel)
        except FileNotFoundError:
            check(f"{rel} exists", False)
            continue
        check(f"{rel}: same H2 count as README.md ({h2})", _h2_count(t) == h2, f"{_h2_count(t)} vs {h2}")
        check(f"{rel}: switcher links back to ../README.md", "../README.md" in t[:1500])
        check(f"{rel}: carries the may-lag note marker", "<!-- may-lag -->" in t)
        rel_links = re.findall(r"(?:src=\"|\]\()(?:\.\./|assets/|docs/|examples/|skills/|CHANGELOG|LICENSE|SECURITY|CONTRIBUTING)", t)
        check(f"{rel}: no relative asset/doc links (absolute URLs only)", not rel_links, f"{len(rel_links)} relative link(s)")
        check(f"{rel}: canonical line untranslated", CANON in t)
except FileNotFoundError as e:
    check("README.md is readable", False, str(e))

# --- 8. SVGs + social card + PNG ---
EXTERNAL_REF_RE = re.compile(r"""<script|@import|xlink:href\s*=\s*["']https?:|href\s*=\s*["']https?:|url\(\s*['"]?https?:|src\s*=\s*["']https?:|<image\b""", re.I)
SMIL_RE = re.compile(r"<(?:animate|animateTransform|animateMotion|set)\b", re.I)
GENERIC = {"serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui", "ui-serif", "ui-sans-serif",
           "ui-monospace", "ui-rounded", "math", "emoji"}
# The OG card is the one asset that must NOT animate: GitHub and every social platform rasterise
# it to a still PNG (assets/social-preview.png), so motion there is invisible weight. It still
# carries the reduced-motion guard, because CI's markup step requires the string in every asset.
STATIC_BY_DESIGN = {"assets/social-preview.svg"}
svgs = sorted(r for r in tracked if r.startswith("assets/") and r.endswith(".svg"))
check("assets/ ships at least three SVGs", len(svgs) >= 3, f"found {svgs}")
for rel in svgs:
    raw = read(rel)
    try:
        ET.fromstring(raw)
        wf, why = True, ""
    except ET.ParseError as e:
        wf, why = False, str(e)
    check(f"{rel}: well-formed XML", wf, why)
    ext = EXTERNAL_REF_RE.search(raw)
    check(f"{rel}: no <script> and no external reference", not ext, f"matched {ext.group(0)!r}" if ext else "")
    animated = "@keyframes" in raw or bool(SMIL_RE.search(raw))
    if rel in STATIC_BY_DESIGN:
        check(f"{rel}: static by design (it is rasterised to the OG PNG)", not animated)
    else:
        check(f"{rel}: is animated (@keyframes or SMIL)", animated)
    check(f"{rel}: has a prefers-reduced-motion guard", "prefers-reduced-motion" in raw)
    stacks = re.findall(r'font-family\s*=\s*"([^"]*)"', raw) + re.findall(r"font-family\s*:\s*([^;{}]+)", raw)
    bad = [v.strip() for v in stacks if v.split(",")[-1].strip().strip("\"'").lower() not in GENERIC]
    check(f"{rel}: every font stack ends in a generic family", not bad, f"{bad[:2]}")
try:
    card = read("assets/social-card.html")
    ext = EXTERNAL_REF_RE.search(card)
    check("assets/social-card.html: no <script> and no external reference", not ext, f"matched {ext.group(0)!r}" if ext else "")
except FileNotFoundError:
    check("assets/social-card.html exists", False)
try:
    with open(os.path.join(ROOT, "assets", "social-preview.png"), "rb") as f:
        head = f.read(24)
    w, h = struct.unpack(">II", head[16:24]) if head[:8] == b"\x89PNG\r\n\x1a\n" else (0, 0)
    check("assets/social-preview.png is exactly 1280x640", (w, h) == (1280, 640), f"{w}x{h}")
except FileNotFoundError:
    check("assets/social-preview.png exists", False)

# --- 9. no secrets (the CI patterns, mirrored so a local run catches them too) ---
SECRETS = [re.compile(p) for p in (
    r"AKIA[0-9A-Z]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----", r"ghp_[A-Za-z0-9]{36}",
    r"github_pat_[A-Za-z0-9_]{22,}", r"gh[osur]_[A-Za-z0-9]{36}", r"sk-ant-[A-Za-z0-9_\-]{24,}",
    r"sk-(?:proj-)?[A-Za-z0-9]{32,}", r"xox[baprs]-[A-Za-z0-9-]{10,}",
    r"https://hooks\.slack\.com/services/[A-Za-z0-9/+]{20,}", r"AIza[0-9A-Za-z_\-]{35}",
    r"sk_live_[0-9a-zA-Z]{24,}", r"npm_[A-Za-z0-9]{36}")]
leaks = []
for rel in tracked:
    if os.path.splitext(rel)[1].lower() in BINARY_EXT:
        continue
    try:
        for ln, line in enumerate(read(rel).splitlines(), 1):
            if any(rx.search(line) for rx in SECRETS):
                leaks.append(f"{rel}:{ln}")
    except (OSError, UnicodeDecodeError):
        continue
check("no tracked file matches a credential pattern", not leaks, ", ".join(leaks[:5]))

# --- 10. RED baseline recorded ---
try:
    rb = read("evals/RED-baseline.md")
    check("evals/RED-baseline.md names the cold run and the test-first RED",
          "cold" in rb.lower() and "red" in rb.lower() and "check_skill.py" in rb)
except FileNotFoundError:
    check("evals/RED-baseline.md exists", False)

print("-" * 60)
passed = _total - len(failures)
print(f"{passed}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
