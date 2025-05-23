# Work Week Calendar Widget

A sleek, modern Python-based calendar widget designed to display work weeks and dates with an intuitive, customizable interface. Stay organized with this handy desktop utility!

## Features

- **Modern Dark-Themed UI**: A visually appealing and clear interface.
- **Work Week Display**: Clearly shows work week numbers alongside dates.
- **Comprehensive Calendar View**: Displays the current month, with days from the previous and next months for context.
- **Today's Date Highlight**: Easily spot the current day.
- **Custom Draggable Window**: A custom title bar allows easy window repositioning.
- **Toggleable Window Layering**:
    - **Always on Top**: Keep the calendar visible above all other applications.
    - **Always on Bottom**: Attempt to place the calendar on the desktop layer (OS-dependent behavior, see 'Platform-Specific Notes').
    - Easily switch between modes with a dedicated pin button.
- **Adjustable Transparency**: Control the window's opacity with a slider for seamless desktop integration.
- **Month Navigation**: Navigate to previous/next months using arrow buttons ("←", "→").
- **"Today" Button**: Quickly jump back to the current month.
- **Auto-Refresh**: Calendar data (e.g., 'today' highlight) auto-refreshes periodically.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Optional Dependencies for Advanced Features

The "Always on Bottom" window mode relies on platform-specific libraries. These are not included in `requirements.txt` to allow the core application to run on any OS without requiring unnecessary installations. If you wish to use the "Always on Bottom" feature, you may need to install the following:

-   **Windows**: `pywin32`
    ```bash
    pip install pywin32
    ```
-   **macOS**: `pyobjc-core` and `pyobjc-framework-cocoa`
    ```bash
    pip install pyobjc-core pyobjc-framework-cocoa
    ```
-   **Linux**: `python-xlib`
    ```bash
    pip install python-xlib
    ```

If these libraries are not present, the "Always on Bottom" mode will attempt to lower the window using standard Tkinter methods, but true desktop-layer integration may not occur. The application will print a message to the console if a required library for an OS-specific feature is missing. Transparency effects also rely on OS and window manager capabilities.

## Running the Calendar Widget

### Windows
Double-click `run_calendar.bat` to start the calendar widget.

### Command Line
Navigate to the project directory and run:
```bash
python src/calendar_widget.py
```

## Usage

- Use the "←" and "→" buttons to navigate between months
- Click "Today" to return to the current month
- Drag the title bar to move the window
- Click the × button to close the calendar
- The calendar automatically refreshes every hour
- Use the pin button to toggle between "Always on Top" and "Always on Bottom" modes.
- Use the slider at the bottom to adjust window transparency.

## Project Structure

- `src/`: Source code directory
  - `calendar_widget.py`: Main calendar widget implementation
  - `main.py`: Work week calculation utilities
- `tests/`: Test files directory
- `requirements.txt`: Project dependencies
- `run_calendar.bat`: Windows shortcut to run the calendar widget 

### Run bat when log on
This works for scripts that don’t need admin privileges and only run when you log in.

Open the Startup Folder:
Press Win + R, type shell:startup, and hit Enter. This opens C:\Users\YourUsername\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup.
Add Your Script:
Place the script file (e.g., my_script.bat) or a shortcut to it in this folder.
For .ps1 or .py scripts, create a shortcut:
Right-click the script > "Create shortcut."
Edit the shortcut’s "Target" to include the interpreter (e.g., powershell.exe -File "C:\Scripts\my_script.ps1" or C:\Python39\python.exe "C:\Scripts\my_script.py").
Move the shortcut to the Startup folder.
Test It:
Log out and back in, or restart, to verify it runs.