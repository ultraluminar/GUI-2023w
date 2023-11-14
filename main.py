from source.classes.app import App
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

app = App()
app.mainloop()
