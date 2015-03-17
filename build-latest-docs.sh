#!/bin/sh
VERSION="latest"

(cd doc; make)

rm -rf /tmp/anillo-doc/
mkdir -p /tmp/anillo-doc/
mv doc/*.html /tmp/anillo-doc/

git checkout gh-pages || exit 1

rm -rf ./$VERSION
mv /tmp/anillo-doc/ ./$VERSION

git add --all ./$VERSION
git commit -a -m "Update ${VERSION} doc"
