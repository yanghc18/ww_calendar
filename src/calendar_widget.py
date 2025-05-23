import tkinter as tk
import platform # Added for OS detection

# OS-specific imports with try-except
try:
    import win32gui, win32con, win32api
except ImportError:
    win32gui = None # Or print a message
    print("Windows specific libraries (pywin32) not found. Skipping Windows-specific features.")

try:
    from AppKit import NSApp, NSWindow, kCGDesktopIconWindowLevel #, NSWindowCollectionBehaviorCanJoinAllSpaces, NSWindowCollectionBehaviorStationary, NSWindowCollectionBehaviorIgnoresCycle
except ImportError:
    NSApp = None # Or print a message
    print("macOS specific libraries (PyObjC) not found. Skipping macOS-specific features.")

try:
    from Xlib import display, X
except ImportError:
    display = None # Or print a message
    print("Linux specific libraries (python-xlib) not found. Skipping Linux-specific features.")

from datetime import date, timedelta
import calendar
from main import get_work_week_number
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class WorkWeekCalendarWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Work Week Calendar")
        self.root.configure(bg='#2E2E2E') # Set root background

        # Define fonts
        self.font_primary = ('Arial', 9)
        self.font_header = ('Arial', 10, 'bold')
        
        # Initialize current view date
        self.current_view = date.today()
        self.is_on_top = True # State variable for pin mode
        self.current_alpha = tk.DoubleVar(value=0.8) # State variable for window transparency
        
        # Make window stay on top (This will be controlled by apply_pin_mode later)
        # self.root.attributes('-topmost', True) 
        
        # Remove window decorations for a cleaner look
        self.root.overrideredirect(True)
        # self.root.attributes('-alpha', 0.8) # Set window transparency (Static - to be replaced by dynamic control)
        
        # Create main frame
        self.frame = tk.Frame(self.root, bg='#2E2E2E', relief='flat')
        self.frame.pack(padx=2, pady=2)
        
        # Add title bar with close button
        self.title_bar = tk.Frame(self.frame, bg='#2E2E2E', relief='flat', height=20)
        self.title_bar.pack(fill='x')
        self.title_bar.pack_propagate(False)
        
        # Add title label
        self.title_label = tk.Label(self.title_bar, text="Work Week Calendar", bg='#2E2E2E', fg='#E0E0E0', font=self.font_primary)
        self.title_label.pack(side='left', padx=5)
        
        # Add close button (packed first to be on the far right)
        self.close_button = tk.Button(self.title_bar, text='✕', command=self.root.quit,
                                    bg='#2E2E2E', fg='#E0E0E0', bd=0, padx=5, pady=2, font=self.font_primary, relief='flat', activebackground='#3C3C3C', activeforeground='#E0E0E0')
        self.close_button.pack(side='right')

        # Add pin toggle button (packed next, will appear to the left of the close button)
        self.pin_toggle_button = tk.Button(self.title_bar, text="Pin Bottom", command=self.toggle_pin_mode,
                                           bg='#2E2E2E', fg='#E0E0E0', relief='flat', bd=0,
                                           font=self.font_primary, activebackground='#3C3C3C',
                                           activeforeground='#E0E0E0', padx=5, pady=2) # Added pady to match close button
        self.pin_toggle_button.pack(side='right')
        
        # Create calendar display
        self.calendar_frame = tk.Frame(self.frame, bg='#2E2E2E')
        self.calendar_frame.pack(padx=10, pady=5)
        
        # Create navigation frame
        self.nav_frame = tk.Frame(self.frame, bg='#2E2E2E')
        self.nav_frame.pack(fill='x', padx=5, pady=5)
        
        # Add navigation buttons
        self.prev_month = tk.Button(self.nav_frame, text="←", command=self.previous_month,
                                  bg='#2E2E2E', fg='#E0E0E0', bd=0, width=4, font=self.font_primary, relief='flat', activebackground='#3C3C3C', activeforeground='#E0E0E0', pady=2)
        self.prev_month.pack(side='left', padx=5)
        
        self.today_button = tk.Button(self.nav_frame, text="Today", command=self.go_to_today,
                                    bg='#2E2E2E', fg='#E0E0E0', bd=0, font=self.font_primary, relief='flat', activebackground='#3C3C3C', activeforeground='#E0E0E0', pady=2)
        self.today_button.pack(side='left', padx=5, expand=True)
        
        self.next_month = tk.Button(self.nav_frame, text="→", command=self.next_month,
                                  bg='#2E2E2E', fg='#E0E0E0', bd=0, width=4, font=self.font_primary, relief='flat', activebackground='#3C3C3C', activeforeground='#E0E0E0', pady=2)
        self.next_month.pack(side='right', padx=5)

        # Add Alpha/Transparency Slider
        self.alpha_slider = tk.Scale(self.nav_frame, orient=tk.HORIZONTAL, from_=0.2, to=1.0,
                                     resolution=0.05, variable=self.current_alpha,
                                     command=self.update_transparency, # Method to be created
                                     length=150, showvalue=0, bg='#2E2E2E', fg='#E0E0E0',
                                     troughcolor='#3C3C3C', highlightbackground='#2E2E2E',
                                     activebackground='#4A4A4A')
        self.alpha_slider.pack(side='bottom', fill='x', pady=5, padx=5)
        
        # Bind mouse events for dragging
        self.title_bar.bind('<Button-1>', self.start_drag)
        self.title_bar.bind('<B1-Motion>', self.drag)
        
        # Update calendar
        self.update_calendar()
        
        # Set up auto-refresh every hour
        self.root.after(3600000, self.update_calendar)  # 3600000 ms = 1 hour

        # Apply the initial pin mode (e.g., set to always on top by default)
        self.apply_pin_mode()
        # Apply the initial transparency setting
        self.update_transparency(self.current_alpha.get())

    def toggle_pin_mode(self):
        """Toggles the always-on-top state of the window."""
        self.is_on_top = not self.is_on_top
        self.apply_pin_mode() # This method will be defined later

    def apply_pin_mode(self):
        """Applies the window layering based on the is_on_top state."""
        if self.is_on_top:
            self.pin_toggle_button.config(text="Pin Bottom")
            # self.undo_os_specific_bottom_settings() # To be created in a future step
            self.root.attributes('-topmost', True)
            print("Mode: Pin Top")
        else:
            self.pin_toggle_button.config(text="Pin Top")
            self.root.attributes('-topmost', False)
            self.root.lower() # General Tkinter attempt to lower

            os_name = platform.system().lower()
            print(f"Applying pin bottom for OS: {os_name}")
            if os_name == "windows":
                self.set_windows_always_on_bottom()
            elif os_name == "darwin":  # macOS
                self.set_macos_always_on_bottom()
            elif os_name == "linux":
                self.set_linux_always_on_bottom()
            else:
                print(f"Pin to bottom OS-specifics not implemented for: {os_name}")
            print("Mode: Pin Bottom")

    def undo_os_specific_bottom_settings(self):
        os_name = platform.system().lower()
        print(f"Undoing OS-specific bottom settings for: {os_name}")

        if os_name == "windows":
            try:
                # For Windows, self.root.attributes('-topmost', True) is often sufficient
                # to bring the window back on top, overriding a previous HWND_BOTTOM.
                # SetWindowPos with HWND_TOPMOST or HWND_NOTOPMOST could also be used if needed.
                # For now, we rely on the subsequent call to self.root.attributes('-topmost', True)
                # in apply_pin_mode which should bring it to the top.
                print("Windows: Relied on subsequent '-topmost', True to undo bottom setting.")
                pass # Explicitly doing nothing here, as '-topmost', True handles it.
            except Exception as e:
                print(f"Windows: Error during undo_os_specific_bottom_settings: {e}")

        elif os_name == "darwin": # macOS
            if not NSApp:
                print("macOS: PyObjC not available for undo.")
                return
            try:
                # NSNormalWindowLevel is typically 0
                NSNormalWindowLevel = 0 
                
                title = self.root.title()
                app_windows = NSApp.windows()
                target_window = None
                for w in app_windows:
                    if w.title() == title:
                        target_window = w
                        break
                
                if target_window:
                    target_window.setLevel_(NSNormalWindowLevel)
                    print("macOS: Attempted to set window level to NSNormalWindowLevel (0).")
                else:
                    print("macOS: Could not find NSWindow to undo bottom setting.")
            except Exception as e:
                print(f"macOS: Error during undo_os_specific_bottom_settings: {e}")

        elif os_name == "linux":
            if not display:
                print("Linux: python-xlib not available for undo.")
                return
            try:
                d = display.Display()
                win_id = self.root.winfo_id()
                # window = d.create_resource_object('window', win_id) # Not directly needed for ClientMessage

                atom_wm_state = d.intern_atom('_NET_WM_STATE')
                atom_below = d.intern_atom('_NET_WM_STATE_BELOW')

                # Data for ClientMessage: action (0=remove), atom1, atom2 (0 if none), source indication
                # _NET_WM_STATE_REMOVE = 0
                event_data = [0,  # Action: _NET_WM_STATE_REMOVE
                              atom_below, 
                              0,  # No second property atom
                              1,  # Source indication: Application
                              0]  # Unused
                
                evt = Xlib.protocol.event.ClientMessage(
                    window=win_id,
                    client_type=atom_wm_state,
                    data=(32, event_data) 
                )
                # Send to root window with appropriate mask
                d.send_event(d.screen().root, evt, event_mask=Xlib.X.SubstructureRedirectMask | Xlib.X.SubstructureNotifyMask)
                
                # If _NET_WM_WINDOW_TYPE_DESKTOP was set, revert to _NET_WM_WINDOW_TYPE_NORMAL
                # (Assuming it wasn't, based on previous steps, so this is commented)
                # atom_window_type = d.intern_atom('_NET_WM_WINDOW_TYPE')
                # atom_normal = d.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL')
                # window.change_property(atom_window_type, X.ATOM, 32, [atom_normal], X.PropModeReplace)
                
                d.sync()
                print("Linux: Attempted to send ClientMessage to remove _NET_WM_STATE_BELOW.")
            except Exception as e:
                print(f"Linux: Error during undo_os_specific_bottom_settings: {e}")
        else:
            print(f"Undo pin to bottom not specifically implemented for {os_name}")

    def update_transparency(self, value):
        """Updates the window transparency based on the slider value."""
        alpha_value = float(value)
        self.root.attributes('-alpha', alpha_value)
        # print(f"Updated transparency to: {alpha_value}") # Optional: for debugging

    # Placeholder methods for OS-specific window behavior
    def set_windows_always_on_bottom(self):
        if not win32gui:
            print("Windows: pywin32 not available.")
            return
        try:
            hwnd = self.root.winfo_id()
            # Ensure window style allows it to be a child or non-topmost
            # style = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
            # style &= ~win32con.WS_POPUP # Remove WS_POPUP if present
            # style |= win32con.WS_CHILD # Add WS_CHILD, though this might be too aggressive. HWND_BOTTOM might be better.
                                         # For now, let's focus on SetWindowPos with HWND_BOTTOM
            # win32api.SetWindowLong(hwnd, win32con.GWL_STYLE, style) # Re-evaluate if SetWindowPos alone is not enough

            # Attempt to place it at the bottom of Z-order
            win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 0, 0, 
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)
            print("Windows: Attempted SetWindowPos with HWND_BOTTOM")
        except Exception as e:
            print(f"Windows: Failed to set window to bottom: {e}")

    def set_macos_always_on_bottom(self):
        if not NSApp:
            print("macOS: PyObjC not available.")
            return
        try:
            # This part is tricky, getting NSWindow from Tkinter root.
            # The title matching approach:
            title = self.root.title()
            app_windows = NSApp.windows()
            target_window = None
            for w in app_windows:
                if w.title() == title:
                    target_window = w
                    break
            
            if target_window:
                target_window.setLevel_(kCGDesktopIconWindowLevel) 
                # kCGDesktopWindowLevel is even lower, might be too low (behind desktop icons)
                # kCGDesktopIconWindowLevel is often preferred for "gadget" type windows.
                
                # Optional: Set collection behavior for spaces and exposé/mission control
                # from AppKit import NSWindowCollectionBehaviorCanJoinAllSpaces, NSWindowCollectionBehaviorStationary, NSWindowCollectionBehaviorIgnoresCycle # Import these if used
                # target_window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces | NSWindowCollectionBehaviorStationary | NSWindowCollectionBehaviorIgnoresCycle)
                print("macOS: Attempted to set window level to kCGDesktopIconWindowLevel")
            else:
                print("macOS: Could not find NSWindow with matching title.")
        except Exception as e:
            print(f"macOS: Failed to set window to bottom: {e}")

    def set_linux_always_on_bottom(self):
        if not display:
            print("Linux: python-xlib not available.")
            return
        try:
            d = display.Display()
            win_id = self.root.winfo_id()
            window = d.create_resource_object('window', win_id)

            # Set _NET_WM_STATE_BELOW
            atom_wm_state = d.intern_atom('_NET_WM_STATE')
            atom_below = d.intern_atom('_NET_WM_STATE_BELOW')
            # The property data must be a list of integers (atoms)
            window.change_property(atom_wm_state, X.ATOM, 32, [atom_below], X.PropModeReplace)

            # Optionally, also set _NET_WM_WINDOW_TYPE_DESKTOP
            # atom_window_type = d.intern_atom('_NET_WM_WINDOW_TYPE')
            # atom_desktop = d.intern_atom('_NET_WM_WINDOW_TYPE_DESKTOP')
            # window.change_property(atom_window_type, X.ATOM, 32, [atom_desktop], X.PropModeReplace) # Keep this commented for now, _NET_WM_STATE_BELOW is primary goal
            
            d.sync()
            print("Linux: Attempted to set _NET_WM_STATE_BELOW")
        except Exception as e:
            print(f"Linux: Failed to set window to bottom: {e}")
    
    def start_drag(self, event):
        """Store initial position for drag operation."""
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        """Handle window dragging."""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def previous_month(self):
        """Go to previous month."""
        year = self.current_view.year
        month = self.current_view.month
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        self.current_view = self.current_view.replace(year=year, month=month, day=1)
        self.update_calendar()
    
    def next_month(self):
        """Go to next month."""
        year = self.current_view.year
        month = self.current_view.month
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        self.current_view = self.current_view.replace(year=year, month=month, day=1)
        self.update_calendar()
    
    def go_to_today(self):
        """Return to current month."""
        self.current_view = date.today()
        self.update_calendar()

    def update_calendar(self):
        """Update the calendar display."""
        # Clear existing calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Get current date info
        today = date.today()
        year = self.current_view.year
        month = self.current_view.month
        
        # Get first Monday of the year for work week calculation
        year_start = date(year, 1, 1)
        first_monday = year_start - timedelta(days=year_start.weekday())
        
        # Create headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, bg='#2E2E2E', fg='#E0E0E0',
                    width=4, font=self.font_primary).grid(row=0, column=i+1)
        tk.Label(self.calendar_frame, text='WW', bg='#2E2E2E', fg='#E0E0E0',
                width=4, font=self.font_primary).grid(row=0, column=0)
        
        # Get calendar for current month
        cal = calendar.monthcalendar(year, month)
        
        # Calculate previous month's last day
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        prev_month_days = calendar.monthrange(prev_year, prev_month)[1]
        
        # Calculate next month's first day
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        # Display calendar with work weeks
        for week_idx, week in enumerate(cal):
            if any(week):  # Only show weeks with days
                # Get the first day of this week
                for day in week:
                    if day != 0:
                        week_date = date(year, month, day)
                        ww = get_work_week_number(week_date, first_monday)
                        break
                
                # Show work week number
                tk.Label(self.calendar_frame, text=f"WW{ww}",
                        bg='#2E2E2E', fg='#E0E0E0', font=self.font_primary).grid(row=week_idx+1, column=0)
                
                # Show days
                for day_idx, day in enumerate(week):
                    if day == 0:
                        # Calculate the date for blank spaces
                        if day_idx < week.index(next(iter([d for d in week if d != 0]), 0)):
                            # This is a day from previous month
                            prev_day = prev_month_days - (week.index(next(iter([d for d in week if d != 0]), 0)) - day_idx - 1)
                            text = str(prev_day)
                            bg_color = '#3C3C3C'  # Different background for previous/next month
                            fg_color = '#E0E0E0'
                        else:
                            # This is a day from next month
                            next_day = day_idx - week.index(next(iter([d for d in week if d != 0][::-1]), 0))
                            text = str(next_day)
                            bg_color = '#3C3C3C'  # Different background for previous/next month
                            fg_color = '#E0E0E0'
                    else:
                        text = str(day)
                        fg_color = '#E0E0E0'
                        # Highlight today
                        if (day == today.day and month == today.month and year == today.year):
                            bg_color = '#00BFA5' # Accent color for today
                        else:
                            bg_color = '#2E2E2E' # Primary background for other days
                    
                    tk.Label(self.calendar_frame, text=text, bg=bg_color, fg=fg_color,
                            width=4, font=self.font_primary).grid(row=week_idx+1, column=day_idx+1)
        
        # Add month/year header
        month_name = calendar.month_name[month]
        tk.Label(self.calendar_frame, text=f"{month_name} {year}",
                bg='#2E2E2E', fg='#E0E0E0', font=self.font_header).grid(row=7, column=0, columnspan=8)

def main():
    app = WorkWeekCalendarWidget()
    # Position window in top-right corner initially
    screen_width = app.root.winfo_screenwidth()
    app.root.geometry(f"+{screen_width-300}+50")
    app.root.mainloop()

if __name__ == "__main__":
    main() 