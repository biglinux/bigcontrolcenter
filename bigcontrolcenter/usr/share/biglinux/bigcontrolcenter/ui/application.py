"""
BigControlCenter - Application class
"""

import gi
import gettext
import json
import os
from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gio, GLib, Adw, Gdk

from ui.category_sidebar import CategorySidebar
from ui.program_grid import ProgramGrid
from ui.device_connection_dialog import DeviceConnectionDialog
from utils.app_finder import AppFinder

# Setup translations
lang_translations = gettext.translation(
    "bigcontrolcenter", localedir="/usr/share/locale", fallback=True
)
lang_translations.install()
_ = lang_translations.gettext


class BigControlCenterApp(Adw.Application):
    """Main application class for BigControlCenter"""

    def __init__(self, application_id, flags):
        super().__init__(application_id=application_id, flags=flags)
        self.connect("activate", self.on_activate)

        # Initialize application data
        self.programs = []
        self.filtered_programs = []
        self.current_category = "Star"
        self.program_grid = None  # Initialize as None until created

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
            width = self.config.get("width", 1000)
            height = self.config.get("height", 620)
            self.window.set_default_size(width, height)

        self.window.set_title(_("Control Center"))

        # Connect window signals to save configuration
        self.window.connect("close-request", self.on_window_close)

        # Set the application icon
        # self.window.set_icon_name("bigcontrolcenter")

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
        self.configure_program_grid_for_fixed_icons()

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
            # Handle program navigation if we have a flow box
            try:
                if (
                    hasattr(self.program_grid, "flow_box")
                    and self.program_grid.flow_box
                ):
                    flow_box = self.program_grid.flow_box

                    # If Enter/Space and something is selected, activate it
                    if keyval in (Gdk.KEY_Return, Gdk.KEY_space):
                        try:
                            child = self._get_selected_flow_child(flow_box)
                            if child:
                                # Manually call child's button click handler instead
                                button = self._find_button_in_child(child)
                                if button:
                                    button.clicked()  # Emit clicked signal directly
                                return True
                        except Exception as e:
                            print(f"Error activating flow box child: {e}")

                    # Arrow key navigation - always force selection and focus
                    elif keyval in (
                        Gdk.KEY_Up,
                        Gdk.KEY_Down,
                        Gdk.KEY_Left,
                        Gdk.KEY_Right,
                    ):
                        # Simplify: just grab focus on the flow box and let GTK handle navigation
                        flow_box.grab_focus()
                        # Don't consume the event - let GTK's default handler manage navigation
                        return False
            except Exception as e:
                print(f"Error in flow box navigation: {e}")

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
            Gdk.KEY_Up,
            Gdk.KEY_Down,
            Gdk.KEY_Left,
            Gdk.KEY_Right,
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
        if self.program_grid:
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
                if hasattr(cat, "button") and cat["button"] is not None:
                    cat["button"].add_css_class("selected")
                for other_cat in self.category_sidebar.categories:
                    if (
                        other_cat["name"] != category
                        and hasattr(other_cat, "button")
                        and other_cat["button"] is not None
                    ):
                        other_cat["button"].remove_css_class("selected")
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
            else:
                print(f"Special command: {app_exec}")
                self.set_status_message(
                    _("Executing special command: {0}").format(app_exec)
                )
        else:
            try:
                self.set_status_message(_("Launching: {0}").format(app_exec))
                GLib.spawn_command_line_async(app_exec)
            except GLib.Error as e:
                self.set_status_message(_("Error launching program: {0}").format(e))
                print(f"Error running command: {e}")

    def show_android_usb_dialog(self):
        """Show dialog with Android USB tethering instructions"""
        dialog = DeviceConnectionDialog(self.window)
        dialog.show_android_dialog()

    def show_ios_usb_dialog(self):
        """Show dialog with iOS USB tethering instructions"""
        dialog = DeviceConnectionDialog(self.window)
        dialog.show_ios_dialog()

    def configure_program_grid_for_fixed_icons(self):
        """Configure the program grid to respect fixed icon sizes"""
        if hasattr(self.program_grid, "flowbox"):
            flowbox = self.program_grid.flowbox
            flowbox.set_homogeneous(False)
            flowbox.set_column_spacing(16)
            flowbox.set_row_spacing(16)
            flowbox.set_valign(Gtk.Align.START)
            flowbox.set_halign(Gtk.Align.START)
            flowbox.set_min_children_per_line(1)
            flowbox.set_max_children_per_line(10)
            self.window.connect("size-allocate", self._on_window_size_change)

        def force_icon_size(widget):
            if widget.has_css_class("program-icon-container"):
                widget.set_size_request(64, 64)
                return True
            if isinstance(widget, Gtk.Box) or isinstance(widget, Gtk.FlowBox):
                for child in widget:
                    force_icon_size(child)
            return False

        if self.program_grid:
            force_icon_size(self.program_grid)

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

    def _get_selected_flow_child(self, flow_box):
        """Get the currently selected flow box child safely"""
        try:
            # In GTK4, selected_children are accessed differently
            child = None

            # Try to get the child that has focus
            current = flow_box.get_first_child()
            while current:
                if current.has_focus():
                    return current
                current = current.get_next_sibling()

            # If no child has focus, try selecting the first one
            if flow_box.get_first_child():
                return flow_box.get_first_child()

        except Exception as e:
            print(f"Error getting selected child: {e}")

        return None

    def _find_button_in_child(self, child):
        """Find the button inside a flow box child"""
        try:
            # The child's child should be our button
            if isinstance(child, Gtk.FlowBoxChild):
                button = child.get_child()
                if isinstance(button, Gtk.Button):
                    return button
        except Exception as e:
            print(f"Error finding button in child: {e}")

        return None

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                self.config = json.load(f)

    def save_config(self):
        """Save window configuration to JSON file"""
        try:
            # Create config directory if it doesn't exist
            os.makedirs(self.config_dir, exist_ok=True)

            # Get current window state
            maximized = self.window.is_maximized()

            if not maximized:
                width, height = self.window.get_default_size()
                self.config["width"] = width
                self.config["height"] = height

            self.config["maximized"] = maximized

            # Save to file
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def on_window_close(self, window):
        """Save window configuration when closing"""
        self.save_config()
        return False  # Allow the window to close

    def _on_window_size_change(self, window, allocation):
        """Update window size in config when size changes (if not maximized)"""
        if not window.is_maximized():
            width = allocation.get_width()
            height = allocation.get_height()
            if width > 0 and height > 0:
                self.config["width"] = width
                self.config["height"] = height
                self.config["maximized"] = False

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
