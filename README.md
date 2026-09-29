# Design Doc Snapshot

**Baseline-aware rewrites for iterated design documents.**

Design Doc Snapshot turns an iterated design document into a clean, independently readable final-state document. It removes rejected-option residue while preserving real removals, changes, dependencies, and compatibility facts.

The skill instructions and package documentation are in English. Generated deliverables should remain in the language requested by the user or used by the source document.

## Use it when

- Design alternatives have been explored and the decisions have converged.
- A full rewrite should describe the final design without relying on draft or chat history.
- You need to audit a design document for rejected-option residue across prose, filenames, diagrams, and code examples.

For routine proofreading or a small local edit with no design decisions, use a normal editing workflow.

## Install

Copy this directory into a skill root supported by your Codex installation, for example:

- $CODEX_HOME/skills/design-doc-snapshot
- ~/.codex/skills/design-doc-snapshot when CODEX_HOME is unset

A team skill marketplace may require a plugin wrapper or its own manifest. This directory is the portable skill source; add marketplace-specific packaging in the target repository.

## Use

Invoke $design-doc-snapshot and provide the current document, the authoritative pre-request baseline or evidence of current system state, and the accepted final decisions. If trusted sources conflict, or a material fact is unknown, the skill should verify it or ask before presenting an affected conclusion as final.

## Exact-term scanner

The optional scanner checks filenames and supported text files for exact substrings after NFKC normalization and case folding. It does not detect synonyms or semantic rewrites. Review every match. Exit code 0 means supported text content in the requested scope was fully scanned with no exact matches; exit code 1 means a match or incomplete scan; exit code 2 means invalid input.

    python scripts/check_terms.py -t "LegacyAuth,trial-component" path/to/final-document.md

Python 3.10 or later is required. The scanner supports common Markdown, text, source-code, configuration, diagram, and markup formats. It does not inspect PDF, Office files, or image contents; extract or render those artifacts and review their actual contents separately.

## Files

- SKILL.md — workflow, decision matrix, output scope, and self-checks
- agents/openai.yaml — UI display name and default prompt
- scripts/check_terms.py — optional exact-term scanner
- references/high-assurance.md — additional guidance for sensitive, public, delegated, or long-session work

## License

No license is included. Choose and add a LICENSE file that matches the owner's intent and the target repository policy before public release.
