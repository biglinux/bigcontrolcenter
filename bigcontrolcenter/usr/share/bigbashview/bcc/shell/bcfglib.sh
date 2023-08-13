#!/usr/bin/env bash
#shellcheck disable=SC2155,SC2034
#shellcheck source=/dev/null

#  bccfglib.sh
#  Description: Control Center to help usage of BigLinux
#
#  Created: 2023/08/04
#  Altered: 2023/08/12
#
#  Copyright (c) 2023-2023, Vilmar Catafesta <vcatafesta@gmail.com>
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

LIBRARY=${LIBRARY:-'/usr/share/bigbashview/bcc/shell'}
[[ -f "${LIBRARY}/bcclib.sh" ]] && source "${LIBRARY}/bcclib.sh"

function sh_reset_brave {
	local result

	# Verifica se o processo está em execução (usando pidof) e se há um resultado não vazio.
	if result=$(pidof brave) && [[ -n $result ]]; then
		# Se estiver em execução, imprime o ID do processo e encerra o script.
		echo -n "$result"
		return
	fi
	cmdlogger rm -r ~/.config/BraveSoftware
	echo -n "#"
	return
}
export -f sh_reset_brave

function sh_reset_chromium {
	local result

	if result=$(pidof chromium) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/chromium
	cmdlogger rm -r ~/.config/chromium-optimize
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/chromium ~/.config/chromium
	fi
	echo -n "#"
	return
}
export -f sh_reset_chromium

function sh_reset_clementine {
	local result

	if result=$(pidof clementine) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/Clementine
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/Clementine ~/.config/Clementine
	fi
	echo -n "#"
	return
}
export -f sh_reset_clementine

function sh_reset_dolphin {
	local result

	if result=$(pidof dolphin) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi
	cmdlogger rm -r ~/.local/share/kxmlgui5/dolphin
	cmdlogger rm -r ~/.local/share/dolphin
	cmdlogger rm ~/.config/session/dolphin_dolphin_dolphin
	cmdlogger rm ~/.config/dolphinrc
	if [ "$1" = "skel" ]; then
		cmdlogger cp -f /etc/skel/.config/dolphinrc ~/.config/dolphinrc
		cmdlogger cp -r /etc/skel/.local/share/kxmlgui5/dolphin ~/.local/share/kxmlgui5/dolphin
	fi
	echo -n "#"
	return
}
export -f sh_reset_dolphin

function sh_reset_firefox {
	local result

	if result=$(pidof firefox) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.mozilla
	echo -n "#"
	return
}
export -f sh_reset_firefox

function sh_reset_gimp {
	local result

	if result=$(pidof gimp-2.10) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	rm -r ~/.config/GIMP
	if [ "$1" = "skel" ]; then
		cp -r /etc/skel/.config/GIMP ~/.config/GIMP
	fi
	echo -n "#"
	return
}
export -f sh_reset_gimp

function sh_reset_chrome {
	local result

	if result=$(pidof google-chrome) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi
	cmdlogger rm -r ~/.config/google-chrome
	echo -n "#"
	return
}
export -f sh_reset_chrome

function sh_reset_gwenview {
	local result

	if result=$(pidof gwenview) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.local/share/kxmlgui5/gwenview
	cmdlogger rm -r ~/.local/share/gwenview
	cmdlogger rm ~/.config/gwenviewrc
	if [[ "$1" = "skel" ]]; then
		cmdlogger cp -r /etc/skel/.local/share/kxmlgui5/gwenview ~/.local/share/kxmlgui5/gwenview
		cmdlogger cp -r /etc/skel/.local/share/gwenview ~/.local/share/gwenview
		cmdlogger cp -f /etc/skel/.config/gwenviewrc ~/.config/gwenviewrc
	fi
	echo -n "#"
	return
}
export -f sh_reset_gwenview

function sh_reset_inkscape {
	local result

	if result=$(pidof inkscape) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi
	cmdlogger rm -r ~/.config/inkscape
	echo -n "#"
	return
}
export -f sh_reset_inkscape

