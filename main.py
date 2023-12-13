from source.classes.app import App
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = App()
app.mainloop()
