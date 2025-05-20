# Network Configuration Tool

This tool reads a network parameters configuration file, verifies its format, and configures virtual network interfaces and routing tables accordingly.

## Configuration File Format

The configuration file contains two sections:

### Address Table
- **Host:** List of interface names (e.g., eth0, eth1, ...).
- **IP_address:** Corresponding IP addresses.
- **Net_mask:** Corresponding network masks (e.g., /24, /25, ...).

Example:
```
Address_table
------------------------------------------------------------
Host: eth0 eth1 eth2 eth3        
IP_address: 10.0.0.1 11.12.34.56 34.56.78.122 56.23.12.1        
Net_mask: /24 /25 /28 /30        
```

### Routing Table
- **Network:** List of network addresses.
- **Mask:** Corresponding subnet masks.
- **Next_bench:** Next hop or gateway for each route.

Example:
```
Routing_table
------------------------------------------------------------
Network: 78.34.5.0 200.1.2.0 0.0.0.0 56.78.9.0 
Mask       : /24 /26 /0 /24 
Next_bench : 11.12.34.78 56.23.12.2 10.0.0.254 56.23.23.124
```

## How It Works

1. The script reads the configuration file provided as an argument.
2. It extracts and validates parameters from the Address Table.
3. For each host, it creates a virtual dummy interface using:  
   `ip link add dummy X type dummy`  
   where X is a number (0, 1, 2, ...).
4. It assigns the corresponding IP address and netmask to the dummy interface.
5. The script then extracts routing parameters, validates them, and adds routes using the `ip route add` command.
6. Errors in the configuration file (e.g. mismatched counts) cause the script to exit with an error message.

## Usage

Run the script with the configuration file as an argument:
```
./configure_network.sh /path/to/config_file
```
Ensure you have the necessary privileges to execute network commands.
