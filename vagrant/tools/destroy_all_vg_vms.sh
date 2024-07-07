vagrant global-status --prune | grep libvirt | awk '{print $1}' | xargs -I {} vagrant destroy -f {}
