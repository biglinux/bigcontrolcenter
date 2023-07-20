#!/usr/bin/env bash

#Install
pamac-installer --build $1 &

# Fix installation in BBV window
PID="$!"
[[ "$PID" = "" ]] && exit

CONTADOR=0
while [ $CONTADOR -lt 100 ]; do
	if [ "$(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ")" != "" ]; then
		xsetprop -id=$(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ") --atom WM_TRANSIENT_FOR --value $(wmctrl -p -l -x | grep Waydroid$ | cut -f1 -d" ") -f 32x
		wmctrl -i -r $(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ") -b add,skip_pager,skip_taskbar
		wmctrl -i -r $(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ") -b toggle,modal
		break
	fi
	sleep 0.1
	let CONTADOR=CONTADOR+1
done
wait

pamac-installer waydroid waydroid-meta-x11 &
PID="$!"
[[ "$PID" = "" ]] && exit

CONTADOR=0
while [ $CONTADOR -lt 100 ]; do
	if [ "$(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ")" != "" ]; then
		xsetprop -id=$(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ") --atom WM_TRANSIENT_FOR --value $(wmctrl -p -l -x | grep Waydroid$ | cut -f1 -d" ") -f 32x
		wmctrl -i -r $(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ") -b add,skip_pager,skip_taskbar
		wmctrl -i -r $(wmctrl -p -l | grep -m1 " $PID " | cut -f1 -d" ") -b toggle,modal
		break
	fi
	sleep 0.1
	let CONTADOR=CONTADOR+1
done
wait

if [[ "$(lsmod | grep nvidia_drm)" != "" ]]; then
	waydroid-big-3d 0
else
	waydroid-big-3d 1
fi
