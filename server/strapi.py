import os
import requests

uri = os.environ.get("STRAPI_URL", "http://localhost:1337")
header = {"Authorization":f"Bearer + {os.environ.get("STRAPI_TOKEN", "")}"}

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
        ans = data[i]['attributes']['question']
        results.append((que, ans))
    print(results)
    return results 

if __name__ == "__main__":
    get_all_faq()