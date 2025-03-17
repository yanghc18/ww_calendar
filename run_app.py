import tkinter as tk
from datetime import date, timedelta
import calendar

def get_work_week_number(current_date: date, start_date: date) -> int:
    start_weekday = start_date.weekday()
    adjusted_start = start_date - timedelta(days=start_weekday)
    current_weekday = current_date.weekday()
    adjusted_current = current_date - timedelta(days=current_weekday)
    weeks_diff = (adjusted_current - adjusted_start).days // 7
    week_num = weeks_diff + 1
    return ((week_num - 1) % 52) + 1

class WorkWeekCalendarWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Work Week Calendar")
        self.current_view = date.today()
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Create main frame
        self.frame = tk.Frame(self.root, bg='white', relief='solid', borderwidth=1)
        self.frame.pack(padx=2, pady=2)
        
        # Add title bar
        self.title_bar = tk.Frame(self.frame, bg='lightgray', relief='raised', height=20)
        self.title_bar.pack(fill='x')
        self.title_bar.pack_propagate(False)
        
        # Add title and close button
        self.title_label = tk.Label(self.title_bar, text="Work Week Calendar", bg='lightgray')
        self.title_label.pack(side='left', padx=5)
        self.close_button = tk.Button(self.title_bar, text='×', command=self.root.quit,
                                    bg='lightgray', bd=0, padx=5)
        self.close_button.pack(side='right')
        
        # Calendar frame
        self.calendar_frame = tk.Frame(self.frame, bg='white')
        self.calendar_frame.pack(padx=10, pady=5)
        
        # Navigation frame
        self.nav_frame = tk.Frame(self.frame, bg='white')
        self.nav_frame.pack(fill='x', padx=5, pady=5)
        
        # Navigation buttons
        self.prev_month = tk.Button(self.nav_frame, text="◀", command=self.previous_month,
                                  bg='white', bd=1, width=4)
        self.prev_month.pack(side='left', padx=2)
        
        self.today_button = tk.Button(self.nav_frame, text="Today", command=self.go_to_today,
                                    bg='white', bd=1)
        self.today_button.pack(side='left', padx=2, expand=True)
        
        self.next_month = tk.Button(self.nav_frame, text="▶", command=self.next_month,
                                  bg='white', bd=1, width=4)
        self.next_month.pack(side='right', padx=2)
        
        # Bind dragging
        self.title_bar.bind('<Button-1>', self.start_drag)
        self.title_bar.bind('<B1-Motion>', self.drag)
        
        self.update_calendar()
        self.root.after(3600000, self.update_calendar)  # Update every hour
    
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
    
    def previous_month(self):
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
        self.current_view = date.today()
        self.update_calendar()

    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        today = date.today()
        year = self.current_view.year
        month = self.current_view.month
        
        # Get first Monday of the year
        year_start = date(year, 1, 1)
        first_monday = year_start - timedelta(days=year_start.weekday())
        
        # Headers
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, bg='white',
                    width=4).grid(row=0, column=i+1)
        tk.Label(self.calendar_frame, text='WW', bg='white',
                width=4).grid(row=0, column=0)
        
        # Calendar
        cal = calendar.monthcalendar(year, month)
        
        # Previous month info
        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year
        prev_month_days = calendar.monthrange(prev_year, prev_month)[1]
        
        # Display calendar
        for week_idx, week in enumerate(cal):
            if any(week):
                # Get work week number
                for day in week:
                    if day != 0:
                        week_date = date(year, month, day)
                        ww = get_work_week_number(week_date, first_monday)
                        break
                
                tk.Label(self.calendar_frame, text=f"WW{ww}",
                        bg='white').grid(row=week_idx+1, column=0)
                
                for day_idx, day in enumerate(week):
                    if day == 0:
                        if day_idx < week.index(next(iter([d for d in week if d != 0]), 0)):
                            prev_day = prev_month_days - (week.index(next(iter([d for d in week if d != 0]), 0)) - day_idx - 1)
                            text = str(prev_day)
                            bg_color = 'lightgray'
                        else:
                            next_day = day_idx - week.index(next(iter([d for d in week if d != 0][::-1]), 0))
                            text = str(next_day)
                            bg_color = 'lightgray'
                    else:
                        text = str(day)
                        bg_color = 'lightblue' if (day == today.day and 
                                                 month == today.month and 
                                                 year == today.year) else 'white'
                    
                    tk.Label(self.calendar_frame, text=text, bg=bg_color,
                            width=4).grid(row=week_idx+1, column=day_idx+1)
        
        # Month/year header
        month_name = calendar.month_name[month]
        tk.Label(self.calendar_frame, text=f"{month_name} {year}",
                bg='white', font=('Arial', 10, 'bold')).grid(row=7, column=0, columnspan=8)

if __name__ == "__main__":
    app = WorkWeekCalendarWidget()
    screen_width = app.root.winfo_screenwidth()
    app.root.geometry(f"+{screen_width-300}+50")
    app.root.mainloop()