from .util import sig2path, facts_relpath

class FactModule:
    def __init__(self, path, signature):
        self.path = path
        self.signature = signature

def bind_anchor_with_module(macro_sig, facts, fact_anchors):
    bind_anchor = None
    for fact in facts:
        if fact.get('target') and fact['target']['signature'] == macro_sig:
            if fact.get('edge_kind') and fact['edge_kind'] == '/kythe/edge/defines/binding':
                if fact.get('source') and fact_anchors.get(fact['source']['signature']):
                    bind_anchor = fact_anchors[fact['source']['signature']]
                    break

    return bind_anchor

def facts_find_modules(facts, fact_files, fact_anchors):
    modules = {}
    for fact in facts:
        if fact['fact_name'] == '/kythe/subkind' and fact['fact_value'] == 'module':
            signature = fact['source']['signature']
            path = fact['source']['path']
            modules[signature] = FactModule(path, signature)
            if fact_files.get(path):
                fact_files[path].modules.append(signature)
            modules[signature].anchor = bind_anchor_with_module(signature, facts, fact_anchors)

    return modules

def dump_module_facts(output, fact_module, paths, output_path):
    output.write(f"# Module `{paths[1]}` from {paths[0]}\n\n")
    line_nr = fact_module.anchor.line_nr
    link_path = facts_relpath(paths[3], output_path / 'sources' / paths[0])
    output.write(f"Location: file [{paths[0]}]({link_path}.md) line {line_nr}\n\n")
    link_path = facts_relpath(paths[3], output_path / 'linesrc' / paths[0])
    output.write(f"Jump to [{paths[0]} line {line_nr}]({link_path}.md#^line-{line_nr})\n\n")

def facts_dump_modules(output_path, fact_modules, strip_path):
    list_modules = []
    for fact_module in fact_modules.values():
        paths = sig2path(fact_module.signature, strip_path)
        output_module_path = output_path / 'modules' / paths[2]
        output_module_path.parent.mkdir(parents=True, exist_ok=True)
        paths.append(output_module_path)
        with open(output_module_path, 'w', encoding="utf-8") as file:
            dump_module_facts(file, fact_module, paths, output_path)
            file.close()
            list_modules.append(paths)

    list_modules_path = output_path / 'modules' / 'list.md'
    with open(list_modules_path, 'w', encoding="utf-8") as file:
        file.write("# List of modules\n\n")
        for m in list_modules:
            link_path = facts_relpath(list_modules_path, m[3])
            file.write(f"- [`{m[1]}`]({link_path}) from {m[0]}\n")
        file.close()
