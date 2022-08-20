#!/bin/bash

if [ "$(lsmod | grep nvidia_drm)" != "" ]; then
    waydroid-big-3d 0
else
    waydroid-big-3d 1
fi
