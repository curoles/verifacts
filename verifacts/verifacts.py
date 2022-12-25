import sys
from pathlib import Path
import verifacts.load.json


class FactFile:
    def __init__(self, path):
        self.path = path
        self.text = ""
        self.modules = []

def facts_find_files(facts):
    files = {}
    for fact in facts:
        if fact['fact_name'] == '/kythe/node/kind' and fact['fact_value'] == 'file':
            path = fact['source']['path']
            files[path] = FactFile(fact['source']['path'])
    for file in files.values():
        for fact in facts:
            if fact.get('source') and fact['source']['path'] == file.path and fact['fact_name'] == '/kythe/text':
                file.text = fact['fact_value']

    return files

class FactModule:
    def __init__(self, path, signature):
        self.path = path
        self.signature = signature

def facts_find_modules(facts, fact_files):
    modules = {}
    for fact in facts:
        if fact['fact_name'] == '/kythe/subkind' and fact['fact_value'] == 'module':
            signature = fact['source']['signature']
            path = fact['source']['path']
            modules[signature] = FactModule(path, signature)
            if fact_files.get(path):
                fact_files[path].modules.append(signature)

    return modules

def facts_dump_files(output_path, fact_files):
    for fact_file in fact_files.values():
        with open(output_path / (fact_file.path + '.md'), 'w', encoding="utf-8") as file:
            file.write("```verilog\n")
            file.write(fact_file.text)
            file.write("\n```\n")
            file.close()
        with open(output_path / (fact_file.path + '.facts.md'), 'w', encoding="utf-8") as file:
            file.write("Modules:\n\n")
            for module in fact_file.modules:
                file.write(f"- {module}\n")
            file.write("\n")
            file.close()

def main(argv):
    if len(argv) > 1:
        json_file = Path(argv[1])
    else:
        print("Usage: verifacts <facts.json> <output dir>")
        exit(1)
    if len(argv) > 2:
        output_path = Path(argv[2])
    else:
        print("Usage: verifacts <facts.json> <output dir>")
        exit(1)

    facts = verifacts.load.json.load_facts_as_json(json_file)
    verifacts.load.json.facts_decode_strings(facts)
    ##for fact in facts:
    ##    print(fact)
    fact_files = facts_find_files(facts)
    facts_find_modules(facts, fact_files)
    facts_dump_files(output_path, fact_files)

