#!/bin/bash

python getappinfo.py $(./loop-search.sh | sed -E 's|.*/(.*).desktop|\1|g') android-usb ios-usb network-connect kcm_users timeshift-gtk biglinuxthemesgui
