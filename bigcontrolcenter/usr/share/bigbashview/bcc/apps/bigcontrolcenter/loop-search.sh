#!/usr/bin/env bash
#shellcheck disable=SC2155
#shellcheck source=/dev/null

#  usr/share/bigbashview/bcc/apps/bigcontrolcenter/loop-search.sh
#  Created: 2022/02/28
#  Altered: 2023/07/21
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

readonly APP="${0##*/}"
readonly _VERSION_="1.0.0-20230721"
readonly LIBRARY=${LIBRARY:-'/usr/share/bigbashview/bcc/shell'}
[[ -f "${LIBRARY}/bcclib.sh" ]] && source "${LIBRARY}/bcclib.sh"
trap 'printf "\n${red}Interrupted! exiting...\n"; cleanup; exit 0' INT TERM HUP

cleanup() {
	sh_info_msg "Removing temporary files..."
	[[ -e "$userpath/reload" ]] && rm -f "$userpath/reload"
	exit 1
}

function sh_config {
	#Translation
	export TEXTDOMAINDIR="/usr/share/locale"
	export TEXTDOMAIN=bigcontrolcenter
	declare -g userpath="$HOME/.config/bigcontrolcenter"
}

function sh_checkdir {
	[[ ! -d "$userpath" ]] && mkdir -p "$userpath"
}

function sh_kservices5_desktop_files {
	local filtered_files
	mapfile -t filtered_files < <(grep -Rl -E '(kcmshell5|control)' /usr/share/kservices5/ \
	| grep -ve 'kcmdolphingeneral.desktop' \
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
    -ve 'kcm_kscreen.desktop' \
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
	    'kcm_kdeconnect'
	    'kwinscreenedges.desktop'
	    'kwintouchscreen.desktop'
	    'keys.desktop'
	    'standard_actions.desktop'
	    'khotkeys.desktop'
	    'qtquicksettings.desktop'
	    'solid-actions'
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
	    'oxygendecorationconfig'
	    'kcm_pulseaudio'
	    'emoticons.desktop'
	    'kcm_nightcolor'
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
	    'kcm_kscreen.desktop'
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
    'system-config-printer.desktop'
    'msm_kde_notifier_settings.desktop'
    'mpv.desktop'
    'manjaro-settings-manager.desktop'
    'org.kde.kuserfeedback-console.desktop'
    'qvidcap.desktop'
    'kdesettings'
    'lstopo.desktop'
    'kdesystemsettings.desktop'
    'qv4l2.desktop')

	# Usando find para encontrar os arquivos e excluindo os arquivos da lista de exclusão
   mapfile -t filtered_files < <(find /usr/share/applications/bigcontrolcenter/ -type f ! \( -name "${excluded_files[0]}" $(printf -- "-o -name %s " "${excluded_files[@]:1}") \) -print0 | xargs -0)
   echo "${filtered_files[@]}"
}

function sh_static_desktop_files {
	local -a filtered_files=('/usr/share/applications/big-store.desktop' '/usr/share/applications/org.manjaro.pamac.manager.desktop' '/usr/share/kservices5/bigcontrolcenter/cmake-gui.desktop'
								'/usr/share/kservices5/bigcontrolcenter/qv4l2.desktop'
								'/usr/share/kservices5/bigcontrolcenter/org.gnome.baobab.desktop'
								'/usr/share/kservices5/bigcontrolcenter/biglinux-grub-restore.desktop'
								'/usr/share/applications/gsmartcontrol.desktop'
								'/usr/share/applications/org.kde.kdeconnect-settings.desktop'
								'/usr/share/applications/org.kde.dolphin.desktop'
								'/usr/share/applications/org.kde.konsole.desktop'
								'/usr/share/applications/guvcview.desktop'
								'/usr/share/applications/hplip.desktop')
	echo "${filtered_files[@]}"
}

function sh_get_config_value {
	local config_file="$1"
	local key="$2"
	local entry_group="Desktop Entry"
	kreadconfig5 --file "$config_file" --group "$entry_group" --key "$key"
}

