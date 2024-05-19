import gi
import sys
import os
import json
import gettext
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

lang_translations = gettext.translation(
    "bigcontrolcenter", localedir="/usr/share/locale", fallback=True
)
lang_translations.install()
# define _ shortcut for translations
_ = lang_translations.gettext

# List of replacements with strings marked for translation
replacements = [
    {
        "app_id": "appimagelaunchersettings",
        "app_name": _("Configure AppimageLauncher"),
        "app_description": _("Choose the behavior of programs available in .appimage"),
        "app_categories": "System",
    },
    {
        "app_id": "audiocd",
        "app_description": _("Usage settings for old music CDs are not valid for MP3 music."),
        "app_categories": "Multimedia",
    },
    {
        "app_id": "avahi-discover",
        "app_name": _("Search for servers (zeroconf)"),
        "app_categories": "Other",
    },
    {
        "app_id": "biglinux-config",
        "app_name": _("Restore program configuration"),
        "app_description": _("biglinux-config"),
        "app_categories": "System Star",
    },
    {
        "app_id": "biglinux-grub-restore",
        "app_description": _("Utility that facilitates the restoration of the installed system, mainly restoring the system boot (Grub). It can also be used to access the package manager and terminal of the installed system."),
        "app_categories": "System Star",
    },
    {
        "app_id": "biglinux-noise-reduction-pipewire",
        "app_categories": "Multimedia",
    },
    {
        "app_id": "biglinuxthemesgui",
        "app_description": _("We provide complete configurations for you to select in an extremely simple way."),
        "app_categories": "Star Personalization",
    },
    {
        "app_id": "big-store",
        "app_description": _("Install or remove programs."),
        "app_categories": "System",
    },
    {
        "app_id": "big-welcome",
        "app_name": _("Introduction to BigLinux"),
        "app_description": _("Introduction to BigLinux"),
        "app_exec": "big-welcome",
        "app_icon": "/usr/share/bigbashview/bcc/apps/big-welcome/icon-logo-biglinux.svg",
        "app_categories": "Star",
    },
    {
        "app_id": "bootsplash-manager",
        "app_name": _("Themes to Bootsplash"),
        "app_categories": "Personalization",
    },
    {
        "app_id": "brightness-controller",
        "app_name": _("Brightness and color"),
        "app_description": _("Control brightness and colors"),
        "app_exec": "brightness-controller",
        "app_categories": "Hardware",
    },
    {
        "app_id": "bssh",
        "app_name": _("Search for SSH servers"),
        "app_categories": "Other",
    },
    {
        "app_id": "bvnc",
        "app_name": _("Search for VNC servers"),
        "app_categories": "Other",
    },
    {
        "app_id": "big-driver-manager",
        "app_description": _("Expand device support"),
        "app_categories": "Star Hardware",
    },
    {
        "app_id": "big-hardware-info",
        "app_categories": "Star About",
    },
    {
        "app_id": "big-kernel-manager",
        "app_description": _("The basis of the system and video card support"),
        "app_categories": "Star System",
    },
    {
        "app_id": "classikdecorationconfig",
        "app_description": _("Configure this window border theme"),
        "app_categories": "Personalization",
    },
    {
        "app_id": "classikstyleconfig",
        "app_description": _("Configure this windows theme."),
        "app_categories": "Personalization",
    },
    {
        "app_id": "cmake-gui",
        "app_categories": "Other",
    },
    {
        "app_id": "desktoppath",
        "app_exec": "kcmshell6 desktoppath",
        "app_categories": "Personalization",
    },
    {
        "app_id": "emoticons",
        "app_categories": "Personalization",
    },
    {
        "app_id": "gnome-alsamixer",
        "app_name": _("Advanced Audio Manager - Alsamixer"),
        "app_description": _("Audio controller in case of no sound."),
        "app_exec": "gnome-alsamixer",
        "app_categories": "Multimedia",
    },
    {
        "app_id": "kcm_soundtheme",
        "app_categories": "Multimedia",
    },
    {
        "app_id": "gparted",
        "app_name": _("Partition or format"),
        "app_description": _("Be careful, this program may erase all data on your computer."),
        "app_categories": "System",
    },
    {
        "app_id": "gsmartcontrol",
        "app_name": _("Storage Information (SMART)"),
        "app_categories": "About",
    },
    {
        "app_id": "kcm_disks",
        "app_categories": "About",
    },
    {
        "app_id": "gufw",
        "app_name": _("Gufw Firewall"),
        "app_description": _("Configure security rules for the internet connection."),
        "app_exec": "pkexec /usr/bin/gufw-pkexec root",
        "app_categories": "Network",
    },
    {
        "app_id": "guvcview",
        "app_name": _("Configure webcam or capture card"),
        "app_categories": "Hardware",
    },
    {
        "app_id": "hardinfo",
        "app_categories": "About",
    },
    {
        "app_id": "hplip",
        "app_name": _("HP printers"),
        "app_description": _("Check status, ink level and maintenance."),
        "app_exec": "hp-toolbox",
        "app_categories": "Hardware",
    },
    {
        "app_id": "hp-uiscan",
        "app_name": _("Scanners HP"),
        "app_categories": "Hardware",
    },
    {
        "app_id": "iDevice-Mounter",
        "app_name": _("Assemble Apple Hardware"),
        "app_description": _("With this program you can access programs on your Apple iPhone or iPad in a similar way to accessing files on a pendrive."),
        "app_exec": "idevice-mounter",
        "app_categories": "Phone",
    },
    {
        "app_id": "android-usb",
        "app_name": _("Connect to the internet using Android"),
        "app_exec": "#dialog-android-usb",
        "app_categories": "Phone",
    },
    {
        "app_id": "network-connect",
        "app_name": _("Connect to Internet"),
        "app_exec": "plasmawindowed org.kde.plasma.networkmanagement",
        "app_categories": "Network",
    },
    {
        "app_id": "kcm_proxy",
        "app_categories": "Network",
    },
    {
        "app_id": "ios-usb",
        "app_name": _("Connect to the internet using iOS"),
        "app_exec": "#dialog-ios-usb",
        "app_categories": "Phone",
    },
    {
        "app_id": "jamesdsp",
        "app_name": _("Equalizer (DSP)"),
        "app_categories": "Multimedia",
    },
    {
        "app_id": "kcm_access",
        "app_categories": "Account",
    },
    {
        "app_id": "kcmaccess",
        "app_categories": "Account",
    },
    {
        "app_id": "kcm_activities",
        "app_name": _("Virtual desktops and activities"),
        "app_description": _("Create more than one virtual desktop by switching between them."),
        "app_exec": "kcmshell6 kcm_kwin_virtualdesktops kcm_activities",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_autostart",
        "app_exec": "kcmshell6 autostart",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_baloofile",
        "app_description": _("Activating the search can consume significant memory and processing resources. This may cause the system to slow down, depending on the number of user files."),
        "app_categories": "System",
    },
    {
        "app_id": "kcm_bluetooth",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_bolt",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_clock",
        "app_description": _("Adjust the date, time and time zone."),
        "app_exec": "kcmshell6 clock",
        "app_categories": "Language",
    },
    {
        "app_id": "kcm_colors",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_componentchooser",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_cursortheme",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_desktoppaths",
        "app_exec": "kcmshell6 desktoppaths",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_desktoptheme",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_device_automounter",
        "app_exec": "kcmshell6 kcm_device_automounter kamera kcm_solid_actions",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_colord",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_filetypes",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_firewall",
        "app_name": _("Plasma Firewall"),
        "app_description": _("Configure security rules for connections. This firewall is based on the Gufw infrastructure"),
        "app_categories": "Network",
    },
    {
        "app_id": "kcm_fonts",
        "app_exec": "kcmshell6 kcm_fonts fontinst",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_icons",
        "app_exec": "kcmshell6 kcm_icons",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_gamecontroller",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_kaccounts",
        "app_name": _("Integration with Google Drive and ownCloud"),
        "app_description": _("Access your files that are on Google Drive or ownCloud directly from the file manager."),
        "app_exec": "kcmshell6 kcm_kaccounts",
        "app_categories": "Network",
    },
    {
        "app_id": "kcm_kamera",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_kded",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_keyboard",
        "app_description": _("Layout settings, hotkeys and other options."),
        "app_exec": "kcmshell6 kcm_keyboard kcm_keys kcm_kwinxwayland kcm_virtualkeyboard",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_kscreen",
        "app_exec": "kcmshell6 kcm_kscreen kcm_nightcolor kgamma kwinscreenedges",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_kwindecoration",
        "app_exec": "kcmshell6 kwindecoration",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_kwin_effects",
        "app_exec": "kcmshell6 kwincompositing kcm_kwin_effects qtquicksettings",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_kwinoptions",
        "app_exec": "kcmshell6 kcm_kwintabbox kcm_kwinoptions kcm_kwinrules kcm_kwin_scripts kcm_kwintabbox",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_launchfeedback",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_mouse",
        "app_exec": "kcmshell6 mouse kcm_workspace",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_networkmanagement",
        "app_name": _("Manage connections"),
        "app_description": _("Advanced network configuration (VPN, wifi, wired, fixed IP, PPPoE, ADSL, wired network, mobile broadband and others)."),
        "app_exec": "kcmshell6 kcm_networkmanagement",
        "app_categories": "Network",
    },
    {
        "app_id": "kcm_nightcolor",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_notifications",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_plymouth",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_powerdevilprofilesconfig",
        "app_exec": "kcmshell6 kcm_powerdevilprofilesconfig kcm_energyinfo",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_recentFiles",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_regionandlang",
        "app_exec": "kcmshell6 kcm_regionandlang",
        "app_categories": "Language",
    },
    {
        "app_id": "kcm_screenlocker",
        "app_exec": "kcmshell6 kcm_screenlocker",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_sddm",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_smserver",
        "app_exec": "kcmshell6 kcm_smserver",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_splashscreen",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_style",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_systemd",
        "app_name": _("Manage services (Systemd)"),
        "app_categories": "System",
    },
    {
        "app_id": "kcm_tablet",
        "app_categories": "Hardware",
        "app_exec": "kcmshell6 kcm_tablet kcm_wacomtablet"
    },
    {
        "app_id": "kcm_touchpad",
        "app_exec": "kcmshell6 touchpad",
        "app_categories": "Hardware",
    },
    {
        "app_id": "kcm_touchscreen",
        "app_categories": "Hardware",
        "app_exec": "kcmshell6 kcm_touchscreen kwintouchscreen"
    },
    {
        "app_id": "kcm_trash",
        "app_categories": "System",
    },
    {
        "app_id": "kcm_updates",
        "app_categories": "System",
    },
    {
        "app_id": "kcm_workspace",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kvantummanager",
        "app_name": _("Configure the Kvantum theme"),
        "app_description": _("For the Kvantum setup to work, apply the Kvantum theme in 'App Style'."),
        "app_categories": "Personalization",
    },
    {
        "app_id": "kwalletconfig5",
        "app_name": _("KDE Password Wallet"),
        "app_exec": "kcmshell6 kwalletconfig5",
        "app_categories": "Account",
    },
    {
        "app_id": "kwinadvanced",
        "app_exec": "kcmshell6 kwinactions kwinadvanced kwinfocus kwinmoving kwinoptions kwinrules kwinscripts kwintabbox",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kcm_wallpaper",
        "app_categories": "Personalization",
    },
    {
        "app_id": "kwindecoration",
        "app_exec": "kcmshell6 kwindecoration classikdecorationconfig",
        "app_categories": "Personalization",
    },
    {
        "app_id": "lstopo",
        "app_categories": "About",
    },
    {
        "app_id": "mintstick-format-kde",
        "app_categories": "System",
    },
    {
        "app_id": "mintstick-kde",
        "app_categories": "System",
    },
    {
        "app_id": "timeshift-gtk",
        "app_categories": "System Star",
        "app_name": _("Snapshots and backups"),
        "app_description": _("Create or activate restore points"),
    },
    {
        "app_id": "kcm_users",
        "app_categories": "Account",
    },
    {
        "app_id": "org.kde.dolphin",
        "app_name": _("Manage files"),
        "app_description": _("Get access to your files and folders."),
        "app_exec": "dolphin",
        "app_categories": "System",
    },
    {
        "app_id": "org.kde.filelight",
        "app_name": _("Storage Usage"),
        "app_categories": "System",
    },
    {
        "app_id": "org.kde.kdeconnect-settings",
        "app_name": _("KDE Connect"),
        "app_description": _("This program can transfer files between smartphones, tablets and other computers. With it, you can, for example, use your smartphone as a wireless mouse and keyboard to control the computer, among other features. It integrates better with BigLinux and sits among the applets located near the system clock. To synchronize with your smartphone, go to the Google Store or Apple Store and install Kde Connect."),
        "app_categories": "Phone",
    },
    {
        "app_id": "org.kde.kinfocenter",
        "app_categories": "About",
    },
    {
        "app_id": "org.kde.konsole",
        "app_name": _("Terminal"),
        "app_description": _("Access the command terminal."),
        "app_categories": "System",
    },
    {
        "app_id": "org.kde.ksystemlog",
        "app_categories": "System About",
    },
    {
        "app_id": "org.kde.kwalletmanager5",
        "app_name": _("Password Manager"),
        "app_exec": "kwalletmanager5",
        "app_categories": "Account",
    },
    {
        "app_id": "org.manjaro.pamac.manager",
        "app_categories": "System",
    },
    {
        "app_id": "kcm_flatpak",
        "app_categories": "System",
    },    {
        "app_id": "org.pipewire.Helvum",
        "app_categories": "Multimedia",
    },
    {
        "app_id": "pavucontrol-qt",
        "app_name": _("Sound and microphone"),
        "app_description": _("Configure or change audio input and output devices. (Ex: HDMI)"),
        "app_exec": "pavucontrol-qt",
        "app_categories": "Star Multimedia",
    },
    {
        "app_id": "powerdevilprofilesconfig",
        "app_exec": "kcmshell6 powerdevilprofilesconfig powerdevilglobalconfig powerdevilactivitiesconfig",
        "app_categories": "Hardware",
    },
    {
        "app_id": "sambasearch",
        "app_categories": "Internet",
    },
    {
        "app_id": "kcm_samba",
        "app_categories": "Network",
        "app_name": _("Shared file information"),
    },
    {
        "app_id": "system-config-printer",
        "app_name": _("Printers"),
        "app_description": _("Install, configure or remove printers."),
        "app_exec": "system-config-printer",
        "app_categories": "Hardware",
    },
    {
        "app_id": "systemsettings",
        "app_name": _("KDE Control Center"),
        "app_exec": "systemsettings",
        "app_categories": "System",
    },
    {
        "app_id": "tlpui",
        "app_name": _("Advanced power configurator"),
        "app_categories": "Hardware",
    },
    {
        "app_id": "user_manager",
        "app_categories": "Account",
    },

    # Add more replacements as needed
]

