#!/usr/bin/env bash

this_script="$(realpath "${BASH_SOURCE[0]}")"
script_dir="$(dirname "$this_script")"

PYTHONPATH=$script_dir python3 -m verifacts $@

