import urllib2

def netid2name(net_id):
    """
    Takes a NetId and returns the name associated with the NetId after a query of publicly available information.
    Based off of the code made by Kevin Lin.
    """
##    if not is_api_key_valid(request.args.get("key", "")):
##        return error("Invalid or unauthorized API key")

    # Parameters from URL
    lookup_net_id = net_id
##    lookup_name = None
    # Replace spaces in name with plus sign, if they exist
##    if lookup_name:
##        lookup_name = "+".join(lookup_name.split())

    # Rice 411 lookup directory
    # Prioritize search by Net ID
    if lookup_net_id is not None:
        url = "http://fouroneone.rice.edu/query.php?tab=people&search=" + lookup_net_id + "&department=&phone=&action=Search"
##    elif lookup_name is not None:
##        url = "http://fouroneone.rice.edu/query.php?tab=people&search=" + lookup_name + "&department=&phone=&action=Search"
    else:
        return error("One of Net ID or Name in URL parameters must be non-null")
    data = urllib2.urlopen(url)

    # Parsing HTML data like this is highly unpredictable. Thus, a bunch of try-excepts:
    students, faculty = [], []
    name, year, department, title, mailstop, office, phone, website, email, college, major, address = (None, None, None, None, None, None, None, None, None, None, None, None)
    for line in data.readlines()[200:]:
        if "name: " in line:
            try:
                name_list = line.strip().lstrip("name: <b>").rstrip(">b/<").split(", ")
                name = name_list[1] + " " + name_list[0]
            except:
                pass
        if "class: " in line:
            try:
                year = line.strip()[7:].split()[0].capitalize()
            except:
                pass
        if "college: " in line:
            try:
                college = line.strip()[9:]
            except:
                pass
        if "major: " in line:
            try:
                major = line.strip()[7:]
            except:
                pass
        if "address: " in line:
            try:
                address = line.strip()[9:]
            except:
                pass
        if "department: " in line:
            try:
                department = line.strip()[12:]
            except:
                pass
        if "title: " in line:
            try:
                title = line.strip()[7:]
            except:
                pass
        if "mailstop: " in line:
            try:
                mailstop = line.strip()[10:]
            except:
                pass
        if "office: " in line:
            try:
                office = line.strip()[8:]
            except:
                pass
        if "phone: " in line:
            try:
                phone = line.strip()[7:]
            except:
                pass
        if "homepage: " in line:
            try:
                temp = line.strip()[26:]
                website = temp[:temp.index("'")]
            except:
                pass
        if "email: " in line:
            try:
                temp = line.strip()[23:]
                email = temp[:temp.index("'")]
                # Email is the last field, so add this new person to the list at this point
                if year.lower() == "staff" or year.lower() == "faculty":
                    faculty.append(dict({"name": name, "department": department, "title": title, "mailstop": mailstop, "office": office, "phone": phone, "website": website, "email": email}))
                else:
                    students.append(dict({"name": name, "year": year, "college": college, "major": major, "address": address}))
                # Reset all variables to null
                name, year, department, title, mailstop, office, phone, website, email, college, major, address = (None, None, None, None, None, None, None, None, None, None, None, None)
            except:
                pass
    search = {"result": "success",
              "message": "null",
              "student": students}
    return search['student'][0]['name']
