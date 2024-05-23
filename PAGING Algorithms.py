import tkinter as tk
from tkinter import ttk

# Paging algorithm functions
# Implement FIFO, Optimal, LRU, and LFU as mentioned earlier
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
                farthest_page = page_table[0]
                farthest_index = -1
                for frame in page_table:
                    index = page_reference_sequence[page_reference_sequence.index(page_reference):].index(frame) if frame in page_reference_sequence[page_reference_sequence.index(page_reference):] else float('inf')
                    if index > farthest_index:
                        farthest_index = index
                        farthest_page = frame

                # Remove the page to be replaced
                page_table.remove(farthest_page)
            # Add the new page to the frames
            page_table.append(page_reference)
            page_faults += 1

        table_data.append((page_reference, " ".join(map(str, page_table))))

    return page_faults, table_data


def lru(page_reference_sequence, number_of_frames):
    page_table = []  # Represents the frames in memory
    page_faults = 0
    table_data = []  # To store data for the table

    for page_reference in page_reference_sequence:
        if page_reference not in page_table:
            if len(page_table) == number_of_frames:
                # Find the page in the frames that was least recently used (LRU)
                oldest_page = min(page_table, key=lambda x: page_reference_sequence[::-1].index(x))
                page_table.remove(oldest_page)
            # Add the new page (most recently used) to the frames
            page_table.append(page_reference)
            page_faults += 1
        else:
            # Move the used page to the end (most recently used position) of the frames
            page_table.remove(page_reference)
            page_table.append(page_reference)

        table_data.append((page_reference, " ".join(map(str, page_table))))

    return page_faults, table_data


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


# Create a function to run the selected algorithm and update the UI
def run_algorithm():
    algorithm = algorithm_var.get()
    page_reference_sequence = list(map(int, input_entry.get().split()))
    number_of_frames = int(frames_entry.get())

    if algorithm == "FIFO":
        page_faults, table_data = fifo(page_reference_sequence, number_of_frames)
    elif algorithm == "Optimal":
        page_faults, table_data = optimal(page_reference_sequence, number_of_frames)
    elif algorithm == "LRU":
        page_faults, table_data = lru(page_reference_sequence, number_of_frames)
    elif algorithm == "LFU":
        page_faults, table_data = lfu(page_reference_sequence, number_of_frames)
    else:
        page_faults, table_data = 0, []

    # Display the results
    result_label.config(text=f"Total Page Faults ({algorithm}): {page_faults}")

    # Clear previous table data
    for row in table.get_children():
        table.delete(row)

    # Update the table with new data
    for i, (page_reference, frames) in enumerate(table_data):
        table.insert('', 'end', values=(i + 1, page_reference, frames))

# Create the GUI window
root = tk.Tk()
root.title("Paging Algorithm Demo")

# Create input fields and labels
input_label = tk.Label(root, text="Enter Page Reference Sequence (space-separated):")
input_label.pack()
input_entry = tk.Entry(root)
input_entry.pack()

frames_label = tk.Label(root, text="Enter Number of Frames:")
frames_label.pack()
frames_entry = tk.Entry(root)
frames_entry.pack()

algorithm_label = tk.Label(root, text="Select Algorithm:")
algorithm_label.pack()
algorithm_var = tk.StringVar()
algorithm_entry = ttk.Combobox(root, textvariable=algorithm_var, values=["FIFO", "Optimal", "LRU", "LFU"])
algorithm_entry.set("FIFO")
algorithm_entry.pack()

calculate_button = tk.Button(root, text="Run Algorithm", command=run_algorithm)
calculate_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Create a table to display page references and frames
table_frame = ttk.Frame(root)
table_frame.pack(pady=10)
table = ttk.Treeview(table_frame, columns=('Step', 'Page', 'Frames'))
table.heading('#1', text='Step')
table.heading('#2', text='Page')
table.heading('#3', text='Frames')
table.pack()

# Start the GUI main loop
root.mainloop()
