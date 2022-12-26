#!/usr/bin/env bash

this_script="$(realpath "${BASH_SOURCE[0]}")"
script_dir="$(dirname "$this_script")"

EXTRACTOR=verible-verilog-kythe-extractor

if ! command -v $EXTRACTOR &> /dev/null
then
    if [ -z "${VERIBLE_HOME+x}" ]
    then
        echo "$EXTRACTOR could not be found"
        echo "VERIBLE_HOME is unset"
        exit
    else
        echo "VERIBLE_HOME is set to '$VERIBLE_HOME'"
        EXTRACTOR=$VERIBLE_HOME/bazel-bin/verilog/tools/kythe/verible-verilog-kythe-extractor
    fi
fi

if [[ "$#" -lt 1 ]]
then
    echo "Usage: extractor.bash <OUTPUT_DIR>"
    exit
fi

OUTPUT_DIR=$1

LIST="--file_list_path $script_dir/project.flist --file_list_root $script_dir"

$EXTRACTOR --print_kythe_facts json $LIST  --verilog_project_name prj-test1 > $OUTPUT_DIR/facts.json
$EXTRACTOR --print_kythe_facts json_debug $LIST --verilog_project_name prj-test1 > $OUTPUT_DIR/facts.debug.json
