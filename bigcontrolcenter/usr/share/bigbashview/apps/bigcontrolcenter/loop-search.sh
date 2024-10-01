#!/usr/bin/env bash
#shellcheck disable=SC2155
#shellcheck source=/dev/null

#  usr/share/bigbashview/bcc/apps/bigcontrolcenter/loop-search.sh
#  Created: 2022/02/28
#  Altered: 2023/09/02
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

function sh_kservices5_desktop_files {
	local filtered_files
	mapfile -t filtered_files < <(grep -Rl -E '(kcmshell6|control)' /usr/share/kservices5/ |
		grep -ve 'kcmdolphingeneral.desktop' \
			-ve 'kcmdolphinnavigation.desktop' \
			-ve 'kcmdolphinservices.desktop' \
			-ve 'kcmdolphinviewmodes.desktop' \
			-ve 'cache.desktop' \
			-ve 'cookies.desktop' \
			-ve 'kcmtrash.desktop' \
			-ve 'netpref.desktop' \
			-ve 'proxy.desktop' \
			-ve 'useragent.desktop' \
			-ve 'webshortcuts.desktop' \
			-ve 'kcm_ssl.desktop' \
			-ve 'bluedevildevices.desktop' \
			-ve 'bluedevilglobal.desktop' \
			-ve 'formats.desktop' \
			-ve 'camera.desktop' \
			-ve 'fontinst.desktop' \
			-ve 'powerdevilactivitiesconfig.desktop' \
			-ve 'kcm_plasmasearch.desktop' \
			-ve 'kcm_kdeconnect' \
			-ve 'kwinscreenedges.desktop' \
			-ve 'kwintouchscreen.desktop' \
			-ve 'keys.desktop' \
			-ve 'standard_actions.desktop' \
			-ve 'khotkeys.desktop' \
			-ve 'qtquicksettings.desktop' \
			-ve 'solid-actions' \
			-ve 'spellchecking.desktop' \
			-ve 'kwinactions.desktop' \
			-ve 'kwinfocus.desktop' \
			-ve 'kwinmoving.desktop' \
			-ve 'kwinoptions.desktop' \
			-ve 'kwinrules.desktop' \
			-ve 'kcm_kwin_scripts.desktop' \
			-ve 'kwintabbox.desktop' \
			-ve 'breezestyleconfig.desktop' \
			-ve 'breezedecorationconfig.desktop' \
			-ve 'oxygenstyleconfig.desktop' \
			-ve 'oxygendecorationconfig' \
			-ve 'kcm_pulseaudio' \
			-ve 'emoticons.desktop' \
			-ve 'kcm_nightcolor' \
			-ve 'kgamma.desktop' \
			-ve 'powerdevilglobalconfig.desktop' \
			-ve 'kwincompositing.desktop' \
			-ve 'kcmsmserver.desktop' \
			-ve 'kcmkded.desktop' \
			-ve 'kamera.desktop' \
			-ve 'kcm_kwin_virtualdesktops.desktop' \
			-ve 'powerdevilprofilesconfig.desktop' \
			-ve 'kcmperformance.desktop' \
			-ve 'kcmkonqyperformance.desktop' \
			-ve 'bookmarks.desktop' \
			-ve 'msm_user.desktop' \
			-ve 'kcm_feedback.desktop' \
			-ve 'kcm_users.desktop' \
			-ve 'msm_kernel.desktop' \
			-ve 'kcm_kdisplay.desktop' \
			-ve 'msm_keyboard.desktop' \
			-ve 'msm_language_packages.desktop' \
			-ve 'msm_locale.desktop' \
			-ve 'msm_mhwd.desktop' \
			-ve 'kcm_lookandfeel.desktop' \
			-ve 'sierrabreezeenhancedconfig.desktop' \
			-ve 'msm_timedate.desktop' \
			-ve 'kcm_virtualkeyboard.desktop' \
			-ve 'lightlystyleconfig.desktop' \
			-ve 'lightlydecorationconfig.desktop' \
			-ve 'kcm_landingpage.desktop' \
			-ve 'libkcddb.desktop' \
			-ve 'kcm_solid_actions.desktop' \
			-ve 'classikstyleconfig.desktop' \
			-ve 'classikdecorationconfig.desktop' \
			-ve 'klassydecorationconfig.desktop' \
			-ve 'plasma-applet-org.kde.plasma.bluetooth.desktop' \
			-ve 'klassystyleconfig.desktop')
	echo ${filtered_files[@]}
}

