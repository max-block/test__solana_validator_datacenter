# import os
# from pprint import pprint
#
# from dotenv import load_dotenv
# from geoip2.database import Reader
#
# load_dotenv()
#
# IP = os.getenv("IP", "216.58.212.142")
#
# with Reader("data/GeoLite2-ASN.mmdb") as reader:
#     res = reader.asn(IP)
#     pprint(res.autonomous_system_organization)
from collections import Counter
from pprint import pprint

import requests
from geoip2.database import Reader

MB_URL = "https://api.mainnet-beta.solana.com"
TDS_URL = "https://testnet.solana.com"


def get_cluster_validators(url: str) -> list[str]:
    params = {"jsonrpc": "2.0", "id": 1, "method": "getClusterNodes"}
    res = requests.post(url, json=params)
    return [v["gossip"].split(":")[0] for v in res.json()["result"]]


def get_asn(reader: Reader, ip: str):
    res = reader.asn(ip)
    return res.autonomous_system_organization


def main():
    asn_reader = Reader("data/GeoLite2-ASN.mmdb")
    mb_validators = get_cluster_validators(MB_URL)
    mb_asn_list = []
    for ip in mb_validators:
        mb_asn_list.append(get_asn(asn_reader, ip))
    pprint(Counter(mb_asn_list))

    tds_validators = get_cluster_validators(TDS_URL)
    tds_asn_list = []
    for ip in tds_validators:
        tds_asn_list.append(get_asn(asn_reader, ip))
    pprint(Counter(tds_asn_list))
    asn_reader.close()


if __name__ == "__main__":
    main()
