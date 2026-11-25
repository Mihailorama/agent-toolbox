---
name: close-session
description: Close a Claude Code or Codex session end to end. Save open threads and reusable lessons to the project's notes or TODO, verify and commit only the work this session owns, integrate it through the repository's own workflow, push, remove only clean merged session branches and worktrees, and end with a short report. Use when the user says "close session", "wrap up", "finalize", "commit and push", "merge and clean up", "закрой сессию", "заверши сессию", "закоммить и запушь", "подведи итоги", or any equivalent end-of-session request.
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
- Update docs (README, architecture notes, changelogs) that this session's change made wrong.
- Do not commit screenshots, recordings, logs, or dumps unless the repository stores them in Git.
- Before moving or deleting any file, grep the whole working tree, including other people's
  uncommitted edits, for links to it.

## 3. Harvest reusable lessons

Review the whole session, not only the last problem, for anything a future session would want:

- a non-obvious verified fact, decision rule, or gotcha;
- a repeatable procedure, command sequence, prompt, or script;
- a failure mode and the recovery that actually worked;
- a correction from the user about how the agent should behave.

For each, find where it belongs and improve the existing entry instead of writing a near-duplicate:

- agent behavior (how to act next time) goes into the agent instructions file or the owning skill;
- project knowledge goes into the project's notes, docs, or knowledge file;
- nothing goes into private agent memory unless the user asked for it.

Capture the evidence, why it matters, the procedure, its limits, and when it was verified. Skip
one-off commands, facts already written down correctly, and anything unverified. Never copy
credentials, customer data, or personal details into shared notes. Record what you harvested or
why you skipped it; the report lists both.

## 4. Verify the deliverable

- Run the smallest complete verification the repository requires for this change: format, lint,
  type check, tests, build, generated-file checks. Use the repository's own entrypoint.
- Fix failures this session caused. Report failures that existed before, with evidence.
- Do not present old, partial, or unrelated CI runs as proof for the current revision.
- If the change can affect a deployment or stored data, follow the repository's backup, deploy, and
  acceptance rules. A green merge is not a deployment result.
- For instruction-only or docs-only changes, review the diff and check that links and paths resolve
  instead of inventing tests.

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
divergence is stated), and the verification ran on the committed revision.

Then report briefly, outcome first:

- what shipped and why: commit, branch, remote, pull or merge request;
- verification actually run and its result;
- tracker or TODO entries added or closed, or "no open threads";
- lessons harvested and where, or why none;
- branches and worktrees removed;
- what was deliberately left untouched (other sessions' files, ambiguous branches, failing checks),
  each with the concrete action needed;
- the next step only when something is blocked or deferred.

If any of these is unknown, the session is not closed: resolve it or report the closeout as blocked.
