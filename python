import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import os
import time

# Elegant theme colors
COLORS = {
    'background': '#FFF0F5',  # Light pink background
    'frame_bg': '#FFE4E8',    # Slightly darker pink for frames
    'text': '#4A4A4A',        # Elegant dark gray for text
    'accent': '#FF99AC',      # Accent pink
    'button': '#FFB6C1'       # Light pink for buttons
}

# Dhikrs with translations
DHIKRS = {
    "Subhanallah": "Glory be to Allah",
    "Alhamdulillah": "Praise be to Allah",
    "Allahu Akbar": "Allah is the Greatest",
    "La ilaha illallah": "There is no god but Allah",
    "Astaghfirullah": "I seek forgiveness from Allah"
}

class TasbihApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Tasbih")
        
        # Make window responsive
        self.root.minsize(400, 600)  # Minimum window size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Set window size to 80% of screen size
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        window_width = min(window_width, 1200)  # Max width
        window_height = min(window_height, 900)  # Max height
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.configure(bg=COLORS['background'])

        # Create main frame with weight configuration for responsiveness
        self.main_frame = tk.Frame(root, bg=COLORS['background'])
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Slideshow frame with rounded corners
        self.slideshow_frame = tk.Frame(self.main_frame, bg=COLORS['frame_bg'], height=200)
        self.slideshow_frame.pack(fill=tk.X, pady=10)
        self.slideshow_label = tk.Label(self.slideshow_frame, bg=COLORS['frame_bg'])
        self.slideshow_label.pack(pady=10)

        # Initialize slideshow variables
        self.slideshow_images = []
        self.image_files = []
        self.current_slide = 0
        
        # Store image file paths
        images_folder = os.path.join(os.path.dirname(__file__), "images")
        if os.path.exists(images_folder):
            self.image_files = sorted([
                os.path.join(images_folder, f) for f in os.listdir(images_folder)
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))
            ])
        
        # Wait for window to be ready before loading images
        self.root.update()
        self.root.after(100, self.load_slideshow_images)

        # Dhikr selection with styled combobox
        dhikr_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        dhikr_frame.pack(pady=30)
        
        self.dhikr_var = tk.StringVar(value="Astaghfirullah")
        tk.Label(
            dhikr_frame,
            text="SELECT DHIKR",
            font=("Arial", 28, "bold"),
            bg=COLORS['background'],
            fg=COLORS['text']
        ).pack(pady=10)
        
        style = ttk.Style()
        style.configure('Custom.TCombobox', 
                       background=COLORS['frame_bg'],
                       fieldbackground=COLORS['frame_bg'],
                       foreground=COLORS['text'])
        
        # Calculate responsive font sizes
        self.base_font_size = int(self.root.winfo_width() / 50)  # Base size for responsive fonts
        
        self.dhikr_menu = ttk.Combobox(
            dhikr_frame,
            textvariable=self.dhikr_var,
            values=list(DHIKRS.keys()),
            font=("Arial", self.base_font_size + 2),
            width=30,
            style='Custom.TCombobox'
        )
        self.dhikr_menu.pack(pady=5)

        # Counter display with beautiful styling
        self.count = 0
        counter_frame = tk.Frame(self.main_frame, bg=COLORS['frame_bg'], pady=20)
        counter_frame.pack(fill='x', pady=30, padx=50)
        
        self.count_label = tk.Label(
            counter_frame,
            text="0",
            font=("Arial", 120, "bold"),
            bg=COLORS['frame_bg'],
            fg=COLORS['text']
        )
        self.count_label.pack(pady=20)

        # Buttons with gradient effect
        button_frame = tk.Frame(self.main_frame, bg=COLORS['background'])
        button_frame.pack(pady=30)

        self.create_styled_button(button_frame, "COUNT", self.increment)
        self.create_styled_button(button_frame, "RESET", self.reset)

        # Challenges section with border and background
        challenge_section = tk.Frame(self.main_frame, bg=COLORS['frame_bg'], bd=2, relief='solid')
        challenge_section.pack(fill='x', pady=20, padx=50)
        
        # Title for challenges
        tk.Label(
            challenge_section,
            text="DAILY CHALLENGES",
            font=("Arial", 24, "bold"),
            bg=COLORS['frame_bg'],
            fg=COLORS['text']
        ).pack(pady=(15, 10))

        # Challenge tracking with elegant styling
        self.challenge_goal = 1000
        self.challenge_label = tk.Label(
            challenge_section,
            text=f"Astaghfirullah Challenge: 0 / {self.challenge_goal}",
            font=("Arial", 20),
            bg=COLORS['frame_bg'],
            fg=COLORS['text']
        )
        self.challenge_label.pack(pady=10)

        # Other challenges
        self.other_challenges = {"Subhanallah": 500, "Total Dhikr": 2000}
        self.other_labels = {}
        
        challenges_frame = tk.Frame(challenge_section, bg=COLORS['frame_bg'])
        challenges_frame.pack(pady=10)
        
        for key, goal in self.other_challenges.items():
            label = tk.Label(
                challenges_frame,
                text=f"{key} Challenge: 0 / {goal}",
                font=("Arial", 18),
                bg=COLORS['frame_bg'],
                fg=COLORS['text']
            )
            label.pack(pady=5)
            self.other_labels[key] = label

    def add_rounded_corners(self, image, radius):
        circle = Image.new('L', (radius * 2, radius * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, radius * 2, radius * 2), fill=255)
        alpha = Image.new('L', image.size, 255)
        w, h = image.size
        alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
        alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
        alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
        alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
        image.putalpha(alpha)
        return image

    def create_styled_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 24, "bold"),
            bg=COLORS['button'],
            fg=COLORS['text'],
            relief=tk.FLAT,
            padx=40,
            pady=20,
            borderwidth=0,
            width=10
        )
        btn.pack(side=tk.LEFT, padx=10)
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.configure(bg=COLORS['accent']))
        btn.bind("<Leave>", lambda e: btn.configure(bg=COLORS['button']))

    def start_slideshow(self):
        def cycle():
            if self.slideshow_images:
                self.current_slide = (self.current_slide + 1) % len(self.slideshow_images)
                self.slideshow_label.config(image=self.slideshow_images[self.current_slide])
                self.slideshow_label.image = self.slideshow_images[self.current_slide]
                self.root.after(5000, cycle)  # 5 seconds per image
        cycle()

    def increment(self):
        self.count += 1
        self.count_label.config(text=str(self.count))
        
        # Update Astaghfirullah challenge
        if self.dhikr_var.get() == "Astaghfirullah":
            self.challenge_label.config(text=f"Daily Challenge: {self.count} / {self.challenge_goal} Astaghfirullah")
            if self.count >= self.challenge_goal:
                messagebox.showinfo("MashaAllah!", "You've completed 1000 Astaghfirullah!")
        
        # Update other challenges
        current_dhikr = self.dhikr_var.get()
        if current_dhikr in self.other_challenges:
            self.other_labels[current_dhikr].config(
                text=f"{current_dhikr} Challenge: {self.count} / {self.other_challenges[current_dhikr]}"
            )
            if self.count >= self.other_challenges[current_dhikr]:
                messagebox.showinfo("MashaAllah!", f"You've completed {self.count} {current_dhikr}!")

    def reset(self):
        self.count = 0
        self.count_label.config(text="0")
        self.challenge_label.config(text=f"Daily Challenge: 0 / {self.challenge_goal} Astaghfirullah")
        
        # Reset other challenge displays
        for key, goal in self.other_challenges.items():
            self.other_labels[key].config(text=f"{key} Challenge: 0 / {goal}")

    def on_resize(self, event=None):
        # Update font sizes based on window size
        if event and event.widget == self.root:
            # Calculate new base font size
            self.base_font_size = int(self.root.winfo_width() / 50)
            
            # Update fonts for all elements
            self.count_label.config(font=("Arial", self.base_font_size * 3, "bold"))
            self.challenge_label.config(font=("Arial", self.base_font_size))
            self.dhikr_menu.config(font=("Arial", self.base_font_size + 2))
            
            # Update button fonts
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, tk.Button):
                    widget.config(font=("Arial", self.base_font_size + 2, "bold"))
            
            # Reload images with new sizes if needed
            if hasattr(self, 'slideshow_images') and self.slideshow_images:
                self.reload_slideshow_images()

    def load_slideshow_images(self):
        # Clear existing images
        self.slideshow_images = []
        
        # Calculate initial image size
        window_width = self.root.winfo_width()
        img_width = int(window_width * 0.5)
        img_height = int(img_width * 0.625)
        
        # Load and process images
        for file_path in self.image_files:
            try:
                img = Image.open(file_path)
                # Resize image
                img = img.resize((img_width, img_height), Image.LANCZOS)
                # Add rounded corners
                img = self.add_rounded_corners(img, int(img_width * 0.05))
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                self.slideshow_images.append(photo)
            except Exception as e:
                print(f"Error loading {os.path.basename(file_path)}: {e}")
        
        # Start slideshow if images were loaded successfully
        if self.slideshow_images:
            self.slideshow_label.config(image=self.slideshow_images[0])
            self.slideshow_label.image = self.slideshow_images[0]
            self.start_slideshow()
    
    def reload_slideshow_images(self):
        if hasattr(self, 'image_files') and self.image_files:
            window_width = self.root.winfo_width()
            img_width = int(window_width * 0.5)
            img_height = int(img_width * 0.625)
            
            self.slideshow_images = []
            for file_path in self.image_files:
                try:
                    img = Image.open(file_path)
                    img = img.resize((img_width, img_height), Image.LANCZOS)
                    img = self.add_rounded_corners(img, int(img_width * 0.05))
                    photo = ImageTk.PhotoImage(img)
                    self.slideshow_images.append(photo)
                except Exception as e:
                    print(f"Error reloading {os.path.basename(file_path)}: {e}")
            
            if self.slideshow_images:
                self.slideshow_label.config(image=self.slideshow_images[self.current_slide])
                self.slideshow_label.image = self.slideshow_images[self.current_slide]

if __name__ == "__main__":
    root = tk.Tk()
    app = TasbihApp(root)
    # Bind resize event
    root.bind("<Configure>", app.on_resize)
    root.mainloop()
