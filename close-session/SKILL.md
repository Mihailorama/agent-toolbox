---
name: close-session
description: Close a Claude Code or Codex session end to end. Save open threads, client facts, content ideas, decisions, playbooks and agent lessons to their folders in the repository, verify and commit only the work this session owns, integrate it through the repository's own workflow, push, remove only clean merged session branches and worktrees, and end with a short report. Use when the user says "close session", "wrap up", "finalize", "commit and push", "merge and clean up", "закрой сессию", "заверши сессию", "закоммить и запушь", "подведи итоги", or any equivalent end-of-session request.
---

# Close Session

Finish the session, do not describe how to finish it. The closeout request authorizes normal
documentation edits, verification, commit, push, integration, and removal of clean merged branches
or worktrees created for this work. It does not authorize production changes, outbound messages or
publication, history rewrites, force deletion, cleanup outside the session's scope, or disposal of
work whose ownership or merge state is unclear.

Keep a checklist of the steps below (use the agent's todo or plan tool when it has one, otherwise a
numbered list in the response). End with every item done or explicitly blocked.

## 1. Establish the repository and what this session owns

- Read the repository's agent instructions (`CLAUDE.md`, `AGENTS.md`, contributing and release docs).
- Resolve the repository root, current branch, remote, the remote's default branch (do not assume
  `main`), and all linked worktrees:

  ```bash
  git status --short
  git diff --stat; git diff --cached --stat
  git log --oneline -10
  git branch -vv
  git worktree list --porcelain
  git remote show origin | grep 'HEAD branch'
  ```

- Reconstruct which changes this session made, from the conversation and the diffs. Everything else
  (pre-existing edits, files from another agent or the user) is not yours: leave it untouched.
- Before switching, resetting, or rebasing a shared checkout, branch, or worktree, establish that
  this session owns it. If you cannot, leave it in place and report the exact ambiguity.

## 2. Leave a durable trace

Before committing, update the project's own records where this session made them stale.

- Record each substantial unfinished thread (a real bug, an edge case, a deferred fix, a follow-up
  check) in the project's tracker or TODO file. Each item states what it is, why it matters, the
  affected file or symptom, and the next step or unblock condition.
- Mark items this session actually finished as done. Remove obsolete claims only on evidence from
  this session.
- Do not invent filler items. If nothing substantial remains, say so in the report.
- Do not write to an external tracker unless the repository instructions say this project uses it.
  Where an item and the code both exist, link them both ways (the item names the file, a comment or
  doc names the item).
- Update docs (README, architecture notes, changelogs) that this session's change made wrong.
- Keep evidence out of Git unless the repository stores it there: screenshots, recordings, raw logs,
  dumps, scans. Put them where the project keeps evidence and link them. If evidence was committed by
  mistake, first make and verify one copy in the right place, update and re-read every reference,
  and only then remove the Git copy. Never delete the only copy.
- Before moving or deleting any file, grep the whole working tree, including other people's
  uncommitted edits, for links to it.

## 3. Harvest: fill the ledger

Review the whole session, not only the last problem, for anything with value beyond the immediate
deliverable. The review is mandatory even when no loose ends remain. Everything goes into the
repository the skill runs in, one place per direction:

- Use the folder or file the repository already has for that purpose (check its instructions,
  index files, and existing layout first).
- Create the default below only when nothing exists for that direction.
- Keep one place per direction. Improve the existing entry instead of writing a near-duplicate, and
  link from an index when the folder has one.

| Direction | What goes there | Default path |
|---|---|---|
| Open threads | unfinished work, bugs, follow-ups, blockers | `TODO.md` |
| Clients and deals | who was contacted, what was agreed, deal status, next step and date, objections, the customer's own wording | `clients/<name>.md` |
| Content | ideas, post or article seeds, quotable cases, measured results worth telling | `content/ideas/` |
| Back office | company admin, vendors, contracts, accounts, infrastructure facts | `back-office/` |
| Product and strategy | decisions taken, options rejected and why, priorities, pricing or positioning choices | `docs/decisions/` |
| Engineering knowledge | architecture facts, gotchas, recovery procedures, playbooks, benchmarks | `docs/playbooks/` |
| Agent rules and skills | how an agent should act next time, user corrections, reusable workflows | `AGENTS.md` or `CLAUDE.md`, `.claude/skills/` |
| Personal and other | anything durable that fits none of the above | `notes/` |

