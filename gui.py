import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import config

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plex TV Channel GUI")

        # Cartoons
        tk.Label(self, text="Cartoons (comma separated)").grid(row=0, column=0, sticky="w")
        self.cartoons_var = tk.Entry(self, width=50)
        self.cartoons_var.insert(0, ",".join(config.cartoons))
        self.cartoons_var.grid(row=0, column=1, padx=5, pady=2)

        # Dir
        tk.Label(self, text="Show Directory").grid(row=1, column=0, sticky="w")
        self.dir_var = tk.Entry(self, width=50)
        self.dir_var.insert(0, config.dir)
        self.dir_var.grid(row=1, column=1, padx=5, pady=2)
        tk.Button(self, text="Browse", command=self.browse_dir).grid(row=1, column=2)

        # Output dir
        tk.Label(self, text="Output Directory").grid(row=2, column=0, sticky="w")
        self.out_var = tk.Entry(self, width=50)
        self.out_var.insert(0, config.tvDirectory)
        self.out_var.grid(row=2, column=1, padx=5, pady=2)
        tk.Button(self, text="Browse", command=self.browse_out).grid(row=2, column=2)

        # Commercials dir
        tk.Label(self, text="Commercials Directory").grid(row=3, column=0, sticky="w")
        self.commercials_var = tk.Entry(self, width=50)
        self.commercials_var.insert(0, config.commercialsDirectory)
        self.commercials_var.grid(row=3, column=1, padx=5, pady=2)
        tk.Button(self, text="Browse", command=self.browse_comm).grid(row=3, column=2)

        # Timezone
        tk.Label(self, text="Timezone").grid(row=4, column=0, sticky="w")
        self.timezone_var = tk.Entry(self, width=20)
        self.timezone_var.insert(0, config.timezone)
        self.timezone_var.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        # Poster
        tk.Label(self, text="Channel Poster URL").grid(row=5, column=0, sticky="w")
        self.poster_var = tk.Entry(self, width=50)
        self.poster_var.insert(0, config.showPoster)
        self.poster_var.grid(row=5, column=1, padx=5, pady=2)

        # Channel name
        tk.Label(self, text="Channel Name").grid(row=6, column=0, sticky="w")
        self.channel_var = tk.Entry(self, width=50)
        self.channel_var.insert(0, config.channelName)
        self.channel_var.grid(row=6, column=1, padx=5, pady=2)

        # Flags
        self.backup_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Backup", variable=self.backup_var).grid(row=7, column=0, sticky="w")
        self.commercials_flag = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Commercials", variable=self.commercials_flag).grid(row=7, column=1, sticky="w")

        tk.Button(self, text="Run", command=self.run_scripts).grid(row=8, column=0, columnspan=3, pady=10)

    def browse_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.dir_var.delete(0, tk.END)
            self.dir_var.insert(0, path)

    def browse_out(self):
        path = filedialog.askdirectory()
        if path:
            self.out_var.delete(0, tk.END)
            self.out_var.insert(0, path)

    def browse_comm(self):
        path = filedialog.askdirectory()
        if path:
            self.commercials_var.delete(0, tk.END)
            self.commercials_var.insert(0, path)

    def save_config(self):
        cartoons = [c.strip() for c in self.cartoons_var.get().split(',') if c.strip()]
        with open('config.py', 'w') as f:
            f.write(f"cartoons = {cartoons}\n")
            f.write(f"dir = r'{self.dir_var.get()}'\n")
            f.write(f"tvDirectory = r'{self.out_var.get()}'\n")
            f.write(f"commercialsDirectory = r'{self.commercials_var.get()}'\n")
            f.write(f"timezone = '{self.timezone_var.get()}'\n")
            f.write(f"showPoster = '{self.poster_var.get()}'\n")
            f.write(f"channelName = '{self.channel_var.get()}'\n")

    def run_scripts(self):
        self.save_config()
        backup = 'yes' if self.backup_var.get() else 'no'
        commercials = 'yes' if self.commercials_flag.get() else 'no'
        try:
            subprocess.run([sys.executable, 'generatePlaylist.py', backup, commercials], check=True)
            subprocess.run([sys.executable, 'generateXMLTV.py'], check=True)
            messagebox.showinfo('Success', 'Files generated successfully!')
        except subprocess.CalledProcessError as e:
            messagebox.showerror('Error', f'An error occurred: {e}')

if __name__ == '__main__':
    App().mainloop()
