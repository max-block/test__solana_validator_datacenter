from dataclasses import dataclass

import pydash

from app.commons import MB_URL, get_cluster_validators


@dataclass
class ServerAddress:
    ip: str
    has_neighbour: bool = False

    @property
    def prefix_ip(self) -> str:
        parts = self.ip.split(".")
        return ".".join(parts[:3])

    @property
    def last_ip(self) -> int:
        parts = self.ip.split(".")
        return int(parts[3])


def main():
    all_validators = get_cluster_validators(MB_URL)
    servers = ([ServerAddress(ip=ip) for ip in all_validators])
    servers = pydash.sort(servers, key=lambda x: x.ip)

    ip_groups: dict[str, set[int]] = {}  # prefix -> a.b.c.d: set of 'd
    for s in servers:
        if s.prefix_ip in ip_groups:
            ip_groups[s.prefix_ip].add(s.last_ip)
        else:
            ip_groups[s.prefix_ip] = {s.last_ip}

    for s in servers:
        if s.last_ip + 1 in ip_groups[s.prefix_ip]:
            s.has_neighbour = True
        if s.last_ip - 1 in ip_groups[s.prefix_ip]:
            s.has_neighbour = True

    neighbour_servers = [s for s in servers if s.has_neighbour]

    for s in neighbour_servers:
        print(s)

    print(f"all={len(all_validators)}, neighbour={len(neighbour_servers)}")


if __name__ == "__main__":
    main()