function sh_apps_desktop_files {
	local -a filtered_files
	# Array com os padrões de exclusão
	local excluded_files=(
		'kcmdolphingeneral.desktop'
		'kcmdolphinnavigation.desktop'
		'kcmdolphinservices.desktop'
		'kcmdolphinviewmodes.desktop'
		'cache.desktop'
		'cookies.desktop'
		'kcmtrash.desktop'
		'netpref.desktop'
		'proxy.desktop'
		'useragent.desktop'
		'webshortcuts.desktop'
		'kcm_ssl.desktop'
		'bluedevildevices.desktop'
		'bluedevilglobal.desktop'
		'formats.desktop'
		'camera.desktop'
		'fontinst.desktop'
		'powerdevilactivitiesconfig.desktop'
		'kcm_plasmasearch.desktop'
		'kcm_kdeconnect.desktop'
		'kwinscreenedges.desktop'
		'kwintouchscreen.desktop'
		'keys.desktop'
		'standard_actions.desktop'
		'khotkeys.desktop'
		'qtquicksettings.desktop'
		'solid-actions.desktop'
		'spellchecking.desktop'
		'kwinactions.desktop'
		'kwinfocus.desktop'
		'kwinmoving.desktop'
		'kwinrules.desktop'
		'kcm_kwin_scripts.desktop'
		'kwintabbox.desktop'
		'breezestyleconfig.desktop'
		'breezedecorationconfig.desktop'
		'oxygenstyleconfig.desktop'
		'oxygendecorationconfig.desktop'
		'kcm_pulseaudio.desktop'
		'emoticons.desktop'
		'kcm_nightcolor.desktop'
		'kgamma.desktop'
		'powerdevilglobalconfig.desktop'
		'kwincompositing.desktop'
		'kcmsmserver.desktop'
		'kcmkded.desktop'
		'kamera.desktop'
		'kcm_kwin_virtualdesktops.desktop'
		'powerdevilprofilesconfig.desktop'
		'kcmperformance.desktop'
		'kcmkonqyperformance.desktop'
		'bookmarks.desktop'
		'msm_user.desktop'
		'kcm_feedback.desktop'
		'kcm_users.desktop'
		'msm_kernel.desktop'
		'kcm_kdisplay.desktop'
		'msm_keyboard.desktop'
		'msm_language_packages.desktop'
		'msm_locale.desktop'
		'msm_mhwd.desktop'
		'kcm_lookandfeel.desktop'
		'sierrabreezeenhancedconfig.desktop'
		'msm_timedate.desktop'
		'kcm_virtualkeyboard.desktop'
		'lightlystyleconfig.desktop'
		'lightlydecorationconfig.desktop'
		'kcm_landingpage.desktop'
		'libkcddb.desktop'
		'kcm_solid_actions.desktop'
		'kcm_krunnersettings.desktop'
		'kcm_about-distro.desktop'
		'kcm_breezedecoration.desktop'
		'kcm_kwinxwayland.desktop'
		'kcm_keys.desktop'
		'kcm_powerdevilglobalconfig.desktop'
		'kcm_powerdevilactivitiesconfig.desktop'
		'kcm_fontinst.desktop'
		'kcm_printer_manager.desktop'
		'kcm_kwinrules.desktop'
		'kcm_kwintabbox.desktop'
		'kcm_qtquicksettings.desktop'
		'kcm_energyinfo.desktop'
		'kcm_kgamma.desktop'
		'kcm_klassydecoration.desktop'
		'kcm_wacomtablet.desktop'
		'kcm_netpref.desktop'
		'kcm_webshortcuts.desktop'
	)
	# Usando find para encontrar os arquivos desejados e excluindo os arquivos da lista de exclusão
	mapfile -t filtered_files < <(find /usr/share/applications/ -name "kcm_*.desktop" -type f ! \( -name "${excluded_files[0]}" $(printf -- "-o -name %s " "${excluded_files[@]:1}") \) -print0 | xargs -0)
	echo "${filtered_files[@]}"
}

function sh_bcc_desktop_files {
	local -a filtered_files
	# Array com os arquivos a serem excluídos
	local excluded_files=(
		'timeshift-gtk.desktop'
		'cups.desktop'
		'htop.desktop'
		'msm_kde_notifier_settings.desktop'
		'mpv.desktop'
		'manjaro-settings-manager.desktop'
		'org.kde.kuserfeedback-console.desktop'
		'qvidcap.desktop'
		'kdesettings'
		'lstopo.desktop'
		'kdesystemsettings.desktop'
		'qv4l2.desktop'
		'org.gnome.baobab.desktop'
		'klassy-settings.desktop'
	)

	# Usando find para encontrar os arquivos e excluindo os arquivos da lista de exclusão
	mapfile -t filtered_files < <(find /usr/share/applications/bigcontrolcenter/ -type f ! \( -name "${excluded_files[0]}" $(printf -- "-o -name %s " "${excluded_files[@]:1}") \) -print0 | xargs -0)
	echo "${filtered_files[@]}"
}

function sh_static_desktop_files {
	local -a filtered_files=(
		'/usr/share/applications/big-store.desktop'
		'/usr/share/applications/bigcontrolcenter/pavucontrol-qt.desktop'
		'/usr/share/applications/org.manjaro.pamac.manager.desktop'
		'/usr/share/kservices5/bigcontrolcenter/cmake-gui.desktop'
		'/usr/share/kservices5/bigcontrolcenter/qv4l2.desktop'
		'/usr/share/applications/biglinux-noise-reduction-pipewire.desktop'
		'/usr/share/applications/biglinux-grub-restore.desktop'
		'/usr/share/applications/gsmartcontrol.desktop'
		'/usr/share/applications/org.kde.kdeconnect-settings.desktop'
		'/usr/share/applications/org.kde.dolphin.desktop'
		'/usr/share/applications/org.kde.konsole.desktop'
		'/usr/share/applications/guvcview.desktop'
		'/usr/share/applications/hplip.desktop'
		'/usr/share/kservices5/smb.desktop'
		'/usr/share/applications/big-driver-manager.desktop'
		'/usr/share/applications/big-hardware-info.desktop'
		'/usr/share/applications/big-kernel-manager.desktop'
	)
	echo "${filtered_files[@]}"
}

function sh_main {
	local partial="$1"
	local -a aAll_Desktop_files

	if ! ((partial)); then
		aAll_Desktop_files+=($(sh_kservices5_desktop_files))
		aAll_Desktop_files+=($(sh_apps_desktop_files))
		aAll_Desktop_files+=($(sh_bcc_desktop_files))
		aAll_Desktop_files+=($(sh_static_desktop_files))

		for i in "${aAll_Desktop_files[@]}"; do
			if [[ -e "$i" ]]; then
				echo "$i"
			fi
		done
	fi
}

sh_main "$@" | sort -u
wait
