#!/bin/bash

CONFIG_FILE="$1"
if [ -z "$CONFIG_FILE" ]; then
    echo "Usage: $0 /path/to/config_file"
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Config file not found!"
    exit 1
fi

# Parse Address_table
HOSTS_LINE=$(grep "^Host:" "$CONFIG_FILE" | head -n1)
IPS_LINE=$(grep "^IP_address:" "$CONFIG_FILE" | head -n1)
MASKS_LINE=$(grep "^Net_mask:" "$CONFIG_FILE" | head -n1)

HOSTS=($(echo "$HOSTS_LINE" | cut -d':' -f2))
IPS=($(echo "$IPS_LINE" | cut -d':' -f2))
MASKS=($(echo "$MASKS_LINE" | cut -d':' -f2))

if [ ${#HOSTS[@]} -ne ${#IPS[@]} ] || [ ${#HOSTS[@]} -ne ${#MASKS[@]} ]; then
    echo "Error: Address_table fields count mismatch."
    exit 1
fi

# Configure virtual interfaces
for i in "${!HOSTS[@]}"; do
    iface="dummy_$i"
    if ip link show "$iface" &>/dev/null; then
        echo "Interface $iface already exists, skipping creation."
    else
        sudo ip link add "$iface" type dummy
    fi
    sudo ip addr add "${IPS[i]}${MASKS[i]}" dev "$iface"
    sudo ip link set "$iface" up
done

# Parse Routing_table
ROUTE_NETWORK_LINE=$(grep "Network:" "$CONFIG_FILE" | head -n1)
ROUTE_MASK_LINE=$(grep "Mask" "$CONFIG_FILE" | head -n1)
ROUTE_GW_LINE=$(grep "Next_bench" "$CONFIG_FILE" | head -n1)

ROUTE_NETWORKS=($(echo "$ROUTE_NETWORK_LINE" | cut -d':' -f2))
ROUTE_MASKS=($(echo "$ROUTE_MASK_LINE" | cut -d':' -f2))
ROUTE_GWS=($(echo "$ROUTE_GW_LINE" | cut -d':' -f2))

if [ ${#ROUTE_NETWORKS[@]} -ne ${#ROUTE_MASKS[@]} ] || [ ${#ROUTE_NETWORKS[@]} -ne ${#ROUTE_GWS[@]} ]; then
    echo "Error: Routing_table fields count mismatch."
    exit 1
fi

# Configure routing table
for i in "${!ROUTE_NETWORKS[@]}"; do
    if [ "${ROUTE_NETWORKS[i]}" == "0.0.0.0" ]; then
        echo "Setting default route via ${ROUTE_GWS[i]}"
        sudo ip route add default via "${ROUTE_GWS[i]}"
    else
        echo "Adding route: ${ROUTE_NETWORKS[i]}${ROUTE_MASKS[i]} via ${ROUTE_GWS[i]}"
        sudo ip route add "${ROUTE_NETWORKS[i]}${ROUTE_MASKS[i]}" via "${ROUTE_GWS[i]}"
    fi
done

echo "Network configuration completed."
