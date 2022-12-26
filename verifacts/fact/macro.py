
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

