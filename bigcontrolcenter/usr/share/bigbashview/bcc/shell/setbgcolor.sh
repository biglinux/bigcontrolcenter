#!/bin/bash

if [ "$1" = "true" ]; then
    echo '1' > ~/.config/bigcontrolcenter_lightmode
else
    echo '0' > ~/.config/bigcontrolcenter_lightmode
fi
