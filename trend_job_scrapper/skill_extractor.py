import json

dict ={
    "computer science": [],
    "computer engineer": [],
    "information technology": [],
    "computer software engineering": [],

    "Electrical and Electronics Engineering": [],
    "Electrical, Electronics and Communications": [],

    "Mechanical Engineering": [],
    "Mechatronics, Robotics, and Automation Engineering": []
}

with open("data_dummy1.json", "r", encoding="utf8") as read_file:
    data = json.load(read_file)
    for company in data: #iterate companies
        for uni in company["universities"]: #iterate universities in company
            for field in uni["fields"]: #iterate fields in university
                field_name = field["field_name"]
                for skill in field["details"]["What they are skilled at"]:
                    new_dict = {"skill_name":skill["skill"], "count":0}
                    if new_dict not in dict[field_name]: 
                        dict[field_name].append(new_dict)
                    else:
                        print("yo")

with open("search_skill.json", "w", encoding="utf8") as write_file:
    json.dump(dict, write_file)
