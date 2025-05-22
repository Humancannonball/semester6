Table of Contents

[Summary of Steps [2](#summary-of-steps)](#summary-of-steps)

[Description of the steps [2](#_Toc196771659)](#_Toc196771659)

[1st Part [2](#_Toc196771660)](#_Toc196771660)

[2nd Part [4](#_Toc196771661)](#_Toc196771661)

[Conclusion [11](#conclusion)](#conclusion)

# Summary of Steps

This lab focused on MAC-IP addressing, switch operations, and ARP.

**Part 1: Basic Router and Switch Setup**
1.  Understanding crossover UTP cable usage for direct device connections.
2.  Basic router configuration (interface IP addressing).
3.  Basic switch configuration (hostname, management IP).
4.  Observing MAC addresses on network devices.

**Part 2: Switched Network Analysis**
1.  Setting up a topology with a router, two switches, and multiple end devices.
2.  Configuring Ethernet ports on end devices.
3.  Examining ARP tables on PCs and the MAC address table on switch SW1-1.
4.  Answering questions about MAC and ARP table contents and their differences.
5.  Performing ping tests between devices on the same and different subnets.
6.  Analyzing ARP tables on all devices after pings.
7.  Observing packet captures (implied by ping packet tables) to understand MAC/IP addressing.
8.  Answering questions about MAC-IP addressing in pings and encapsulation changes across a router.

[]{#_Toc196771659 .anchor}Description of the steps

[]{#_Toc196771660 .anchor}1st Part:

A crossover UTP (Unshielded Twisted Pair) cable swaps transmit and receive wires, enabling direct connection between similar devices (e.g., PC to PC, switch to switch without auto-MDIX) without an intermediary device like a router or switch. This is useful for small or temporary setups.

A simplified router configuration sequence was performed.
Switch configuration included setting the hostname and IP for interface VLAN 1.
MAC addresses on devices were observed.

[]{#_Toc196771661 .anchor}2nd Part:

A network topology for Part 2 was established.
Ethernet port configurations and initial ARP table states for PC1, PC2, and Laptop were examined.

a. Which host addresses are listed in the SW1-1 MAC table?
SW1-1's MAC table would list MAC addresses of directly connected devices or those learned via frames passing through its ports. This typically includes PC1, R1 (interface connected to SW1-1), and SW1-2.

b. Are there switch ports that have more than one MAC address assigned and why?
Yes, a switch port connected to another switch (e.g., a trunk port or an access port leading to multiple devices via another switch) can learn multiple MAC addresses. It learns MACs of all devices reachable through that port. For instance, port Fa2/0/9, if connected to SW1-2, will learn MACs of devices behind SW1-2.

c. Is there a difference between the host addresses recorded in the ARP
table of PC1 and the MAC table of SW1-1, and why?
Yes, they differ:
*   **PC1's ARP table** maps IP addresses to MAC addresses for hosts on the *same IP subnet* PC1 has communicated with, or its default gateway's (R1) MAC if reaching other subnets.
*   **SW1-1's MAC address table** maps MAC addresses to its switch ports. It's a Layer 2 mapping, unaware of IP addresses, learned from source MACs of incoming frames.

ARP tables of all devices were checked after some network communication.
Pings were performed from PC1 to Laptop (same subnet) and from PC1 to PC2 (different subnets, via router).
The filled Ping Packet Addressing Tables (referencing `LW4 tables.md`) were considered.

a. What is the difference in MAC-IP addressing of two initial ping
packets?
When PC1 pings Laptop (same subnet, assuming Laptop's MAC is not in PC1's ARP cache):
*   **ARP Process:** PC1 broadcasts an ARP request for Laptop's IP. Laptop replies with its MAC.
*   **ICMP Echo Request:** PC1 sends the ping with Source IP: PC1's IP, Dest IP: Laptop's IP, Source MAC: PC1's MAC, Dest MAC: Laptop's MAC.

If PC1 pings PC2 (different subnet):
*   PC1 ARPs for its default gateway's (R1) MAC address (if not cached).
*   The ICMP Echo Request to PC2 has: Source IP: PC1's IP, Dest IP: PC2's IP, Source MAC: PC1's MAC, Dest MAC: R1's MAC (gateway).

b. How and why did the encapsulation of PC1->PC2 packet change from
initial departure to arrival at PC2?
The IP packet (Source IP: PC1, Destination IP: PC2) remains unchanged in its IP header. However, the encapsulating Ethernet frame changes at each Layer 2 hop:
1.  **PC1 to R1:** Source MAC: PC1's MAC; Destination MAC: R1's MAC (on PC1's subnet).
2.  **R1 to PC2:** R1 routes the packet and re-encapsulates it. Source MAC: R1's MAC (on PC2's subnet); Destination MAC: PC2's MAC (R1 ARPs for PC2's MAC if needed).
MAC addresses are local to each network segment. Routers decapsulate frames to read IP headers for routing and then re-encapsulate them with new Layer 2 headers for the next hop.

# Conclusion

This project provided practical experience configuring Cisco equipment, particularly Switches, and establishing a wired LAN. Wireshark was used to analyze ARP packets during network setup. Connectivity tests across subnets using ping verified Ethernet communication. The lab deepened understanding of Ethernet MAC/IP addressing interaction, the ARP process, and packet structure. A key takeaway was a clearer view of MAC-IP encapsulation and address resolution at the network level.