function sh_reset_kate {
	local result

	if result=$(pidof kate) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.local/share/kate
	cmdlogger rm -r ~/.local/share/kxmlgui5/kate
	cmdlogger rm -r ~/.local/share/kxmlgui5/katepart
	cmdlogger rm -r ~/.local/share/ktexteditor_snippets
	cmdlogger rm ~/.config/katevirc
	cmdlogger rm ~/.config/katemetainfos
	cmdlogger rm ~/.config/kateschemarc
	cmdlogger rm ~/.config/katesyntaxhighlightingrc
	cmdlogger rm ~/.config/katerc
	if [ "$1" = "skel" ]; then
		cmdlogger cp -f /etc/skel/.config/katevirc ~/.config/katevirc
		cmdlogger cp -f /etc/skel/.config/katemetainfos ~/.config/katemetainfos
		cmdlogger cp -f /etc/skel/.config/kateschemarc ~/.config/kateschemarc
		cmdlogger cp -f /etc/skel/.config/katesyntaxhighlightingrc ~/.config/katesyntaxhighlightingrc
		cmdlogger cp -f /etc/skel/.config/katerc ~/.config/katerc
		cmdlogger cp -r /etc/skel/.local/share/kate ~/.local/share/kate
		cmdlogger cp -r /etc/skel/.local/share/kxmlgui5/kate ~/.local/share/kxmlgui5/kate
		cmdlogger cp -r /etc/skel/.local/share/kxmlgui5/katepart ~/.local/share/kxmlgui5/katepart
		cmdlogger cp -r /etc/skel/.local/share/ktexteditor_snippets ~/.local/share/ktexteditor_snippets
	fi
	echo -n "#"
	return
}
export -f sh_reset_kate