def get_icon_path(icon, icon_theme):
    """
    Attempts to find the icon path based on the GIcon, suitable for SVG, PNG, and other formats.
    If the icon is not found, it tries to progressively remove parts of the name separated by '-'.
    """
    if isinstance(icon, Gio.ThemedIcon):
        icon_names = icon.get_names()
    elif isinstance(icon, Gio.FileIcon):
        return icon.get_file().get_path()  # Direct path for file-based icons
    else:
        icon_names = [icon.to_string()]

    for icon_name in icon_names:
        if icon_name.startswith('/'):
            return icon_name  # Returns the absolute path if specified
        
        # Tries to find the icon with the full name and, if necessary, removes parts of the name
        parts = icon_name.split('-')
        for end in range(len(parts), 0, -1):
            modified_icon_name = '-'.join(parts[:end])
            for size in [64, 48, 128, 32, 256, 512, 24, 22, 16]:
                icon_info = icon_theme.lookup_icon(modified_icon_name, size, Gtk.IconLookupFlags.USE_BUILTIN)
                if icon_info:
                    return icon_info.get_filename()

    return "Icon not found"

def get_executable(exec_field):
    """
    Processes the Exec field to obtain the complete executable command.
    """
    # Splits the Exec field into parts to remove possible options and arguments
    exec_parts = exec_field.split()
    # May need further adjustments to handle specific cases
    executable = " ".join(exec_parts)  # Rejoins, considering valid arguments
    return executable

