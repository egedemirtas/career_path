import json


skills_arr = []
with open("data_dummy1.json", "r", encoding="utf8") as read_file:
    data = json.load(read_file)
    for company in data: #iterate companies
        for uni in company["universities"]: #iterate universities in company
            for field in uni["fields"]: #iterate fields in university
                ##field_name = field["field_name"]
                for skill in field["details"]["What they do"]:
                    if skill['skill'] not in skills_arr:
                        skills_arr.append(skill['skill'])


with open("whattheydo-copy.json", "w", encoding="utf8") as write_file:
    json.dump(skills_arr, write_file)

