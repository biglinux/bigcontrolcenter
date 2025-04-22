# BigControlCenter

A modern GTK4-based control center for system settings.

## Overview

BigControlCenter is a user-friendly application that provides easy access to system settings and configuration tools. It displays applications categorized by functionality, allowing users to quickly find and launch the tools they need.

## Features

- Modern GTK4 interface with Adwaita styling
- Category-based navigation
- Search functionality for quick access
- Descriptive tooltips for each program
- JSON-based data storage

## Requirements

- Python 3.13 or newer
- GTK4
- libadwaita
- PyGObject

## Installation

1. Ensure you have the required dependencies installed:

```bash
# For Debian/Ubuntu-based systems
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1-dev

# For Arch/Manjaro-based systems
sudo pacman -S python-gobject gtk4 libadwaita
```

2. Clone the repository:

```bash
git clone https://github.com/biglinux/bigcontrolcenter.git
cd bigcontrolcenter
```

3. Make the main script executable:

```bash
chmod +x main.py
```

## Usage

To run BigControlCenter:

```bash
./main.py
```

## Directory Structure

- `main.py`: Main application entry point
- `ui/`: UI components
  - `application.py`: Main application window
  - `category_sidebar.py`: Category navigation sidebar
  - `program_grid.py`: Grid view of programs
- `utils/`: Utility modules
  - `app_finder.py`: Find desktop applications
  - `data_manager.py`: JSON data storage and retrieval
- `data/`: Configuration files
  - `categories.json`: Category definitions

## License

This project is licensed under BSD license.