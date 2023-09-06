import os
import requests

uri = os.environ.get("STRAPI_URL", "http://localhost:1337")
header = {"Authorization":f"Bearer {os.environ.get('STRAPI_TOKEN', '')}"}

def get_all_faq():
    results = []
    try:
        response = requests.get(uri + "/api/faqs", headers = header)
        response.raise_for_status()
    except Exception as err:
        print(f'[ERR] Strapi API | {err}')
        return []
    data = response.json()['data']
    for i in range(len(data)):
        que = data[i]['attributes']['question']
        ans = data[i]['attributes']['answer']
        results.append((que, ans))
    return results 

def get_all_knowledge():
    results = []
    try:
        response = requests.get(uri + "/api/knowledges", headers = header)
        response.raise_for_status()
    except Exception as err:
        print(f'[ERR] Strapi API | {err}')
        return []
    data = response.json()['data']
    for i in range(len(data)):
        proj = data[i]['attributes']['project']
        desc = data[i]['attributes']['description']
        results.append((proj, desc))
    return results 

# TODO: update this function
def get_subscribers(project: str):
    results = []
    try:
        # TODO: add filtering on db side
        # response = requests.get(uri + f"/api/knowledges?project=eq.{project}&select=*", headers = header)
        response = requests.get(uri + f"/api/knowledges", headers = header)
        response.raise_for_status()
    except Exception as err:
        print(f'[ERR] Strapi API | {err}')
        return []
    data = response.json()['data']
    for i in range(len(data)):
        if project == data[i]['attributes']['project']:
            subs = data[i]['attributes']['subscriptions']
            results.append(subs)
    
    print(len(results))
    if len(results) == 0:
        for i in range(len(data)):
            if "general" == data[i]['attributes']['project']:
                subs = data[i]['attributes']['subscriptions']
                results.append(subs)
    print(results[0])
    return results[0] 