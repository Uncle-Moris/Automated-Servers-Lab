# Don't place Shebang line here !!!

# Check for available network interfaces
INTERFACES=$(ls /sys/class/net)
echo "Available interfaces: $INTERFACES"

# Determine the right interface to configure
for INTERFACE in $INTERFACES; do
       if [[ "$INTERFACE" == "eth1" ]]; then
        TARGET_INTERFACE=$INTERFACE
       break
    fi
done

if [[ -z "$TARGET_INTERFACE" ]]; then
    echo "No suitable interface found. Exiting."
    exit 1
else
    echo "Configuring $TARGET_INTERFACE"
fi

# Configure static IP
echo "DEVICE=$TARGET_INTERFACE" > /etc/sysconfig/network-scripts/ifcfg-$TARGET_INTERFACE
echo "BOOTPROTO=static" >> /etc/sysconfig/network-scripts/ifcfg-$TARGET_INTERFACE
echo "ONBOOT=yes" >> /etc/sysconfig/network-scripts/ifcfg-$TARGET_INTERFACE
echo "IPADDR=$1" >> /etc/sysconfig/network-scripts/ifcfg-$TARGET_INTERFACE
echo "NETMASK=255.255.255.0" >> /etc/sysconfig/network-scripts/ifcfg-$TARGET_INTERFACE

# Restart network services
if systemctl is-active --quiet NetworkManager; then
    systemctl restart NetworkManager
else
    systemctl restart network
fi

# Set up port forwarding
iptables -t nat -A PREROUTING -p tcp --dport $2 -j REDIRECT --to-port 22

# Ensure iptables rules persist across reboots
iptables-save > /etc/sysconfig/iptables

echo "Network configuration and port forwarding have been set up on $TARGET_INTERFACE."

# Set up PasswordAuthentication to yes 
sudo sed -i 's/^#PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config


# Open 80 port

sudo firewall-cmd --zone=public --add-port=80/tcp --permanent
sudo firewall-cmd --reload

sudo systemctl restart sshd 