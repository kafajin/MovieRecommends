import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import PhotoImage
from PIL import Image, ImageTk  


API_KEY = "e2263032"  

# Function to fetch movie data from OMDb API
def fetch_movie_data():
    title = movie_title_entry.get()  # Get the movie title entered by the user
    if title:
        url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            movie_data = response.json()

            if movie_data["Response"] == "True":
                # Display movie information
                display_movie_info(movie_data)
            else:
                messagebox.showerror("Error", "Movie not found. Please try again.")
        else:
            messagebox.showerror("Error", "Unable to fetch data from OMDb. Try again later.")
    else:
        messagebox.showwarning("Input Error", "Please enter a movie title.")

# Function to display movie details in the GUI
def display_movie_info(movie_data):
    # Clear previous movie information
    movie_info_label.delete(1.0, tk.END)  # Clear the Text widget content

    title = movie_data["Title"]
    year = movie_data["Year"]
    genre = movie_data["Genre"]
    plot = movie_data["Plot"]
    director = movie_data["Director"]
    poster_url = movie_data["Poster"]

    # Construct the movie details text with wrapping
    movie_info = (
        f"Title: {title}\n"
        f"Year: {year}\n"
        f"Genre: {genre}\n"
        f"Director: {director}\n\n"
        f"Plot:\n{plot}\n"
    )

    movie_info_label.config(state=tk.NORMAL)
    movie_info_label.insert(tk.END, movie_info)  # Insert new text
    movie_info_label.config(state=tk.DISABLED)  # Disable editing

    # Show the movie poster with scaling
    try:
        # Fetch the poster image
        movie_poster = requests.get(poster_url, stream=True).raw
        img = Image.open(movie_poster)
        
        # Resize the image to fit the Tkinter window (max width = 300px)
        img = img.resize((300, int(img.height / img.width * 300)), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)

        # Update the poster label with the image
        poster_label.config(image=img_tk)
        poster_label.image = img_tk  # Keep a reference to the image
    except Exception as e:
        poster_label.config(text="No poster available")

# Function to clear the search input and result
def clear_search():
    movie_title_entry.delete(0, tk.END)
    movie_info_label.config(state=tk.NORMAL)
    movie_info_label.delete(1.0, tk.END)
    movie_info_label.config(state=tk.DISABLED)
    poster_label.config(image=None)

# Setting up the Tkinter window
root = tk.Tk()
root.title("Movie Recommendation App")
root.geometry("500x600")

# Add a background color to the window
root.config(bg="#2c3e50")

# Create a frame for the input section
input_frame = tk.Frame(root, bg="#2c3e50")
input_frame.pack(pady=20)

# Input field for movie title
movie_title_label = tk.Label(input_frame, text="Enter a movie title:", font=("Arial", 14), fg="#ecf0f1", bg="#2c3e50")
movie_title_label.pack(pady=5)

movie_title_entry = tk.Entry(input_frame, width=40, font=("Arial", 12), bd=2, relief="solid")
movie_title_entry.pack(pady=5)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=10)

# Button to fetch movie data
search_button = tk.Button(button_frame, text="Search Movie", command=fetch_movie_data, font=("Arial", 14), bg="#27ae60", fg="white", relief="solid", width=20)
search_button.pack(pady=10)

# Button to clear the search
clear_button = tk.Button(button_frame, text="Clear", command=clear_search, font=("Arial", 14), bg="#e74c3c", fg="white", relief="solid", width=20)
clear_button.pack(pady=5)

# Label to display movie information
movie_info_label = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), width=50, height=10, bd=2, relief="solid", padx=10, pady=10, state=tk.DISABLED)
movie_info_label.pack(pady=10)

# Label to display movie poster
poster_label = tk.Label(root, bg="#34495e", width=40, height=20)
poster_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
