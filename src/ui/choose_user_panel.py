import tkinter as tk

# INFO: This panel allows the user to choose between Admin and User modes. Rather than doing it from the CLI.
## It will then call the controller to switch frames accordingly.

# -- Choose User Panel --
class ChooseUserPanel(tk.Frame):
    def __init__(self, parent, controller=None) -> None:
        super().__init__(parent)
        self.controller = controller
        self.built = False

    def build_ui(self) -> None:
        """Create widgets once when the panel is shown."""
        self.configure(background="lightblue")
        title = tk.Label(self, text="Choose User Type Panel",
                         bg="lightblue", font=("Arial", 16))
        title.pack(pady=20)
        tk.Button(self, text="Admin", command=self.admin_selected,
                  width=20, height=2, font=("Arial", 12)).pack(pady=10)
        tk.Button(self, text="User", command=self.user_selected,
                  width=20, height=2, font=("Arial", 12)).pack(pady=10)
        self.built = True

    def on_show(self) -> None:
        """Called by the controller when this frame is shown."""
        if not self.built:
            self.build_ui()
        # additional refresh logic could go here

    def admin_selected(self) -> bool:
        print("Admin selected")
        if self.controller:
            try:
                self.controller.show_frame("AdminPanel")
            except Exception as e:
                print("Error switching to AdminPanel:", e)
        return True

    def user_selected(self) -> bool:
        print("User selected")
        if self.controller:
            try:
                # target name should match the key used in AppController
                self.controller.show_frame("FacialStudentPanel")
            except Exception as e:
                print("Error switching to user panel:", e)
        return True

    def close(self) -> None:
        """Clean up resources when the application is closed."""
        self.winfo_toplevel().destroy()

# -- END Choose User Panel --

def main() -> None:
    root = tk.Tk()
    root.title("Choose User Panel")
    root.geometry("400x300")
    # When used standalone, controller can be None
    app = ChooseUserPanel(root)
    app.on_show()
    app.pack(fill="both", expand=True)
    
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == '__main__':
    main()
