#!/usr/bin/env bash
#shellcheck disable=SC2155
#shellcheck source=/dev/null

#  usr/share/bigbashview/bcc/apps/bigcontrolcenter/loop-search.sh
#  Created: 2022/02/28
#  Altered: 2023/08/12
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
_VERSION_="1.0.0-20230812"
export BOOTLOG="/tmp/bigcontrolcenter-$USER-$(date +"%d%m%Y").log"
export LOGGER='/dev/tty8'
LIBRARY=${LIBRARY:-'/usr/share/bigbashview/bcc/shell'}
[[ -f "${LIBRARY}/bcclib.sh" ]] && source "${LIBRARY}/bcclib.sh"
trap 'printf "\n${red}Interrupted! exiting...\n"; cleanup; exit 0' INT TERM HUP

function cleanup {
	sh_info_msg "Removing temporary files..."
	[[ -e "$userpath/reload" ]] && cmdlogger rm -f "$userpath/reload"
	exit 1
}

function sh_config {
	#Translation
	export TEXTDOMAINDIR="/usr/share/locale"
	export TEXTDOMAIN=bigcontrolcenter
	declare -g userpath="$HOME/.config/bigcontrolcenter"
	declare -g userfilespath="$HOME/.config/bcc/files"
	declare -gA Afiles=(
		[big - welcome, NAME]=$"Introdução ao BigLinux"
		[big - welcome, COMMENT]=$"Introdução ao BigLinux"
		[big - welcome, ICON]="/usr/share/bigbashview/bcc/apps/big-welcome/icon-logo-biglinux.png"
		[big - welcome, CATEGORY]="Star"
		[big - welcome, EXEC]="big-welcome"
		[01example, NAME]=$"Integração com Google Drive e ownCloud"
		[01example, COMMENT]=$"Acesse seus arquivos que estão no Google Drive ou ownCloud diretamente no gerenciador de arquivos."
		[01example, ICON]="icons/kcm_kaccounts.png"
		[01example, CATEGORY]="Internet"
		[01example, EXEC]=""
		[appimagelaunchersettings, NAME]=$"Configurar o AppimageLauncher"
		[appimagelaunchersettings, COMMENT]=$"Escolher o comportamento dos programas disponibilizados em .appimage"
		[appimagelaunchersettings, ICON]=""
		[appimagelaunchersettings, CATEGORY]="System"
		[appimagelaunchersettings, EXEC]=""
		[assistant, NAME]=$"Qt Assistant"
		[assistant, COMMENT]=$"Programas de desenvolvimento para QT."
		[assistant, ICON]="icons/assistant.png"
		[assistant, CATEGORY]="Desenv"
		[assistant, EXEC]=""
		[audiocd, NAME]=$""
		[audiocd, COMMENT]=$"Configurações de uso dos antigos CDs de música, não são válidas para músicas em MP3."
		[audiocd, ICON]="icons/kcm_kaccounts.png"
		[audiocd, CATEGORY]="Multimedia"
		[audiocd, EXEC]=""
		[avahi-discover, NAME]=$"Procurar servidores (zeroconf)"
		[avahi-discover, COMMENT]=$""
		[avahi-discover, ICON]="icons/icon_find-server-zeroconf.png"
		[avahi-discover, CATEGORY]="Server"
		[avahi-discover, EXEC]=""
		[biglinux-config, NAME]=$"Restaurar a configuração de programas"
		[biglinux-config, COMMENT]="biglinux-config"
		[biglinux-config, ICON]="icons/icon-restaurar-configuracoes.png"
		[biglinux-config, CATEGORY]="System"
		[biglinux-config, EXEC]=""
		[biglinux-grub - restore, NAME]=$""
		[biglinux-grub - restore, COMMENT]=$"Utilitário que facilita a restauração do sistema instalado, principalmente a restauração do boot do sistema (Grub). Também pode ser utilizado para acessar o gerenciador de pacotes e o terminal do sistema instalado."
		[biglinux-grub - restore, ICON]=""
		[biglinux-grub - restore, CATEGORY]="System Star"
		[biglinux-grub - restore, EXEC]=""
		[biglinux-themes-gui, NAME]=$"Temas, Desktop e Ajustes"
		[biglinux-themes-gui, COMMENT]=$"Disponiblizamos configurações completas para você selecionar de forma extremamente simples."
		[biglinux-themes-gui, ICON]="icons/icon-aparencia-desempenho-usabilidade.png"
		[biglinux-themes-gui, CATEGORY]="Personalization"
		[biglinux-themes-gui, EXEC]=""
		[big-store, NAME]=$""
		[big-store, COMMENT]=$"Instalar ou remover programas."
		[big-store, ICON]="icons/icon-big-store.svg"
		[big-store, CATEGORY]="System"
		[big-store, EXEC]=""
		[bootsplash - manager, NAME]=$"Temas do Bootsplash"
		[bootsplash - manager, COMMENT]=$""
		[bootsplash - manager, ICON]="icons/bootsplash-manager-gui.png"
		[bootsplash - manager, CATEGORY]="Personalization"
		[bootsplash - manager, EXEC]=""
		[brightness - controller, NAME]=$"Brilho e cor"
		[brightness - controller, COMMENT]=$"Controle o brilho e as cores"
		[brightness - controller, ICON]="icons/brightness-adjust.svg"
		[brightness - controller, CATEGORY]="Hardware"
		[brightness - controller, EXEC]="brightness-controller"
		[bssh, NAME]=$"Procurar servidores SSH"
		[bssh, COMMENT]=$""
		[bssh, ICON]="icons/icon_find-server-SSH.png"
		[bssh, CATEGORY]="Server"
		[bssh, EXEC]=""
		[bvnc, NAME]=$"Procurar servidores VNC"
		[bvnc, COMMENT]=$""
		[bvnc, ICON]="icons/icon_find-server-VNC.png"
		[bvnc, CATEGORY]="Server"
		[bvnc, EXEC]=""
		[classikdecorationconfig, NAME]=$""
		[classikdecorationconfig, COMMENT]=$"Configurar este tema de borda de janelas"
		[classikdecorationconfig, ICON]=""
		[classikdecorationconfig, CATEGORY]="Personalization"
		[classikdecorationconfig, EXEC]=""
		[classikstyleconfig, NAME]=$""
		[classikstyleconfig, COMMENT]=$"Configurar este tema de janelas."
		[classikstyleconfig, ICON]=""
		[classikstyleconfig, CATEGORY]="Personalization"
		[classikstyleconfig, EXEC]=""
		[cmake-gui, NAME]=$""
		[cmake-gui, COMMENT]=$""
		[cmake-gui, ICON]=""
		[cmake-gui, CATEGORY]="Desenv"
		[cmake-gui, EXEC]=""
		[designer, NAME]=$"Qt Designer"
		[designer, COMMENT]=$"Programas de desenvolvimento para QT."
		[designer, ICON]="icons/QtProject-designer.png"
		[designer, CATEGORY]="Desenv"
		[designer, EXEC]=""
		[desktoppath, NAME]=$""
		[desktoppath, COMMENT]=$""
		[desktoppath, ICON]=""
		[desktoppath, CATEGORY]="Personalization"
		[desktoppath, EXEC]="kcmshell5 desktoppath"
		[emoticons, NAME]=$""
		[emoticons, COMMENT]=$""
		[emoticons, ICON]=""
		[emoticons, CATEGORY]="Personalization"
		[emoticons, EXEC]=""
		[gnome-alsamixer, NAME]=$"Gerenciador de áudio avançado - Alsamixer"
		[gnome-alsamixer, COMMENT]=$"Controlador de áudio em caso de ausência som."
		[gnome-alsamixer, ICON]="icons/audio-01.png"
		[gnome-alsamixer, CATEGORY]="Multimedia"
		[gnome-alsamixer, EXEC]="gnome-alsamixer"
		[gparted, NAME]=$"Particionar ou formatar"
		[gparted, COMMENT]=$"Cuidado, este programa poderá apagar todos os dados do computador."
		[gparted, ICON]="icons/gparted.png"
		[gparted, CATEGORY]="System"
		[gparted, EXEC]=""
		[gsmartcontrol, NAME]=$"Informações de armazenamento (SMART)"
		[gsmartcontrol, COMMENT]=$""
		[gsmartcontrol, ICON]="/usr/share/icons/hicolor/128x128/apps/gsmartcontrol.png"
		[gsmartcontrol, CATEGORY]="About"
		[gsmartcontrol, EXEC]=""
		[gufw, NAME]=$"Firewall"
		[gufw, COMMENT]=$"Configurar regras de segurança para a conexão com a internet."
		[gufw, ICON]="icons/gufw.png"
		[gufw, CATEGORY]="Privacy"
		[gufw, EXEC]="pkexec /usr/bin/gufw-pkexec root"
		[guvcview, NAME]=$"Configurar webcam ou placa de captura"
		[guvcview, COMMENT]=$""
		[guvcview, ICON]="icons/icon_webcam.png"
		[guvcview, CATEGORY]="Hardware"
		[guvcview, EXEC]=""
		[hardinfo, NAME]=$""
		[hardinfo, COMMENT]=$""
		[hardinfo, ICON]=""
		[hardinfo, CATEGORY]="About"
		[hardinfo, EXEC]=""
		[hplip, NAME]=$"Impressoras HP"
		[hplip, COMMENT]=$"Verificar o status, nível de tinta e manutenção."
		[hplip, ICON]="icons/icon_print-HP.png"
		[hplip, CATEGORY]="Hardware"
		[hplip, EXEC]=""
		[hp-uiscan, NAME]=$"Scanners HP"
		[hp-uiscan, COMMENT]=$""
		[hp-uiscan, ICON]="icons/icon_scanner-HP.png"
		[hp-uiscan, CATEGORY]="Hardware"
		[hp-uiscan, EXEC]=""
		[iDevice - Mounter, NAME]=$"Montar Hardware Apple"
		[iDevice - Mounter, COMMENT]=$"Com esse programa você pode acessar os programas do seu iPhone ou iPad Apple de forma similar ao acesso de arquivos em um pendrive."
		[iDevice - Mounter, ICON]=""
		[iDevice - Mounter, CATEGORY]="Phone"
		[iDevice - Mounter, EXEC]="idevice-mounter"
		[jamesdsp, NAME]=$"Equalizador (DSP)"
		[jamesdsp, COMMENT]=$""
		[jamesdsp, ICON]=""
		[jamesdsp, CATEGORY]="Multimedia"
		[jamesdsp, EXEC]=""
		[kcm_access, NAME]=$""
		[kcm_access, COMMENT]=$""
		[kcm_access, ICON]=""
		[kcm_access, CATEGORY]="Account"
		[kcm_access, EXEC]=""
		[kcmaccess, NAME]=$""
		[kcmaccess, COMMENT]=$""
		[kcmaccess, ICON]=""
		[kcmaccess, CATEGORY]="Account"
		[kcmaccess, EXEC]=""
		[kcm_activities, NAME]=$"Áreas de trabalho virtuais e atividades"
		[kcm_activities, COMMENT]=$"Crie mais de uma área de trabalho vitual alternando entre elas."
		[kcm_activities, ICON]=""
		[kcm_activities, CATEGORY]="Personalization"
		[kcm_activities, EXEC]="kcmshell5 kcm_kwin_virtualdesktops kcm_activities"
		[kcm_autostart, NAME]=$""
		[kcm_autostart, COMMENT]=$""
		[kcm_autostart, ICON]=""
		[kcm_autostart, CATEGORY]="Personalization"
		[kcm_autostart, EXEC]="kcmshell5 autostart kcmkded"
		[kcm_baloofile, NAME]=$""
		[kcm_baloofile, COMMENT]=$"Ativar a pesquisa aumenta o consumo de memória e processamento do sistema."
		[kcm_baloofile, ICON]=""
		[kcm_baloofile, CATEGORY]="System"
		[kcm_baloofile, EXEC]=""
		[kcm_bluetooth, NAME]=$""
		[kcm_bluetooth, COMMENT]=$""
		[kcm_bluetooth, ICON]=""
		[kcm_bluetooth, CATEGORY]="Hardware"
		[kcm_bluetooth, EXEC]=""
		[kcm_keys, ICON]="icons/preferences-desktop-keyboard-shortcuts.svg"
		[kcm_bolt, NAME]=$""
		[kcm_bolt, COMMENT]=$""
		[kcm_bolt, ICON]=""
		[kcm_bolt, CATEGORY]="Hardware"
		[kcm_bolt, EXEC]=""
		[kcm_clock, NAME]=$""
		[kcm_clock, COMMENT]=$"Ajuste a data, hora e fuso horário."
		[kcm_clock, ICON]=""
		[kcm_clock, CATEGORY]="Language"
		[kcm_clock, EXEC]="kcmshell5 msm_timedate clock"
		[kcm_colors, NAME]=$""
		[kcm_colors, COMMENT]=$""
		[kcm_colors, ICON]=""
		[kcm_colors, CATEGORY]="Personalization"
		[kcm_colors, EXEC]=""
		[kcm_componentchooser, NAME]=$""
		[kcm_componentchooser, COMMENT]=$""
		[kcm_componentchooser, ICON]=""
		[kcm_componentchooser, CATEGORY]="Personalization"
		[kcm_componentchooser, EXEC]=""
		[kcm_cursortheme, NAME]=$""
		[kcm_cursortheme, COMMENT]=$""
		[kcm_cursortheme, ICON]=""
		[kcm_cursortheme, CATEGORY]="Personalization"
		[kcm_cursortheme, EXEC]=""
		[kcm_desktoppaths, NAME]=$""
		[kcm_desktoppaths, COMMENT]=$""
		[kcm_desktoppaths, ICON]="icons/icon_find-localizacoes-directory.png"
		[kcm_desktoppaths, CATEGORY]="Personalization"
		[kcm_desktoppaths, EXEC]="kcmshell5 desktoppaths"
		[kcm_device_automounter, NAME]=$""
		[kcm_device_automounter, COMMENT]=$""
		[kcm_device_automounter, ICON]="icons/pendrive.svg"
		[kcm_device_automounter, CATEGORY]="Hardware"
		[kcm_device_automounter, EXEC]="kcmshell5 kcm_device_automounter kamera kcm_solid_actions"
		[kcm_filetypes, NAME]=$""
		[kcm_filetypes, COMMENT]=$""
		[kcm_filetypes, ICON]=""
		[kcm_filetypes, CATEGORY]="Personalization"
		[kcm_filetypes, EXEC]=""
		[kcm_firewall, NAME]=$""
		[kcm_firewall, COMMENT]=$""
		[kcm_firewall, ICON]=""
		[kcm_firewall, CATEGORY]="Privacy"
		[kcm_firewall, EXEC]=""
		[kcm_fonts, NAME]=$""
		[kcm_fonts, COMMENT]=$""
		[kcm_fonts, ICON]=""
		[kcm_fonts, CATEGORY]="Personalization"
		[kcm_fonts, EXEC]="kcmshell5 kcm_fonts fontinst"
		[kcm_icons, NAME]=$"Ícones e emoticons"
		[kcm_icons, COMMENT]=$""
		[kcm_icons, ICON]=""
		[kcm_icons, CATEGORY]="Personalization"
		[kcm_icons, EXEC]="kcmshell5 kcm_icons emoticons"
		[kcm_joystick, NAME]=$"Joystick"
		[kcm_joystick, COMMENT]=$""
		[kcm_joystick, ICON]=""
		[kcm_joystick, CATEGORY]="Hardware"
		[kcm_joystick, EXEC]=""
		[kcm_kaccounts, NAME]=$"Integração com Google Drive e ownCloud"
		[kcm_kaccounts, COMMENT]=$"Acesse seus arquivos que estão no Google Drive ou ownCloud diretamente no gerenciador de arquivos."
		[kcm_kaccounts, ICON]="icons/kcm_kaccounts.png"
		[kcm_kaccounts, CATEGORY]="Network"
		[kcm_kaccounts, EXEC]="kcmshell5 kcm_kaccounts"
		[kcm_kded, NAME]=$""
		[kcm_kded, COMMENT]=$""
		[kcm_kded, ICON]=""
		[kcm_kded, CATEGORY]="Personalization"
		[kcm_kded, EXEC]=""
		[kcm_keyboard, NAME]=$""
		[kcm_keyboard, COMMENT]=$"Configurações de layout, teclas de atalho e outras opções."
		[kcm_keyboard, ICON]=""
		[kcm_keyboard, CATEGORY]="Hardware"
		[kcm_keyboard, EXEC]="kcmshell5 msm_keyboard keyboard keys standard_actions khotkeys"
		[kcm_kscreen, NAME]=$""
		[kcm_kscreen, COMMENT]=$""
		[kcm_kscreen, ICON]=""
		[kcm_kscreen, CATEGORY]="Hardware"
		[kcm_kscreen, EXEC]="kcmshell5 kcm_kscreen kcm_nightcolor kgamma kwintouchscreen kwinscreenedges"
		[kcm_kwindecoration, NAME]=$""
		[kcm_kwindecoration, COMMENT]=$""
		[kcm_kwindecoration, ICON]=""
		[kcm_kwindecoration, CATEGORY]="Personalization"
		[kcm_kwindecoration, EXEC]="kcmshell5 kwindecoration"
		[kcm_kwin_effects, NAME]=$""
		[kcm_kwin_effects, COMMENT]=$""
		[kcm_kwin_effects, ICON]=""
		[kcm_kwin_effects, CATEGORY]="Personalization"
		[kcm_kwin_effects, EXEC]="kcmshell5 kwincompositing kcm_kwin_effects"
		[kcm_kwinoptions, NAME]=$""
		[kcm_kwinoptions, COMMENT]=$""
		[kcm_kwinoptions, ICON]=""
		[kcm_kwinoptions, CATEGORY]="Personalization"
		[kcm_kwinoptions, EXEC]="kcmshell5 kcm_kwinactions kcm_kwinadvanced kcm_kwinfocus kcm_kwinmoving kcm_kwintabbox kcm_kwinoptions kcm_kwinrules kcm_kwin_scripts kcm_kwintabbox"
		[kcm_launchfeedback, NAME]=$""
		[kcm_launchfeedback, COMMENT]=$""
		[kcm_launchfeedback, ICON]=""
		[kcm_launchfeedback, CATEGORY]="Personalization"
		[kcm_launchfeedback, EXEC]=""
		[kcm_mouse, NAME]=$""
		[kcm_mouse, COMMENT]=$""
		[kcm_mouse, ICON]=""
		[kcm_mouse, CATEGORY]="Hardware"
		[kcm_mouse, EXEC]="kcmshell5 mouse kcm_workspace"
		[kcm_networkmanagement, NAME]=$"Gerenciar conexões"
		[kcm_networkmanagement, COMMENT]=$"Configuração avançada de rede (VPN, wifi, cabeada, IP fixo, PPPoE, ADSL, rede com fio, banda larga móvel e outros)."
		[kcm_networkmanagement, ICON]="icons/icon_gerenciar-conexoes.png"
		[kcm_networkmanagement, CATEGORY]="Network Star"
		[kcm_networkmanagement, EXEC]="kcmshell5 kcm_networkmanagement"
		[kcm_nightcolor, NAME]=$""
		[kcm_nightcolor, COMMENT]=$""
		[kcm_nightcolor, ICON]=""
		[kcm_nightcolor, CATEGORY]="Hardware"
		[kcm_nightcolor, EXEC]=""
		[kcm_notifications, NAME]=$""
		[kcm_notifications, COMMENT]=$""
		[kcm_notifications, ICON]=""
		[kcm_notifications, CATEGORY]="Privacy"
		[kcm_notifications, EXEC]=""
		[kcm_plymouth, NAME]=$""
		[kcm_plymouth, COMMENT]=$""
		[kcm_plymouth, ICON]="icons/kcm_kaccounts.png"
		[kcm_plymouth, CATEGORY]="Account"
		[kcm_plymouth, EXEC]=""
		[kcm_printer_manager, NAME]=$"Impressoras"
		[kcm_printer_manager, COMMENT]=$"Instalar, configurar ou remover impressoras."
		[kcm_printer_manager, ICON]="icons/icon_print.png"
		[kcm_printer_manager, CATEGORY]="Star Hardware"
		[kcm_printer_manager, EXEC]="system-config-printer"
		[kcm_recentFiles, NAME]=$""
		[kcm_recentFiles, COMMENT]=$""
		[kcm_recentFiles, ICON]=""
		[kcm_recentFiles, CATEGORY]="Personalization"
		[kcm_recentFiles, EXEC]=""
		[kcm_regionandlang, NAME]=$""
		[kcm_regionandlang, COMMENT]=$""
		[kcm_regionandlang, ICON]="icons/icon-multiple-language.svg"
		[kcm_regionandlang, CATEGORY]="Language"
		[kcm_regionandlang, EXEC]="kcmshell5 regionandlang msm_language_packages formats translations"
		[kcm_screenlocker, NAME]=$""
		[kcm_screenlocker, COMMENT]=$""
		[kcm_screenlocker, ICON]=""
		[kcm_screenlocker, CATEGORY]="Personalization"
		[kcm_screenlocker, EXEC]="kcmshell5 kcm_screenlocker"
		[kcm_sddm, NAME]=$""
		[kcm_sddm, COMMENT]=$""
		[kcm_sddm, ICON]=""
		[kcm_sddm, CATEGORY]="Personalization"
		[kcm_sddm, EXEC]=""
		[kcm_smserver, NAME]=$""
		[kcm_smserver, COMMENT]=$""
		[kcm_smserver, ICON]="icons/icon_sessao-area-de-trabalho.png"
		[kcm_smserver, CATEGORY]="Personalization"
		[kcm_smserver, EXEC]="kcmshell5 kcm_smserver"
		[kcm_splashscreen, NAME]=$""
		[kcm_splashscreen, COMMENT]=$""
		[kcm_splashscreen, ICON]=""
		[kcm_splashscreen, CATEGORY]="Personalization"
		[kcm_splashscreen, EXEC]=""
		[kcm_style, NAME]=$""
		[kcm_style, COMMENT]=$""
		[kcm_style, ICON]=""
		[kcm_style, CATEGORY]="Personalization"
		[kcm_style, EXEC]=""
		[kcm_systemd, NAME]=$"Gerenciar serviços (Systemd)"
		[kcm_systemd, COMMENT]=$""
		[kcm_systemd, ICON]=""
		[kcm_systemd, CATEGORY]="System"
		[kcm_systemd, EXEC]=""
		[kcm_tablet, NAME]=$""
		[kcm_tablet, COMMENT]=$""
		[kcm_tablet, ICON]=""
		[kcm_tablet, CATEGORY]="Hardware"
		[kcm_tablet, EXEC]=""
		[kcm_touchpad, NAME]=$""
		[kcm_touchpad, COMMENT]=$""
		[kcm_touchpad, ICON]=""
		[kcm_touchpad, CATEGORY]="Hardware"
		[kcm_touchpad, EXEC]="kcmshell5 touchpad"
		[kcm_touchscreen, NAME]=$""
		[kcm_touchscreen, COMMENT]=$""
		[kcm_touchscreen, ICON]=""
		[kcm_touchscreen, CATEGORY]="Hardware"
		[kcm_touchscreen, EXEC]=""
		[kcm_trash, NAME]=$"Lixeira"
		[kcm_trash, COMMENT]=$""
		[kcm_trash, ICON]="icons/user-trash.svg"
		[kcm_trash, CATEGORY]="System"
		[kcm_trash, EXEC]=""
		[kcm_wacomtablet, NAME]=$""
		[kcm_wacomtablet, COMMENT]=$""
		[kcm_wacomtablet, ICON]=""
		[kcm_wacomtablet, CATEGORY]="Hardware"
		[kcm_wacomtablet, EXEC]=""
		[kcm_workspace, NAME]=$""
		[kcm_workspace, COMMENT]=$""
		[kcm_workspace, ICON]=""
		[kcm_workspace, CATEGORY]="Personalization"
		[kcm_workspace, EXEC]=""
		[kvantummanager, NAME]=$"Configurar o tema Kvantum"
		[kvantummanager, COMMENT]=$"Para a configuração do Kvantum funcionar, aplique o tema Kvantum em 'Estilo do aplicativo'."
		[kvantummanager, ICON]="icons/kvantum.png"
		[kvantummanager, CATEGORY]="Personalization"
		[kvantummanager, EXEC]=""
		[kwalletconfig5, NAME]=$"Carteira de senhas do KDE"
		[kwalletconfig5, COMMENT]=$""
		[kwalletconfig5, ICON]=""
		[kwalletconfig5, CATEGORY]="Privacy"
		[kwalletconfig5, EXEC]="kcmshell5 kwalletconfig5"
		[kwinadvanced, NAME]=$""
		[kwinadvanced, COMMENT]=$""
		[kwinadvanced, ICON]=""
		[kwinadvanced, CATEGORY]="Personalization"
		[kwinadvanced, EXEC]="kcmshell5 kwinactions kwinadvanced kwinfocus kwinmoving kwinoptions kwinrules kwinscripts kwintabbox"
		[kwindecoration, NAME]=$""
		[kwindecoration, COMMENT]=$""
		[kwindecoration, ICON]=""
		[kwindecoration, CATEGORY]="Personalization"
		[kwindecoration, EXEC]="kcmshell5 kwindecoration classikdecorationconfig"
		[linguist, NAME]=$"Qt Linguist"
		[linguist, COMMENT]=$"Programas de desenvolvimento para QT."
		[linguist, ICON]="icons/linguist.png"
		[linguist, CATEGORY]="Desenv"
		[linguist, EXEC]=""
		[lstopo, NAME]=$""
		[lstopo, COMMENT]=$""
		[lstopo, ICON]=""
		[lstopo, CATEGORY]="About"
		[lstopo, EXEC]=""
		[mintstick - format - kde, NAME]=$""
		[mintstick - format - kde, COMMENT]=$""
		[mintstick - format - kde, ICON]="icons/pendrive-format.svg"
		[mintstick - format - kde, CATEGORY]="System"
		[mintstick - format - kde, EXEC]=""
		[mintstick - kde, NAME]=$""
		[mintstick - kde, COMMENT]=$""
		[mintstick - kde, ICON]="icons/pendrive-image-recorder.svg"
		[mintstick - kde, CATEGORY]="System"
		[mintstick - kde, EXEC]=""
		[msm_users, NAME]=$"Gerenciador de usuários"
		[msm_users, COMMENT]=$"Adiciona, remove ou edita usuários e grupos do sistema."
		[msm_users, ICON]="icons/icon_useraccount.png"
		[msm_users, CATEGORY]="Other"
		[msm_users, EXEC]=""
		[org.gnome.baobab, NAME]=$""
		[org.gnome.baobab, COMMENT]=$""
		[org.gnome.baobab, ICON]=""
		[org.gnome.baobab, CATEGORY]="System"
		[org.gnome.baobab, EXEC]="baobab"
		[org.kde.dolphin, NAME]=$"Gerenciar arquivos"
		[org.kde.dolphin, COMMENT]=$"Tenha acesso a seus arquivos e pastas."
		[org.kde.dolphin, ICON]="icons/system-file-manager.png"
		[org.kde.dolphin, CATEGORY]="System"
		[org.kde.dolphin, EXEC]="dolphin"
		[org.kde.filelight, NAME]=$"Uso de armazenamento"
		[org.kde.filelight, COMMENT]=$""
		[org.kde.filelight, ICON]=""
		[org.kde.filelight, CATEGORY]="System"
		[org.kde.filelight, EXEC]=""
		[org.kde.kdeconnect - settings, NAME]=$"KDE Connect"
		[org.kde.kdeconnect - settings, COMMENT]=$"Esse programa pode transferir arquivos entre smartphones, tablets e outros computadores.  Com ele você pode, por exemplo, utilizar  seu smartphone como mouse e teclado sem fio para controlar o computador, entre outros recursos.  Ele se integra melhor ao BigLinux e fica entre os applets localizados perto do relógio do sistema. Para sincronizar com o seu smartphone acesse a Google Store ou Apple Store e instale o Kde Connect."
		[org.kde.kdeconnect - settings, ICON]="icons/preferences-kde-connect.png"
		[org.kde.kdeconnect - settings, CATEGORY]="Phone"
		[org.kde.kdeconnect - settings, EXEC]=""
		[org.kde.kinfocenter, NAME]=$""
		[org.kde.kinfocenter, COMMENT]=$""
		[org.kde.kinfocenter, ICON]=""
		[org.kde.kinfocenter, CATEGORY]="About"
		[org.kde.kinfocenter, EXEC]=""
		[org.kde.konsole, NAME]=$"Terminal"
		[org.kde.konsole, COMMENT]=$"Acesse o terminal de comandos."
		[org.kde.konsole, ICON]="icons/terminal.png"
		[org.kde.konsole, CATEGORY]="System"
		[org.kde.konsole, EXEC]=""
		[org.kde.ksystemlog, NAME]=$""
		[org.kde.ksystemlog, COMMENT]=$""
		[org.kde.ksystemlog, ICON]=""
		[org.kde.ksystemlog, CATEGORY]="System About"
		[org.kde.ksystemlog, EXEC]=""
		[org.kde.kwalletmanager5, NAME]=$"Gerenciador de senhas"
		[org.kde.kwalletmanager5, COMMENT]=$""
		[org.kde.kwalletmanager5, ICON]="icons/icone_password-manager.svg"
		[org.kde.kwalletmanager5, CATEGORY]="Privacy"
		[org.kde.kwalletmanager5, EXEC]="kwalletmanager5"
		[org.manjaro.pamac.manager, NAME]=$""
		[org.manjaro.pamac.manager, COMMENT]=$""
		[org.manjaro.pamac.manager, ICON]="/usr/share/icons/Fluent/scalable/apps/system-software-install.svg"
		[org.manjaro.pamac.manager, CATEGORY]="System"
		[org.manjaro.pamac.manager, EXEC]=""
		[org.pipewire.Helvum, NAME]=$""
		[org.pipewire.Helvum, COMMENT]=$""
		[org.pipewire.Helvum, ICON]=""
		[org.pipewire.Helvum, CATEGORY]="Multimedia"
		[org.pipewire.Helvum, EXEC]=""
		[pavucontrol-qt, NAME]=$"Som e microfone"
		[pavucontrol-qt, COMMENT]=$"Configurar ou alterar dispositivos de entrada e saída de áudio. (Ex: HDMI)"
		[pavucontrol-qt, ICON]="icons/kmix.png"
		[pavucontrol-qt, CATEGORY]="Star Multimedia"
		[pavucontrol-qt, EXEC]="pavucontrol-qt"
		[powerdevilprofilesconfig, NAME]=$""
		[powerdevilprofilesconfig, COMMENT]=$""
		[powerdevilprofilesconfig, ICON]=""
		[powerdevilprofilesconfig, CATEGORY]="Hardware"
		[powerdevilprofilesconfig, EXEC]="kcmshell5 powerdevilprofilesconfig powerdevilglobalconfig powerdevilactivitiesconfig"
		[qdbusviewer, NAME]=$"Qt QDBusViewer "
		[qdbusviewer, COMMENT]=$"Programas de desenvolvimento para QT."
		[qdbusviewer, ICON]="icons/qdbusviewer.png"
		[qdbusviewer, CATEGORY]="Desenv"
		[qdbusviewer, EXEC]=""
		[systemsettings, NAME]=$"Centro de controle do KDE"
		[systemsettings, COMMENT]=$""
		[systemsettings, ICON]="icons/systemsettings.png"
		[systemsettings, CATEGORY]="System"
		[systemsettings, EXEC]="systemsettings"
		[tlpui, NAME]=$"Configurador avançado de energia"
		[tlpui, COMMENT]=$""
		[tlpui, ICON]="icons/power-manager.png"
		[tlpui, CATEGORY]="Hardware"
		[tlpui, EXEC]=""
		[user_manager, NAME]=$""
		[user_manager, COMMENT]=$""
		[user_manager, ICON]=""
		[user_manager, CATEGORY]="Account"
		[user_manager, EXEC]=""
	)
}

