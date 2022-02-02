"""
Password Generator

All packages used in this script are built-in packages.

This application has a graphical user interface - it does this with the aid of the TK UI toolkit.

Function names with _ is just a naming convention that signifies that these are internal functions only.

This application uses the my "Williams" ttk theme to make Tkinter look nice and modern.

~Tyler Williams
"""

# Import Packages
import tkinter as tk;
from tkinter import ttk;
from tkinter import filedialog as fd;
from tkinter import messagebox as mb;
import os, string, random;

# Global Variables
cwd = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"); # Current working directory
srandom = random.SystemRandom(); # Cryptographically secure randomness

# Code
class passwordWindow():
    def __init__(self) -> None:
        self.checkboxStates = {}; # This keeps track of the states of any checkbox (or switchButton)

        # Generate password and set self.outputWindow's text
        def _generatePassword() -> None:
            # The next 3 lines return strings that contain all of a certain type of ascii characters (e.g letters) if the correct switch is toggled on
            chars = "";
            if self.hasLettersValue.get() == True: chars += string.ascii_letters;
            if self.hasDigitsValue.get() == True: chars += string.digits;
            if self.hasPunctuationValue.get() == True: chars += string.punctuation;

            if len(chars.strip()) != 0:
                self.outputWindow["state"] = ""; # The entry is read only so the user can copy and paste text, however this also means that I cannot change the text so I need to disable readonly
                self.outputWindow.delete(0, len(self.outputWindow.get())); # Clear display
                self.outputWindow.insert(0, "".join([srandom.choice(chars) for i in range(int(self.stringLengthDisplay["text"]))])); # Set display to randomly generated stringg that only uses the characters the user has allowed
                self.outputWindow["state"] = "readonly"; # Re-enable readonly

        # Change the label that displays the current selected length via the scale
        def _updateLengthDisplay(value) -> None: self.stringLengthDisplay["text"] = value.split(".")[0];

        # Copy self.outputWindow's text into the clipboard
        def _copyPassword() -> None: self.window.clipboard_clear(); self.window.clipboard_append(self.outputWindow.get());

        def _controlA(event) -> None: event.widget.select_range(0, "end"); event.widget.icursor("end"); return "break";

        # Save last generated password to file
        def _savePassword() -> None:
            if len(self.outputWindow.get().strip()) != 0:
                try:
                    file = fd.asksaveasfilename(filetypes=(('Text files', 'txt'), ('All files', '*'))); # Ask user to open file or create file that is .txt
                    if len(file.strip()) != 0:
                        if file.split(".")[0] == file: # Cannot be split
                            file = file + ".txt";
                        with open(file, "w") as filew:
                            filew.write(self.outputWindow.get());
                            mb.showinfo(title="Password Generator", message="Password written to file successfully!");
                except:
                    pass; # Ignore
            else:
                mb.showwarning(title="Password Generator", message="No password generated...");

        # [WIDGET].place() is a function that allows me to describe where a specific widget should be

        # Window
        self.window = tk.Tk(); # Create window
        self.window.call("source", cwd + "/Williams Theme/Williams.tcl")
        ttk.Style().theme_use('Williams')
        self.window.title("Password Generator");
        self.window.geometry("420x190");
        self.window.resizable(width=False, height=False);

        # Output Display
        self.outputWindow = ttk.Entry(self.window, state="readonly");
        self.outputWindow.place(x=10, y=10, width=260, height=35);
        self.outputWindow.bind("<Control-a>", _controlA);

        self.copy = ttk.Button(self.window, text="Copy", command=_copyPassword);
        self.copy.place(x=280, y=10, width=60, height=35)

        self.save = ttk.Button(self.window, text="Save", command=_savePassword);
        self.save.place(x=350, y=10, width=60, height=35)

        # Scale Display
        scaleTextLabel = ttk.Label(self.window, anchor="w", text="Number of characters (max 128):");
        scaleTextLabel.place(x=10, y=55, width=400, height=20);

        self.stringLength = ttk.Scale(self.window, from_=1, to=128, value=1.0, command=_updateLengthDisplay)
        self.stringLength.place(x=10, y=80, width=360, height=20);

        self.stringLengthDisplay = ttk.Label(self.window, anchor="center", text=str(self.stringLength.get()).split(".")[0]);
        self.stringLengthDisplay.place(x=380, y=80, width=30, height=20);

        # Settings Display
        self.hasLettersValue = tk.BooleanVar(self.window);
        self.hasLetters = ttk.Checkbutton(self.window, text="Has Letters", style="Switch", onvalue=True, offvalue=False, variable=self.hasLettersValue)
        self.hasLetters.place(x=10, y=110, width=122, height=20);
	
        self.hasDigitsValue = tk.BooleanVar(self.window);
        self.hasDigits = ttk.Checkbutton(self.window, text="Has Digits", style="Switch", onvalue=True, offvalue=False, variable=self.hasDigitsValue)
        self.hasDigits.place(x=137, y=110, width=122, height=20);

        self.hasPunctuationValue = tk.BooleanVar(self.window);
        self.hasPunctuation = ttk.Checkbutton(self.window, text="Has Punctuation", style="Switch", onvalue=True, offvalue=False, variable=self.hasPunctuationValue)
        self.hasPunctuation.place(x=259, y=110, width=151, height=20);

        # Generate Button
        self.generatePassword = ttk.Button(self.window, style="Accent", text="Generate Password", command=_generatePassword);
        self.generatePassword.place(x=10, y=145, width=400, height=35);

        # Start Window Loop
        self.window.mainloop(); # Start TK mainloop

if __name__ == "__main__":
    passwordWindow(); # Start the application