import requests, json

def get_text_topics(text):
    url = "http://api.meaningcloud.com/class-1.1"

    key = "ba0fca3d6a9dfba10ead53c32c3265af"
    # text = "My name is Sebi and I like movies,but I also like songs"
    model = "IAB_en" # or "IPTC_en" or "SocialMedia_en"

    payload = "key=" + key + "&txt=" + text + "&model=" + model
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", url, data=payload, headers=headers)
    # Uncategorized
    text = response.text
    resp_json = json.loads(text)
    category_list = resp_json["category_list"]
    mini_category_list = []
    for category in category_list:
        cat = category["label"]
        subcat = ""
        if ">" in category["label"]:
            cat, subcat = category["label"].split(">")
        mini_category_list += [{"score":int(category["relevance"]),
                                "category":cat,
                                "subcategory":subcat}]
    mini_category_list = sorted(mini_category_list,key = lambda element: element["score"], reverse=True)

    return mini_category_list
