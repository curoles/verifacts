from .util import fact_make_output_path

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

def dump_module_facts(output, fact_module):
    output.write(f"# Module {fact_module.signature}\n\n")

def facts_dump_modules(output_path, fact_modules, strip_path):
    for fact_module in fact_modules.values():
        output_module_path = fact_make_output_path(fact_module.path, strip_path, output_path / 'modules', '.md')
        with open(output_module_path, 'w', encoding="utf-8") as file:
            dump_module_facts(file, fact_module)
            file.close()
