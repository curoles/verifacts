from .util import sig_path2path

class FactMacro:
    def __init__(self, path, signature):
        self.path = path
        self.signature = signature

def facts_find_macros(facts, fact_files):
    macros = {}
    for fact in facts:
        if fact['fact_name'] == '/kythe/node/kind' and fact['fact_value'] == 'macro':
            signature = fact['source']['signature']
            path = fact['source']['path']
            macros[signature] = FactMacro(path, signature)
            if fact_files.get(path):
                fact_files[path].macros.append(signature)

    return macros

def dump_macro_facts(output, fact_macro, paths):
    output.write(f"# Macro `{paths[1]}` from {paths[0]}\n\n")

def facts_dump_macros(output_path, fact_macros, strip_path):
    for fact_macro in fact_macros.values():
        paths = sig_path2path(fact_macro.signature, fact_macro.path, strip_path)
        output_macro_path = output_path / 'macros' / paths[2]
        output_macro_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_macro_path, 'w', encoding="utf-8") as file:
            dump_macro_facts(file, fact_macro, paths)
            file.close()
