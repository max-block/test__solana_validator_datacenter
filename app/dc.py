from collections import Counter
from pprint import pprint

from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

from app.commons import get_cluster_validators, MB_URL, TDS_URL


def get_asn(reader: Reader, ip: str):
    try:
        res = reader.asn(ip)
        return res.autonomous_system_organization
    except AddressNotFoundError:
        return "unknown"


def main():
    asn_reader = Reader("./data/GeoLite2-ASN.mmdb")
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
