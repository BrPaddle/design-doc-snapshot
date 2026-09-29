# Design Doc Snapshot

**Turn iterated design discussions into clean, baseline-aware design documents.**

Design Doc Snapshot helps rewrite or audit a design document after decisions have converged. It removes residue from rejected options while preserving real changes, removals, dependencies, and compatibility facts.

The skill instructions are written in English. Generated documents should use the language requested by the user or used by the source document.

## What It Does

The skill compares:

- **Baseline:** the authoritative state before the rewrite request.
- **Final design:** the user's confirmed requirements, constraints, and accepted decisions.
- **Exploration history:** options that were considered and rejected.

It uses that comparison to produce a self-contained final document without relying on drafts or chat history.

## Use It When

- Design alternatives have been explored and decisions have converged.
- A complete rewrite should describe the final design.
- You need to check a document for rejected-option residue in prose, tables, diagrams, filenames, or code examples.

For routine proofreading or a small local edit with no design decisions, use a normal editing workflow.

## Compatibility

This skill follows the `SKILL.md` directory format used by the open Agent Skills convention. It can be used with agents that support this format and the resources used by this skill.

Agent products differ in how they discover skills, where they expect skill folders, and whether they allow bundled scripts. Check your agent's documentation for its skills directory and loading behavior.

The `agents/openai.yaml` file provides optional OpenAI/Codex interface metadata. Other agents can ignore it; the core instructions are in `SKILL.md`.

## Install

Clone this repository to your computer:

```bash
git clone https://github.com/BrPaddle/design-doc-snapshot.git
```

Move the cloned `design-doc-snapshot` folder into the skills directory used by your agent. Keep the folder name and its contents together.

The installed layout should look like this:

```text
<agent-skills-directory>/
└── design-doc-snapshot/
    ├── SKILL.md
    ├── README.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   └── high-assurance.md
    └── scripts/
        └── check_terms.py
```

Replace `<agent-skills-directory>` with the skills directory documented by your agent. Do not move only `SKILL.md`; the skill may use the reference and script files alongside it.

Reload or restart the agent if its documentation says newly installed skills must be rediscovered.

To update a cloned installation later, open a terminal in the installed skill folder and run:

```bash
git pull
```

## Quick Start

Use your agent's normal way to select or invoke a skill, then provide:

1. The current design document.
2. The authoritative pre-request baseline, or evidence of the current system state.
3. The accepted final requirements and decisions.
4. The intended audience, format, and requested scope.

If a material fact is unknown or trusted sources conflict, the skill should verify it or ask before presenting the affected content as final.

## Requirements

The core skill instructions have no runtime dependencies.

Python 3.10 or later is required only to run the optional exact-term scanner.

## Exact-Term Scanner

The optional scanner checks filenames and supported text files for exact rejected-term matches. Matching uses Unicode NFKC normalization and case-insensitive substring matching.

```bash
python scripts/check_terms.py \
  -t "LegacyAuth,trial-component" \
  path/to/final-document.md
```

For many terms, put one term per line in a UTF-8 text file:

```bash
python scripts/check_terms.py \
  -f rejected-terms.txt \
  path/to/final-document.md
```

The scanner does not detect synonyms or semantic rewrites. It does not inspect PDF, Office, or image contents; extract or render those files and review their actual contents separately.

| Exit code | Meaning                                                      |
| --------- | ------------------------------------------------------------ |
| `0`       | Supported text files in the requested scope were scanned with no exact matches. |
| `1`       | A match was found or the scan was incomplete.                |
| `2`       | The input or terms file is invalid.                          |

A clean scan does not replace semantic review.

## Package Contents

- `SKILL.md` — workflow, baseline/final decision matrix, and review steps
- `agents/openai.yaml` — optional OpenAI/Codex interface metadata
- `references/high-assurance.md` — additional guidance for sensitive, public, delegated, or long-session work
- `scripts/check_terms.py` — optional exact-term scanner

- references/worked-example.md — a complete end-to-end walkthrough of the workflow

## License

See the repository root's `LICENSE` file for the applicable license terms.
