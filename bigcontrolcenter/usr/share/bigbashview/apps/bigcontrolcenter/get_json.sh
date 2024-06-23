#!/bin/bash

# If the first argument is "cache", then cache the json file
if [[ $1 = "cache" ]]; then
    python getappinfo.py $(./loop-search.sh | sed -E 's|.*/(.*).desktop|\1|g') android-usb ios-usb network-connect kcm_users timeshift-gtk big-themes-gui > ~/.cache/bigcontrolcenter.json
    rm ~/.cache/pre-cache-bigcontrolcenter.json
    exit
fi

# Wait for pre-cache file is deleted, if it is not deleted in 5 seconds, display without cache
for i in {1..50}; do
    if [ ! -f "$HOME/.cache/pre-cache-bigcontrolcenter.json" ]; then
        echo "$(< ~/.cache/bigcontrolcenter.json)"
        exit 0
    fi
    sleep 0.1
done

python getappinfo.py $(./loop-search.sh | sed -E 's|.*/(.*).desktop|\1|g') android-usb ios-usb network-connect kcm_users timeshift-gtk big-themes-gui
