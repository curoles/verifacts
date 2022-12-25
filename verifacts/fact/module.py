
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

