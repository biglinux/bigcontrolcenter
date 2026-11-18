"""
BigControlCenter - Application class
"""

import gettext
import json
import logging
import os
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gdk, Gio, GLib, Gtk

from ui.category_sidebar import CategorySidebar
from ui.device_connection_dialog import DeviceConnectionDialog
from ui.program_grid import ProgramGrid
from utils.app_finder import AppFinder

# Setup translations
lang_translations = gettext.translation(
    "bigcontrolcenter", localedir="/usr/share/locale", fallback=True
)
lang_translations.install()
_ = lang_translations.gettext

logger = logging.getLogger(__name__)


class BigControlCenterApp(Adw.Application):
    """Main application class for BigControlCenter"""

    def __init__(self, application_id, flags):
        super().__init__(application_id=application_id, flags=flags)
        self.connect("activate", self.on_activate)

        # Set application icon - needed for taskbar in Wayland
        GLib.set_prgname(application_id)

        # Initialize application data
        self.programs = []
        self.filtered_programs = []
        self.current_category = "Star"

        # Config file path
        self.config_dir = os.path.expanduser("~/.config/bigcontrolcenter")
        self.config_path = os.path.join(self.config_dir, "config.json")
        self.config = {}

        # Set up CSS provider for styling
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(b"""
            .status-bar {
                border-top: 1px solid @borders;
                padding: 6px 10px;
            }
        """)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def on_activate(self, app):
        """Callback for application activation"""

        # Load configuration before creating the window
        self.load_config()

        # Create the main window with a simplified structure
        self.window = Adw.ApplicationWindow(application=app)

        # Apply saved window size and state
        if self.config.get("maximized", False):
            self.window.maximize()
        else:
            width = self.config.get("width", 1100)
            height = self.config.get("height", 620)
            self.window.set_default_size(width, height)

        self.window.set_title(_("Control Center"))

        # Connect window signals to save configuration
        self.window.connect("close-request", self.on_window_close)

        # Create the toast overlay for notifications (can be used for status messages)
        toast_overlay = Adw.ToastOverlay()
        toast_overlay.add_css_class("background-as-view-bg-color")

        # Add transparent background style to CSS provider
        css_data = (
            self.css_provider.to_string()
            + """
            .background-as-view-bg-color {
            background-color: var(--view-bg-color);
            }
        """
        )
        self.css_provider.load_from_data(css_data.encode())
        self.window.set_content(toast_overlay)

        # Create the main layout with NavigationSplitView as the primary structure
        self.split_view = Adw.NavigationSplitView()
        toast_overlay.set_child(self.split_view)

        # Create sidebar navigation view
        self.sidebar_view = Adw.NavigationView()

        # Create the category sidebar with toolbar
        sidebar_toolbar_view = Adw.ToolbarView()

        # Add header to sidebar
        sidebar_header = Adw.HeaderBar()

        # Create action for the about dialog
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action)
        self.add_action(about_action)

        # Add BigControlCenter icon as a clickable button that opens the About dialog
        app_icon_button = Gtk.Button()
        app_icon_button.set_tooltip_text(_("About Control Center"))
        app_icon = Gtk.Image.new_from_icon_name("bigcontrolcenter")
        app_icon.set_pixel_size(25)  # Larger icon size
        # Create css to after apply 5px padding left and right
        app_icon_button.add_css_class("icon-button-padded")
        self.css_provider.load_from_data(
            (
                self.css_provider.to_string()
                + """
            .icon-button-padded {
            padding: 0px;
            }
            .flat:hover {
            background-color: transparent;
            box-shadow: none;
            }
        """
            ).encode()
        )

        app_icon_button.set_child(app_icon)
        app_icon_button.add_css_class("flat")
        # Connect to wrapper method to handle parameter mismatch
        app_icon_button.connect("clicked", self.on_app_icon_clicked)

        # Set cursor using GTK native property instead of CSS
        controller = Gtk.EventControllerMotion.new()
        controller.connect("enter", self.on_app_icon_enter)
        controller.connect("leave", self.on_app_icon_leave)
        app_icon_button.add_controller(controller)

        # Create a WindowHandle to make the icon area draggable
        handle = Gtk.WindowHandle()
        handle.set_child(app_icon_button)
        sidebar_header.pack_start(handle)

        sidebar_header.set_title_widget(Adw.WindowTitle.new(_("Control Center"), ""))
        sidebar_toolbar_view.add_top_bar(sidebar_header)

        # Create the category sidebar
        self.category_sidebar = CategorySidebar(self)
        sidebar_toolbar_view.set_content(self.category_sidebar)

        # Create sidebar page
        sidebar_page = Adw.NavigationPage.new(sidebar_toolbar_view, _("Categories"))
        self.sidebar_view.push(sidebar_page)

        # Create content navigation view
        self.content_view = Adw.NavigationView()

        # Create content with toolbar
        content_toolbar_view = Adw.ToolbarView()

        # Add header to content
        content_header = Adw.HeaderBar()
        self.content_title = Adw.WindowTitle.new(_("Programs"), "")
        content_header.set_title_widget(self.content_title)

        # Create search entry (always visible, not hidden)
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(_("Search..."))
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.set_visible(True)  # Always visible
        self.search_entry.set_hexpand(False)
        self.search_entry.set_width_chars(20)
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.append(self.search_entry)
        content_header.set_title_widget(search_box)

        content_toolbar_view.add_top_bar(content_header)

        # Add status bar at the bottom of the content
        self.status_revealer = Gtk.Revealer()
        self.status_revealer.set_transition_type(Gtk.RevealerTransitionType.CROSSFADE)
        self.status_revealer.set_transition_duration(
            150
        )  # 150ms for smooth transitions
        self.status_bar = Gtk.Label()
        self.status_bar.set_wrap(True)
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        status_box.append(self.status_bar)
        status_box.add_css_class("status-bar")
        self.status_revealer.set_child(status_box)
        self.status_revealer.set_reveal_child(False)
        self.status_revealer.set_visible(False)
        content_toolbar_view.add_bottom_bar(self.status_revealer)

        # Create the program grid
        self.program_grid = ProgramGrid(self)
        content_toolbar_view.set_content(self.program_grid)

        # Create content page
        self.content_page = Adw.NavigationPage.new(content_toolbar_view, "Programs")
        self.content_view.push(self.content_page)

        # Set up the split view with navigation views
        sidebar_nav_page = Adw.NavigationPage.new(self.sidebar_view, "Categories")
        content_nav_page = Adw.NavigationPage.new(self.content_view, "Content")
        self.split_view.set_sidebar(sidebar_nav_page)
        self.split_view.set_content(content_nav_page)

        # Set initial status message
        self.set_status_message("")

        # Load application data
        self.load_programs()

        # Now that everything is initialized, set the initial category
        self.category_sidebar.select_initial_category()

        # Show the window
        self.window.present()

        # Add key event controller to redirect key presses to search
        key_controller = Gtk.EventControllerKey.new()
        key_controller.connect("key-pressed", self._on_key_pressed)
        self.window.add_controller(key_controller)

    def _on_key_pressed(self, controller, keyval, keycode, state):
        """Handle key presses and redirect to search entry"""
        # Check for backspace key - always remove characters from search
        if keyval == Gdk.KEY_BackSpace:
            current_text = self.search_entry.get_text()
            if current_text:  # Only if there's text to delete
                self.search_entry.grab_focus()
                self.search_entry.set_text(current_text[:-1])
                self.search_entry.set_position(-1)  # Position cursor at end
                return True

        # Check for navigation keys
        if keyval in (
            Gdk.KEY_Up,
            Gdk.KEY_Down,
            Gdk.KEY_Left,
            Gdk.KEY_Right,
            Gdk.KEY_Return,
            Gdk.KEY_space,
        ):
            flow_box = self.program_grid.flow_box

            # Enter/Space launches the focused program, or the first one
            if keyval in (Gdk.KEY_Return, Gdk.KEY_space):
                child = flow_box.get_focus_child() or flow_box.get_first_child()
                if child:
                    child.activate()
                    return True

            # Arrow keys move focus into the grid and let GTK navigate it
            else:
                flow_box.grab_focus()
                return False

        # Skip if search is already focused
        if self.search_entry.has_focus():
            return False

        # Skip if modifier keys are pressed (like Ctrl, Alt, etc.)
        if state & (
            Gdk.ModifierType.CONTROL_MASK
            | Gdk.ModifierType.ALT_MASK
            | Gdk.ModifierType.SHIFT_MASK
        ):
            return False

        # Skip special keys
        if keyval in (
            Gdk.KEY_Escape,
            Gdk.KEY_Tab,
            Gdk.KEY_Return,
        ):
            return False

        # Get the character
        ch = chr(Gdk.keyval_to_unicode(keyval))

        # Skip if not a printable character
        if not ch.isprintable():
            return False

        # Focus search entry and append the character
        self.search_entry.grab_focus()
        current_text = self.search_entry.get_text()
        self.search_entry.set_text(current_text + ch)

        # Position cursor at the end
        self.search_entry.set_position(-1)

        # Mark event as handled
        return True

    def load_programs(self):
        """Load program data from app_finder"""
        app_finder = AppFinder()
        # Force regeneration of the JSON data on every startup
        self.programs = app_finder.get_programs()

        # Update which categories are visible based on program availability
        if hasattr(self, "category_sidebar"):
            self.category_sidebar.update_categories_visibility(self.programs)

        self.filter_programs()
        self.set_status_message("")

    def filter_programs(self):
        """Filter programs based on search text and selected category"""
        search_text = self.search_entry.get_text().lower()
        if search_text:
            self.filtered_programs = [
                program
                for program in self.programs
                if (
                    search_text in program["app_name"].lower()
                    or (
                        program.get("app_description")
                        and search_text in program["app_description"].lower()
                    )
                    or search_text in program["app_id"].lower()
                )
            ]
        else:
            self.filtered_programs = [
                program
                for program in self.programs
                if self.current_category in program.get("app_categories", "").split()
            ]
        self.filtered_programs.sort(key=lambda x: x["app_name"])
        self.program_grid.update_grid(self.filtered_programs)
        self.set_status_message("")

    def on_search_changed(self, search_entry):
        """Callback for search text changes"""
        self.filter_programs()

    def set_category(self, category):
        """Set the current category and update the programs display"""
        self.current_category = category
        self.search_entry.set_text("")  # Clear search when changing category
        self.filter_programs()
        category_label = "Programs"
        for cat in self.category_sidebar.categories:
            if cat["name"] == category:
                category_label = cat["label"]
                break
        self.content_page.set_title(category_label)
        self.content_title.set_title(category_label)

    def set_status_message(self, message):
        """Set status message and control revealer visibility"""
        self.status_bar.set_text(message)
        is_visible = message != ""
        self.status_revealer.set_reveal_child(is_visible)
        self.status_revealer.set_visible(is_visible)

    def show_description(self, description):
        """Show program description in the status bar"""
        if description:
            self.set_status_message(description)

    def hide_description(self):
        """Reset status bar to empty after showing description"""
        self.set_status_message("")

    def run_program(self, app_exec):
        """Execute a program"""
        if app_exec.startswith("#"):
            if app_exec == "#dialog-android-usb":
                self.show_android_usb_dialog()
            elif app_exec == "#dialog-ios-usb":
                self.show_ios_usb_dialog()
            elif app_exec == "#dialog-reset-display":
                self.show_reset_display_dialog()
            else:
                logger.warning("Unknown special command: %s", app_exec)
                self.set_status_message(
                    _("Executing special command: {0}").format(app_exec)
                )
        else:
            try:
                self.set_status_message(_("Launching: {0}").format(app_exec))
                GLib.spawn_command_line_async(app_exec)
            except GLib.Error as e:
                self.set_status_message(_("Error launching program: {0}").format(e))
                logger.warning("Error running command %s: %s", app_exec, e)

    def show_android_usb_dialog(self):
        """Show dialog with Android USB tethering instructions"""
        dialog = DeviceConnectionDialog(self.window)
        dialog.show_android_dialog()

    def show_ios_usb_dialog(self):
        """Show dialog with iOS USB tethering instructions"""
        dialog = DeviceConnectionDialog(self.window)
        dialog.show_ios_dialog()

    def show_reset_display_dialog(self):
        """Confirm resetting KDE's monitor settings"""
        dialog = Adw.AlertDialog(
            heading=_("Reset display settings?"),
            body=_(
                "Resolution, position, refresh rate, scale and rotation of every monitor return to the defaults detected at the next login, on Wayland and Xorg. This session ends to apply them."
            ),
        )
        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("reset", _("Reset and Log Out"))
        dialog.set_response_appearance("reset", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.set_close_response("cancel")
        dialog.connect("response", self._on_reset_display_response)
        dialog.present(self.window)

    def _on_reset_display_response(self, dialog, response):
        if response != "reset":
            return
        # KWin writes its monitor layout when it exits, so bigcontrolcenter-session
        # resets after the session ends; closing the window ends it.
        try:
            Path(os.environ["BIGCONTROLCENTER_RESET_DISPLAY"]).touch()
        except OSError as e:
            self.set_status_message(
                _("Could not reset display settings: {0}").format(e)
            )
            return
        self.window.close()

    def on_about_action(self, action, param):
        """Show the About dialog for BigControlCenter"""
        about = Adw.AboutWindow.new()
        about.set_application_name(_("Control Center"))
        about.set_version("3.0")
        about.set_developer_name(_("BigLinux Team"))
        about.set_license_type(Gtk.License.GPL_3_0)
        about.set_website("https://www.biglinux.com.br/")
        about.set_issue_url("https://github.com/biglinux/bigcontrolcenter/issues")
        about.set_application_icon("bigcontrolcenter")
        about.set_copyright(_("© 2025 BigLinux Team"))
        about.set_developers([_("BigLinux Team")])
        about.present()

    def load_config(self):
        """Load the saved window state; an unreadable file only costs the saved size."""
        try:
            with open(self.config_path, encoding="utf-8") as f:
                config = json.load(f)
            if not isinstance(config, dict):
                raise TypeError("not a JSON object")
            if not all(
                isinstance(config.get(key, 0), int) for key in ("width", "height")
            ):
                raise TypeError("width and height must be integers")
        except FileNotFoundError:
            return
        except (OSError, ValueError, TypeError) as e:
            logger.warning("Ignoring config %s: %s", self.config_path, e)
            return
        self.config = config

    def save_config(self):
        """Save window configuration to JSON file"""
        maximized = self.window.is_maximized()
        if not maximized:
            width, height = self.window.get_default_size()
            self.config["width"] = width
            self.config["height"] = height
        self.config["maximized"] = maximized

        # A staging file renamed over the config keeps a crash from leaving it truncated.
        staging_path = f"{self.config_path}.{os.getpid()}.tmp"
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            config_name = os.path.basename(self.config_path)
            for stale_path in Path(self.config_dir).glob(f"{config_name}.*.tmp"):
                owner_pid = stale_path.name.removeprefix(f"{config_name}.")
                owner_pid = owner_pid.removesuffix(".tmp")
                if not os.path.exists(f"/proc/{owner_pid}"):
                    stale_path.unlink(missing_ok=True)
            with open(staging_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            os.replace(staging_path, self.config_path)
        except OSError as e:
            logger.warning("Error saving config: %s", e)
            Path(staging_path).unlink(missing_ok=True)

    def on_window_close(self, window):
        """Save window configuration when closing"""
        self.save_config()
        return False  # Allow the window to close

    # Add these new methods to handle button click and cursor changes
    def on_app_icon_clicked(self, button):
        """Wrapper method to call on_about_action with correct parameters"""
        self.on_about_action(None, None)

    def on_app_icon_enter(self, controller, x, y):
        """Change cursor to pointer when mouse enters the app icon button"""
        window = controller.get_widget().get_root()
        if window:
            cursor = Gdk.Cursor.new_from_name("pointer", None)
            window.set_cursor(cursor)

    def on_app_icon_leave(self, controller):
        """Reset cursor when mouse leaves the app icon button"""
        window = controller.get_widget().get_root()
        if window:
            window.set_cursor(None)
