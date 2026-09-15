#!/usr/bin/env python3
"""Fail loudly before a KnotJob batch if the runtime cannot load the jar.

The distributed KnotJob.jar is compiled at class-file major version 67, so it
needs a JDK 23 or newer. A JDK 21 host raises UnsupportedClassVersionError at
main-class load, which looks like an ordinary nonzero exit inside the batch
runners and is easy to mistake for a computational failure. TOOLING.md states
the requirement; nothing checked it.
"""
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

REQUIRED_CLASS_FILE_MAJOR = 67  # Java 23
RECORDED_JAR_SHA256 = 'b63daf5f689660a276ed37bbca3393cb26fe62e097427cdd599647b874304718'


def check(java, jar):
    jar = Path(jar)
    problems = []
    digest = hashlib.sha256(jar.read_bytes()).hexdigest()
    if digest != RECORDED_JAR_SHA256:
        problems.append('jar sha256 %s does not match the jar behind the stored runs (%s)'
                        % (digest, RECORDED_JAR_SHA256))
    raw = subprocess.run([java, '-version'], capture_output=True, text=True).stderr
    # A proxied container prints a JAVA_TOOL_OPTIONS banner first; keep only
    # the real version lines so the banner cannot be parsed as a release.
    version_text = '\n'.join(l for l in raw.splitlines() if 'version' in l.lower()
                             and 'JAVA_TOOL_OPTIONS' not in l)
    feature = None
    for token in version_text.split():
        if token.startswith('"') and token.endswith('"'):
            feature = int(token.strip('"').split('.')[0])
            break
    if feature is None:
        problems.append('could not parse a feature release from: %r' % raw)
    elif feature < REQUIRED_CLASS_FILE_MAJOR - 44:
        problems.append('java %d cannot load class-file major %d; need JDK %d+'
                        % (feature, REQUIRED_CLASS_FILE_MAJOR, REQUIRED_CLASS_FILE_MAJOR - 44))
    return digest, version_text.strip().splitlines()[:1], problems


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('java')
    p.add_argument('jar')
    a = p.parse_args()
    digest, version, problems = check(a.java, a.jar)
    print('jar_sha256 =', digest)
    print('java =', version[0] if version else '(unknown)')
    for problem in problems:
        print('FAIL:', problem, file=sys.stderr)
    sys.exit(1 if problems else 0)
