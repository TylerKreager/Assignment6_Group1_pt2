import tkinter as tk
from tkinter import Tk, messagebox, filedialog
from tkinter import ttk
from tkinter.ttk import Frame, Label, Button, Style
import requests
from PIL import Image, ImageTk
import io
from requests.exceptions import HTTPError


class MainWindow(Tk):

    BASE_URL = "http://127.0.0.1:5000"

    def __init__(self):
        super().__init__()
        self.title("Image API Client")
        self.geometry("600x500")
        self.configure(bg="lightblue")

        self.selected_image_name = tk.StringVar()
        self.image_label = None #only keeping label as 
        self.image_display = None

        self.create_widgets()
        self.fetch_image_list()  # Automatically load dropdown


    # GUI Main Window

    def create_widgets(self):
        style = Style()
        style.configure("Blue.TFrame", background="lightblue") #default stylings lifted one-to-one from last assignment
        style.configure("TLabel", background="lightblue")

        self.main_frame = Frame(self, style="Blue.TFrame")
        self.main_frame.pack(expand=True, fill="both", pady=20)

        title = Label(self.main_frame, text="Image Viewer", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Dropdown row
        dropdown_row = Frame(self.main_frame, style="Blue.TFrame")
        dropdown_row.pack(pady=10)

        Label(dropdown_row, text="Select Image:").grid(row=0, column=0, padx=5) #will not need to change the label at any point

        self.dropdown = ttk.Combobox(dropdown_row, textvariable=self.selected_image_name, state="readonly") #add the label and dropdown side by side
        self.dropdown.grid(row=0, column=1, padx=5)

        load_btn = Button(dropdown_row, text="Load Image", command=self.load_selected_image) #handle the load image of retrieving image from collection
        load_btn.grid(row=0, column=2, padx=5)

        # Image display
        self.image_label = Label(self.main_frame) #actual display label that holds the loaded image
        self.image_label.pack(pady=10)

        # Upload button
        upload_btn = Button(self.main_frame, text="Upload Image", command=self.upload_image) #handle uploading image back to server
        upload_btn.pack(pady=10)

    # Server Client Code

    def fetch_image_list(self):
        try:
            response = requests.get(f"{self.BASE_URL}/allImages")
            response.raise_for_status()

            image_list = response.json()
            self.dropdown["values"] = image_list

            if image_list:
                self.dropdown.current(0) #as long as image_list has loaded, set the first value to current "selected"
        except HTTPError as http_error:
            print(f'HTTP error occurred: {http_error}')  #Manage various HTTP errors
        except Exception as e: #added appropriate error handling for HTTP related fetch
            messagebox.showerror("Error", str(e))

    def load_selected_image(self): #load the one image given by its url that was retrieved by fetch_image list
        filename = self.selected_image_name.get()
        if not filename: #each catch-all if passed a null
            return

        try:
            response = requests.get(f"{self.BASE_URL}/oneImage/{filename}", stream=True)
            response.raise_for_status()

            image = Image.open(io.BytesIO(response.content))
            image = image.resize((300, 300))

            self.image_display = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.image_display)
            self.image_label.image = self.image_display

            messagebox.showinfo("Image Info", f"Format: {image.format}\nSize: {image.size}\nMode: {image.mode}")

        except HTTPError as http_error:
            messagebox.showerror("HTTP Error", f"Image load failed:\n{http_error}")  #Manage various HTTP errors
        except OSError as os_error:
            messagebox.showerror("File Error", f"Image processing error:\n{os_error}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))

    def upload_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")]) #enforces strict compliance with image format to avoid bad actors
        if not filepath: #each catch-all if passed a null
            return

        try:
            # Open file in binary mode and send it with the correct key
            with open(filepath, "rb") as file:
                files = {"image": file}  # key must match server: 'image'
                response = requests.post(f"{self.BASE_URL}/upload", files=files)
                response.raise_for_status()

            messagebox.showinfo("Success", "Image uploaded successfully!")
            self.fetch_image_list()

        except HTTPError as http_error:
            messagebox.showerror("HTTP Error", f"Upload failed:\n{http_error}")  #Manage various HTTP errors
        except OSError as os_error:
            messagebox.showerror("File Error", f"File error:\n{os_error}")
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))



app = MainWindow()
app.mainloop()
