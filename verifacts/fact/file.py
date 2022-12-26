from .util import fact_make_output_path

class FactFile:
    def __init__(self, path):
        self.path = path
        self.text = ""
        self.modules = []
        self.macros = []

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

def dump_file_facts(output, fact_file):
    output.write(f"# File {fact_file.path}\n\n")
    nr_modules = len(fact_file.modules)
    nr_macros = len(fact_file.macros)
    output.write(f"modules: {nr_modules} macros: {nr_macros}\n\n")
    if nr_modules > 0:
        output.write("Modules:\n\n")
        for module in fact_file.modules:
            output.write(f"- `{module}`\n")
        output.write("\n")
    if nr_macros > 0:
        output.write("Macros:\n\n")
        for macro in fact_file.macros:
            output.write(f"- `{macro}`\n")
        output.write("\n")


def facts_dump_files(output_path, fact_files, strip_path):
    for fact_file in fact_files.values():
        output_fact_file_path = fact_make_output_path(fact_file.path, strip_path, output_path / 'sources', '.md')
        with open(output_fact_file_path, 'w', encoding="utf-8") as file:
            file.write("```verilog\n")
            file.write(fact_file.text)
            file.write("\n```\n")
            file.close()
        output_fact_file_path = fact_make_output_path(fact_file.path, strip_path, output_path / 'files', '.md')
        with open(output_fact_file_path, 'w', encoding="utf-8") as file:
            dump_file_facts(file, fact_file)
            file.close()
