import unittest
import customtkinter as ctk
from source.classes.app import App
from tkinter import Widget

def getFullName(widget: Widget):
    name_list = [widget.winfo_name()]
    while True:
        widget = widget.master
        name = widget.winfo_name()
        if name == "tk":
            name_list.append("")
            return ".".join(reversed(name_list))
        name_list.append(name)

class TestApp(unittest.TestCase):

    async def _start_app(self):
        self.app.mainloop()

    def setUp(self):
        self.app = App()
        with self.assertWarns(RuntimeWarning) as warn:
            self._start_app()

        self.assertEqual(str(warn.warning), "coroutine 'TestApp._start_app' was never awaited")


    def tearDown(self):
        self.app.quit()


    def test_login(self):
        username_entry: ctk.CTkEntry = self.app.nametowidget(".!ctkframe.!canvas.!mainloginframe.!loginformframe.!ctkentry")
        password_entry: ctk.CTkEntry = self.app.nametowidget(".!ctkframe.!canvas.!mainloginframe.!loginformframe.!ctkentry2")
        login_button: ctk.CTkButton = self.app.nametowidget(".!ctkframe.!canvas.!mainloginframe.!loginformframe.!ctkbutton")

        login_map = [
            ["", "", "please give a username"],
            ["a", "", "username doesn't exist"],
            ["Frau Meyer", "", "please give a password"],
            ["Frau Meyer", "a", "password incorrect"],
            ["Frau Meyer", "P112", "logged in"]
        ]

        for user, password, log_message in login_map:
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")
            username_entry.insert(0, user)
            password_entry.insert(0, password)

            with self.assertLogs() as captured:
                login_button.invoke()

            self.assertEqual(len(captured.records), 1)
            self.assertEqual(captured.records[0].getMessage(), log_message)