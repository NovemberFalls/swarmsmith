#!/usr/bin/env python3
"""swarmsmith coding-v5.0 — installer.

A skill and the tool it invokes are a CONTRACT, not two independent files. v5.0
emits SEARCH/REPLACE blocks in one exact format; the applier parses that format
and applies iff the SEARCH matches exactly once. Ship them apart and they drift —
someone pairs the skill with a hand-rolled applier that force-applies on a fuzzy
match, the deterministic guarantee is gone, and the skill still claims it. The
measured cost of that failure is in FINDINGS.md: a model handed a flawed "exact"
patch scored 8/16, BELOW the same model interpreting the spec at 10/20.

So this package installs both, pinned together, and verifies them by checksum.

    python install.py                # install skill + applier
    python install.py --check        # verify; exit 1 on drift or missing
    python install.py --uninstall    # remove everything it installed
    python install.py --dest DIR     # install somewhere else (testing)

Installs to:
    <claude>/commands/orch-anth-5.0.md   the skill
    <claude>/commands/fix.md             single-issue path
    <claude>/tools/orch-apply/           the applier + its manifest

<claude> is $CLAUDE_CONFIG_DIR, else ~/.claude. Nothing else is touched: this
package registers no hooks and edits no settings.

stdlib only. Python 3.8+. Windows / macOS / Linux.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

VERSION = "5.0.1"
PACKAGE = "coding-v5.0"

HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE_HOME = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(
    os.path.expanduser("~"), ".claude")

COMMANDS = ["orch-anth-5.0.md", "fix.md"]
TOOLS = ["apply_blocks.py"]
TOOLS_SUBDIR = os.path.join("tools", "orch-apply")
MANIFEST_NAME = "MANIFEST.json"
RECEIPT_NAME = "INSTALLED.json"

MIN_PYTHON = (3, 8)


def sha256(path: str) -> str:
    """Checksum with line endings normalized to LF.

    Git rewrites line endings on checkout (this repo pins `text=auto eol=lf`),
    so the same committed file is CRLF on one clone and LF on another. Hashing
    raw bytes would make the manifest platform-dependent: a manifest built on
    Windows fails verification on every Linux clone, and the installer refuses
    to install -- dead on arrival for everyone but the author.

    Normalizing preserves what this checksum is actually for -- detecting
    tampering and drift -- while surviving the checkout that git guarantees.
    Every shipped file is text; EOL is not a property worth failing over.
    """
    with open(path, "rb") as fh:
        data = fh.read()
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def source_files() -> dict[str, str]:
    """Package-relative path -> sha256, for everything this package ships."""
    out = {}
    for name in COMMANDS:
        p = os.path.join(HERE, "commands", name)
        if os.path.exists(p):
            out[f"commands/{name}"] = sha256(p)
    for name in TOOLS:
        p = os.path.join(HERE, "tools", name)
        if os.path.exists(p):
            out[f"tools/{name}"] = sha256(p)
    return out


def load_manifest() -> dict | None:
    p = os.path.join(HERE, MANIFEST_NAME)
    if not os.path.exists(p):
        return None
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def verify_source() -> list[str]:
    """Has the package itself been tampered with since it was built?"""
    manifest = load_manifest()
    if not manifest:
        return ["MANIFEST.json missing or unreadable"]
    expected = manifest.get("files", {})
    actual = source_files()
    problems = []
    for rel, want in sorted(expected.items()):
        if rel not in actual:
            problems.append(f"{rel} (missing from package)")
        elif actual[rel] != want:
            problems.append(f"{rel} (checksum differs from MANIFEST)")
    for rel in sorted(set(actual) - set(expected)):
        problems.append(f"{rel} (present but not in MANIFEST)")
    return problems


def install_paths(dest: str) -> dict[str, str]:
    """Package-relative source -> absolute install target."""
    paths = {}
    for name in COMMANDS:
        paths[f"commands/{name}"] = os.path.join(dest, "commands", name)
    for name in TOOLS:
        paths[f"tools/{name}"] = os.path.join(dest, TOOLS_SUBDIR, name)
    return paths


def install(dest: str = CLAUDE_HOME, force: bool = False) -> dict:
    problems = verify_source()
    if problems and not force:
        # ASCII only in printed output: a Windows console defaults to cp1252 and
        # would mojibake anything else, in the one message a user must read.
        raise SystemExit(
            "install: package integrity check FAILED - refusing to install.\n  "
            + "\n  ".join(problems)
            + "\n  (re-clone the repo, or pass --force if you edited it deliberately)")

    installed, overwritten = [], []
    for rel, target in install_paths(dest).items():
        os.makedirs(os.path.dirname(target), exist_ok=True)
        src = os.path.join(HERE, rel.replace("/", os.sep))
        if os.path.exists(target) and sha256(target) != sha256(src):
            shutil.copy2(target, target + ".bak")
            overwritten.append(os.path.basename(target))
        shutil.copy2(src, target)
        installed.append(rel)

    receipt = {
        "package": PACKAGE,
        "version": VERSION,
        "installed_from": HERE,
        "python": sys.executable,
        "files": {rel: os.path.abspath(t) for rel, t in install_paths(dest).items()},
        "checksums": source_files(),
    }
    receipt_path = os.path.join(dest, TOOLS_SUBDIR, RECEIPT_NAME)
    os.makedirs(os.path.dirname(receipt_path), exist_ok=True)
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2, sort_keys=True)

    return {"dest": dest, "installed": installed, "overwritten": overwritten,
            "receipt": receipt_path}


def check(dest: str = CLAUDE_HOME) -> dict:
    src_problems = verify_source()
    missing, drifted = [], []
    for rel, target in install_paths(dest).items():
        src = os.path.join(HERE, rel.replace("/", os.sep))
        if not os.path.exists(target):
            missing.append(rel)
        elif os.path.exists(src) and sha256(target) != sha256(src):
            drifted.append(rel)
    return {
        "dest": dest,
        "package_problems": src_problems,
        "missing": missing,
        "drifted": drifted,
        "ok": not (src_problems or missing or drifted),
    }


def uninstall(dest: str = CLAUDE_HOME) -> dict:
    removed = []
    for rel, target in install_paths(dest).items():
        if os.path.exists(target):
            os.remove(target)
            removed.append(rel)
    receipt = os.path.join(dest, TOOLS_SUBDIR, RECEIPT_NAME)
    if os.path.exists(receipt):
        os.remove(receipt)
    tools_dir = os.path.join(dest, TOOLS_SUBDIR)
    if os.path.isdir(tools_dir) and not os.listdir(tools_dir):
        os.rmdir(tools_dir)
    return {"removed": removed, "dest": dest}


def build_manifest() -> dict:
    """Regenerate MANIFEST.json. Run after editing anything the package ships."""
    manifest = {"package": PACKAGE, "version": VERSION, "files": source_files()}
    with open(os.path.join(HERE, MANIFEST_NAME), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
    return manifest


def main(argv: list[str] | None = None) -> int:
    if sys.version_info < MIN_PYTHON:
        print(f"install: needs Python {'.'.join(map(str, MIN_PYTHON))}+, "
              f"found {sys.version.split()[0]}", file=sys.stderr)
        return 2

    ap = argparse.ArgumentParser(description="Install swarmsmith coding-v5.0.")
    ap.add_argument("--dest", default=CLAUDE_HOME, help="Claude config dir")
    ap.add_argument("--check", action="store_true", help="verify only; exit 1 on problems")
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--force", action="store_true", help="install despite integrity problems")
    ap.add_argument("--build-manifest", action="store_true",
                    help="maintainers: regenerate MANIFEST.json")
    args = ap.parse_args(argv)

    if args.build_manifest:
        m = build_manifest()
        print(f"install: MANIFEST.json rebuilt ({len(m['files'])} files, v{VERSION})")
        return 0

    if args.uninstall:
        res = uninstall(args.dest)
        print(f"install: removed {len(res['removed'])} file(s) from {res['dest']}")
        return 0

    if args.check:
        res = check(args.dest)
        if res["ok"]:
            print(f"coding-v5.0: installed and current at {res['dest']}")
            return 0
        for p in res["package_problems"]:
            print(f"  PACKAGE: {p}")
        for m in res["missing"]:
            print(f"  MISSING: {m}")
        for d in res["drifted"]:
            print(f"  DRIFTED: {d}")
        print(f"  fix: python {os.path.join(HERE, 'install.py')}")
        return 1

    res = install(args.dest, force=args.force)
    print(f"coding-v5.0 v{VERSION}: installed {len(res['installed'])} file(s) "
          f"to {res['dest']}")
    for name in res["overwritten"]:
        print(f"  note: replaced existing {name} (backup written alongside as .bak)")
    print()
    print("  Skill:   /orch-anth-5.0   (and /fix for single-issue work)")
    print(f"  Applier: python \"{os.path.join(args.dest, TOOLS_SUBDIR, 'apply_blocks.py')}\"")
    print()
    print("Verify anytime:  python install.py --check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
