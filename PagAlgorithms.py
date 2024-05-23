import tkinter as tk
from tkinter import ttk

def fifo(page_reference_sequence, number_of_frames):
    page_table = []  # Represents the frames in memory
    page_faults = 0
    table_data = []  # To store data for the table

    for page_reference in page_reference_sequence:
        if page_reference not in page_table:
            if len(page_table) == number_of_frames:
                # Remove the oldest page (first-in) if the frames are full
                page_table.pop(0)
            # Add the new page (first-in) to the frames
            page_table.append(page_reference)
            page_faults += 1

        table_data.append((page_reference, " ".join(map(str, page_table))))

    return page_faults, table_data

def optimal(page_reference_sequence, number_of_frames):
    page_table = []  # Represents the frames in memory
    page_faults = 0
    table_data = []

    for page_reference in page_reference_sequence:
        if page_reference not in page_table:
            if len(page_table) == number_of_frames:
                # Find the page in the frames that will not be used for the longest time (Optimal)
                farthest_page = -1
                farthest_index = -1
                for i, frame in enumerate(page_table):
                    if frame not in page_reference_sequence[page_reference_sequence.index(page_reference):]:
                        return i  # This page will not be used again, so replace it
                    else:
                        index = page_reference_sequence[page_reference_sequence.index(page_reference):].index(frame)
                        if index > farthest_index:
                            farthest_index = index
                            farthest_page = i
                
                # Remove the page to be replaced
                page_table.pop(farthest_page)
            # Add the new page to the frames
            page_table.append(page_reference)
            page_faults += 1

        table_data.append((page_reference, " ".join(map(str, page_table))))

    return page_faults, table_data

# Define an LRU and LFU function here
def lru(page_reference_sequence, number_of_frames):
    page_table = []  # Represents the frames in memory
    page_faults = 0
    table_data = []  # To store data for the table

    for page_reference in page_reference_sequence:
        if page_reference not in page_table:
            if len(page_table) == number_of_frames:
                # Find the page in the frames that was least recently used (LRU)
                oldest_page = min(page_table, key=lambda x: page_reference_sequence.index(x))
                page_table.remove(oldest_page)
            # Add the new page (most recently used) to the frames
            page_table.append(page_reference)
            page_faults += 1

        table_data.append((page_reference, " ".join(map(str, page_table))))

    return page_faults, table_data

# Define LFU algorithm
def lfu(page_reference_sequence, number_of_frames):
    page_table = []  # Represents the frames in memory
    page_faults = 0
    page_access_count = {}  # To store the frequency of each page
    table_data = []  # To store data for the table

    for page_reference in page_reference_sequence:
        if page_reference not in page_table:
            if len(page_table) == number_of_frames:
                # Find the page with the lowest access count (LFU)
                min_count_page = min(page_access_count, key=page_access_count.get)
                page_table.remove(min_count_page)
                del page_access_count[min_count_page]
            # Add the new page to the frames
            page_table.append(page_reference)
            page_faults += 1

        # Update the access count for the page
        page_access_count[page_reference] = page_access_count.get(page_reference, 0) + 1

        table_data.append((page_reference, " ".join(map(str, page_table))))

    return page_faults, table_data

# Create a global variable to store the reference to the table
table = None

# Function to run the selected algorithm and update the GUI step by step
def run_algorithm_and_update_gui(root, page_reference_sequence, number_of_frames, selected_algorithm, algorithm_func):
    global table
    page_table = []  # Represents the frames in memory
    page_faults = 0
    table_data = []  # To store data for the table

    for page_reference in page_reference_sequence:
        if page_reference not in page_table:
            if len(page_table) == number_of_frames:
                # Remove the oldest page (first-in) if the frames are full
                page_table.pop(0)
            # Add the new page (first-in) to the frames
            page_table.append(page_reference)
            page_faults += 1

        table_data.append((page_reference, " ".join(map(str, page_table))))
        
        # Update the table with the data for this step
        update_table(table, table_data)
        root.update()  # Update the GUI to show the changes
        
    # Update the GUI with the final results
    ttk.Label(root, text=f"{selected_algorithm}: {page_faults} page faults").pack()


