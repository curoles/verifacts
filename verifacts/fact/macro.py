from .util import sig_path2path, facts_relpath

class FactMacro:
    def __init__(self, path, signature):
        self.path = path
        self.signature = signature

def bind_anchor_with_macro(macro_sig, facts, fact_anchors):
    bind_anchor = None
    for fact in facts:
        if fact.get('target') and fact['target']['signature'] == macro_sig:
            if fact.get('edge_kind') and fact['edge_kind'] == '/kythe/edge/defines/binding':
                if fact.get('source') and fact_anchors.get(fact['source']['signature']):
                    bind_anchor = fact_anchors[fact['source']['signature']]
                    break

    return bind_anchor

def facts_find_macros(facts, fact_files, fact_anchors):
    macros = {}
    for fact in facts:
        if fact['fact_name'] == '/kythe/node/kind' and fact['fact_value'] == 'macro':
            signature = fact['source']['signature']
            path = fact['source']['path']
            macros[signature] = FactMacro(path, signature)
            if fact_files.get(path):
                fact_files[path].macros.append(signature)
            macros[signature].anchor = bind_anchor_with_macro(signature, facts, fact_anchors)

    return macros

def dump_macro_facts(output, fact_macro, paths, output_path):
    output.write(f"# Macro `{paths[1]}` from {paths[0]}\n\n")
    line_nr = fact_macro.anchor.line_nr
    link_path = facts_relpath(paths[3], output_path / 'sources' / paths[0])
    output.write(f"Location: file [{paths[0]}]({link_path}.md) line {line_nr}\n\n")
    link_path = facts_relpath(paths[3], output_path / 'linesrc' / paths[0])
    output.write(f"Jump to [{paths[0]} line {line_nr}]({link_path}.md#^line-{line_nr})\n\n")

def facts_dump_macros(output_path, fact_macros, strip_path):
    list_macros = []
    for fact_macro in fact_macros.values():
        paths = sig_path2path(fact_macro.signature, fact_macro.path, strip_path)
        output_macro_path = output_path / 'macros' / paths[2]
        output_macro_path.parent.mkdir(parents=True, exist_ok=True)
        paths.append(output_macro_path)
        with open(output_macro_path, 'w', encoding="utf-8") as file:
            dump_macro_facts(file, fact_macro, paths, output_path)
            file.close()
            list_macros.append(paths)

    list_macros_path = output_path / 'macros' / 'list.md'
    with open(list_macros_path, 'w', encoding="utf-8") as file:
        file.write("# List of macros\n\n")
        for m in list_macros:
            link_path = facts_relpath(list_macros_path, m[3])
            file.write(f"- [`{m[1]}`]({link_path}) from {m[0]}\n")
        file.close()
