#!/bin/bash

#Translation
export TEXTDOMAINDIR="/usr/share/locale"
export TEXTDOMAIN=bigcontrolcenter

OIFS=$IFS
IFS=$'\n'

##########################
#
#    ALL KCMSHELL5 OPEN AND APPS
#
##########################


rm -f "$HOME/.config/bigcontrolcenter/cache-.*.html"
rm -f "$HOME/.config/bigcontrolcenter/show_other"

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

}

SERVICES="$(grep -Rl 'kcmshell5\|kcontrol' /usr/share/kservices5/ | grep -ve kcmdolphingeneral.desktop -ve kcmdolphinnavigation.desktop -ve kcmdolphinservices.desktop -ve kcmdolphinviewmodes.desktop -ve cache.desktop -ve cookies.desktop -ve kcmtrash.desktop -ve netpref.desktop -ve proxy.desktop -ve useragent.desktop -ve webshortcuts.desktop -ve kcm_ssl.desktop -ve bluedevildevices.desktop -ve bluedevilglobal.desktop -ve formats.desktop -ve camera.desktop -ve fontinst.desktop -ve powerdevilactivitiesconfig.desktop -ve kcm_plasmasearch.desktop -ve kcm_kdeconnect -ve kwinscreenedges.desktop -ve kwintouchscreen.desktop -ve keys.desktop -ve standard_actions.desktop -ve khotkeys.desktop -ve qtquicksettings.desktop -ve solid-actions -ve spellchecking.desktop -ve kwinactions.desktop -ve kwinfocus.desktop -ve kwinmoving.desktop -ve kwinoptions.desktop -ve kwinrules.desktop -ve kwinscripts.desktop -ve kwintabbox.desktop -ve breezestyleconfig.desktop -ve breezedecorationconfig.desktop -ve oxygenstyleconfig.desktop -ve oxygendecorationconfig -ve kcm_pulseaudio -ve emoticons.desktop -ve kcm_nightcolor -ve kgamma.desktop -ve powerdevilglobalconfig.desktop -ve kwincompositing.desktop -ve kcmsmserver.desktop -ve kcmkded.desktop -ve kamera.desktop -ve kcm_kwin_virtualdesktops.desktop -ve powerdevilprofilesconfig.desktop -ve kcmperformance.desktop -ve kcmkonqyperformance.desktop -ve bookmarks.desktop -ve msm_user.desktop -ve kcm_kscreen.desktop -ve kcm_feedback.desktop -ve kcm_users.desktop -ve msm_kernel.desktop -ve kcm_kdisplay.desktop -ve msm_keyboard.desktop -ve msm_language_packages.desktop -ve msm_locale.desktop -ve msm_mhwd.desktop -ve kcm_lookandfeel.desktop -ve sierrabreezeenhancedconfig.desktop -ve msm_timedate.desktop -ve kcm_virtualkeyboard.desktop -ve lightlystyleconfig.desktop -ve lightlydecorationconfig.desktop -ve kcm_landingpage.desktop -ve libkcddb.desktop -ve kcm_solid_actions.desktop )"

SERVICES2="$(ls /usr/share/applications/kcm_*.desktop | grep -ve kcmdolphingeneral.desktop -ve kcmdolphinnavigation.desktop -ve kcmdolphinservices.desktop -ve kcmdolphinviewmodes.desktop -ve cache.desktop -ve cookies.desktop -ve kcmtrash.desktop -ve netpref.desktop -ve proxy.desktop -ve useragent.desktop -ve webshortcuts.desktop -ve kcm_ssl.desktop -ve bluedevildevices.desktop -ve bluedevilglobal.desktop -ve formats.desktop -ve camera.desktop -ve fontinst.desktop -ve powerdevilactivitiesconfig.desktop -ve kcm_plasmasearch.desktop -ve kcm_kdeconnect -ve kwinscreenedges.desktop -ve kwintouchscreen.desktop -ve keys.desktop -ve standard_actions.desktop -ve khotkeys.desktop -ve qtquicksettings.desktop -ve solid-actions -ve spellchecking.desktop -ve kwinactions.desktop -ve kwinfocus.desktop -ve kwinmoving.desktop -ve kwinoptions.desktop -ve kwinrules.desktop -ve kwinscripts.desktop -ve kwintabbox.desktop -ve breezestyleconfig.desktop -ve breezedecorationconfig.desktop -ve oxygenstyleconfig.desktop -ve oxygendecorationconfig -ve kcm_pulseaudio -ve emoticons.desktop -ve kcm_nightcolor -ve kgamma.desktop -ve powerdevilglobalconfig.desktop -ve kwincompositing.desktop -ve kcmsmserver.desktop -ve kcmkded.desktop -ve kamera.desktop -ve kcm_kwin_virtualdesktops.desktop -ve powerdevilprofilesconfig.desktop -ve kcmperformance.desktop -ve kcmkonqyperformance.desktop -ve bookmarks.desktop -ve msm_user.desktop -ve kcm_kscreen.desktop -ve kcm_feedback.desktop -ve kcm_users.desktop -ve msm_kernel.desktop -ve kcm_kdisplay.desktop -ve msm_keyboard.desktop -ve msm_language_packages.desktop -ve msm_locale.desktop -ve msm_mhwd.desktop -ve kcm_lookandfeel.desktop -ve sierrabreezeenhancedconfig.desktop -ve msm_timedate.desktop -ve kcm_virtualkeyboard.desktop -ve lightlystyleconfig.desktop -ve lightlydecorationconfig.desktop -ve kcm_landingpage.desktop -ve libkcddb.desktop -ve kcm_solid_actions.desktop)"


SERVICES3="$(ls /usr/share/applications/bigcontrolcenter/* | grep -ve timeshift-gtk.desktop -ve cups.desktop -ve htop.desktop -ve system-config-printer.desktop -ve msm_kde_notifier_settings.desktop -ve mpv.desktop -ve manjaro-settings-manager.desktop -ve org.kde.kuserfeedback-console.desktop -ve qvidcap.desktop -ve kdesettings -ve lstopo.desktop -ve kdesystemsettings.desktop -ve qv4l2.desktop)"

    for i  in  $(echo "$SERVICES
/usr/share/applications/big-store.desktop
/usr/share/applications/org.manjaro.pamac.manager.desktop
/usr/share/kservices5/bigcontrolcenter/cmake-gui.desktop
/usr/share/kservices5/bigcontrolcenter/qv4l2.desktop
/usr/share/kservices5/bigcontrolcenter/org.gnome.baobab.desktop
/usr/share/kservices5/bigcontrolcenter/biglinux-grub-restore.desktop
/usr/share/applications/gsmartcontrol.desktop
/usr/share/applications/org.kde.kdeconnect-settings.desktop
/usr/share/applications/org.kde.dolphin.desktop
/usr/share/applications/org.kde.konsole.desktop
/usr/share/applications/guvcview.desktop
$SERVICES2
$SERVICES3"); do

        if [ -e "$i" ]; then
            parallel_search "$i" &
        fi
        
    done


wait


IFS=$OIFS
