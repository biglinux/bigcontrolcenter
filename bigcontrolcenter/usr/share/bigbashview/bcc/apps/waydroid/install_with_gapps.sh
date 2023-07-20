#!/usr/bin/env bash

if grep -q nvidia_drm <<< $(lsmod); then
	waydroid-big-3d 0
else
	waydroid-big-3d 1
fi