function sh_checkdir {
	[[ ! -d "$userpath" ]] && cmdlogger mkdir -p "$userpath"
}

function sh_kservices5_desktop_files {
	local filtered_files
	mapfile -t filtered_files < <(grep -Rl -E '(kcmshell5|control)' /usr/share/kservices5/ |
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
		'qv4l2.desktop'
	)

	# Usando find para encontrar os arquivos e excluindo os arquivos da lista de exclusão
	mapfile -t filtered_files < <(find /usr/share/applications/bigcontrolcenter/ -type f ! \( -name "${excluded_files[0]}" $(printf -- "-o -name %s " "${excluded_files[@]:1}") \) -print0 | xargs -0)
	echo "${filtered_files[@]}"
}

function sh_static_desktop_files {
	local -a filtered_files=(
		'/usr/share/applications/big-store.desktop'
		'/usr/share/applications/org.manjaro.pamac.manager.desktop'
		'/usr/share/kservices5/bigcontrolcenter/cmake-gui.desktop'
		'/usr/share/kservices5/bigcontrolcenter/qv4l2.desktop'
		'/usr/share/kservices5/bigcontrolcenter/org.gnome.baobab.desktop'
		'/usr/share/kservices5/bigcontrolcenter/biglinux-grub-restore.desktop'
		'/usr/share/applications/gsmartcontrol.desktop'
		'/usr/share/applications/org.kde.kdeconnect-settings.desktop'
		'/usr/share/applications/org.kde.dolphin.desktop'
		'/usr/share/applications/org.kde.konsole.desktop'
		'/usr/share/applications/guvcview.desktop'
		'/usr/share/applications/hplip.desktop'
	)
	echo "${filtered_files[@]}"
}