### What is worth saving

- a non-obvious verified fact, decision rule, or recurring pattern;
- a repeatable process, checklist, command sequence, prompt, script, or template;
- a failure mode, recovery path, operational gotcha, or useful boundary condition;
- a client fact: agreement, objection, exact customer phrasing, next step;
- a source-backed event or market or technology signal, or a timely content hook;
- a content thesis, example, story, or measured result that would make a future piece stronger;
- a correction from the user about how the agent should behave.

Skip one-off commands, facts already written down correctly, anything unverified, and anything too
context-dependent to be worth maintaining. "No time", "the code is already committed", and "the
README already mentions it" are not skip reasons.

### Preserve usefulness, not just a lesson

- Lead with the strongest verified result of the session, not the last incident.
- For a technical extraction keep the problem, the tools actually used, the method, the measured
  benefit, why it matters, and its limits or transfer conditions.
- Keep numbers whole: before and after values, units, what exactly was measured, scope and sample
  size, source, and the date verified. Compute ratios from those values. Keep stage time, summed job
  time, end-to-end time, and throughput apart. Label targets and projections as unproven.
- Separate time saved or capacity freed from actual money saved, and keep the assumptions next to any
  money estimate.
- Record which model or tool did the work only when the run metadata shows it.
- Content carries a reader-facing account of the same value, not a bare link to the engineering note.
  Generalize it: remove names, client details, and restricted data, and keep the useful lesson. Skip
  content for confidentiality only if nothing useful remains after that.

### Agent rules and skills are not optional

When the session shows a repeatable workflow, a correction, a recovery technique, a tool sequence,
or a safety boundary that would change how a future agent acts, write it into the instructions file
or the owning skill, not only into a project note:

1. Reconstruct the proven behavior from the conversation, the commands, the failure, and the
   recovery. Separate evidence from inference and keep authorization limits.
2. Find the owning instruction or skill. Update it when the behavior extends or corrects it; create a
   new skill only for a distinct capability with a clear trigger.
3. When the instructions exist in several files (for example `AGENTS.md` and `CLAUDE.md`), reconcile
   conflicting wording in the same change.
4. For instruction-only changes, review the diff and the links instead of inventing tests.

### Privacy

- Never write credentials, tokens, or keys into any file.
- Before writing client data, deal amounts, or personal details, check whether the repository is
  private (`gh repo view --json visibility`, the hosting settings, or the instructions). If it is
  public or you cannot tell, do not write them; write a generalized note and warn the user.
- Public financial facts about third parties need the entity, a source URL, the metric, the period,
  the currency, and the date verified. Never infer an amount.
- Saving content does not authorize publishing or sending it.

### The ledger

Before verification, write the ledger as one line per direction from the table: `updated` with the
file, `already covered` with the existing file, `nothing` with a one-line reason, or `blocked` with
the exact unblock condition. An unrelated dirty file elsewhere in the checkout is not a reason to
block: stage only your own paths. The session is not closed while any line is blank.

## 4. Verify the deliverable

- Run the smallest complete verification the repository requires for this change: format, lint,
  type check, tests, build, generated-file checks. Use the repository's own entrypoint, and do not
  run the same suite twice under two names.
- Fix failures this session caused. Report failures that existed before, with evidence.
- Do not present old, partial, or unrelated CI runs as proof for the current revision.
- For instruction-only or docs-only changes, review the diff and check that links and paths resolve
  instead of inventing tests.

### Notes and links check

Check the notes this session wrote, using the repository's link checker if it has one, otherwise by
hand:

- every new file is linked from its folder's index or a parent document;
- every link and path this session added resolves;
- links broken or files orphaned before this session are reported, not fixed here.

