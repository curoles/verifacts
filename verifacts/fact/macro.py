from .util import sig_path2path, facts_relpath

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
    output.write(f"Location: file {paths[0]} line ???\n\n")

def facts_dump_macros(output_path, fact_macros, strip_path):
    list_macros = []
    for fact_macro in fact_macros.values():
        paths = sig_path2path(fact_macro.signature, fact_macro.path, strip_path)
        output_macro_path = output_path / 'macros' / paths[2]
        output_macro_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_macro_path, 'w', encoding="utf-8") as file:
            dump_macro_facts(file, fact_macro, paths)
            file.close()
            paths.append(output_macro_path)
            list_macros.append(paths)

    list_macros_path = output_path / 'macros' / 'list.md'
    with open(list_macros_path, 'w', encoding="utf-8") as file:
        file.write("# List of macros\n\n")
        for m in list_macros:
            link_path = facts_relpath(list_macros_path, m[3])
            file.write(f"- [`{m[1]}`]({link_path}) from {m[0]}\n")
        file.close()
