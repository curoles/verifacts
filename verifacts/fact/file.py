from .util import fact_make_output_path, facts_relpath, strip_root

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

def dump_file_facts(output, fact_file, src_file, strip_path):
    path = strip_root(fact_file.path, strip_path)
    output.write(f"# File {path}\n\n")
    output.write(f"[Source code]({src_file})\n\n")
    nr_modules = len(fact_file.modules)
    nr_macros = len(fact_file.macros)
    if nr_modules > 0:
        output.write(f"Modules ({nr_modules}):\n\n")
        for module in fact_file.modules:
            module_name = strip_root(module, strip_path)
            output.write(f"- `{module_name}`\n")
        output.write("\n")
    if nr_macros > 0:
        output.write(f"Macros ({nr_macros}):\n\n")
        for macro in fact_file.macros:
            output.write(f"- `{macro}`\n")
        output.write("\n")


def facts_dump_files(output_path, fact_files, strip_path):
    for fact_file in fact_files.values():
        output_src_file_path = fact_make_output_path(fact_file.path, strip_path, output_path / 'sources', '.md')
        with open(output_src_file_path, 'w', encoding="utf-8") as file:
            file.write("```verilog\n")
            file.write(fact_file.text)
            file.write("\n```\n")
            file.close()
        output_fact_file_path = fact_make_output_path(fact_file.path, strip_path, output_path / 'files', '.md')
        src_file = facts_relpath(output_fact_file_path, output_src_file_path)
        with open(output_fact_file_path, 'w', encoding="utf-8") as file:
            dump_file_facts(file, fact_file, src_file, strip_path)
            file.close()
