
class FactFile:
    def __init__(self, path):
        self.path = path
        self.text = ""
        self.modules = []

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

def facts_dump_files(output_path, fact_files):
    for fact_file in fact_files.values():
        with open(output_path / (fact_file.path + '.md'), 'w', encoding="utf-8") as file:
            file.write("```verilog\n")
            file.write(fact_file.text)
            file.write("\n```\n")
            file.close()
        with open(output_path / (fact_file.path + '.facts.md'), 'w', encoding="utf-8") as file:
            file.write("Modules:\n\n")
            for module in fact_file.modules:
                file.write(f"- {module}\n")
            file.write("\n")
            file.close()
