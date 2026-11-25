"""Stage only your own added lines from files that another session also edited.

Usage (one FILE=REGEX rule per file; an added line is kept when it matches REGEX):
  git diff -U0 -- <files...> | python3 partial-stage.py 'TODO.md=my-feature|cache retry' > own.patch
  git apply --cached --unidiff-zero own.patch
  git diff --cached        # the other session's lines must not appear

Reads a zero-context diff on stdin, writes the filtered patch on stdout, never calls git itself.
Files without a rule are skipped. Hunks with deleted lines are refused: resolve those by hand.
Self-check: python3 partial-stage.py --selftest
"""
import re
import sys


def filter_diff(diff_text, rules):
    out, cur, files = [], None, {}
    for line in diff_text.splitlines():
        if line.startswith('diff --git'):
            cur = line.split(' b/', 1)[1]
            files[cur] = []
        if cur is not None:
            files[cur].append(line)
    for path, lines in files.items():
        rx = rules.get(path)
        if rx is None:
            continue
        header = [l for l in lines if l.startswith(('diff ', 'index ', '--- ', '+++ '))]
        hunks, h = [], None
        for l in lines:
            if l.startswith('@@'):
                h = {'head': l, 'plus': [], 'minus': []}
                hunks.append(h)
            elif h is not None and l.startswith('+') and not l.startswith('+++'):
                h['plus'].append(l)
            elif h is not None and l.startswith('-') and not l.startswith('---'):
                h['minus'].append(l)
        body = []
        for h in hunks:
            if h['minus']:
                sys.exit(f'{path}: hunk has deletions, stage it by hand')
            keep = [l for l in h['plus'] if rx.search(l[1:])]
            if not keep:
                continue
            m = re.match(r'@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', h['head'])
            body.append(f'@@ -{m.group(1)},0 +{m.group(2)},{len(keep)} @@')
            body += keep
        if body:
            out += header + body
    return '\n'.join(out) + '\n' if out else ''


def selftest():
    diff = ('diff --git a/TODO.md b/TODO.md\nindex 1..2 100644\n--- a/TODO.md\n+++ b/TODO.md\n'
            '@@ -3,0 +4,3 @@\n+- mine: fix cache\n+- theirs: other work\n+- mine: add test\n')
    got = filter_diff(diff, {'TODO.md': re.compile('mine')})
    assert '+- theirs' not in got and got.count('+- mine') == 2, got
    assert '@@ -3,0 +4,2 @@' in got, got
    print('selftest ok')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
        sys.exit(0)
    if not sys.argv[1:]:
        sys.exit(__doc__)
    rules = {}
    for arg in sys.argv[1:]:
        path, _, rx = arg.partition('=')
        rules[path] = re.compile(rx)
    sys.stdout.write(filter_diff(sys.stdin.read(), rules))
