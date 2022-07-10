#!/bin/bash

pamac-installer --build waydroid waydroid-image-gapps
pamac-installer waydroid-meta-x11

if [ "$(lsmod | grep nvidia_drm)" != "" ]; then
    waydroid-big-3d 0
else
    waydroid-big-3d 1
fi
