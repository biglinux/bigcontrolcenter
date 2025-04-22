"""
BigControlCenter - Category sidebar component
"""

import gi
import gettext

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, GLib, Pango, Gdk

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


class CategoryRow(Gtk.ListBoxRow):
    """Custom ListBoxRow that stores a category name"""

    def __init__(self, category_name):
        super().__init__()
        self.category_name = category_name
        self.set_selectable(False)
        self.set_activatable(True)
        # Add CSS class for styling
        self.add_css_class("category-row")
        # Remove the problematic line that was trying to set background color directly


class CategorySidebar(Gtk.Box):
    """Sidebar with category buttons for filtering applications"""

    def __init__(self, app):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.app = app

        # Create and load CSS for active category styling
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .active-category {
                background-color: alpha(currentColor, 0.1);
                border-radius: 6px;
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        self.set_hexpand(False)
        self.set_vexpand(True)
        self.set_size_request(220, -1)  # Width 220, default height

        # Add CSS classes
        self.add_css_class("sidebar")

        # Create a scrolled window for the category list
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        self.append(scrolled_window)

        # Create a list box for categories
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.list_box.add_css_class("navigation-sidebar")

        # Connect the row-activated signal directly to the list box
        self.list_box.connect("row-activated", self._on_row_activated)

        scrolled_window.set_child(self.list_box)

        # Define categories with English labels and translations
        self.categories = [
            {"name": "Star", "icon": "view-app-grid-symbolic", "label": _("Main")},
            {
                "name": "Network",
                "icon": "network-wireless-symbolic",
                "label": _("Network and Internet"),
            },
            {"name": "Phone", "icon": "phone-symbolic", "label": _("Phone")},
            {
                "name": "Personalization",
                "icon": "preferences-desktop-display-symbolic",
                "label": _("Customize"),
            },
            {
                "name": "Language",
                "icon": "globe-symbolic",
                "label": _("Region and Language"),
            },
            {
                "name": "Multimedia",
                "icon": "audio-x-generic-symbolic",
                "label": _("Multimedia"),
            },
            {
                "name": "Account",
                "icon": "system-users-symbolic",
                "label": _("Accounts"),
            },
            {
                "name": "Hardware",
                "icon": "preferences-system-devices-symbolic",
                "label": _("Devices"),
            },
            {
                "name": "System",
                "icon": "preferences-system-symbolic",
                "label": _("System"),
            },
            {"name": "About", "icon": "help-about-symbolic", "label": _("About")},
            {
                "name": "Other",
                "icon": "applications-other-symbolic",
                "label": _("Other"),
            },
        ]

        # Create the category buttons
        self.category_buttons = {}
        self.category_rows = {}

        for category in self.categories:
            # Create each category row with its own handler
            self._add_category_row(category)

        # Keep track of non-empty categories
        self.non_empty_categories = set()

    def _add_category_row(self, category):
        """Add a single category row to the list box"""
        # Use our custom row class that stores the category name
        row = CategoryRow(category["name"])

        self.list_box.append(row)

        button = self._create_category_button(category)
        row.set_child(button)
        self.category_buttons[category["name"]] = button
        self.category_rows[category["name"]] = row

        # Initially hide all rows until we know which ones have apps
        row.set_visible(False)

    def _on_row_activated(self, list_box, row):
        """Handle row activation - gets the category name from the row attribute"""
        if hasattr(row, "category_name"):
            print(f"Category selected: {row.category_name}")  # Debug output
            self._on_category_selected(row.category_name)

    def select_initial_category(self):
        """Select the initial category after all UI components are initialized"""
        # First try to select "Star" if it has apps
        if "Star" in self.non_empty_categories:
            self._on_category_selected("Star")
        # Otherwise select the first non-empty category
        elif len(self.non_empty_categories) > 0:
            self._on_category_selected(next(iter(self.non_empty_categories)))

    def update_categories_visibility(self, programs):
        """Update which categories are visible based on program availability"""
        # Clear previous set of non-empty categories
        self.non_empty_categories.clear()

        # Find all categories that have at least one app
        category_counts = {}
        for program in programs:
            categories = program.get("app_categories", "").split()
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1
                self.non_empty_categories.add(category)

        # Show/hide categories based on whether they have programs
        for category in self.categories:
            name = category["name"]
            if name in self.category_rows:
                row = self.category_rows[name]
                has_programs = name in self.non_empty_categories
                row.set_visible(has_programs)

        print(f"Non-empty categories: {self.non_empty_categories}")

    def _create_category_button(self, category):
        """Create a button for a category"""
        button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button.set_margin_start(12)
        button.set_margin_end(12)
        button.set_margin_top(8)
        button.set_margin_bottom(8)

        # Create icon with consistent sizing
        icon = Gtk.Image.new_from_icon_name(category["icon"])
        icon.set_pixel_size(24)  # Standard size for sidebar icons
        icon.set_margin_end(8)
        button.append(icon)

        # Create label with proper text wrapping
        label = Gtk.Label(label=category["label"])
        label.set_halign(Gtk.Align.START)
        label.set_hexpand(True)
        label.set_wrap(True)
        label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        label.set_xalign(0.0)  # Left-align text
        label.set_max_width_chars(20)
        button.append(label)

        return button

    def _on_category_selected(self, category_name):
        """Handle category selection"""
        # Update UI to show active category
        for name, row in self.category_rows.items():
            if name == category_name:
                row.add_css_class("active-category")
            else:
                row.remove_css_class("active-category")

        # Update application state
        self.app.set_category(category_name)
