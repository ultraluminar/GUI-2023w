import unittest

from source.classes.app import App

class TestApp(unittest.TestCase):

    async def _start_app(self):
        self.app.mainloop()

    def setUp(self):
        self.app = App()
        self._start_app()


    def tearDown(self):
        self.app.destroy()

    # test from here
    def test_exit_button(self):
        self.assertEqual(self.app.nametowidget(".!mainsidebar.!ctkbutton2").cget("text"), "Abmelden")