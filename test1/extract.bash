#!/bin/bash

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

$EXTRACTOR --print_kythe_facts json --file_list_path project.flist --verilog_project_name prj-test1 > $OUTPUT_DIR/facts.json
$EXTRACTOR --print_kythe_facts json_debug --file_list_path project.flist --verilog_project_name prj-test1 > $OUTPUT_DIR/facts.debug.json
