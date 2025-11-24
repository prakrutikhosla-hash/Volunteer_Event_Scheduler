# volunteer_schedule_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

class VolunteerEvent:
    def __init__(self, name, date, time, location, volunteers_needed, description=""):
        self.name = name
        self.date = date
        self.time = time
        self.location = location
        self.volunteers_needed = volunteers_needed
        self.description = description
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'volunteers_needed': self.volunteers_needed,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data):
        event = cls(
            data['name'],
            data['date'],
            data['time'],
            data['location'],
            data['volunteers_needed'],
            data['description']
        )
        event.id = data['id']
        return event

class VolunteerSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Volunteer Event Scheduler")
        self.root.geometry("800x600")
        
        self.data_file = "events.json"
        self.events = []
        self.load_events()
        
        self.setup_ui()
        self.refresh_events_list()
    
    def load_events(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.events = [VolunteerEvent.from_dict(event_data) for event_data in data]
            except (json.JSONDecodeError, KeyError):
                self.events = []
    
    def save_events(self):
        with open(self.data_file, 'w') as f:
            json.dump([event.to_dict() for event in self.events], f, indent=2)
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Volunteer Event Scheduler", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Add Event Form
        form_frame = ttk.LabelFrame(main_frame, text="Add New Event", padding="10")
        form_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        form_frame.columnconfigure(1, weight=1)
        
        # Event Name
        ttk.Label(form_frame, text="Event Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Date
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.date_entry = ttk.Entry(form_frame, width=30)
        self.date_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Time
        ttk.Label(form_frame, text="Time (HH:MM):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.time_entry = ttk.Entry(form_frame, width=30)
        self.time_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Location
        ttk.Label(form_frame, text="Location:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.location_entry = ttk.Entry(form_frame, width=30)
        self.location_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Volunteers Needed
        ttk.Label(form_frame, text="Volunteers Needed:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.volunteers_entry = ttk.Spinbox(form_frame, from_=1, to=1000, width=28)
        self.volunteers_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Description
        ttk.Label(form_frame, text="Description:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.description_entry = tk.Text(form_frame, width=30, height=3)
        self.description_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Add Button
        add_button = ttk.Button(form_frame, text="Add Event", command=self.add_event)
        add_button.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Events List
        list_frame = ttk.LabelFrame(main_frame, text="Upcoming Events", padding="10")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Treeview for events
        columns = ('Name', 'Date', 'Time', 'Location', 'Volunteers')
        self.events_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.events_tree.heading('Name', text='Event Name')
        self.events_tree.heading('Date', text='Date')
        self.events_tree.heading('Time', text='Time')
        self.events_tree.heading('Location', text='Location')
        self.events_tree.heading('Volunteers', text='Volunteers Needed')
        
        # Set column widths
        self.events_tree.column('Name', width=150)
        self.events_tree.column('Date', width=100)
        self.events_tree.column('Time', width=80)
        self.events_tree.column('Location', width=120)
        self.events_tree.column('Volunteers', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.events_tree.yview)
        self.events_tree.configure(yscrollcommand=scrollbar.set)
        
        self.events_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Delete button
        delete_button = ttk.Button(list_frame, text="Delete Selected Event", command=self.delete_event)
        delete_button.grid(row=1, column=0, pady=10, sticky=tk.W)
    
    def add_event(self):
        name = self.name_entry.get().strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        location = self.location_entry.get().strip()
        volunteers_needed = self.volunteers_entry.get().strip()
        description = self.description_entry.get("1.0", tk.END).strip()
        
        # Basic validation
        if not all([name, date, time, location, volunteers_needed]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        try:
            volunteers_needed = int(volunteers_needed)
        except ValueError:
            messagebox.showerror("Error", "Volunteers needed must be a number.")
            return
        
        # Create and add event
        event = VolunteerEvent(name, date, time, location, volunteers_needed, description)
        self.events.append(event)
        self.save_events()
        
        # Clear form
        self.name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.volunteers_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        
        self.refresh_events_list()
        messagebox.showinfo("Success", "Event added successfully!")
    
    def delete_event(self):
        selected_item = self.events_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an event to delete.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this event?"):
            item = selected_item[0]
            event_name = self.events_tree.item(item, 'values')[0]
            
            # Find and remove event
            self.events = [event for event in self.events if event.name != event_name]
            self.save_events()
            self.refresh_events_list()
    
    def refresh_events_list(self):
        # Clear current list
        for item in self.events_tree.get_children():
            self.events_tree.delete(item)
        
        # Add events to treeview
        for event in sorted(self.events, key=lambda x: (x.date, x.time)):
            self.events_tree.insert('', tk.END, values=(
                event.name,
                event.date,
                event.time,
                event.location,
                event.volunteers_needed
            ))

def main():
    root = tk.Tk()
    app = VolunteerSchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()