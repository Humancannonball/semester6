**LAN Addressing Table**

| **Host** |          | **MAC address**   | **IP address** | **Switching port** |          |
| :------- | :------- | :---------------- | :------------- | :----------------- | :------- |
| **Name** | **Port** |                   |                | **Switch**         | **Port** |
| R1       | Gi0/0    | 6c-20-56-82-26-a0 | 192.168.1.1    | SW1-2              | Fa2/0/9  |
| R1       | Gi0/1    | 6c-20-56-82-26-a1 | 10.1.1.1       | SW2                | Fa1/1    |
| PC1      | Ethernet | 00-e0-4c-68-01-d2 | 192.168.1.5    | SW1-1              | Fa2/0/23 |
| PC2      | Ethernet | 00-e0-4c-68-00-e6 | 10.1.1.5       | SW2                | Fa0/0    |
| Laptop   | Ethernet | 40-c2-ba-82-94-67 | 192.168.1.4    | SW1-2              | Fa2/0/9  |

**Ping Packets Addressing Tables**

**Ping packet sent from PC1 to Laptop**

|             | Destination MAC      | Source MAC        | Source IP   | Destination IP |
| :---------- | :------------------- | :---------------- | :---------- | :------------- |
| Addresses:  | 40-c2-ba-82-09-40-67 | 00-e0-4c-68-01-d2 | 192.168.1.5 | 192.168.1.4  |
| Host:       | Laptop               | PC1               | PC1         | Laptop         |

**Ping packet sent from PC1 to PC2**

|             | Destination MAC     | Source MAC        | Source IP   | Destination IP |
| :---------- | :------------------ | :---------------- | :---------- | :------------- |
| Addresses:  | 6c-20-56-82-26-a0   | 00-e0-4c-68-01-d2 | 192.168.1.5 | 10.1.1.5       |
| Host:       | R1                  | PC1               | PC1         | PC2            |

**Ping packet from PC1 as received in PC2**

|             | Destination MAC     | Source MAC        | Source IP   | Destination IP |
| :---------- | :------------------ | :---------------- | :---------- | :------------- |
| Addresses:  | 00-e0-4c-68-00-e6   | 6c-20-56-82-26-a1 | 192.168.1.5 | 10.1.15        |
| Host:       | PC2                 | R1                | PC1         | PC2            |
