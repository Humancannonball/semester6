Table of Contents

[Summary of Steps](#summary-of-steps) [1 Questions](#1-questions) [2
Description of the Steps Part 2](#2-description-of-the-steps-part-2) [3
Description of the Steps Part 3](#3-description-of-the-steps-part-3) [4
Conclusion](#4-conclusion)

# Summary of Steps

This lab introduced Cisco LAN equipment and basic router configuration. Key activities included:
1.  Answering theoretical questions about the Cisco 1941 router: application scenarios, port speeds, and physical layer standards.
2.  Connecting to a Cisco router via serial console using PuTTY.
3.  Navigating Cisco IOS CLI and using `show` commands to inspect router port status (`show ip interface brief`) and IOS version (`show version`).
4.  Configuring router interfaces (GigabitEthernet0/0, GigabitEthernet0/1) with IP addresses/subnet masks for two LAN subnets (LAN1, LAN2).
5.  Enabling interfaces (`no shutdown`).
6.  Verifying interface status post-configuration.
7.  Configuring PC IP addresses in each subnet (one via DHCP, one manually).
8.  Using Wireshark to observe DHCP packets.
9.  Testing Ethernet communication within and across subnets (inter-subnet routing via router) using ping.
10. Troubleshooting connectivity, noting potential firewall interference.

# 1 Questions

1\. What is Cisco 1941 and what application scenarios is it intended
for?
The Cisco 1941 is a modular Integrated Services Router (ISR G2) for small to medium-sized businesses and enterprise branch offices. It supports high-performance routing, secure WAN connectivity, and integrated services (voice, video, security, wireless). Common uses include secure branch office connectivity, internet access, VPN termination, and as a platform for network services.

2\. The Cisco 1941 has two Ethernet ports, as shown in Figure 3. Please
answer what is the maximum data transmission speed of these ports and
what physical layer media/standard is used in them?
The Cisco 1941 has two built-in Gigabit Ethernet (10/100/1000 Mbps) ports. Their maximum speed is 1 Gbps. They use twisted-pair copper cables (Cat5e/Cat6) with RJ-45 connectors, adhering to Ethernet standards like IEEE 802.3ab (1000BASE-T), operating at OSI Layers 1 and 2.

# 2 Description of the Steps Part 2 : Starting the PuTTY application,
selecting 'Serial' connection and correct COM port.

The PuTTY application was started, and a 'Serial' connection was established using the correct COM port.
The Cisco IOS CLI of the connected router was accessed.

Information about router ports and their status was checked using `show ip interface brief`. Initially, the line protocol for interfaces was down as they were not yet configured.

Information about the IOS version installed on the router was obtained using `show version`.

Steps to configure the router as an interconnecting device between LAN1 and LAN2:
Interfaces GigabitEthernet0/0 and GigabitEthernet0/1 were configured with IP addresses and subnet masks.
Each interface was then enabled using the `no shutdown` command.

After configuration, `show ip interface brief` confirmed that both interfaces were "up" and their protocol state was also "up", indicating successful activation.

By the end of this part, both GigabitEthernet0/0 and GigabitEthernet0/1 were configured with IP addresses and enabled, changing their status from "administratively down" to "up."

# 3 Description of the Steps Part 3 :

Two LAN subnets were practically implemented.
PC1's IP configuration was obtained via DHCP using `ipconfig /renew` (assuming a DHCP server was active on its subnet).
PC2 was manually configured with IP address 192.168.1.11, subnet mask 255.255.255.0, and default gateway 192.168.1.1.

Wireshark was used on a computer to capture and observe DHCP packets.

Ethernet communications were tested using ping:
- From PCs to demonstrate connectivity.
- From the router's PuTTY console to PCs in each subnet.

# 4 Conclusion

This lab provided practical experience in basic Cisco device configuration and wired LAN setup. Wireshark was used to analyze DHCP packets. Ethernet communication tests were conducted between different subnets and devices. Some configuration challenges, mainly due to PC firewalls, were encountered and troubleshooting methods were discussed. Overall, the lab offered a valuable opportunity to apply theoretical networking knowledge practically.
