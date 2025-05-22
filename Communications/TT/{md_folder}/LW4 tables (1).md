**LAN Addressing Table**

| **Host** |          | **MAC address**   | **IP address** | **Switching port** |         |
| :------- | :------- | :---------------- | :------------- | :----------------- | :------ |
| **Name** | **Port** |                   |                | **Switch**         | **Port**|
| R1       | Gi0/0    | 58bc.2728.8b03    | 192.168.1.1    | SW1-1              | Fa0/1   |
| R1       | Gi0/1    | 6c20.5682.26a0    | 10.1.1.1       | SW1-2              | Fa0/1   |
| PC1      | Ethernet | 00e0-4c68-0ld2    | 192.168.1.4    | SW1-1              | Fa0/10  |
| PC2      | Ethernet | 00e0-4c68-00e6    | 10.1.1.4       | SW1-2              | Fa0/10  |
| Laptop   | Ethernet | 70-08-94-17-23-e2 | 192.168.1.5    | SW2                | Fa0/31  |

**Ping Packets Addressing Tables**

**Ping packet sent from PC1 to Laptop**

|             | Destination MAC | Source MAC | Source IP | Destination IP |
| :---------- | :-------------- | :--------- | :-------- | :------------- |
| Addresses:  |                 |            |           |                |
| Host:       |                 |            |           |                |

**Ping packet sent from PC1 to PC2**

|             | Destination MAC | Source MAC | Source IP | Destination IP |
| :---------- | :-------------- | :--------- | :-------- | :------------- |
| Addresses:  |                 |            |           |                |
| Host:       |                 |            |           |                |

**Ping packet from PC1 as received in PC2**

|             | Destination MAC | Source MAC | Source IP | Destination IP |
| :---------- | :-------------- | :--------- | :-------- | :------------- |
| Addresses:  |                 |            |           |                |
| Host:       |                 |            |           |                |
