import environ
import json
import requests

def get_results(query):
    url = "https://bing-web-search1.p.rapidapi.com/search"
    querystring = {
        "q" : query,
        "freshness" : "Day",
        "textFormat" : "Raw",
        "safeSearch" : "Off",
        "mkt" : "en-us"
    }

    env = environ.Env()
    environ.Env.read_env()

    headers = {
        'x-bingapis-sdk': "true",
        'x-rapidapi-host': "bing-web-search1.p.rapidapi.com",
        'x-rapidapi-key': env('API_KEY')
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    json_response = json.loads(response.text)['webPages']

    results = []
    for result in json_response['value']:
        results.append({
            'title': result['name'],
            'link': result['url'],
            'summary': result['snippet']
        })

    return results

def main():
    print('Enter query')
    query = input()
    results = get_results(query)
    for result in results:
        print(result['title'])
        print('-' * len(result['title']))
        print(result['summary'])
        print(result['link'])
        print()


if __name__ == '__main__':
    main()