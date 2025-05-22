Table of Contents

[Summary of Steps [2](#summary-of-steps)](#summary-of-steps)

[1 Description of the steps
[2](#description-of-the-steps)](#description-of-the-steps)

[Part 1 [2](#_Toc194008768)](#_Toc194008768)

[Part 2 [7](#part-2)](#part-2)

[2 Conclusion [10](#conclusion)](#conclusion)

# Summary of Steps

This lab involved configuring and testing VLANs on a network with a router and a switch. Key steps included:

**Part 1: Router-on-a-Stick Configuration**
1.  Configuring router subinterfaces for VLAN 10 and VLAN 20: IP addressing, dot1q encapsulation, and DHCP services.
2.  Verifying router subinterface configuration.
3.  Configuring the switch: creating VLAN 10 and VLAN 20, assigning access ports, and configuring a trunk port to the router.
4.  Verifying switch VLAN and trunk configuration.
5.  Checking IP configuration on end devices (Laptop 1, PC1, PC2) for correct DHCP scope assignment.
6.  Testing intra-VLAN and inter-VLAN connectivity (via router).
7.  Observing the switch's MAC address table for VLAN-specific learning.

**Part 2: Layer 3 Switch Configuration**
1.  Simulating router failure by disconnecting the router-switch link.
2.  Testing connectivity: observing intra-VLAN success and inter-VLAN failure.
3.  Configuring the switch as a Layer 3 switch: enabling IP routing, creating Switched Virtual Interfaces (SVIs) for VLAN 10 and VLAN 20 with IP addresses (default gateways).
4.  Retesting connectivity: verifying restored inter-VLAN communication via the L3 switch.
5.  Checking switch IP interfaces and routing table to confirm L3 capabilities.

# 1 Description of the steps

[]{#_Toc194008768 .anchor}Part 1
Router setup for VLAN subnets involved creating virtual subinterfaces for VLAN 10 and VLAN 20. These were assigned IP addresses, dot1q encapsulation, and DHCP configurations to ensure each VLAN operated correctly with its designated gateway.

Router subinterface configuration was verified using "show ip interface brief".

The switch was configured to assign devices to appropriate VLANs. Access ports were set for specific VLANs, and a trunk port was configured for inter-VLAN packet transmission to the router. VLANs 10 and 20 were created and named.
*Note: Switch configuration typically involves creating VLANs, assigning interfaces to VLANs (access mode), and setting trunk mode on the router-connected interface.*

Proper VLAN configuration on the switch was confirmed by checking VLAN assignments and trunk settings to ensure correct port mapping and active trunk links, crucial for inter-VLAN communication.

IP configurations for devices were checked:
Laptop 1: 10.0.10.2 (VLAN 10)
PC1: 10.0.20.2 (VLAN 20)
PC2: 10.0.20.3 (VLAN 20)

Connectivity tests:
- PC1 (VLAN 20) to PC2 (VLAN 20): Successful.
- PC2 (VLAN 20) to PC1 (VLAN 20): Successful.
- Laptop 1 (VLAN 10) to PC1 (VLAN 20) and PC2 (VLAN 20): Pings appeared to fail.
It was noted that university firewalls might block ICMP replies, causing apparent timeouts even if packets were routed correctly, as confirmed by Wireshark.

The switch's MAC address table was viewed to verify that MAC addresses of connected devices were correctly linked to their assigned VLANs, essential for proper traffic routing.

## Part 2

The router-switch connection was interrupted.
Communication tests showed that intra-VLAN packet transmission (e.g., PC1 to PC2, both VLAN 20) remained successful, while inter-VLAN communication failed (e.g., Laptop 1 in VLAN 10 to PC1 in VLAN 20).

The switch was then configured as a Layer 3 switch to route packets between its VLAN subnets without an external router. This involved enabling IP routing and creating SVIs for VLAN 10 and VLAN 20 with appropriate IP addresses.

After L3 switch configuration, packet transmissions were successful both within and between VLANs.
Pings from Laptop1 (VLAN 10) to PC2 (VLAN 20) using the L3 switch for routing were tested. Similar to Part 1, firewall issues caused apparent timeouts, but Wireshark confirmed packet delivery.

After enabling IP routing, the switch's active IP interfaces (SVIs) and routing table state were checked, demonstrating its capability to manage packet routing independently.

# 2 Conclusion

This lab provided hands-on experience in setting up and managing VLANs with routers and switches. Creating VLAN subnets helped separate network traffic, enhancing security and efficiency. The setup was validated by implementing VLAN IDs, DHCP services, and trunk connections. Furthermore, configuring a Layer 3 switch for independent VLAN management and IP routing was successfully tested. This exercise significantly improved practical skills in network configuration and troubleshooting.