parallel_search () {
    EXEC="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Exec)"
    if [ "$EXEC" = "" ]; then
        EXEC="kcmshell5 $(kreadconfig5 --file "$1" --group "Desktop Entry" --key X-KDE-Library)"
    fi
    EXEC="$(echo "$EXEC" | sed 's|kcm_||g;s|systemsettings|kcmshell5|g;s|%.*||g')"
    NAME="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Name)"
    COMMENT="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Comment)"
    CATEGORY="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key X-KDE-System-Settings-Parent-Category)"
    ICON="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Icon)"

    if [ ! -e "$ICON" ]; then
        ICON_ORIG1="$ICON"
        ICON="icons/${ICON}.png"
    fi
    if [ ! -e "$ICON" ]; then
        ICON_ORIG="$(geticons "$ICON_ORIG1")"
        ICON_ORIG_PNG="$(grep -i -m 1 "64x64.*png" <<< "$ICON_ORIG")"
        if [ ! -e "$ICON_ORIG_PNG" ]; then
            ICON_ORIG_SVG="$(grep -i -m 1 ".svg" <<< "$ICON_ORIG" | tail -1)"
            else
            ICON_ORIG="$ICON_ORIG_PNG"
        fi
        if [ -e "$ICON_ORIG_SVG" ]; then
            ksvgtopng5 64 64 "$ICON_ORIG_SVG" "$HOME/.config/bigcontrolcenter/${ICON_ORIG1}.png" &
            ICON="$HOME/.config/bigcontrolcenter/${ICON_ORIG1}.png"
        else
            ICON="$ICON_ORIG"
        fi
    fi
    if [ "$(echo "$CATEGORY" | grep -i "Star\|System\|Hardware\|Personalization\|Phone\|Multimedia\|Network\|Aplications\|Account\|Language\|Privacy\|Server\|About")" = "" ]; then
        CATEGORY="Other"
    fi
    filename="$(echo "$1" | sed 's|.*/||g;s|\.desktop||g')"
    . files/$filename
    if [ "$CATEGORY" = "Other" ]; then
        #kdialog --msgbox "$1 $EXEC"
        > "$HOME/.config/bigcontrolcenter/show_other"
    fi
cat << EOF >> "$HOME/.config/bigcontrolcenter/cache-$filename.html"
        <div class="box-1 box-2 box-3 box-4 box-5 box-items $CATEGORY">
        <div id="box-status-bar"><div id="tit-status-bar">$COMMENT</div>
        </div>
        <button onclick="_run('$EXEC')" id="box-subtitle" class="box-geral-icons box-geral-button"> <!-- class="status-button" CHAMA MODAL (POP-UP) -->
            <div class="box-imagem-icon"><img class="box-imagem-icon" src="$ICON" title="$NAME" alt="$NAME"></div>
            <div class="box-titulo">$NAME</div>
            <!--<div class="box-comentario">$COMMENT</div>-->
        </button>
    </div>
EOF
wait
}

