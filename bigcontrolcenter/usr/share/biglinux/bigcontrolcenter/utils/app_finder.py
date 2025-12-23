"""
BigControlCenter - Application finder utility

This module is responsible for finding desktop applications
and generating program information similar to the original
loop-search.sh and getappinfo.py scripts.
"""

import os
import subprocess
import glob
import gettext
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gio

# Setup translations
try:
    lang_translations = gettext.translation(
        "bigcontrolcenter", localedir="/usr/share/locale", fallback=True
    )
    lang_translations.install()
    _ = lang_translations.gettext
except Exception:
    # Fallback if translation fails
    def _(x):
        return x


class AppFinder:
    """
    Utility class to find desktop applications and generate program information
    """

    def __init__(self):
        """Initialize the app finder"""
        self.session_type = os.environ.get("XDG_SESSION_TYPE", "wayland")
        self.replacements = self._get_replacements()

    def _get_session_excluded_patterns(self):
        """
        Get list of desktop file patterns to exclude based on session type.
        In Wayland: exclude _x11 variants
        In X11: exclude non-_x11 variants (for modules that have _x11 version)
        """
        # Modules that have both normal and _x11 versions
        x11_modules = [
            "kcm_animations",
            "kcm_kwin_effects",
            "kcm_kwin_scripts",
            "kcm_kwin_virtualdesktops",
            "kcm_kwindecoration",
            "kcm_kwinoptions",
            "kcm_kwinrules",
            "kcm_kwinscreenedges",
            "kcm_kwintabbox",
            "kcm_kwintouchscreen",
        ]
        
        if self.session_type == "x11":
            # In X11, exclude the non-_x11 versions
            return [f"{m}.desktop" for m in x11_modules]
        else:
            # In Wayland, exclude all _x11 variants
            return [f"{m}_x11.desktop" for m in x11_modules]


    def get_programs(self):
        """
        Get program information by scanning the system
        """
        # Find desktop files
        desktop_files = self._find_desktop_files()

        # Use a dictionary to deduplicate entries by app_id
        program_dict = {}

        # Get program info for each desktop file
        for desktop_file in desktop_files:
            app_id = self._get_app_id_from_path(desktop_file)

            # Skip if we already have this app_id processed
            if app_id in program_dict:
                continue

            program_info = self._get_app_info(app_id, desktop_file)
            if program_info:
                program_dict[app_id] = program_info

        # Add special entries that don't have desktop files
        special_entries = [
            "android-usb",
            "ios-usb",
            "network-connect",
            "big-themes-gui",
        ]
        for entry_id in special_entries:
            # Skip if we already have this special entry processed from desktop files
            if entry_id in program_dict:
                continue

            replacement = self._find_replacement(entry_id)
            if replacement and "app_id" in replacement:
                # Create a minimal program entry that will be populated by the replacement
                program_info = {
                    "app_id": entry_id,
                    "app_name": entry_id,
                    "app_exec": "",
                    "app_description": "",
                    "app_icon": "",
                    "app_categories": "Other",
                }

                # Apply the replacement data
                for key in [
                    "app_name",
                    "app_exec",
                    "app_description",
                    "app_icon",
                    "app_categories",
                ]:
                    if key in replacement:
                        program_info[key] = replacement[key]

                program_dict[entry_id] = program_info

        # Convert dictionary to list, maintaining only unique entries
        programs = list(program_dict.values())

        return programs

    def _find_desktop_files(self):
        """
        Find desktop files
        """
        # Keep track of app_ids we've already seen to avoid processing duplicate entries
        unique_app_ids = set()
        unique_files = []

        # 1. Static files first
        static_files = self._find_static_desktop_files()
        for file_path in static_files:
            app_id = self._get_app_id_from_path(file_path)
            if app_id not in unique_app_ids and os.path.exists(file_path):
                unique_app_ids.add(app_id)
                unique_files.append(file_path)

        # 2. Big Control Center
        bcc_files = self._find_bcc_desktop_files()
        for file_path in bcc_files:
            app_id = self._get_app_id_from_path(file_path)
            if app_id not in unique_app_ids and os.path.exists(file_path):
                unique_app_ids.add(app_id)
                unique_files.append(file_path)

        # 3. Regular application desktop files with kcm prefix
        app_files = self._find_app_desktop_files()
        for file_path in app_files:
            app_id = self._get_app_id_from_path(file_path)
            if app_id not in unique_app_ids and os.path.exists(file_path):
                unique_app_ids.add(app_id)
                unique_files.append(file_path)

        # 4. KDE Service desktop files last (most likely to have duplicates)
        kde_service_files = self._find_kde_service_files()
        for file_path in kde_service_files:
            app_id = self._get_app_id_from_path(file_path)
            if app_id not in unique_app_ids and os.path.exists(file_path):
                unique_app_ids.add(app_id)
                unique_files.append(file_path)

        return unique_files

    def _find_kde_service_files(self):
        """Find KDE service desktop files"""
        excluded_patterns = [
            "kcmdolphingeneral.desktop",
            "kcmdolphinnavigation.desktop",
            "kcmdolphinservices.desktop",
            "kcmdolphinviewmodes.desktop",
            "cache.desktop",
            "cookies.desktop",
            "kcmtrash.desktop",
            "netpref.desktop",
            "proxy.desktop",
            "useragent.desktop",
            "webshortcuts.desktop",
            "kcm_ssl.desktop",
            "bluedevildevices.desktop",
            "bluedevilglobal.desktop",
            "formats.desktop",
            "camera.desktop",
            "fontinst.desktop",
            "powerdevilactivitiesconfig.desktop",
            "kcm_plasmasearch.desktop",
            "kwinscreenedges.desktop",
            "kwintouchscreen.desktop",
            "keys.desktop",
            "standard_actions.desktop",
            "khotkeys.desktop",
            "qtquicksettings.desktop",
            "solid-actions.desktop",
            "spellchecking.desktop",
            "kwinactions.desktop",
            "kwinfocus.desktop",
            "kwinmoving.desktop",
            "kwinoptions.desktop",
            "kwinrules.desktop",
            "kwintabbox.desktop",
            "breezestyleconfig.desktop",
            "breezedecorationconfig.desktop",
            "oxygenstyleconfig.desktop",
            "oxygendecorationconfig.desktop",
            "kcm_pulseaudio.desktop",
            "emoticons.desktop",
            "kcm_nightcolor.desktop",
            "kgamma.desktop",
            "powerdevilglobalconfig.desktop",
            "kwincompositing.desktop",
            "kcmsmserver.desktop",
            "kcmkded.desktop",
            "kamera.desktop",
            "powerdevilprofilesconfig.desktop",
            "kcmperformance.desktop",
            "kcmkonqyperformance.desktop",
            "bookmarks.desktop",
            "msm_user.desktop",
            "kcm_feedback.desktop",
            "kcm_users.desktop",
            "msm_kernel.desktop",
            "kcm_kdisplay.desktop",
            "msm_keyboard.desktop",
            "msm_language_packages.desktop",
            "msm_locale.desktop",
            "msm_mhwd.desktop",
            "kcm_lookandfeel.desktop",
            "sierrabreezeenhancedconfig.desktop",
            "msm_timedate.desktop",
            "lightlystyleconfig.desktop",
            "lightlydecorationconfig.desktop",
            "kcm_landingpage.desktop",
            "libkcddb.desktop",
            "kcm_solid_actions.desktop",
            "classikstyleconfig.desktop",
            "classikdecorationconfig.desktop",
            "klassydecorationconfig.desktop",
            "plasma-applet-org.kde.plasma.bluetooth.desktop",
            "klassystyleconfig.desktop",
        ]

        # Add session-based exclusions (exclude _x11 in Wayland, exclude non-_x11 in X11)
        excluded_patterns.extend(self._get_session_excluded_patterns())

        result = []

        try:
            cmd = ["grep", "-Rl", "-E", "(kcmshell6|control)", "/usr/share/kservices5/"]
            output = subprocess.check_output(cmd, text=True).strip()
            if output:
                for file_path in output.split("\n"):
                    # Check against exclusion patterns
                    if file_path and not any(
                        pattern in file_path for pattern in excluded_patterns
                    ):
                        result.append(file_path)
        except subprocess.SubprocessError:
            # Grep command failed - silent handling
            pass

        return result

    def _find_app_desktop_files(self):
        """Find application desktop files with kcm_ prefix"""
        excluded_patterns = [
            "kcm_kdisplay.desktop",
            "kcm_workspace.desktop",
            # "kcm_keyboard.desktop",
            "kcm_krunnersettings.desktop",
            "kcm_about-distro.desktop",
            "kcm_breezedecoration.desktop",
            "kcm_kwinxwayland.desktop",
            "kcm_keys.desktop",
            "kcm_powerdevilglobalconfig.desktop",
            "kcm_powerdevilactivitiesconfig.desktop",
            "kcm_fontinst.desktop",
            "kcm_printer_manager.desktop",
            "kcm_kwinrules.desktop",
            "kcm_kwintabbox.desktop",
            "kcm_qtquicksettings.desktop",
            "kcm_energyinfo.desktop",
            "kcm_kgamma.desktop",
            "kcm_klassydecoration.desktop",
            "kcm_wacomtablet.desktop",
            "kcm_netpref.desktop",
            "kcm_webshortcuts.desktop",
            "kcm_kwin_scripts.desktop",
            "kcm_virtualkeyboard.desktop",
            "kcm_nightlight.desktop",
            "kcm_pulseaudio.desktop",
            "kcm_kwin_virtualdesktops.desktop",
            "kcm_mobile_power.desktop",
            "kcm_mobile_wifi.desktop",
            "kcm_mobile_hotspot.desktop",
        ]

        # Add session-based exclusions (exclude _x11 in Wayland, exclude non-_x11 in X11)
        excluded_patterns.extend(self._get_session_excluded_patterns())

        result = []

        # Find kcm_*.desktop files in /usr/share/applications/
        for file_path in glob.glob("/usr/share/applications/kcm_*.desktop"):
            # Check against exclusion patterns
            if not any(pattern in file_path for pattern in excluded_patterns):
                result.append(file_path)

        return result

    def _find_bcc_desktop_files(self):
        """Find BigControlCenter specific desktop files"""
        excluded_patterns = [
            # "timeshift-gtk.desktop",
            "cups.desktop",
            "htop.desktop",
            "msm_kde_notifier_settings.desktop",
            "mpv.desktop",
            "manjaro-settings-manager.desktop",
            "org.kde.kuserfeedback-console.desktop",
            "qvidcap.desktop",
            "kdesettings",
            "lstopo.desktop",
            "kdesystemsettings.desktop",
            "qv4l2.desktop",
            "org.gnome.baobab.desktop",
            "klassy-settings.desktop",
            "kcm_pulseaudio.desktop",
            "stoken-gui-small.desktop",
            "org.fcitx.Fcitx5.desktop",
        ]

        # Add session-based exclusions (exclude _x11 in Wayland, exclude non-_x11 in X11)
        excluded_patterns.extend(self._get_session_excluded_patterns())

        result = []

        # Find files in /usr/share/applications/bigcontrolcenter/
        if os.path.exists("/usr/share/applications/bigcontrolcenter/"):
            for file_path in glob.glob("/usr/share/applications/bigcontrolcenter/*"):
                if os.path.isfile(file_path):
                    # Check against exclusion patterns
                    if not any(pattern in file_path for pattern in excluded_patterns):
                        result.append(file_path)

        return result

    def _find_static_desktop_files(self):
        """Return a list of static desktop files paths based on the shell script"""
        static_files = [
            "/usr/share/applications/big-store.desktop",
            "/usr/share/applications/bigcontrolcenter/pavucontrol-qt.desktop",
            "/usr/share/applications/bigcontrolcenter/me.timschneeberger.jdsp4linux.desktop",
            "/usr/share/applications/org.manjaro.pamac.manager.desktop",
            "/usr/share/kservices5/bigcontrolcenter/cmake-gui.desktop",
            "/usr/share/kservices5/bigcontrolcenter/qv4l2.desktop",
            "/usr/share/applications/biglinux-noise-reduction-pipewire.desktop",
            "/usr/share/applications/br.com.biglinux.grub-restore.desktop",
            "/usr/share/applications/gsmartcontrol.desktop",
            # "/usr/share/applications/org.kde.kdeconnect-settings.desktop",
            "/usr/share/applications/org.kde.dolphin.desktop",
            "/usr/share/applications/org.kde.konsole.desktop",
            "/usr/share/applications/guvcview.desktop",
            "/usr/share/applications/hplip.desktop",
            "/usr/share/kservices5/smb.desktop",
            "/usr/share/applications/big-driver-manager.desktop",
            "/usr/share/applications/big-hardware-info.desktop",
            "/usr/share/applications/big-kernel-manager.desktop",
            "/usr/share/applications/br.com.biglinux.networkinfo.desktop",
            "/usr/share/applications/org.kde.kwalletmanager.desktop",
            "/usr/share/applications/org.ffado.FfadoMixer.desktop",
            "/usr/share/applications/stoken-gui.desktop",
        ]

        # Filter out files that don't exist
        return [file_path for file_path in static_files if os.path.exists(file_path)]

    def _get_app_id_from_path(self, file_path):
        """Extract the app ID from a desktop file path"""
        base_name = os.path.basename(file_path)
        return os.path.splitext(base_name)[0]

    def _get_app_info(self, app_id, file_path):
        """
        Get application information for a desktop file using GIO
        """
        try:
            app_info = Gio.DesktopAppInfo.new_from_filename(file_path)
            if not app_info:
                return None

            # Get icon path
            icon = app_info.get_icon()
            icon_path = self._get_icon_path(icon) if icon else None

            # Get executable with parameters - KEEP the parameters as in the JSON template
            exec_field = app_info.get_string("Exec") or "null"
            executable = exec_field.strip().split("%")[0]

            # Get categories from desktop file - preserve original format
            categories = app_info.get_categories() or "Other"

            # Create info dictionary
            info_dict = {
                "app_id": app_id,
                "app_name": app_info.get_display_name() or app_id,
                "app_exec": executable,
                "app_description": app_info.get_description(),  # Allow None/null values
                "app_icon": icon_path or "",
                "app_categories": categories,
            }

            # Apply replacements if available (this is crucial for matching expected output)
            replacement = self._find_replacement(app_id)
            if replacement:
                for key in [
                    "app_name",
                    "app_exec",
                    "app_description",
                    "app_icon",
                    "app_categories",
                ]:
                    if key in replacement:
                        info_dict[key] = replacement[key]

            return info_dict
        except Exception as e:
            print(f"Error processing {app_id}: {e}")
            return None

    def _get_icon_path(self, icon):
        """Get path for an icon using GIO with progressive fallback strategy"""
        if not icon:
            return ""

        # If icon is a FileIcon (absolute path)
        if isinstance(icon, Gio.FileIcon):
            return icon.get_file().get_path()

        # Get icon names
        if isinstance(icon, Gio.ThemedIcon):
            icon_names = icon.get_names()
        else:
            # Convert icon to string as fallback
            icon_str = icon.to_string()
            if icon_str.startswith("/"):
                return icon_str
            icon_names = [icon_str]

        # Try each icon name with progressive fallback
        for icon_name in icon_names:
            if icon_name.startswith("/"):
                # Absolute path
                return icon_name

            # First try using just the icon name - this is the key change
            # that will let the system find icons in any theme first
            if icon_name:
                # Return just the icon name to let the system handle theme lookup
                return icon_name

            # Progressive name simplification (remove parts from the end)
            parts = icon_name.split("-")
            for end in range(len(parts), 0, -1):
                modified_name = "-".join(parts[:end])

                # Return the simplified name if we found it
                if modified_name:
                    return modified_name

        # If all else fails, return a default icon name
        return "application-default-icon"

    def _find_replacement(self, app_id):
        """Find a replacement entry for the app_id"""
        for replacement in self.replacements:
            if replacement.get("app_id") == app_id:
                return replacement
        return None

    def _get_replacements(self):
        """
        Get a comprehensive list of program replacements using icon names instead of absolute paths
        """
        # Return the list of replacements with icon names instead of absolute paths
        return [
            {
                "app_id": "appimagelaunchersettings",
                "app_name": _("Configure AppimageLauncher"),
                "app_exec": "AppImageLauncherSettings %f",
                "app_description": _(
                    "Choose the behavior of programs available in .appimage"
                ),
                "app_icon": "AppImageLauncher",
                "app_categories": "System",
            },
            {
                "app_id": "avahi-discover",
                "app_name": _("Search for Zeroconf servers"),
                "app_categories": "Other",
                "app_icon": "network-workgroup",
            },
            {
                "app_id": "br.com.biglinux.networkinfo",
                "app_categories": "Star Network",
            },
            {
                "app_id": "kcm_mobile_hotspot",
                "app_categories": "Network",
                "app_icon": "kcm_mobile_hotspot",
            },
            {
                "app_id": "big-driver-manager",
                "app_description": _("Expand device support"),
                "app_categories": "Star Hardware",
            },
            {
                "app_id": "big-hardware-info",
                "app_description": _("Detailed information about your computer"),
                "app_categories": "Star About",
            },
            {
                "app_id": "big-kernel-manager",
                "app_description": _("System foundation and video card support"),
                "app_categories": "Star System",
            },
            {
                "app_id": "biglinux-config",
                "app_description": _("Restore program configuration"),
                "app_categories": "System Star",
            },
            {
                "app_id": "bssh",
                "app_name": _("Search for SSH servers"),
                "app_icon": "folder-remote",
                "app_categories": "Other",
            },
            {
                "app_id": "bvnc",
                "app_name": _("Search for VNC servers"),
                "app_icon": "preferences-system-network-remote",
                "app_categories": "Other",
            },
            {
                "app_id": "cmake-gui",
                "app_description": _("Cross-platform buildsystem"),
                "app_categories": "System",
            },
            {
                "app_id": "firewall-config",
                "app_name": _("Advanced Firewall Settings"),
                "app_categories": "Network",
            },
            {
                "app_id": "gnome-alsamixer",
                "app_name": _("Advanced Audio Manager - Alsamixer"),
                "app_icon": "/usr/share/pixmaps/gnome-alsamixer/gnome-alsamixer-icon.png",
                "app_categories": "Multimedia",
            },
            {
                "app_id": "me.timschneeberger.jdsp4linux",
                "app_name": _("JamesDSP improving music and audio quality"),
                "app_description": _(
                    "Enhance your sound with equalizer, bass boost, surround, and other effects."
                ),
                "app_categories": "Multimedia",
            },
            {
                "app_id": "gparted",
                "app_name": _("Partition or Format"),
                "app_categories": "System",
            },
            {
                "app_id": "hplip",
                "app_name": _("HP Printers"),
                "app_description": _("Check status, ink level, and maintenance."),
                "app_categories": "Hardware",
            },
            {
                "app_id": "hp-uiscan",
                "app_name": _("HP Scanners"),
                "app_description": _("Configure and use HP scanning devices"),
                "app_icon": "scanner",
                "app_categories": "Hardware",
            },
            {
                "app_id": "kvantummanager",
                "app_name": _("Configure Kvantum Theme"),
                "app_description": _(
                    "For Kvantum configuration to work, apply the Kvantum theme in 'Application Style'."
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "mintstick-format-kde",
                "app_name": _("USB Device Formatter"),
                "app_exec": "mintstick -m format",
                "app_description": _("Format a USB device"),
                "app_icon": "media-flash-memory-stick",
                "app_categories": "Hardware",
            },
            {
                "app_id": "mintstick-kde",
                "app_name": _("USB Image Writer"),
                "app_exec": "mintstick -m iso",
                "app_description": _("Create a bootable USB device"),
                "app_icon": "drive-removable-media-usb-symbolic",
                "app_categories": "System",
            },
            {
                "app_id": "org.kde.filelight",
                "app_name": _("Storage Usage"),
                "app_categories": "System",
            },
            {
                "app_id": "org.kde.kinfocenter",
                "app_categories": "About",
            },
            {
                "app_id": "org.kde.ksystemlog",
                "app_categories": "System About",
            },
            {
                "app_id": "pavucontrol-qt",
                "app_name": _("Sound and microphone"),
                "app_description": _(
                    "Configure or change audio input and output devices. (Ex: HDMI)"
                ),
                "app_categories": "Star Multimedia",
            },
            {
                "app_id": "system-config-printer",
                "app_name": _("Printers"),
                "app_description": _("Install, configure or remove printers."),
                "app_categories": "Hardware",
            },
            {
                "app_id": "systemsettings",
                "app_name": _("KDE Control Center"),
                "app_categories": "System",
            },
            {
                "app_id": "big-store",
                "app_categories": "System",
            },
            {
                "app_id": "guvcview",
                "app_name": _("Configure webcam or capture card"),
                "app_description": _(
                    "Adjust settings and control webcams or video capture devices"
                ),
                "app_icon": "guvcview",
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_access",
                "app_description": _(
                    "Configure accessibility options for users with special needs"
                ),
                "app_categories": "Account",
            },
            {
                "app_id": "kcm_activities",
                "app_name": _("Virtual desktops and activities"),
                "app_exec": "kcmshell6 kcm_kwin_virtualdesktops kcm_activities",
                "app_description": _(
                    "Create more than one virtual work environment by switching between them."
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_autostart",
                "app_description": _(
                    "Manage applications that start automatically on login"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_baloofile",
                "app_description": _(
                    "Enabling search can consume significant memory and processing resources. This may cause the system to slow down, depending on the number of user files."
                ),
                "app_categories": "System",
            },
            {
                "app_id": "kcm_bluetooth",
                "app_description": _("Connect and manage Bluetooth devices"),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_bolt",
                "app_description": _(
                    "Manage Thunderbolt devices and security settings"
                ),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_clock",
                "app_description": _("Adjust date, time and timezone."),
                "app_categories": "Language",
            },
            {
                "app_id": "kcm_colors",
                "app_description": _(
                    "Customize the color scheme of your desktop environment"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_componentchooser",
                "app_description": _(
                    "Select which applications to use for specific tasks"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_cursortheme",
                "app_description": _("Change mouse cursor appearance and themes"),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_desktoppaths",
                "app_description": _(
                    "Configure default paths for documents, downloads and other folders"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_desktoptheme",
                "app_description": _(
                    "Change the visual appearance of the Plasma desktop"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_filetypes",
                "app_description": _(
                    "Configure which applications open specific file types"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_firewall",
                "app_categories": "Network",
            },
            {
                "app_id": "kcm_app-permissions",
                "app_description": _("Manage permissions for Flatpak applications"),
                "app_categories": "System",
                "app_icon": "preferences"
            },
            {
                "app_id": "kcm_animations",
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_nighttime",
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_fonts",
                "app_exec": "kcmshell6 kcm_fonts fontinst",
                "app_description": _(
                    "Install and configure system fonts and typography settings"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_gamecontroller",
                "app_description": _("Configure game controllers and joysticks"),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_icons",
                "app_description": _(
                    "Change the icon theme used throughout the system"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_kaccounts",
                "app_categories": "Network Account",
            },
            {
                "app_id": "kcm_kamera",
                "app_description": _(
                    "Configure digital camera integration with your system"
                ),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_kded",
                "app_description": _(
                    "Manage system services running in the background"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_keyboard",
                "app_exec": "kcmshell6 kcm_keyboard kcm_keys kcm_kwinxwayland kcm_virtualkeyboard",
                "app_description": _("Layout settings, shortcuts and other options."),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_kscreen",
                "app_exec": "kcmshell6 kcm_nightlight kgamma kcm_kscreen kwinscreenedges",
                "app_description": _(
                    "Configure monitors, resolution, and screen arrangement"
                ),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_kwindecoration",
                "app_name": _("Window Decorations"),
                "app_description": _(
                    "Change the appearance of window title bars and borders"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_kwin_effects",
                "app_exec": "kcmshell6 kwincompositing kcm_kwin_effects qtquicksettings",
                "app_description": _(
                    "Configure visual effects and animations for the desktop"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_kwinoptions",
                "app_exec": "kcmshell6 kcm_kwintabbox kcm_kwinoptions kcm_kwinrules kcm_kwin_scripts kcm_kwintabbox",
                "app_description": _("Configure how windows behave and interact"),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_mouse",
                "app_exec": "kcmshell6 mouse kcm_workspace",
                "app_description": _(
                    "Configure mouse sensitivity, buttons and behavior"
                ),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_networkmanagement",
                "app_description": _(
                    "Advanced network configuration (VPN, WiFi, Wired, Static IP, PPPoE, ADSL, wired network, mobile broadband and others)."
                ),
                "app_categories": "Network",
            },
            {
                "app_id": "kcm_nightlight",
                "app_categories": "Hardware",
            },
            {
                "app_id": "qefientrymanager",
                "app_name": _("QEFI Entry Manager"),
                "app_description": _(
                    "Manage and configure boot entries for UEFI systems"
                ),
                "app_icon": "/usr/share/icons/bigicons-papient/scalable/apps/cc.inoki.qefientrymanager.svg",
                "app_categories": "System",
            },
            {
                "app_id": "kcm_notifications",
                "app_description": _("Configure system and application notifications"),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_plymouth",
                "app_name": _("Boot Screen"),
                "app_description": _(
                    "Change the splash screen shown during system startup"
                ),
                "app_icon": "preferences-desktop-display",
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_powerdevilprofilesconfig",
                "app_exec": "kcmshell6 kcm_powerdevilprofilesconfig kcm_energyinfo kcm_mobile_power",
                "app_description": _("Configure energy saving and battery settings"),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_proxy",
                "app_description": _(
                    "Configure network proxy settings for internet access"
                ),
                "app_categories": "Network",
            },
            {
                "app_id": "kcm_recentFiles",
                "app_description": _("Manage the history of recently accessed files"),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_regionandlang",
                "app_description": _("Configure language, region, and format settings"),
                "app_categories": "Language",
            },
            {
                "app_id": "kcm_screenlocker",
                "app_description": _(
                    "Configure screen locking settings and appearance"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_sddm",
                "app_description": _(
                    "Configure the login screen appearance and behavior"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_smserver",
                "app_name": _("Desktop Session"),
                "app_exec": "kcmshell6 kcm_smserver",
                "app_description": _("Configure session startup and shutdown behavior"),
                "app_icon": "system-log-out",
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_soundtheme",
                "app_description": _("Configure sound effects for system events"),
                "app_icon": "folder-music",
                "app_categories": "Multimedia",
            },
            {
                "app_id": "kcm_splashscreen",
                "app_description": _(
                    "Configure the splash screen shown while starting applications"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_style",
                "app_description": _("Configure the visual appearance of applications"),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_tablet",
                "app_exec": "kcmshell6 kcm_tablet kcm_wacomtablet",
                "app_description": _("Configure drawing tablets and stylus settings"),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_touchpad",
                "app_description": _("Configure laptop touchpad behavior and gestures"),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_touchscreen",
                "app_exec": "kcmshell6 kcm_touchscreen kwintouchscreen",
                "app_description": _("Configure touchscreen behavior and calibration"),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_trash",
                "app_description": _(
                    "Configure trash bin behavior and cleanup settings"
                ),
                "app_categories": "System",
            },
            {
                "app_id": "kcm_wallpaper",
                "app_description": _(
                    "Change desktop background image and slideshow settings"
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_landingpage",
                "app_description": _(
                    "Configure the system's landing page and default widgets."
                ),
                "app_categories": "Personalization",
            },
            {
                "app_id": "org.ffado.FfadoMixer",
                "app_name": _("Manage FireWire Audio Interfaces - FfadoMixer"),
                "app_description": _(
                    "Control Panel for your FireWire Audio Interfaces."
                ),
                "app_categories": "Multimedia",
            },
            {
                "app_id": "org.kde.dolphin",
                "app_description": _("Access your files and folders."),
                "app_categories": "System",
            },
            {
                "app_id": "org.kde.kdeconnect.app",
                "app_description": _(
                    "This program can transfer files between smartphones, tablets, and other computers. With it, you can, for example, use your smartphone as a wireless mouse and keyboard to control the computer, among other features. It integrates best with BigLinux and sits among the applets located near the system clock. To sync with your smartphone, go to the Google Store or Apple Store and install KDE Connect."
                ),
                "app_categories": "Phone",
            },
            {
                "app_id": "org.kde.konsole",
                "app_description": _("Access the command terminal."),
                "app_categories": "System",
            },
            {
                "app_id": "org.kde.kwalletmanager",
                "app_name": _("Password Manager - KWalletManager"),
                "app_exec": "kwalletmanager5",
                "app_description": _("Tool for managing KDE wallets"),
                "app_icon": "kwalletmanager",
                "app_categories": "Account",
            },
            {
                "app_id": "org.manjaro.pamac.manager",
                "app_exec": "pamac-manager",
                "app_description": _("Add or remove programs installed on the system"),
                "app_categories": "System",
            },
            {
                "app_id": "android-usb",
                "app_name": _("Connect to internet using Android"),
                "app_exec": "#dialog-android-usb",
                "app_icon": "android-usb",
                "app_categories": "Phone",
            },
            {
                "app_id": "ios-usb",
                "app_name": _("Connect to internet using iOS"),
                "app_exec": "#dialog-ios-usb",
                "app_icon": "ios-usb",
                "app_categories": "Phone",
            },
            {
                "app_id": "kcm_cellular_network",
                "app_categories": "Phone",
            },
            {
                "app_id": "network-connect",
                "app_name": _("Connect to Internet"),
                "app_exec": "plasmawindowed org.kde.plasma.networkmanagement",
                "app_description": None,
                "app_icon": "network-connect",
                "app_categories": "Network",
            },
            {
                "app_id": "kcm_users",
                "app_categories": "Account",
            },
            {
                "app_id": "br.com.biglinux.grub-restore",
                "app_icon": "/usr/share/icons/bigicons-papient/scalable/apps/biglinux-grub-restore.svg",
                "app_categories": "Star System",
            },
            {
                "app_id": "timeshift-gtk",
                "app_name": _("Snapshots and backups"),
                "app_description": _("Create or activate restore points"),
                "app_icon": "timeshift",
                "app_categories": "Star System",
            },
            {
                "app_id": "biglinux-settings",
                "app_name": _("Biglinux Settings"),
                "app_description": _("Simplify switching BigLinux operation."),
                "app_icon": "biglinux-settings",
                "app_categories": "Star System",
            },
            {
                "app_id": "big-themes-gui",
                "app_name": _("BigLinux Themes"),
                "app_exec": "big-theme-gui",
                "app_description": _(
                    "We provide complete configurations for you to select in an extremely simple way."
                ),
                "app_icon": "big-theme-gui",
                "app_categories": "Star Personalization",
            },
            {
                "app_id": "kcm_lookandfeel",
                "app_categories": "Personalization",
            },
            {
                "app_id": "kcm_feedback",
                "app_description": _(
                    "Configure feedback and usage report preferences."
                ),
                "app_categories": "System",
            },
            {
                "app_id": "kcm_solid_actions",
                "app_description": _(
                    "Configure automatic actions for when devices are connected."
                ),
                "app_categories": "Hardware",
            },
            {
                "app_id": "kcm_plasmasearch",
                "app_exec": "kcmshell6 kcm_plasmasearch",
                "app_description": _(
                    "Configure search and indexing options in Plasma."
                ),
                "app_categories": "System",
            },
            {
                "app_id": "kcm_kwin_virtualdesktops",
                "app_categories": "System",
            },
            {
                "app_id": "stoken-gui",
                "app_categories": "Hardware",
            },
        ]
