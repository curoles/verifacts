import json
import base64

def decode_base64_string(base64_string):
    base64_bytes = base64_string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string

def facts_decode_strings(facts):
    for fact in facts:
        if fact.get('fact_value'):
            fact['fact_value'] = decode_base64_string(fact['fact_value'])
        if fact.get("source"):
            if fact["source"].get("signature"):
                 fact["source"]["signature"] = decode_base64_string(fact["source"]["signature"])
        if fact.get("target"):
            if fact["target"].get("signature"):
                 fact["target"]["signature"] = decode_base64_string(fact["target"]["signature"])

def load_facts_as_json(json_file_path):
    facts = []
    with open(json_file_path, 'r') as json_file:
        for json_line in json_file: # 1 json object per line
            json_line = json_line.strip()
            if json_line:
                #print(json_line)
                fact = json.loads(json_line)
                facts.append(fact)
        json_file.close()
    print(f'number of loaded facts is {len(facts)}')
    return facts
