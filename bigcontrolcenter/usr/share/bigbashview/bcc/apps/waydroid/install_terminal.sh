#!/usr/bin/env bash
#shellcheck disable=SC2155,SC2034
#shellcheck source=/dev/null

#  /usr/share/bigbashview/bcc/apps/big-store/install_terminal.sh
#  Description: Big Store installing programs for BigLinux
#
#  Created: 2022/01/11
#  Altered: 2023/08/13
#
#  Copyright (c) 2023-2023, Vilmar Catafesta <vcatafesta@gmail.com>
#                2022-2023, Bruno Gonçalves <www.biglinux.com.br>
#                2022-2023, Rafael Ruscher <rruscher@gmail.com>
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
#  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

APP="${0##*/}"
_VERSION_="1.0.0-20230813"
LIBRARY=${LIBRARY:-'/usr/share/bigbashview/bcc/shell'}
#export BOOTLOG="/tmp/bigwaydroid-$USER-$(date +"%d%m%Y").log"
#export LOGGER='/dev/tty8'
#[[ -f "${LIBRARY}/bcclib.sh"  ]] && source "${LIBRARY}/bcclib.sh"
#[[ -f "${LIBRARY}/bstrlib.sh" ]] && source "${LIBRARY}/bstrlib.sh"

OIFS=$IFS
IFS=$'\n'

	MARGIN_TOP_MOVE="-90" WINDOW_HEIGHT=20 PID_BIG_DEB_INSTALLER="$$" WINDOW_ID="$WINDOW_ID" ./install_terminal_resize.sh &

	case "$ACTION" in
	"install")
		pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY KDE_SESSION_VERSION=5 KDE_FULL_SESSION=true ACTION=install /usr/share/bigbashview/bcc/apps/waydroid/install.sh
		kdialog --msgbox "ok"
		;;
	"install_gapps")
		pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY KDE_SESSION_VERSION=5 KDE_FULL_SESSION=true ACTION=install_gapps /usr/share/bigbashview/bcc/apps/waydroid/install.sh
		;;
	esac


if [ "$(xwininfo -id $WINDOW_ID 2>&1 | grep -i "No such window")" != "" ]; then
	kill -9 $PID_BIG_DEB_INSTALLER
	exit 0
fi

IFS=$OIFS
