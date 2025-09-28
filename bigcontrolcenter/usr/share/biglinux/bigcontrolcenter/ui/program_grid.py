"""
BigControlCenter - Program grid component
"""

import gi
import os

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Pango


class ProgramGrid(Gtk.Box):
    """Grid view of program entries"""

    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.app = app

        self.set_hexpand(True)
        self.set_vexpand(True)

        # Add CSS for program buttons - remove background and frames
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .program-button {
            background: none;
            padding: 8px;
            font-weight: inherit;
            min-width: 150px;
            }

            .program-button:hover {
            background: alpha(currentColor, 0.08);
            }

            .program-button:active {
            transform: scale(0.94);
            transition: transform 0.15s ease;
            background-color: alpha(currentColor, 0.15);
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        # Create a scrolled window for the grid
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        self.append(scrolled_window)

        # Create a flow box for the program grid
        self.flow_box = Gtk.FlowBox()
        self.flow_box.set_valign(Gtk.Align.START)
        self.flow_box.set_max_children_per_line(20)
        self.flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.flow_box.set_homogeneous(False)
        self.flow_box.set_column_spacing(12)
        self.flow_box.set_row_spacing(18)
        self.flow_box.set_margin_start(16)
        self.flow_box.set_margin_end(16)
        self.flow_box.set_margin_top(16)
        self.flow_box.set_margin_bottom(16)

        # Connect activation signal
        self.flow_box.connect("child-activated", self._on_child_activated)

        scrolled_window.set_child(self.flow_box)

    def _on_child_activated(self, flow_box, child):
        """Handle activation of a flow box child (button)"""
        # Find the corresponding program and execute it
        index = child.get_index()
        if 0 <= index < len(self.app.filtered_programs):
            program = self.app.filtered_programs[index]
            self.app.run_program(program.get("app_exec", ""))

    def update_grid(self, programs):
        """Update the grid with the given list of programs"""
        # Remove all existing children
        while True:
            child = self.flow_box.get_first_child()
            if child is None:
                break
            self.flow_box.remove(child)

        # Add program buttons
        for program in programs:
            program_button = self._create_program_button(program)
            self.flow_box.append(program_button)

    def _create_program_button(self, program):
        """Create a button for a program"""
        # Create a button
        button = Gtk.Button()
        button.add_css_class("program-button")
        button.connect(
            "clicked", lambda w: self.app.run_program(program.get("app_exec", ""))
        )

        # This will update the status bar instead of showing tooltips
        motion = Gtk.EventControllerMotion.new()
        motion.connect(
            "enter",
            lambda c, x, y: self.app.show_description(
                program.get("app_description", "")
            ),
        )
        motion.connect("leave", lambda c: self.app.hide_description())
        button.add_controller(motion)

        # Create the content box
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        content.set_halign(Gtk.Align.CENTER)
        content.set_valign(Gtk.Align.START)
        button.set_child(content)

        # Program icon - handle both icon names and file paths
        icon_file = program.get("app_icon", "")
        icon = self._create_icon_from_path_or_name(icon_file)
        content.append(icon)

        # Program name - allow text to wrap when it exceeds the window width
        name_label = Gtk.Label(label=program.get("app_name", ""))
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_max_width_chars(20)
        name_label.set_width_chars(10)
        name_label.set_wrap(True)
        name_label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        name_label.set_lines(3)
        name_label.set_justify(Gtk.Justification.CENTER)
        name_label.add_css_class("program-name")
        content.append(name_label)

        # Make the button focusable
        button.set_focusable(True)
        button.set_focus_on_click(True)

        return button

    def _create_icon_from_path_or_name(self, icon_path):
        """Create an icon from either a file path or an icon name"""
        icon = None

        # If empty path, use default icon
        if not icon_path:
            icon = Gtk.Image.new_from_icon_name("application-x-executable")
            icon.set_pixel_size(64)
            return icon

        # Check if it's an absolute path
        if icon_path.startswith("/") and os.path.exists(icon_path):
            try:
                # Load directly from file for absolute paths
                icon = Gtk.Image.new_from_file(icon_path)
                icon.set_pixel_size(64)
                return icon
            except Exception as e:
                print(f"Error loading icon from file '{icon_path}': {e}")
                # Fall through to icon name handling on failure

        # Try to load as an icon name with specific sizes in order of preference
        theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())

        # Check if the icon exists in the theme
        if theme.has_icon(icon_path):
            # Try preferred sizes in order: scalable(SVG), 64x64, 48x48, 128x128
            for size in [64, 48, 128]:
                try:
                    # Try to get the icon at preferred size
                    paintable = theme.lookup_icon(
                        icon_path, size, 1, Gtk.TextDirection.NONE, 0
                    )
                    if paintable:
                        icon = Gtk.Image.new_from_paintable(paintable)
                        icon.set_pixel_size(64)
                        return icon
                except Exception:
                    pass

        # Default approach - may not respect size preferences but will work
        icon = Gtk.Image.new_from_icon_name(icon_path)
        icon.set_pixel_size(64)
        return icon
