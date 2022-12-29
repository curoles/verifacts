
class FactAnchor:
    def __init__(self, path, signature):
        self.path = path
        self.signature = signature
        loc_str = signature.strip('@#')
        start_stop = loc_str.split(':', 1)
        self.loc = [int(start_stop[0]), int(start_stop[1])]
        self.find_line_in_source_code()

    def find_line_in_source_code(self):
        with open(self.path, 'r') as file:
            text = file.read()
            self.text = text[self.loc[0] : self.loc[1]]
            self.line_nr = text[: self.loc[0]].count('\n')
            file.close()

def facts_find_anchors(facts):
    anchors = {}
    for fact in facts:
        if fact['fact_name'] == '/kythe/node/kind' and fact['fact_value'] == 'anchor':
            signature = fact['source']['signature']
            path = fact['source']['path']
            anchors[signature] = FactAnchor(path, signature)

    return anchors
