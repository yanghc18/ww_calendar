# Work Week Calendar Widget

A Python-based calendar widget that displays work weeks and dates in a clean, modern interface.

## Features

- Displays current month with work week numbers
- Shows previous and next month dates for better context
- Highlights today's date
- Draggable window interface
- Always-on-top display
- Navigation between months
- Auto-refreshes every hour

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

## Running the Calendar Widget

### Windows
Double-click `run_calendar.bat` to start the calendar widget.

### Command Line
Navigate to the project directory and run:
```bash
python src/calendar_widget.py
```

## Usage

- Use the "◀" and "▶" buttons to navigate between months
- Click "Today" to return to the current month
- Drag the title bar to move the window
- Click the × button to close the calendar
- The calendar automatically refreshes every hour

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