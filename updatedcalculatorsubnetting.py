import re


class SubnetCalculator:
    def __init__(self, ip_address, cidr=None):
        self.ip_address = ip_address
        self.cidr = cidr

        self.network_address = None
        self.broadcast_address = None
        self.first_host = None
        self.last_host = None
        self.total_hosts = None
        self.total_subnets = None
        self.mask_decimal = None
        self.mask_cidr = None

        self.calculate_subnet_info()

    def validate_ip(self):
        ip_regex = r"^([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$"
        if re.match(ip_regex, self.ip_address):
            return True
        else:
            return False

    def validate_cidr(self, cidr):
        if 0 <= cidr <= 32:
            return True
        else:
            return False

    def calculate_subnet_info(self):
        if not self.validate_ip():
            raise ValueError("Invalid IP address")

        if self.cidr is not None and not self.validate_cidr(self.cidr):
            raise ValueError("Invalid CIDR notation")

        octets = list(map(int, self.ip_address.split(".")))

        if self.cidr is None:
            # Infer subnet mask from class
            if octets[0] <= 127:
                self.cidr = 8
            elif octets[0] <= 191:
                self.cidr = 16
            else:
                self.cidr = 24

        self.mask_decimal = (0xffffffff << (32 - self.cidr)) & 0xffffffff
        self.mask_cidr = str(self.cidr)

        subnet_network = (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]
        subnet_network &= self.mask_decimal
        self.network_address = '.'.join(map(str, [(subnet_network >> 24) & 0xFF, (subnet_network >> 16) & 0xFF,
                                                  (subnet_network >> 8) & 0xFF, subnet_network & 0xFF]))

        subnet_broadcast = subnet_network | (0xffffffff >> self.cidr)
        self.broadcast_address = '.'.join(map(str, [(subnet_broadcast >> 24) & 0xFF, (subnet_broadcast >> 16) & 0xFF,
                                                    (subnet_broadcast >> 8) & 0xFF, subnet_broadcast & 0xFF]))

        self.total_hosts = 2 ** (32 - self.cidr) - 2

        if self.cidr >= 24:
            self.total_subnets = 2 ** (self.cidr - 24)
        else:
            self.total_subnets = 2 ** (24 - self.cidr)

        self.first_host = self.network_address.split('.')
        self.first_host[3] = str(int(self.first_host[3]) + 1)
        self.first_host = '.'.join(self.first_host)

        self.last_host = self.broadcast_address.split('.')
        self.last_host[3] = str(int(self.last_host[3]) - 1)
        self.last_host = '.'.join(self.last_host)


ip_address = input("Enter an IP address: ")
cidr = int(input("Enter a CIDR notation (0-32): "))
subnet_calc = SubnetCalculator(ip_address, cidr)

print("IP address:", subnet_calc.ip_address)
print("CIDR notation:", subnet_calc.cidr)
print("Subnet mask (decimal):", subnet_calc.mask_decimal)
print("Subnet mask (CIDR notation):", subnet_calc.mask_cidr)
print("Network address:", subnet_calc.network_address)
print("Broadcast address:", subnet_calc.broadcast_address)
print("First host address:", subnet_calc.first_host)
print("Last host address:", subnet_calc.last_host)
print("Total number of hosts:", subnet_calc.total_hosts)
print("Total number of subnets:",subnet_calc.total_subnets)
