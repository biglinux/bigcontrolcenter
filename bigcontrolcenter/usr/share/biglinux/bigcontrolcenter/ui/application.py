"""
BigControlCenter - Application class
"""

import gi
import os
import json
import gettext
from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gio, GLib, Adw, Gdk, Pango

from ui.category_sidebar import CategorySidebar
from ui.program_grid import ProgramGrid
from ui.device_connection_dialog import DeviceConnectionDialog
from utils.app_finder import AppFinder

# Setup translations
try:
    lang_translations = gettext.translation(
        "bigcontrolcenter", localedir="/usr/share/locale", fallback=True
    )
    lang_translations.install()
    _ = lang_translations.gettext
except Exception:
    # Fallback if translation fails
    _ = lambda x: x


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
        self.icon_size = 64  # Set standard icon size

        # Set up CSS provider for styling
        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(b"""
            .category-button {
                padding: 12px;
                border-radius: 0;
                margin: 0;
            }
            
            .category-button:hover {
                background-color: alpha(@accent_bg_color, 0.1);
            }
            
            .category-button.selected {
                background-color: alpha(@accent_bg_color, 0.1);
            }
            
            .program-button {
                padding: 8px;
                border-radius: 12px;
                margin: 6px;
            }
            
            .program-button:hover {
                background-color: alpha(@accent_bg_color, 0.1);
            }
            
            .program-icon {
                min-width: 64px !important;
                min-height: 64px !important;
                max-width: 64px !important;
                max-height: 64px !important;
                width: 64px !important;
                height: 64px !important;
                -gtk-icon-size: fixed;
                -gtk-icon-transform: none;
                -gtk-icon-effect: none;
                object-fit: contain;
                padding: 0;
                margin: 0;
                box-sizing: border-box;
                flex-shrink: 0;
                flex-grow: 0;
                scale: 1;
            }
            
            image.program-icon {
                width: 64px !important;
                height: 64px !important;
            }
            
            .fixed-drawing-area {
                min-width: 64px !important;
                min-height: 64px !important;
                max-width: 64px !important;
                max-height: 64px !important;
                width: 64px !important;
                height: 64px !important;
                padding: 0 !important;
                margin: 0 !important;
                box-sizing: border-box !important;
            }
            
            /* Additional rule to prevent parent widgets from affecting size */
            .fixed-drawing-area * {
                min-width: 64px !important;
                min-height: 64px !important;
                max-width: 64px !important;
                max-height: 64px !important;
            }
            
            .program-name {
                font-weight: bold;
                margin-top: 8px;
            }
            
            .search-bar {
                margin: 8px 16px;
            }
            
            .status-bar {
                border-top: 1px solid @borders;
                padding: 6px 10px;
                font-size: 0.9em;
                color: @text_color;
                background-color: @view_bg_color;
            }
            
            .sidebar-content {
                padding: 12px;
                background-color: @view_bg_color;
            }
            
            .navigation-sidebar {
                background-color: @sidebar_bg_color;
            }
            
            .navigation-sidebar:backdrop {
                background-color: @sidebar_bg_color;
            }
            
            .navigation-title {
                font-weight: bold;
                font-size: 1.1em;
            }
            
            .view-switcher {
                margin: 8px 0;
            }
            
            /* Fixed container for program icons to prevent parent influence */
            .program-icon-container {
                min-width: 64px !important;
                max-width: 64px !important;
                min-height: 64px !important;
                max-height: 64px !important;
                width: 64px !important;
                height: 64px !important;
                overflow: hidden;
                margin: auto;
                position: relative !important;
                transform: none !important;
                scale: none !important;
                resize: none !important;
                box-sizing: border-box !important;
                background-size: 64px 64px !important;
                transform-origin: center !important;
                isolation: isolate !important;
            }
            
            /* Ensure icons themselves never resize */
            image {
                transform-box: fill-box !important;
                transform: none !important;
                transition: none !important;
                animation: none !important;
                scale: 1 !important;
            }
            
            /* Override any attempts to scale by parent containers */
            box .program-icon-container,
            grid .program-icon-container,
            flowbox .program-icon-container {
                width: 64px !important;
                height: 64px !important;
                scale: 1 !important;
                min-width: 64px !important;
                min-height: 64px !important;
                max-width: 64px !important;
                max-height: 64px !important;
            }
            
            /* Additional constraints for FlowBoxChild and all possible parents */
            flowboxchild, button, box {
                min-width: fit-content;
                min-height: fit-content;
            }
            
            /* Ensure the program grid doesn't compress icons */
            flowbox {
                min-child-width: 80px;
                min-child-height: 100px;
            }
        """)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def on_activate(self, app):
        """Callback for application activation"""
        # Remove the unsupported property setting
        # Gtk.Settings.get_default().set_property("gtk-icon-size", 64)  # This is not supported in GTK4

        # Create the main window with a simplified structure
        self.window = Adw.ApplicationWindow(application=app)
        self.window.set_default_size(1000, 700)
        self.window.set_title(_("Control Center"))

        # Set the application icon
        # self.window.set_icon_name("bigcontrolcenter")

        # Create the toast overlay for notifications (can be used for status messages)
        toast_overlay = Adw.ToastOverlay()
        self.window.set_content(toast_overlay)

        # Create the main layout with NavigationSplitView as the primary structure
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_min_sidebar_width(240)
        self.split_view.set_sidebar_width_fraction(0.25)
        self.split_view.set_show_content(True)
        toast_overlay.set_child(self.split_view)

        # Create sidebar navigation view
        self.sidebar_view = Adw.NavigationView()

        # Create the category sidebar with toolbar
        sidebar_toolbar_view = Adw.ToolbarView()

        # Add header to sidebar
        sidebar_header = Adw.HeaderBar()

        # Add bigger BigControlCenter icon to the sidebar header
        app_icon = Gtk.Image.new_from_icon_name("bigcontrolcenter")
        app_icon.set_pixel_size(25)  # Larger icon size
        app_icon.set_margin_start(8)
        app_icon.set_margin_end(8)

        # Create a WindowHandle to make the icon area draggable (without checking description)
        handle = Gtk.WindowHandle()
        handle.set_child(app_icon)
        sidebar_header.pack_start(handle)

        sidebar_header.set_title_widget(Adw.WindowTitle.new(_("Control Center"), ""))
        sidebar_header.set_show_end_title_buttons(False)

        # Remove search button from header - we'll keep search visible instead
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

        # Create menu button for About dialog
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu_button.set_tooltip_text(_("Menu"))

        # Create menu model
        menu = Gio.Menu()
        menu.append(_("About"), "app.about")
        menu_button.set_menu_model(menu)
        content_header.pack_end(menu_button)

        # Add action for the about dialog
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action)
        self.add_action(about_action)

        # Create search entry (always visible, not hidden)
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(_("Search..."))
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.set_visible(True)  # Always visible
        # Remove horizontal expansion to keep the search field at its natural width
        self.search_entry.set_hexpand(False)

        # Set a reasonable width for the search entry
        self.search_entry.set_width_chars(
            20
        )  # Set a width for approximately 20 characters

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
        self.status_bar.set_halign(Gtk.Align.START)
        self.status_bar.set_hexpand(True)
        self.status_bar.set_margin_start(10)
        self.status_bar.set_margin_end(10)
        self.status_bar.set_margin_top(6)
        self.status_bar.set_margin_bottom(6)
        self.status_bar.set_wrap(True)
        self.status_bar.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.status_bar.set_xalign(0.0)
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
        self.configure_program_grid_for_fixed_icons()  # Add this line

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

    def load_programs(self):
        """Load program data from app_finder"""
        app_finder = AppFinder()
        # Force regeneration of the JSON data on every startup
        self.programs = app_finder.get_programs(generate_cache=True)

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

    def on_search_button_toggled(self, button):
        """This method is no longer needed since search is always visible,
        but we'll keep it for backward compatibility"""
        pass

    def create_fixed_size_icon(self, icon_name):
        """Create an icon with fixed 64x64 size that won't resize with window"""
        drawing_area = Gtk.DrawingArea()
        drawing_area.set_content_width(64)
        drawing_area.set_content_height(64)
        drawing_area.set_size_request(64, 64)
        drawing_area.set_hexpand(False)
        drawing_area.set_vexpand(False)
        drawing_area.add_css_class("program-icon-container")
        drawing_area.add_css_class("fixed-drawing-area")

        def draw_function(widget, cr, width, height, data):
            theme = Gtk.IconTheme.get_for_display(widget.get_display())
            try:
                icon_info = theme.lookup_icon(
                    icon_name, [], 64, 1, Gtk.TextDirection.NONE, 0
                )
                if icon_info:
                    cr.set_source_rgba(0, 0, 0, 0)
                    cr.paint()
                    texture = icon_info.get_texture()
                    if texture:
                        x = (64 - texture.get_width()) / 2
                        y = (64 - texture.get_height()) / 2
                        Gdk.cairo_set_source_texture(cr, texture, x, y)
                        cr.paint()
            except Exception as e:
                print(f"Error loading icon {icon_name}: {e}")

        drawing_area.set_draw_func(draw_function, None)
        frame = Gtk.AspectFrame()
        frame.set_child(drawing_area)
        frame.set_size_request(64, 64)
        frame.set_hexpand(False)
        frame.set_vexpand(False)
        frame.set_ratio(1.0)
        frame.set_obey_child(False)
        frame.set_xalign(0.5)
        frame.set_yalign(0.5)
        return frame

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

    def _on_window_size_change(self, widget, allocation):
        """Force icon sizes whenever window is resized"""

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
