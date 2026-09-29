# High-Assurance Closeout

Read this reference only when the task involves sensitive content, public release, hard-to-reverse publication, delegated or cross-session production, or finalization after a long or compacted conversation. The main SKILL.md workflow is sufficient for routine document iteration.

This guidance governs document hygiene. It does not grant permission to publish, send, delete, or modify external systems; follow the user's authorization and the host's approval requirements.

## Authoritative baseline

Choose an authoritative baseline separately for each deliverable surface:

- Repository changes: the task-start commit or merge base.
- Release statements: the released version.
- Document edits: the version confirmed by the user.

Record the baseline and its scope. If trusted sources conflict, mark the affected state unknown until the conflict is resolved. Do not treat an incomplete search as proof of absence.

Assistant drafts and temporary edits are conversation history. Completed publication, upload, deletion, or migration is an audit fact even if later rolled back; do not erase it to make a deliverable look clean.

## Clean-context production

When asking a fresh session or delegated producer to write the document, provide a clean specification instead of the conversation history:

- Positive goal: what the final design must do.
- Accepted baseline facts and observed state.
- Required facts and intended audience for each deliverable.
- Required format and allowed output files.

Keep the rejected-option list with the reviewer, not the producer. If an exclusion must be shared, minimize it and assume it could leak into the output.

If the host cannot provide genuinely isolated context, produce from the clean specification in the current context and describe the isolation as best-effort.

## Freeze, execute, read back, and recheck

1. **Freeze:** Render or capture each deliverable before an external action; record the audience and baseline.
2. **Execute:** Use the reviewed content as-is after the user has authorized the external action. Do not regenerate outbound text during the action.
3. **Read back:** Inspect the actual result, including files rewritten by hooks or platform-generated wrappers.
4. **Recheck:** Run the main skill's semantic review and exact-term scan on every readable final artifact. Draft any delivery summary from the read-back result.

Any later edit invalidates the affected checks. Recheck after changes. If two repair rounds leave a material ambiguity, ask the user; do not present failed, unreadable, or unverified content as clean.
