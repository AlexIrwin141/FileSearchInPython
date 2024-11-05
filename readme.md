

File Search Application
A GUI-based file search tool built with Python and Tkinter that allows users to search for files in a specified directory based on file name patterns, text content, and within a range of last modified dates. Includes advanced filtering options, progress tracking, and supports opening matched files in their default applications.

Features
File Pattern Search: Search by file names or extensions with wildcards (e.g., *.txt).  
Text Content Search: Search within files for specific text content.  
Date Filtering: Filter results by last modified date (between two selectable dates).  
Sort Results: Order results by file name or last modified date in ascending or descending order.  
Progress Bar: View search progress with a dynamic progress bar.  
Open Matched Files: Open files directly from the results with their default application.  

Dependencies
Python: Version 3.6 or higher
Tkinter: Typically included with Python
Other libraries: Listed in requirements.txt


Installation
Clone the repository:
git clone https://github.com/AlexIrwin141/FileSearchInPython
cd FileSearchInPython

Install Required Packages:
Install dependencies using pip:
pip install -r requirements.txt
Note: Ensure you have Python 3.6 or higher installed.

Run the application:  
python main.py  

Interface Guide:

Directory Selection: Use the "Browse" button to choose a folder.  
File Pattern: Enter file pattern (e.g., *.txt).  
Search Text: Enter text to search within files (optional).  
Date Range: Select "From" and "To" dates for last modified date filtering (optional).  
Sort By: Choose sorting options for the search results.  
Search Button: Start the search and view progress.  

Results:  

The matching files are displayed with the file name, path, and last modified date.
Double-click any file in the results list to open it in its default program.

License
This project is licensed under the MIT License - see the LICENSE file for details.
