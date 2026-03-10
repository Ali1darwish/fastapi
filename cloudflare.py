import requests

account_id = "7706cd8d0c733d9cf6f643a65970eea1"
database_id = "8732fbbc-799b-4cb7-a165-c8cd083e949a"
api_token = "7PGgsEtIQ_sBvcmPfMXJExH41MtDoOiJb7rQuKTD"

url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/d1/database/{database_id}/query"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json",
}

def execute_sql(query, parameters=None):
    payload = {
        "sql": query,
        "params": parameters or []
    }

    res = requests.post(url, headers=headers, json=payload)
    print(res.text)
    return res.json()