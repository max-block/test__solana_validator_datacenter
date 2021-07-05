import requests

MB_URL = "https://api.mainnet-beta.solana.com"
TDS_URL = "https://api.testnet.solana.com"



def get_cluster_validators(url: str) -> list[str]:
    params = {"jsonrpc": "2.0", "id": 1, "method": "getClusterNodes"}
    res = requests.post(url, json=params)
    return [v["gossip"].split(":")[0] for v in res.json()["result"]]
