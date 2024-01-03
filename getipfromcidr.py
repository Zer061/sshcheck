import ipaddress

# Read CIDR ranges from cidr.txt
with open('cidr.txt', 'r') as file:
    cidr_ranges = file.readlines()

# Process each CIDR range
for cidr in cidr_ranges:
    cidr = cidr.strip()  # Remove leading/trailing whitespaces and newlines
    if cidr and not cidr.startswith('#'):  # Ignore empty lines and comments
        #print(f"IP addresses in {cidr}:")
        # Create an IPv4 network object from the CIDR range
        network = ipaddress.ip_network(cidr)
        
        # Iterate through all IP addresses in the network and print them
        for ip in network:
            print(ip)
        print()  # Add a newline for separation
