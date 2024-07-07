import json

file_path = 'domain-list.json'

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

unique_data = set(data["blocklist"])

blocklist = list(unique_data)
blocklist.sort()
data["blocklist"] = blocklist

with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
