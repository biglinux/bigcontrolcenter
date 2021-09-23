#!/bin/bash

#Translation
export TEXTDOMAINDIR="/usr/share/locale"
export TEXTDOMAIN=bigcontrolcenter


CATEGORY_Star=$"Principais"
CATEGORY_Design=$"Aparência"
CATEGORY_Hardware=$"Hardware"
CATEGORY_System=$"Sistema"
CATEGORY_Personalization=$"Personalização"
CATEGORY_Other=$"Outros"
SEARCH=$"Pesquisar..."
TITLE=$"Central de Controle"
CLOSE=$"Fechar"



OIFS=$IFS
IFS=$'\n'

##########################
#
#    ALL KCMSHELL5 OPEN AND APPS
#
##########################


rm -f "$HOME/.config/bigcontrolcenter/cache-.*.html"

parallel_search () {

    EXEC="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Exec)"

    if [ "$EXEC" = "" ]; then
        EXEC="kcmshell5 $(kreadconfig5 --file "$1" --group "Desktop Entry" --key X-KDE-Library)"
    fi
    EXEC="$(echo "$EXEC" | sed 's|kcm_||g')"
    NAME="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Name)"
    COMMENT="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Comment)"
    CATEGORY="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key X-KDE-System-Settings-Parent-Category)"
    ICON="$(kreadconfig5 --file "$1" --group "Desktop Entry" --key Icon)"

    if [ ! -e "$ICON" ]; then
        ICON="icons/${ICON}.png"
    fi


    if [ ! -e "$ICON" ]; then
        ICON_ORIG="$(./desktop-file.py "$1")"

        if [ "$(echo "$ICON_ORIG" | grep '.svg')" != "" ]; then
            ksvgtopng5 128 128 "$ICON_ORIG" "$HOME/.config/bigcontrolcenter/${ICON}"
            ICON="$HOME/.config/bigcontrolcenter/${ICON}"
        else
            ICON="$ICON_ORIG"
        fi

    fi

    if [ "$(echo "$CATEGORY" | grep -i "Star\|Design\|Hardware\|System\|Other\|Personalization")" = "" ]; then
        CATEGORY="Other"
    fi

    filename="$(echo "$1" | sed 's|.*/||g;s|\.desktop||g')"
    . files/$filename


       echo "<div class=\"col-md-2 box waves-effect waves-light $CATEGORY\"><a onclick=\"_run('./run.run $EXEC')\" class=\"tooltipped with-gap\" data-position=\"top\" data-delay=\"400\" data-tooltip=\"$COMMENT\">
            <p class=\"name\"><img src=\"$ICON\" width=38 height=38> $NAME</p>
            </center></a>
        </div>" >> "$HOME/.config/bigcontrolcenter/cache-$filename.html"

}

SERVICES="$(grep -Rl 'kcmshell5\|kcontrol' /usr/share/kservices5/ | grep -ve kcmdolphingeneral.desktop -ve kcmdolphinnavigation.desktop -ve kcmdolphinservices.desktop -ve kcmdolphinviewmodes.desktop -ve cache.desktop -ve cookies.desktop -ve kcmtrash.desktop -ve netpref.desktop -ve proxy.desktop -ve useragent.desktop -ve webshortcuts.desktop -ve kcm_ssl.desktop -ve bluedevildevices.desktop -ve bluedevilglobal.desktop -ve formats.desktop -ve camera.desktop -ve fontinst.desktop -ve powerdevilactivitiesconfig.desktop -ve kcm_plasmasearch.desktop -ve kcm_kdeconnect -ve kwinscreenedges.desktop -ve kwintouchscreen.desktop -ve keys.desktop -ve standard_actions.desktop -ve khotkeys.desktop -ve qtquicksettings.desktop -ve solid-actions -ve spellchecking.desktop -ve kwinactions.desktop -ve kwinfocus.desktop -ve kwinmoving.desktop -ve kwinoptions.desktop -ve kwinrules.desktop -ve kwinscripts.desktop -ve kwintabbox.desktop -ve breezestyleconfig.desktop -ve breezedecorationconfig.desktop -ve oxygenstyleconfig.desktop -ve oxygendecorationconfig -ve kcm_networkmanagement.desktop -ve kcm_pulseaudio -ve emoticons.desktop -ve kcm_nightcolor -ve kgamma.desktop -ve powerdevilglobalconfig.desktop -ve kwincompositing.desktop -ve kcmsmserver.desktop -ve kcmkded.desktop -ve kamera.desktop -ve kcm_kwin_virtualdesktops.desktop -ve powerdevilprofilesconfig.desktop -ve kcmperformance.desktop -ve kcmkonqyperformance.desktop -ve bookmarks.desktop -ve msm_user.desktop -ve kcm_kscreen.desktop -ve kcm_feedback.desktop -ve kcm_users.desktop -ve msm_kernel.desktop -ve kcm_kdisplay.desktop -ve msm_keyboard.desktop -ve msm_language_packages.desktop -ve msm_locale.desktop -ve msm_mhwd.desktop -ve kcm_lookandfeel.desktop -ve sierrabreezeenhancedconfig.desktop -ve msm_timedate.desktop -ve kcm_virtualkeyboard.desktop -ve lightlystyleconfig.desktop -ve lightlydecorationconfig.desktop -ve kcm_landingpage.desktop -ve libkcddb.desktop)"



    for i  in  $(echo "$SERVICES
/usr/share/applications/big-store.desktop
/usr/share/applications/org.manjaro.pamac.manager.desktop
/usr/share/kservices5/bigcontrolcenter/cmake-gui.desktop
/usr/share/kservices5/bigcontrolcenter/qv4l2.desktop
/usr/share/kservices5/bigcontrolcenter/cmake-gui.desktop
/usr/share/kservices5/bigcontrolcenter/org.gnome.baobab.desktop"); do

        if [ -e "$i" ]; then
            parallel_search "$i" &
        fi
        
    done


wait


IFS=$OIFS
