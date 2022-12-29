from .util import sig2path, facts_relpath

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

def dump_module_facts(output, fact_module, paths):
    output.write(f"# Module `{paths[1]}` from {paths[0]}\n\n")

def facts_dump_modules(output_path, fact_modules, strip_path):
    list_modules = []
    for fact_module in fact_modules.values():
        paths = sig2path(fact_module.signature, strip_path)
        output_module_path = output_path / 'modules' / paths[2]
        output_module_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_module_path, 'w', encoding="utf-8") as file:
            dump_module_facts(file, fact_module, paths)
            file.close()
            paths.append(output_module_path)
            list_modules.append(paths)

    list_modules_path = output_path / 'modules' / 'list.md'
    with open(list_modules_path, 'w', encoding="utf-8") as file:
        file.write("# List of modules\n\n")
        for m in list_modules:
            link_path = facts_relpath(list_modules_path, m[3])
            file.write(f"- [`{m[1]}`]({link_path}) from {m[0]}\n")
        file.close()
