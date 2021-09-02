#!/usr/bin/env bash
set -ex

rm -rf endless_sky/endless-sky
mkdir -p endless_sky/endless-sky
cp -r endless-sky/source endless_sky/endless-sky/source
cp -r endless-sky/tests endless_sky/endless-sky/tests