function sh_create_file_html {
	local cprefix

	[[ $# -eq 0 ]] && cprefix='cache-' || cprefix="$1"
	cat <<-EOF >"$userpath/$cprefix$filename.html"
		<div class="box-1 box-2 box-3 box-4 box-5 box-items $CATEGORY">
		<div id="box-status-bar"><div id="tit-status-bar">
		$COMMENT
		</div></div>
		<button onclick="_run('$EXEC')" id="box-subtitle" class="box-geral-icons box-geral-button">
		<!-- class="status-button" CHAMA MODAL (POP-UP) -->
		<div class="box-imagem-icon">
		<img class="box-imagem-icon" src="$ICON" title="$NAME" alt="$NAME">
		</div>
		<div class="box-titulo">
		$NAME
		</div>
		<!--<div class="box-comentario">$COMMENT</div>-->
		</button>
		</div>
	EOF
}

function sh_get_config_value {
	local config_file="$1"
	local key="$2"
	local entry_group="Desktop Entry"
	kreadconfig5 --file "$config_file" --group "$entry_group" --key "$key"
}

function sh_debug_icon {
	#debug
	echo "$config_file" >>/tmp/config_file
	if [[ "$filename" = "kcm_keys" ]]; then
		xdebug "\n" \
			"config_file : $config_file\n" \
			"EXEC        : $EXEC\n" \
			"NAME        : $NAME\n" \
			"COMMENT     : $COMMENT\n" \
			"CATEGORY    : $CATEGORY\n" \
			"ICON        : $ICON\n"
	fi
	#debug
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

	filename="${1##*/}"
	filename="${filename%.desktop}"

	#debug
#	sh_debug_icon
	#debug

#echo "$count.0 ICON           : $ICON"

	# Verifica se o ícone original não existe
	if [[ ! -e "$ICON" ]]; then
		ICON_ORIGINAL="$ICON"
		ICON="icons/${ICON}.png"

		# Verifica se o ícone ainda não existe após a primeira tentativa
		if [[ ! -e "$ICON" ]]; then
			ICON_GET="$(geticons "$ICON_ORIGINAL")"
			ICON="$(grep -i -m 1 "64x64.*png" <<< "$ICON_GET")"

			# Verifica se existe um ícone PNG original
			if [[ ! -e "$ICON" ]]; then
				ICON="$(grep -i -m 1 ".svg" <<< "$ICON_GET" | tail -1)"

				# Verifica se existe um ícone SVG original
				if [[ -e "$ICON" ]]; then
					# Converte o ícone SVG para PNG
					if ksvgtopng5 64 64 "$ICON" "$HOME/.config/bigcontrolcenter/${ICON_ORIGINAL}.png"; then
						ICON="$HOME/.config/bigcontrolcenter/${ICON_ORIGINAL}.png"
					fi
				else
					#catch
					if [[ -n "$ICON_GET" ]]; then
						ICON="$ICON_GET"
					else
						ICON="$ICON_ORIGINAL"
					fi
				fi
			fi
		fi
	fi

#echo
#echo "$count.1 ICON           : $ICON"
#echo "$count.2 ICON_ORIGINAL  : $ICON_ORIGINAL"
#echo "$count.3 ICON_GET       : $ICON_GET"
#echo "$count.4 ICON_PNG       : $ICON_PNG"
#echo "$count.5 ICON_SVG       : $ICON_SVG"
#echo "$count.6 ICON           : $ICON"
#echo

	#debug
#	sh_debug_icon
	#debug

	case "$CATEGORY" in
	*[Ss]tar*) ;;
	*[Ss]ystem*) ;;
	*[Hh]ardware*) ;;
	*[Pp]ersonalization*) ;;
	*[Pp]hone*) ;;
	*[Mm]ultimedia*) ;;
	*[Nn]etwork*) ;;
	*[Aa]pplications*) ;;
	*[Aa]ccount*) ;;
	*[Ll]anguage*) ;;
	*[Pp]rivacy*) ;;
	*[Ss]erver*) ;;
	*[Aa]bout*) ;;
	*) CATEGORY="Other" ;;
	esac

	#	if [[ -e files/"$filename" ]]; then
	#		. files/"$filename"
	#	fi

	# Definindo as variáveis somente se não estiverem vazias
	CATEGORY="${Afiles[$filename, CATEGORY]:-$CATEGORY}"
	EXEC="${Afiles[$filename, EXEC]:-$EXEC}"
	ICON="${Afiles[$filename, ICON]:-$ICON}"
	NAME="${Afiles[$filename, NAME]:-$NAME}"
	COMMENT="${Afiles[$filename, COMMENT]:-$COMMENT}"

	if [[ "$CATEGORY" = "Other" ]]; then
		>"$userpath/show_other"
	fi

	sh_create_file_html
	wait
}

function sh_process_custom_user_files {
	local afilesUser=()
	local file

	[[ ! -d "$userfilespath" ]] && cmdlogger mkdir -p "$userfilespath"

	while IFS= read -r -d '' file; do
		afilesUser+=("$file")
	done < <(find "$userfilespath" -type f,l -print0)

	for file in "${afilesUser[@]}"; do
		if [[ -e "$file" ]]; then
			EXEC=""
			ICON=""
			NAME=""
			COMMENT=""
			source "$file"
			CATEGORY="Custom" #force
			filename="${file##*/}"
			filename="${filename%.*}"
			sh_create_file_html 'custom-'
		fi
	done
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
				sh_parallel_search "$i" &
			fi
		done
		[[ -e "$userpath/reload" ]] && cmdlogger rm -f "$userpath/reload"
	fi
	sh_process_custom_user_files
}

#sh_debug
sh_config
sh_checkdir
sh_main "$@"
