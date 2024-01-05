from source.classes.app import App
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # set logging level to INFO

app = App()  # create app
app.mainloop()  # start mainloop
