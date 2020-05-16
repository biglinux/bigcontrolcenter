#!/bin/bash

#Translation
export TEXTDOMAINDIR="/usr/share/locale"
export TEXTDOMAIN=bigcontrolcenter

rm -Rf ~/.local/share/kscreen

kdialog --msgbox $"As configurações da tela foram resetadas." --title $"Configurações da tela"