# wierd code alg
# Create a GUI window
def create_gui():
    # Create the root window
    root = tk.Tk()
    root.title("Page Replacement Algorithms")

    # Create a frame for the input fields
    input_frame = ttk.Frame(root)
    input_frame.pack()

    # Create radio buttons for selecting the algorithm
    algorithm_var = tk.StringVar()
    algorithms = ["FIFO", "Optimal", "LRU", "LFU"]
    for i, algorithm in enumerate(algorithms):
        ttk.Radiobutton(input_frame, text=algorithm, variable=algorithm_var, value=algorithm).grid(row=i, column=0)

    # Create a button to run the selected algorithm and update the GUI
    run_button = ttk.Button(input_frame, text="Run Algorithm", command=lambda: update_gui(
        root,
        [1, 2, 3, 2, 1, 5, 2, 1, 6, 2, 5, 6, 3, 1, 3, 6, 1, 2, 4, 3],
        3,
        algorithm_var.get(),
        fifo,
        optimal,
        lru,
        lfu
    ))
    run_button.grid(row=len(algorithms), column=0, columnspan=2)

    # Create a Treeview widget for the table
    table = ttk.Treeview(root)
    table["columns"] = ("Page Reference", "Page Table")
    table.column("#0", width=0, stretch=tk.NO)
    table.column("Page Reference", anchor=tk.W, width=120)
    table.column("Page Table", anchor=tk.W, width=120)
    table.heading("#0", text="", anchor=tk.W)
    table.heading("Page Reference", text="Page Reference", anchor=tk.W)
    table.heading("Page Table", text="Page Table", anchor=tk.W)
    table.pack()

    # Start the Tkinter event loop
    root.mainloop()

def update_gui(root, page_reference_sequence, number_of_frames, selected_algorithm, fifo, optimal, lru, lfu):
    # Map the algorithm names to the functions
    algorithms = {"FIFO": fifo, "Optimal": optimal, "LRU": lru, "LFU": lfu}

    # Run the selected algorithm
    page_faults, table_data = algorithmsselected_algorithm

    # Update the GUI with the results
    ttk.Label(root, text=f"{selected_algorithm}: {page_faults} page faults").pack()

    # Update the table with the data
    for i, (page_reference, page_table) in enumerate(table_data):
        table.insert(parent="", index=i, iid=i, text="", values=(page_reference, page_table))

    # Insert the number of page faults at the end of the table
    table.insert(parent="", index="end", iid="end", text="", values=("Page Faults", page_faults))
    
    #Start the main loop
    create_gui()
    
    # ... (previous code)

# Create a GUI window
def create_gui():
    # Create the root window
    root = tk.Tk()
    root.title("Page Replacement Algorithms")

    # Create a frame for the input fields
    input_frame = ttk.Frame(root)
    input_frame.pack()

    # Create radio buttons for selecting the algorithm
    algorithm_var = tk.StringVar()
    algorithms = ["FIFO", "Optimal", "LRU", "LFU"]
    for i, algorithm in enumerate(algorithms):
        ttk.Radiobutton(input_frame, text=algorithm, variable=algorithm_var, value=algorithm).grid(row=i, column=0)

    # Create a button to run the selected algorithm and update the GUI
    run_button = ttk.Button(input_frame, text="Run Algorithm", command=lambda: update_gui(
        root,
        [1, 2, 3, 2, 1, 5, 2, 1, 6, 2, 5, 6, 3, 1, 3, 6, 1, 2, 4, 3],
        3,
        algorithm_var.get(),
        fifo,
        optimal,
        lru,
        lfu
    ))
    run_button.grid(row=len(algorithms), column=0, columnspan=2)

    # Create a Treeview widget for the table
    table = ttk.Treeview(root)
    table["columns"] = ("Page Reference", "Page Table")
    table.column("#0", width=0, stretch=tk.NO)
    table.column("Page Reference", anchor=tk.W, width=120)
    table.column("Page Table", anchor=tk.W, width=120)
    table.heading("#0", text="", anchor=tk.W)
    table.heading("Page Reference", text="Page Reference", anchor=tk.W)
    table.heading("Page Table", text="Page Table", anchor=tk.W)
    table.pack()

    # Start the Tkinter event loop
    root.mainloop()

def update_gui(root, page_reference_sequence, number_of_frames, selected_algorithm, fifo, optimal, lru, lfu):
    # Map the algorithm names to the functions
    algorithms = {"FIFO": fifo, "Optimal": optimal, "LRU": lru, "LFU": lfu}

    # Run the selected algorithm
    page_faults, table_data = algorithms[selected_algorithm]

    # Clear the existing table data
    for item in table.get_children():
        table.delete(item)

    # Update the GUI with the results
    ttk.Label(root, text=f"{selected_algorithm}: {page_faults} page faults").pack()

    # Update the table with the data
    for i, (page_reference, page_table) in enumerate(table_data):
        table.insert(parent="", index=i, iid=i, text="", values=(page_reference, page_table))

    # Insert the number of page faults at the end of the table
    table.insert(parent="", index="end", iid="end", text="", values=("Page Faults", page_faults))


# Call the create_gui function to start the GUI
create_gui()
