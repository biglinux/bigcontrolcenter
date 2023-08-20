#!/usr/bin/env bash

if pacman -Q waydroid-image-gapps &>/dev/null; then
	pamac-installer --remove waydroid waydroid-meta-x11 waydroid-image-gapps waydroid-biglinux libgbinder python-gbinder
elif pacman -Q waydroid-image &>/dev/null; then
	pamac-installer --remove waydroid waydroid-meta-x11 waydroid-image waydroid-biglinux libgbinder python-gbinder
else
	pamac-installer --remove waydroid waydroid-meta-x11 waydroid-biglinux libgbinder python-gbinder
fi
# Remove images
rm -R /var/lib/waydroid/images/
rm /var/lib/waydroid/waydroid*
kill $(ps -aux | grep waydroid | grep container | awk '{print $2}')