If the agent keeps a memory directory for this project, list every memory file the session wrote or
changed in the report, one line each, so the user can review and reject them.

### Delivery states

When the change can reach a deployment or stored data, follow the repository's backup, deploy, and
acceptance rules, and check each state separately:

1. the running system is healthy at an exact revision;
2. the change is in every required long-lived branch, including hotfix backports;
3. staging, if any, runs the intended revision and passes its smoke test;
4. the tracker shows the verified state without skipping human acceptance.

A green merge is not a deployment result, and evidence for one state does not prove another. A
hotfix can make production healthy while the branch, staging, or tracker still lag: report that as
"running, delivery incomplete".

### Forms, uploads, and paid batches

- Web forms: tell apart what was typed, saved as a draft, uploaded, submitted, and accepted. Read
  values back after saving or reloading, including zeros. Keep the final receipt and its date. Do not
  click submit again to test a hypothesis, and keep declarations and the final submit behind the
  user's approval when asked. After success, mark preparation files as historical so nobody submits
  them twice.
- Scans and uploads: keep the original untouched, record exactly which derived file was accepted and
  which pages it holds, and check every page before uploading. A successful upload does not prove the
  pages are complete or legible.
- Screenshots during browser work: re-read the current page after any tab switch, and check the image
  itself against the page it claims to show.
- Paid or quota-limited batches: count processed records separately from billed attempts (retries
  cost too), check downstream eligibility before scaling spend, and read back every claimed record.
  A paused process or a saved PID is not a checkpoint: do not signal stale PIDs or resume spending to
  flush results; record the persisted tail and what a clean resume needs.

## 5. Stage and commit deliberately

- Stage explicit session-owned paths. Never `git add -A` or `git add .` in a checkout that holds
  anyone else's changes.
- When one file mixes your lines with another session's lines in the same hunk, do not stage the
  whole file. Stage only your added lines with a zero-context patch:

  ```bash
  git diff -U0 -- TODO.md | python3 <skill-dir>/references/partial-stage.py 'TODO.md=cache retry|parser fix' > own.patch
  git apply --cached --unidiff-zero own.patch
  ```

  The rule keeps added lines matching the regex. The script refuses hunks with deletions: stage
  those by hand (`git add -p`). Afterwards re-read `git diff --cached`: the other lines must be absent.
- Re-read the staged diff and run `git diff --cached --check` before committing.
- Follow the repository's commit message style. Add a co-author or session footer only when the
  environment supplies its exact value.
- No session-owned change means no commit. Never create an empty commit.

### When a hook fails

A pre-commit or commit-msg hook that fails means the commit did not happen. Read the output, fix the
cause, re-stage, and create the commit again. Do not use `--no-verify`, do not amend an earlier
commit to work around it, and do not disable the hook. If the hook fails on files this session did
not touch, report it as a blocker with the exact output.

## 6. Integrate through the repository's actual workflow

Read the repository instructions and the remote state to find the required path: direct push to the
default branch, pull request, or merge request. Never bypass branch protection or required review.

### Already on the target branch

1. `git fetch`, then pull with rebase if the target moved and your local commits are your own.
2. Push the verified commit.
3. If the push is rejected because the remote moved, fetch and rebase again, re-run the checks that
   the new upstream commits could affect, then push. Never force-push a shared branch.
4. If a rebase stops on conflicts inside another session's unpushed commits, run
   `git rebase --abort` and leave their work alone. Publish only your own commit from a clean
   temporary worktree:

   ```bash
   git worktree add --detach /tmp/close-session-push origin/<target>
   git -C /tmp/close-session-push cherry-pick <your-commit>
   git -C /tmp/close-session-push push origin HEAD:<target>
   git worktree remove /tmp/close-session-push
   ```

   The local branch still holds the same patch, and a later rebase skips it as already applied.
   Report the ahead and behind counts and the conflicting commit for its owner.

### On a feature branch or linked worktree