def find_replacement(app_id):
    """
    Searches for replacements for the provided app_id in the replacements list.
    Returns a dictionary with the found replacements or None if not found.
    """
    for replacement in replacements:
        if replacement["app_id"] == app_id:
            return replacement
    return None

def get_app_info(app_ids):
    app_info_list = []
    processed_app_ids = set()
    icon_theme = Gtk.IconTheme.get_default()

    for app_id in app_ids:
        if app_id in processed_app_ids:
            continue
        
        app_info = None
        try:
            app_info = Gio.DesktopAppInfo.new(f"{app_id}.desktop")
        except Exception:
            alternative_paths = [
                f"{app_id}.desktop",
                f"/usr/share/applications/bigcontrolcenter/{app_id}.desktop",
                f"/usr/share/kservices5/{app_id}.desktop",
            ]
            for path in alternative_paths:
                if os.path.exists(path):
                    try:
                        app_info = Gio.DesktopAppInfo.new_from_filename(path)
                    except:
                        break
        
        if app_info:
            try:
                icon = app_info.get_icon()
                icon_path = get_icon_path(icon, icon_theme) if icon else "null"
                exec_field = app_info.get_string('Exec') or "null"

                app_info_dict = {
                    "app_id": app_id,
                    "app_name": app_info.get_display_name(),
                    "app_exec": get_executable(exec_field),
                    "app_description": app_info.get_description(),
                    "app_icon": icon_path,
                    "app_categories": app_info.get_categories() or "Other",
                }

                replacement = find_replacement(app_id)
                if replacement:
                    for key in ['app_name', 'app_exec', 'app_description', 'app_icon', 'app_categories']:
                        if key in replacement:
                            app_info_dict[key] = replacement[key]

                app_info_list.append(app_info_dict)
                processed_app_ids.add(app_id)
            except Exception as e:
                print(f"Error processing {app_id}: {e}")
                
    return json.dumps(app_info_list, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app_ids = sys.argv[1:]
        print(get_app_info(app_ids))
    else:
        print("Please provide application IDs as arguments.")
