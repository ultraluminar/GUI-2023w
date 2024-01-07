from source.classes.app import App
from pathlib import Path
import subprocess
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # set logging level to INFO

if not Path("./data/patients.csv").is_file():  # check if data files exist
    logging.info("Data Files not found, running parsingExcelData.py")
    subprocess.run(["python", "./source/parsingExcelData.py"])  # run parsingExcelData.py
    logging.info("Excel data parsed to Data Files")

app = App()  # create app
app.mainloop()  # start mainloop