# ALL KCMSHELL5 OPEN AND APPS
#############################
function sh_parallel_search {
	local config_file="$1"

	EXEC=$(sh_get_config_value "$config_file" "Exec")
	if [[ -z "$EXEC" ]]; then
		kde_library=$(sh_get_config_value "$config_file" "X-KDE-Library")
      EXEC="kcmshell5 $kde_library"
	fi
	EXEC=${EXEC//kcm_/}
	EXEC=${EXEC//systemsettings/kcmshell5}
	EXEC=${EXEC%%\%*}

	    NAME=$(sh_get_config_value "$config_file" "Name")
	 COMMENT=$(sh_get_config_value "$config_file" "Comment")
	CATEGORY=$(sh_get_config_value "$config_file" "X-KDE-System-Settings-Parent-Category")
   	 ICON=$(sh_get_config_value "$config_file" "Icon")

:<<'comment'
	if [[ ! -e "$ICON" ]]; then
	   ICON_ORIG1="$ICON"
	   ICON="icons/${ICON%.*}.png"
	fi
	if [[ ! -e "$ICON" ]]; then
	   ICON_ORIG=$(geticons "$ICON_ORIG1")
		ICON_ORIG_PNG="${ICON_ORIG/*64x64/}"
	   if [[ ! -e "$ICON_ORIG_PNG" ]]; then
			ICON_ORIG_SVG="${ICON_ORIG##*.svg}"
	   else
	      ICON_ORIG="$ICON_ORIG_PNG"
	   fi
	   if [[ -e "$ICON_ORIG_SVG" ]]; then
	      ksvgtopng5 64 64 "$ICON_ORIG_SVG" "$userpath/${ICON_ORIG1}.png" &
	      ICON="$userpath/${ICON_ORIG1}.png"
	   else
	      ICON="$ICON_ORIG"
	   fi
	fi
	case "$CATEGORY" in
	  *[Ss]tar* | *[Ss]ystem* | *[Hh]ardware* | *[Pp]ersonalization* | *[Pp]hone* | *[Mm]ultimedia* | *[Nn]etwork* | *[Aa]pplications* | *[Aa]ccount* | *[Ll]anguage* | *[Pp]rivacy* | *[Ss]erver* | *[Aa]bout* )
	    ;;
	  *)
	    CATEGORY="Other"
	    ;;
	esac

	filename="${1##*/}"
	filename="${filename%.desktop}"
	[[ -e files/"$filename" ]] && . files/"$filename"

	if [ "$CATEGORY" = "Other" ]; then
#	   if command -v kdialog &>/dev/null; then
#	      kdialog --msgbox "$1 $EXEC"
#	   fi
	   > "$userpath/show_other"
	fi
comment
	if [ ! -e "$ICON" ]; then
		ICON_ORIG1="$ICON"
		ICON="icons/${ICON}.png"
	fi

	if [ ! -e "$ICON" ]; then
		ICON_ORIG="$(geticons "$ICON_ORIG1")"
		ICON_ORIG_PNG="$(grep -i -m 1 "64x64.*png" <<< "$ICON_ORIG")"
		if [ ! -e "$ICON_ORIG_PNG" ]; then
			ICON_ORIG_SVG="$(grep -i -m 1 ".svg" <<< "$ICON_ORIG" | tail -1)"
		else
			ICON_ORIG="$ICON_ORIG_PNG"
		fi

		if [ -e "$ICON_ORIG_SVG" ]; then
			ksvgtopng5 64 64 "$ICON_ORIG_SVG" "$HOME/.config/bigcontrolcenter/${ICON_ORIG1}.png" &
			ICON="$HOME/.config/bigcontrolcenter/${ICON_ORIG1}.png"
		else
			ICON="$ICON_ORIG"
		fi
	fi

	case "$CATEGORY" in
	  *[Ss]tar* | *[Ss]ystem* | *[Hh]ardware* | *[Pp]ersonalization* | *[Pp]hone* | *[Mm]ultimedia* | *[Nn]etwork* | *[Aa]pplications* | *[Aa]ccount* | *[Ll]anguage* | *[Pp]rivacy* | *[Ss]erver* | *[Aa]bout* )
	    ;;
	  *)
	    CATEGORY="Other"
	    ;;
	esac

#	filename="$(echo "$1" | sed 's|.*/||g;s|\.desktop||g')"
	filename="${1##*/}"
	filename="${filename%.desktop}"
	[[ -e files/"$filename" ]] && . files/"$filename"

	if [ "$CATEGORY" = "Other" ]; then
		#if command -v kdialog &>/dev/null; then
			#kdialog --msgbox "$1 $EXEC"
		#fi
		> "$userpath/show_other"
	fi

cat <<-EOF > "$userpath/cache-$filename.html"
	<div class="box-1 box-2 box-3 box-4 box-5 box-items $CATEGORY">
	<div id="box-status-bar"><div id="tit-status-bar">
	$COMMENT
	</div>
	</div>
	<button onclick="_run('$EXEC')" id="box-subtitle" class="box-geral-icons box-geral-button"> <!-- class="status-button" CHAMA MODAL (POP-UP) -->
	<div class="box-imagem-icon"><img class="box-imagem-icon" src="$ICON" title="$NAME" alt="$NAME"></div>
	<div class="box-titulo">$NAME</div>
	<!--<div class="box-comentario">$COMMENT</div>-->
	</button>
	</div>
EOF
	wait
}

function sh_init {
	declare -a aAll_Desktop_files
	aAll_Desktop_files+=($(sh_kservices5_desktop_files))
	aAll_Desktop_files+=($(sh_apps_desktop_files))
	aAll_Desktop_files+=($(sh_bcc_desktop_files))
	aAll_Desktop_files+=($(sh_static_desktop_files))

	for i in "${aAll_Desktop_files[@]}"; do
		if [[ -e "$i" ]]; then
			sh_parallel_search "$i" &
		fi
	done
	wait
	[[ -e "$userpath/reload" ]] && rm -f "$userpath/reload"
}

#sh_debug
sh_config
sh_checkdir
sh_init