function sh_reset_kde {
	local result

	if result=$(pidof dolphin) && [[ -n $result ]]; then
		kill -9 "$result"
		return
	fi

	#Remove(home) folders
	cmdlogger rm -r ~/.cache/*
	cmdlogger rm -r ~/.config/dconf
	cmdlogger rm -r ~/.config/gtk-3.0
	cmdlogger rm -r ~/.config/gtk-4.0
	cmdlogger rm -r ~/.config/KDE
	cmdlogger rm -r ~/.config/kde.org
	cmdlogger rm -r ~/.config/kdeconnect
	cmdlogger rm -r ~/.config/kdedefaults
	cmdlogger rm -r ~/.config/Kvantum
	cmdlogger rm -r ~/.config/latte
	cmdlogger rm -r ~/.config/pulse
	cmdlogger rm -r ~/.kdebiglinux
	cmdlogger rm -r ~/.local/share/kactivitymanagerd
	cmdlogger rm -r ~/.local/share/kcookiejar
	cmdlogger rm -r ~/.local/share/kded5
	cmdlogger rm -r ~/.local/share/knewstuff3
	cmdlogger rm -r ~/.local/share/konsole
	cmdlogger rm -r ~/.local/share/kpeoplevcard
	cmdlogger rm -r ~/.local/share/kscreen
	cmdlogger rm -r ~/.local/share/ksysguard
	cmdlogger rm -r ~/.local/share/kwalletd
	cmdlogger rm -r ~/.local/share/kwin
	cmdlogger rm -r ~/.local/share/kxmlgui5
	cmdlogger rm -r ~/.local/share/plasma_icons
	cmdlogger rm -r ~/.local/share/plasma

	#Remove(home) files
	cmdlogger rm ~/.bash_history
	cmdlogger rm ~/.bash_logout
	cmdlogger rm ~/.bashrc
	cmdlogger rm ~/.bash_profile
	cmdlogger rm ~/.big_desktop_theme
	cmdlogger rm ~/.big_performance
	cmdlogger rm ~/.big_preload
	cmdlogger rm ~/.gtkrc-2.0
	cmdlogger rm ~/.config/akregatorrc
	cmdlogger rm ~/.config/arkrc
	cmdlogger rm ~/.config/baloofileinformationrc
	cmdlogger rm ~/.config/baloofilerc
	cmdlogger rm ~/.config/bluedevilglobalrc
	cmdlogger rm ~/.config/breezerc
	cmdlogger rm ~/.config/drkonqirc
	cmdlogger rm ~/.config/gtkrc
	cmdlogger rm ~/.config/gtkrc-2.0
	cmdlogger rm ~/.config/latte
	cmdlogger rm ~/.config/kactivitymanagerdrc
	cmdlogger rm ~/.config/kcminputrc
	cmdlogger rm ~/.config/kconf_updaterc
	cmdlogger rm ~/.config/kded5rc
	cmdlogger rm ~/.config/kdeglobals
	cmdlogger rm ~/.config/kdialogrc
	cmdlogger rm ~/.config/kfontinstuirc
	cmdlogger rm ~/.config/kgammarc
	cmdlogger rm ~/.config/kglobalshortcutsrc
	cmdlogger rm ~/.config/khotkeysrc
	cmdlogger rm ~/.config/kiorc
	cmdlogger rm ~/.config/klaunchrc
	cmdlogger rm ~/.config/klassyrc
	cmdlogger rm ~/.config/kmenueditrc
	cmdlogger rm ~/.config/kmixrc
	cmdlogger rm ~/.local/share/krunnerstaterc
	cmdlogger rm ~/.config/kscreenlockerrc
	cmdlogger rm ~/.config/kservicemenurc
	cmdlogger rm ~/.config/ksmserverrc
	cmdlogger rm ~/.config/ksplashrc
	cmdlogger rm ~/.config/ksysguardrc
	cmdlogger rm ~/.config/ktimezonedrc
	cmdlogger rm ~/.config/kwalletrc
	cmdlogger rm ~/.config/kwinrc
	cmdlogger rm ~/.config/kwinrulesrc
	cmdlogger rm ~/.config/kxkbrc
	cmdlogger rm ~/.config/plasma-localerc
	cmdlogger rm ~/.config/plasma-nm
	cmdlogger rm ~/.config/plasma-org.kde.plasma.desktop-appletsrc
	cmdlogger rm ~/.config/plasma.emojierrc
	cmdlogger rm ~/.config/plasma_calendar_holiday_regions
	cmdlogger rm ~/.config/plasma_workspace.notifyrc
	cmdlogger rm ~/.config/plasmanotifyrc
	cmdlogger rm ~/.config/plasmarc
	cmdlogger rm ~/.config/plasmashellrc
	cmdlogger rm ~/.config/plasmavaultrc
	cmdlogger rm ~/.config/plasmawindowed-appletsrc
	cmdlogger rm ~/.config/plasmawindowedrc
	cmdlogger rm ~/.config/powerdevil.notifyrc
	cmdlogger rm ~/.config/powerdevilrc
	cmdlogger rm ~/.config/powermanagementprofilesrc
	cmdlogger rm ~/.config/spectaclerc
	cmdlogger rm ~/.config/systemmonitorrc
	cmdlogger rm ~/.config/systemsettingsrc
	cmdlogger rm ~/.config/Trolltech.conf
	cmdlogger rm ~/.config/xdg-desktop-portal-kderc
	cmdlogger rm ~/.local/share/RecentDocuments/*
	cmdlogger rm ~/.local/share/Trash/files/*

	#Copy(skel) folders
	cmdlogger cp -rf /etc/skel/.config ~
	cmdlogger cp -rf /etc/skel/.local ~
	cmdlogger cp -rf /etc/skel/.pje ~
	cmdlogger cp -rf /etc/skel/.pki ~

	#Copy(skel) files
	cmdlogger cp -f /etc/skel/.bash_logout ~
	cmdlogger cp -f /etc/skel/.bash_profile ~
	cmdlogger cp -f /etc/skel/.bashrc ~
	cmdlogger cp -f /etc/skel/.gtkrc-2.0 ~
	cmdlogger cp -f /etc/skel/.xinitrc ~

	#Default theme
	first-login-theme &>/dev/null

	#Compositing mode - based on biglinux-themes
	MODE="$(<$HOME/.big_performance)"
	if [ "$MODE" = "0" ]; then
		# Animation 0
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key AnimationSpeed 3
		kwriteconfig5 --file ~/.config/kdeglobals --group KDE --key AnimationDurationFactor ""
		kwriteconfig5 --file ~/.config/klaunchrc --group BusyCursorSettings --key Blinking false
		kwriteconfig5 --file ~/.config/klaunchrc --group BusyCursorSettings --key Bouncing true

		# Composition on
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key Enabled true

		# Opengl 2
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key GLCore false
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key Backend OpenGL
	else
		# Animation 2
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key AnimationSpeed 1
		kwriteconfig5 --file ~/.config/kdeglobals --group KDE --key AnimationDurationFactor 0.5
		kwriteconfig5 --file ~/.config/klaunchrc --group BusyCursorSettings --key Blinking true
		kwriteconfig5 --file ~/.config/klaunchrc --group BusyCursorSettings --key Bouncing false

		# Composition on
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key Enabled true

		# Opengl 2
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key GLCore false
		kwriteconfig5 --file ~/.config/kwinrc --group Compositing --key Backend OpenGL
	fi
	sleep 1
	echo -n "#"
	return
}
export -f sh_reset_kde

function sh_reset_konsole {
	local result

	if result=$(pidof konsole) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/konsole.knsrc
	cmdlogger rm -r ~/.config/konsolerc
	cmdlogger rm -r ~/.local/share/konsole
	cmdlogger rm -r ~/.local/share/kxmlgui5/konsole
	if [ "$1" = "skel" ]; then
		cmdlogger cp /etc/skel/.config/konsole.knsrc ~/.config/konsole.knsrc
		cmdlogger cp /etc/skel/.config/konsolerc ~/.config/konsolerc
		cmdlogger cp -r /etc/skel/.local/share/konsole ~/.local/share/konsole
	fi
	echo -n "#"
	return
}
export -f sh_reset_konsole

function sh_reset_ksnip {
	local result

	if result=$(pidof ksnip) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/ksnip
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/ksnip ~/.config/ksnip
	fi
	echo -n "#"
	return
}
export -f sh_reset_ksnip

function sh_reset_libreoffice {
	local result

	if result=$(pidof soffice.bin) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/libreoffice
	cmdlogger rm -r ~/.config/LanguageTool
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/libreoffice ~/.config/libreoffice
	fi
	echo -n "#"
	return
}
export -f sh_reset_libreoffice

function sh_reset_mystiq {
	local result

	if result=$(pidof mystiq) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/mystiq
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/mystiq ~/.config/mystiq
	fi
	echo -n "#"
	return
}
export -f sh_reset_mystiq

function sh_reset_okular {
	local result

	if result=$(pidof okular) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.local/share/kxmlgui5/okular
	cmdlogger rm -r ~/.local/share/okular
	cmdlogger rm ~/.config/okularpartrc
	cmdlogger rm ~/.config/okularrc
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.local/share/kxmlgui5/okular ~/.local/share/kxmlgui5/okular
		cmdlogger cp -f /etc/skel/.config/okularpartrc ~/.config/okularpartrc
		cmdlogger cp -f /etc/skel/.config/okularrc ~/.config/okularrc
	fi
	echo -n "#"
	return
}
export -f sh_reset_okular

function sh_reset_qbittorrent {
	local result

	if result=$(pidof qbittorrent) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/qBittorrent
	cmdlogger rm -r ~/.local/share/data/qBittorrent
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/qBittorrent ~/.config/qBittorrent
		cmdlogger cp -r /etc/skel/.local/share/data/qBittorrent ~/.local/share/data/qBittorrent
	fi
	echo -n "#"
	return
}
export -f sh_reset_qbittorrent

function sh_reset_smplayer {
	local result

	if result=$(pidof smplayer) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/smplayer
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/smplayer ~/.config/smplayer
	fi
	echo -n "#"
	return
}
export -f sh_reset_smplayer

function sh_reset_vokoscreenNG {
	local result

	if result=$(pidof vokoscreenNG) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/vokoscreenNG
	echo -n "#"
	return
}
export -f sh_reset_vokoscreenNG

function sh_reset_vlc {
	local result

	if result=$(pidof vlc) && [[ -n $result ]]; then
		echo -n "$result"
		return
	fi

	cmdlogger rm -r ~/.config/vlc
	if [ "$1" = "skel" ]; then
		cmdlogger cp -r /etc/skel/.config/vlc ~/.config/vlc
	fi
	echo -n "#"
	return
}
export -f sh_reset_vlc

function sh_reset_xfce {
	local result

	if result=$(pidof dolphin) && [[ -n $result ]]; then
		kill -9 "$result"
		return
	fi

	#Remove(home) folders
	cmdlogger rm -r ~/.cache/*
	cmdlogger mv ~/.config/xfce4 /tmp/./config/xfce4_backup

	#Remove(home) files
	cmdlogger rm ~/.bash_history
	cmdlogger rm ~/.bash_logout
	cmdlogger rm ~/.bashrc
	cmdlogger rm ~/.bash_profile
	cmdlogger rm ~/.big_desktop_theme
	cmdlogger rm ~/.big_performance
	cmdlogger rm ~/.big_preload
	cmdlogger rm ~/.local/share/RecentDocuments/*
	cmdlogger rm ~/.local/share/Trash/files/*

	#Copy(skel) folders
	cmdlogger cp -rf /etc/skel/.config ~
	cmdlogger cp -rf /etc/skel/.local ~
	cmdlogger cp -rf /etc/skel/.pje ~
	cmdlogger cp -rf /etc/skel/.pki ~

	#Copy(skel) files
	cmdlogger cp -f /etc/skel/.bash_logout ~
	cmdlogger cp -f /etc/skel/.bash_profile ~
	cmdlogger cp -f /etc/skel/.bashrc ~
	cmdlogger cp -f /etc/skel/.xinitrc ~

	sleep 1
	echo -n "#"
	return
}
export -f sh_reset_xfce

function sh_main {
   local execute_app="$1"
   local param_skel="$2"

   eval "$execute_app $param_skel"
   return
}

#sh_debug
sh_main "$@"
