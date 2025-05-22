Table of Contents

[Summary of Steps [2](#summary-of-steps)](#summary-of-steps)

[1 Description of the steps
[2](#description-of-the-steps)](#description-of-the-steps)

[2 Questions [16](#questions)](#questions)

[3 Conclusion [16](#conclusion)](#conclusion)

# Summary of Steps

This lab focused on configuring routers for inter-subnet communication and implementing Network Address Translation (NAT). Key steps included:
1.  Initial configuration of R1 and R2 routers with specified IP addresses and interface settings.
2.  IP configuration for end devices (PC1, Laptop, PC2) in their respective subnets.
3.  Testing initial connectivity between terminals and router ports using pings.
4.  Documenting connectivity in a matrix, noting successes and failures based on subnet and switch connections.
5.  Configuring static routing on R1 for communication towards R2's subnet.
6.  Implementing NAT (PAT/overload) on R1 to allow private network devices (behind R1) to communicate with devices in R2's network using R1's external IP.
7.  Retesting connectivity after routing and NAT, updating the connectivity matrix.
8.  Analyzing ping packet headers with Wireshark to observe IP address changes due to NAT.
9.  Answering questions on NAT functionality and the choice of NAT overload.

# 1 Description of the steps

The lab involved configuring a network topology with two routers (R1, R2) and several end devices.

Initial configuration sequences were applied to R1 and R2. The IP interface status of both routers was checked post-configuration.

IP configurations for end devices were:
PC1: 172.16.1.3
Laptop: 172.16.1.4
PC2: 10.1.1.3

Connectivity tests between terminals and router ports were performed using ping commands from PC1, PC2, Laptop, R2, and R1.

Connectivity matrix (before R1 routing and NAT):

| **Terminal** | **IP address** | **PC1** | **Laptop** | **R1 Gi0/1** | **R1 Gi0/0** | **R2 Gi0/0** | **R2 Gi0/1** | **PC2** |
| :----------- | :------------- | :------ | :--------- | :----------- | :----------- | :----------- | :----------- | :------ |
| PC1          | 172.16.1.3     |         | YES        | YES          | YES          | NO           | NO           | NO      |
| Laptop       | 172.16.1.4     | YES     |            | YES          | YES          | NO           | NO           | NO      |
| R1 Gi0/1     | 172.16.1.1     | YES     | YES        |              | YES          | YES          | NO           | NO      |
| R1 Gi0/0     | 8.8.8.11       | YES     | YES        | YES          |              | YES          | NO           | NO      |
| R2 Gi0/0     | 8.8.8.22       | NO      | NO         | NO           | YES          |              | YES          | YES     |
| R2 Gi0/1     | 10.1.1.1       | NO      | NO         | NO           | YES          | YES          |              | YES     |
| PC2          | 10.1.1.3       | NO      | NO         | NO           | NO           | YES          | YES          |         |

Many pings were successful, but not all.
**Successful pings:**
- PC1 to Laptop (and vice-versa) as they are on the same switch.
- PC1/Laptop to R1 (and vice-versa) as they are on the same switch and subnet.

**Failed pings:**
- PC1/Laptop to R2 (and vice-versa) due to different subnets and lack of routing.
- PC1/Laptop to PC2 (and vice-versa) for the same reasons.
Successful pings occurred between devices on the same subnets and switches.

Additional configuration of R1 involved setting up a static route and NAT.
Pings were re-tested after these changes, from PC1 and Laptop to R2's interfaces and PC2.

It was noted that pings from Laptop to 10.1.1.3 (PC2) timed out, but Wireshark showed packets were being sent and received.
*Note: Ping timeouts can occur due to firewall settings on the destination PC, even if ICMP packets are successfully delivered and replies sent.*

Second connectivity matrix (after R1 routing and NAT):

| **Terminal** | **IP address** | **PC1** | **Laptop** | **R1 Gi0/1** | **R1 Gi0/0** | **R2 Gi0/0** | **R2 Gi0/1** | **PC2** |
| :----------- | :------------- | :------ | :--------- | :----------- | :----------- | :----------- | :----------- | :------ |
| PC1          | 172.16.1.3     |         | YES        | YES          | YES          | YES          | YES          | YES     |
| Laptop       | 172.16.1.4     | YES     |            | YES          | YES          | YES          | YES          | YES     |
| R1 Gi0/1     | 172.16.1.1     | YES     | YES        |              | YES          | YES          | YES          | YES     |
| R1 Gi0/0     | 8.8.8.11       | YES     | YES        | YES          |              | YES          | YES          | YES     |
| R2 Gi0/0     | 8.8.8.22       | NO      | NO         | NO           | YES          |              | YES          | YES     |
| R2 Gi0/1     | 10.1.1.1       | NO      | NO         | NO           | YES          | YES          |              | YES     |
| PC2          | 10.1.1.3       | YES     | YES        | YES          | YES          | YES          | YES          |         |
*Note: Connectivity from R2's networks to R1's internal network would require return routes on R2 or further NAT/firewall configurations, potentially explaining "NO" entries for R2 Gi0/0 and R2 Gi0/1 to PC1/Laptop if not specifically configured.*

After configuring static routing and NAT on R1, full connectivity between most devices was achieved. The default route allowed R1 to forward packets to R2, and NAT enabled communication between different subnets by translating internal IPs.

Ping packet analysis from PC1 to PC2:

**Outbound ping packet sent from PC1 to PC2 (before NAT by R1)**
The packet from PC1 (172.16.1.3) to PC2 (10.1.1.3) would initially have PC1's MAC as source and R1's Gi0/1 MAC as destination.

**Inbound ping packet from PC1, as received at PC2 (after NAT by R1)**
After R1 performs NAT, the source IP becomes R1's public IP (8.8.8.11). The source MAC would be R2's interface MAC connected to PC2's segment, and destination MAC PC2's MAC.

When PC1 pings PC2, R1 replaces PC1's source IP (172.16.1.3) with its public IP (8.8.8.11) due to NAT. PC2 thus sees the ping originating from 8.8.8.11.

# 2 Questions

1.  What is NAT and why did enabling it on the R1 router help with
    specific connectivity issues?

Network Address Translation (NAT) allows multiple devices on a local network to share a single public IP address for internet access. It translates private IP addresses of local devices to a public IP when sending data and reverses this for incoming responses.
Activating NAT on R1 resolved connectivity by enabling devices on the local network (PC1, Laptop) to communicate with devices on other subnets through R1's public IP.

2.  Why was the 'NAT overload' method chosen when programming the NAT
    functionality?

NAT overload (Port Address Translation - PAT) was chosen because it allows numerous devices on a local network to share a single public IP address efficiently. It uses unique port numbers to track connections for each internal device. This conserves public IP addresses and is cost-effective and scalable.

# 3 Conclusion

This lab aimed to connect two LANs via a simulated public internet connection, using NAT for IP address translation. It provided practical experience with advanced networking concepts and troubleshooting. Connectivity matrices were useful for understanding inter-subnet communication and how NAT resolves related issues.
