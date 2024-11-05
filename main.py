# import required libraries
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import re
import queue
from datetime import datetime
from tkcalendar import DateEntry


def main():
    # Initialize main window
    root = tk.Tk()
    root.title("File Search By Me")
    root.geometry("600x700")

    # Window frame for the search options
    search_frame = tk.Frame(root, padx=10, pady=10)
    search_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    # Add controls within the search_frame

    # Label for directory selection
    directory_label = tk.Label(search_frame, text="Select Folder:")
    directory_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Entry box for directory path
    directory_entry = tk.Entry(search_frame, width=50)
    directory_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Button to open select folder dialog
    def select_folder():
        """Prompt user to select a directory and update the directory entry with the selected path."""    
        folder_selected = filedialog.askdirectory()
        # clear any current content
        directory_entry.delete(0, tk.END)
        # insert selected folder
        directory_entry.insert(0, folder_selected)
        

    select_button = tk.Button(search_frame, text="Browse", command=select_folder)
    select_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    # Label for file name patterns
    file_label = tk.Label(search_frame, text="File Pattern (e.g., *.txt):")
    file_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    # Entry box for file name patterns
    file_entry = tk.Entry(search_frame, width=50)
    file_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Label for text search (optional)
    text_label = tk.Label(search_frame, text="Containing text (optional):")
    text_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

    # Entry box for text search input
    text_entry = tk.Entry(search_frame, width=50)
    text_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Label for date range option
    date_label = tk.Label(search_frame, text="Date Modified Between:")
    date_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    # Date pickers for "From" and "To" dates
    from_date_picker = DateEntry(search_frame, width=15, background="SpringGreen4", foreground="white", borderwidth=2)
    from_date_picker.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    to_date_picker = DateEntry(search_frame, width=15, background="SpringGreen4", foreground="white", borderwidth=2)
    to_date_picker.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Sort options for displaying the files that are found
    sort_label = tk.Label(search_frame, text="Sort By:")
    sort_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

    sort_var = tk.StringVar(value="Name Ascending")  # Default sorting option
    sort_options = ["Name Ascending", "Name Descending", "Date Ascending", "Date Descending"]
    sort_menu = tk.OptionMenu(search_frame, sort_var, *sort_options)
    sort_menu.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Search button
    search_button = tk.Button(search_frame, text="Search Now")
    search_button.grid(row=6, column=1, padx=5, pady=10, sticky="w")

    # Status label
    status_label = tk.Label(search_frame, text="Status: Ready")
    status_label.grid(row=7, column=1, padx=5, pady=5, sticky="w")

    # Progress bar
    progress = ttk.Progressbar(search_frame, orient="horizontal", mode="determinate", length=300)
    progress.grid(row=8, column=1, padx=5, pady=5, sticky="w")

    # Frame for search results
    result_frame = tk.Frame(root)
    result_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    # Listbox to display results
    result_listbox = tk.Listbox(result_frame, width=80, height=20)
    result_listbox.grid(row=0, column=0, sticky="nw")

    # Scrollbar for the results listbox
    scrollbar = tk.Scrollbar(result_frame)
    scrollbar.grid(row=0, column=1, sticky="ns")
    result_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=result_listbox.yview)

    # Function to search for files
    def search_files(directory, file_pattern=None, search_text=None, from_date=None, to_date=None, result_queue=None):
        """
        Search for files in the specified directory.

        Args:
            directory (str): The directory to search in.
            file_pattern (str, optional): A pattern to match filenames (e.g., '*.txt').
            search_text (str, optional): Text to search for within files.
            from_date (datetime.date, optional): The start date for filtering files by last modified date.
            to_date (datetime.date, optional): The end date for filtering files by last modified date.
            result_queue (queue.Queue): A queue to send results back to the main thread.

        Returns:
            None: Results are sent to the result queue for display.
        """

        # First of all check that the from date is not later than the to date


        # set initial value of all files in directory path to check against search criteria
        total_files = sum(len(files) for _, _, files in os.walk(directory))
        processed_files = 0
        results = []

        # walk through directory paths
        for root_dir, _, files in os.walk(directory):
            for file in files:
                # Update progress
                processed_files += 1
                result_queue.put(('progress', processed_files / total_files * 100))
                # I'm using regex to compare file patterns so I want to convert any wildcards.
                if file_pattern:
                    file_pattern_regex = file_pattern.replace("*", ".*").replace("?", ".")
                    if not re.match(file_pattern_regex, file): # Not a match so move on to next file
                        continue

                # Full file path
                file_path = os.path.join(root_dir, file)
                
                # Get the last modified date
                last_modified_timestamp = os.path.getmtime(file_path)
                last_modified_date = datetime.fromtimestamp(last_modified_timestamp).date()

                # Filter by date range. Move on to next file if last modified date falls outside selected range
                if from_date and last_modified_date < from_date:
                    continue
                if to_date and last_modified_date > to_date:
                    continue

                # Check for text within file
                if search_text:
                    try:
                        with open(file_path, 'r', encoding="utf-8") as f:
                            contents = f.read()
                            if search_text in contents:
                                result_queue.put(f"{file_path} (Last Modified: {last_modified_date})")
                    except Exception:
                        result_queue.put(f"Skipped unreadable file: {file_path}")
                        continue
                else:
                    results.append((file_path, last_modified_date))


        # Sort results based on the selected option
        sort_option = sort_var.get()
        if sort_option == "Name Ascending":
            results.sort(key=lambda x: x[0])  # Sort by file name (including path) ascending
        elif sort_option == "Name Descending":
            results.sort(key=lambda x: x[0], reverse=True)  # Sort by file name (including path) descending
        elif sort_option == "Date Ascending":
            results.sort(key=lambda x: x[1])  # Sort by last modified date ascending
        elif sort_option == "Date Descending":
            results.sort(key=lambda x: x[1], reverse=True)  # Sort by last modified date descending


        # send results after sorting to the result queue
        for result in results:
            result_queue.put(f"{result[0]} (Last Modified: {result[1]})")

        result_queue.put(None)  # Signal that the search is complete



    # Function to start the search in a new thread
    def start_search():
        """Initiate the file search in a separate thread and update the UI accordingly."""


        directory = directory_entry.get()
        file_pattern = file_entry.get()
        search_text = text_entry.get()


        # Get the "from" and "to" dates from the date pickers
        from_date = from_date_picker.get_date()
        to_date = to_date_picker.get_date()

        if not directory:
            status_label.config(text="Please select a directory.")
            return
        # initialze queue
        result_queue = queue.Queue()

        # Clear the results listbox and reset the progress bar
        result_listbox.delete(0, tk.END)
        progress["value"] = 0
        status_label.config(text="Search running...")

        # Start a new thread for the search
        search_thread = threading.Thread(target=search_files, args=(directory, file_pattern, search_text, from_date, to_date, result_queue))
        search_thread.start()

        # Process the results in the main thread
        root.after(100, process_queue, result_queue)

    

    # Function to process the queue and update the UI
    def process_queue(result_queue):
        """ Process results from the search queue and update the UI components.

        Args:
            result_queue (queue.Queue): The queue containing results from the search.

        Returns:
            None: Updates the status label and progress bar based on the search results.
        """
        
        try:
            result = result_queue.get_nowait()
            if result is None:
                status_label.config(text="Search completed.")
                progress["value"] = 100
            elif isinstance(result, tuple) and result[0] == 'progress':
                # Update progress bar
                progress["value"] = result[1]
                root.after(100, process_queue, result_queue)  # Continue checking
            else:
            # file found
                result_listbox.insert(tk.END, result)
                root.after(100, process_queue, result_queue)  # Continue checking
        except queue.Empty:
            root.after(100, process_queue, result_queue)  # Continue checking

    # Function to open the selected file
    def open_file(event):
        """ Open the selected file in the associated program when double-clicked in the results list.

        Args:
            event: The event object containing information about the double-click.

        Returns:
            None: The function attempts to open the file and updates the status label if an error occurs.
        """    
        selected_index = result_listbox.curselection()
        if selected_index:  # Check if something is selected
            selected_file = result_listbox.get(selected_index)
            file_path = selected_file.split(" (Last Modified:")[0]  # Extract the file path
            try:
                os.startfile(file_path)

            except Exception as e:
                status_label.config(text=f"Error opening file: {e}")

    # Bind double-click event to open file
    result_listbox.bind('<Double-1>', open_file)

    # Bind the search button to the start_search function
    search_button.config(command=start_search)

    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()
