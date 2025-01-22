from tkinter import *
from tkinter import messagebox
import pandas as pd

def update_dropdowns(*args):
    '''
    Updates the dropdown menus for Genre, Platform, and Publisher
    based on the selected Year to show only valid options.
    '''
    filtered_df = df.copy()

    # Apply year filter
    year = year_var.get()
    if year != "Select Year":
        try:
            year = float(year)
            filtered_df = filtered_df[filtered_df['Year'] == year]
        except ValueError:
            messagebox.showerror("Error", "Invalid year selected.")
            return

    # Update genre dropdown
    genres = ["Select Genre"] + list(filtered_df['Genre'].unique())
    genre_menu['menu'].delete(0, 'end')
    for genre in genres:
        genre_menu['menu'].add_command(label=genre, command=lambda value=genre: genre_var.set(value))

    # Update platform dropdown
    platforms = ["Select Platform"] + list(filtered_df['Platform'].unique())
    platform_menu['menu'].delete(0, 'end')
    for platform in platforms:
        platform_menu['menu'].add_command(label=platform, command=lambda value=platform: platform_var.set(value))

    # Update publisher dropdown
    publishers = ["Select Publisher"] + list(filtered_df['Publisher'].unique())
    publisher_menu['menu'].delete(0, 'end')
    for publisher in publishers:
        publisher_menu['menu'].add_command(label=publisher, command=lambda value=publisher: publisher_var.set(value))

def filter_results():
    '''
    Filters the dataset based on selected criteria (Year, Genre, Platform, Publisher)
    and displays the top games with their sales. Saves the results to a CSV file.
    '''
    clear_output()
    filtered_df = df.copy()

    # Apply year filter
    year = year_var.get()
    if year != "Select Year":
        try:
            year = float(year)
            filtered_df = filtered_df[filtered_df['Year'] == year]
        except ValueError:
            messagebox.showerror("Error", "Invalid year selected.")
            return

    # Apply genre filter
    genre = genre_var.get()
    if genre != "Select Genre":
        filtered_df = filtered_df[filtered_df['Genre'] == genre]

    # Apply platform filter
    platform = platform_var.get()
    if platform != "Select Platform":
        filtered_df = filtered_df[filtered_df['Platform'] == platform]

    # Apply publisher filter
    publisher = publisher_var.get()
    if publisher != "Select Publisher":
        filtered_df = filtered_df[filtered_df['Publisher'] == publisher]

    # Check if any results remain
    if filtered_df.empty:
        messagebox.showerror("Error", "No results found for the selected criteria.")
        return

    # Get top results
    try:
        top_n = int(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for the top # of games.")
        return

    top_results = filtered_df.nlargest(top_n, 'Global_Sales')

    # Display results
    result_label = Label(results_frame, text=f"Top {top_n} Games:", anchor=W)
    result_label.pack()
    for _, row in top_results.iterrows():
        game_label = Label(results_frame, text=f"{row['Name']} - {row['Global_Sales']}M sales", anchor=W)
        game_label.pack()

    # Save results to CSV
    write_to_csv(top_results, "Filtered_Results")

def clear_output():
    '''
    Clears all results in the results frame.
    '''
    for widget in results_frame.winfo_children():
        widget.destroy()

def write_to_csv(results, name):
    '''
    Saves the filtered results to a CSV file.
    '''
    results.to_csv(f"{name}.csv", index=False)
    messagebox.showinfo("Complete", f"The results were saved to {name}.csv")

# Load and clean dataset
df = pd.read_csv('vgsales.csv')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # Keep Year as floats for compatibility
df['Global_Sales'] = pd.to_numeric(df['Global_Sales'], errors='coerce')  # Ensure Global_Sales is numeric
df = df.dropna(subset=['Name', 'Genre', 'Platform', 'Publisher', 'Global_Sales'])  # Drop rows with missing data

# Main GUI setup
window = Tk()
window.title("Game Sales Analysis")

# Input for top # of games
amount_frame = Frame(window)
amount_frame.pack(anchor=W)
amount_label = Label(amount_frame, text="Top # of Games", anchor=W)
amount_label.pack(side=LEFT)
amount_entry = Entry(amount_frame)
amount_entry.pack(side=LEFT)

# Year dropdown
year_frame = Frame(window)
year_frame.pack()
year_label = Label(year_frame, text="Year", width=15, anchor=W)
year_label.pack(side=LEFT)
year_var = StringVar(value="Select Year")
year_var.trace("w", update_dropdowns)
year_menu = OptionMenu(year_frame, year_var, "Select Year", *sorted(df['Year'].unique()))
year_menu.pack(side=LEFT)

# Genre dropdown
genre_frame = Frame(window)
genre_frame.pack()
genre_label = Label(genre_frame, text="Genre", width=15, anchor=W)
genre_label.pack(side=LEFT)
genre_var = StringVar(value="Select Genre")
genre_menu = OptionMenu(genre_frame, genre_var, "Select Genre")
genre_menu.pack(side=LEFT)

# Platform dropdown
platform_frame = Frame(window)
platform_frame.pack()
platform_label = Label(platform_frame, text="Platform", width=15, anchor=W)
platform_label.pack(side=LEFT)
platform_var = StringVar(value="Select Platform")
platform_menu = OptionMenu(platform_frame, platform_var, "Select Platform")
platform_menu.pack(side=LEFT)

# Publisher dropdown
publisher_frame = Frame(window)
publisher_frame.pack()
publisher_label = Label(publisher_frame, text="Publisher", width=15, anchor=W)
publisher_label.pack(side=LEFT)
publisher_var = StringVar(value="Select Publisher")
publisher_menu = OptionMenu(publisher_frame, publisher_var, "Select Publisher")
publisher_menu.pack(side=LEFT)

# Button to filter results
filter_button = Button(window, text="Find Results", command=filter_results)
filter_button.pack(pady=10)

# Frame to display results
results_frame = Frame(window)
results_frame.pack()

window.mainloop()