1. Push the branch first, as a recoverable backup.
2. Refresh the target without touching local work. In a shared dirty checkout do not switch,
   reset, or rebase it; use another clean worktree.
3. Check mergeability against the current target.
4. Open or update the pull or merge request when the repository uses them; otherwise merge normally
   without rewriting history. Resolve conflicts that clearly fall within this session's scope and
   verify the combined result. Ask only when the right result cannot be determined from the
   instructions and both versions, or when resolving would discard someone else's work.
5. Before pushing to an existing request branch, re-read its state. If it was already merged or
   closed, do not recreate the deleted branch: start a new branch from the current target, carry
   only the new commits, and open a new request.
6. Run any required post-merge checks on the exact merged revision, then push.

A released hotfix may be missing from the integration branch while its patch is already there under
another commit. Do not copy the code again. Prove the patches are equal (`git patch-id --stable` on
both), then record the ancestry with `git cherry-pick --keep-redundant-commits -x <hotfix>` and send
that empty commit through the normal review. If they are not exactly equal, do a normal backport.

### When the push fails

- Authentication or permission error: stop, report the exact message and what the user must do.
  Do not switch remotes, accounts, or tokens on your own.
- Protected branch or required review: open the pull or merge request instead.
- Rejected by a server hook or required check: read the reason, fix it if it is in scope,
  otherwise report it. Keep the local commit; it is the recoverable state.

## 7. Clean up only what is proven disposable

Remove a branch or worktree only when all of these hold:

- this session created it or was explicitly given it;
- its worktree is clean, untracked files included (`git -C <path> status --short` is empty);
- its tip is reachable from the target (`git merge-base --is-ancestor <branch> origin/<target>`),
  or the provider confirms the exact request was merged at that revision;
- it is not the active checkout and nobody else uses it;
- no open request, deployment, or review depends on it.

If the provider rebased the branch while a clean worktree still holds the old tip, the staged diff
that appears is not automatically disposable. Reset it to the new tip only when the index equals the
old tip, the worktree equals the index, and the provider confirms the new tip was merged; otherwise
leave it as ambiguous.

Then remove the exact items:

```bash
git worktree remove <exact-path>
git branch -d <exact-branch>
git push origin --delete <exact-branch>   # only after a confirmed merge, if the repo deletes merged branches
```

Use `git worktree prune` only for entries whose directory is already gone. Do not use force-push,
`reset --hard`, `branch -D`, `worktree remove --force`, or `rm -rf` to make cleanup look finished.
Leave everything else in place and list it in the report.

## 8. Stop and ask before

Unless the request explicitly covered it:

- a push or merge that triggers a production release or deploy;
- a migration, backfill, deletion, or any other change to production data;
- an email, chat message, post, comment, or any other outbound communication;
- a force-push, history rewrite, unmerged branch deletion, dirty worktree removal, or a conflict
  resolution that discards work;
- merging someone else's unreviewed work, or widening the closeout beyond the session's scope.

Authentication failures, protected-branch rejections, failing required checks, and unclear
ownership are also stop points. Keep the recoverable state and name the exact unblock action
instead of weakening a safety check.

## 9. Report

Before reporting, check every repository you touched: branch and upstream are explicit, no
unreported session changes remain, local and remote revisions match after the push (or the
divergence is stated), the verification ran on the committed revision, every ledger line is filled,
and every removal passed the checks in step 7.

Then report briefly, outcome first:

- what shipped and why: commit, branch, remote, pull or merge request;
- verification actually run and its result;
- tracker or TODO entries added or closed, or "no open threads";
- the ledger, one line per direction, as written in step 3;
- a short preview (3-6 sentences) of any content created: angle, method, strongest verified figure,
  main caveat, and whether it is a seed or a draft. The preview does not authorize publishing;
- branches and worktrees removed;
- what was deliberately left untouched (other sessions' files, ambiguous branches, failing checks),
  each with the concrete action needed;
- the next step only when something is blocked or deferred.

If any of these is unknown, the session is not closed: resolve it or report the closeout as blocked.
