from tkcalendar import Calendar
from customtkinter import CTk
from tkinter import StringVar

from datetime import datetime
from dateutil.relativedelta import relativedelta, MO

class CallApp(CTk):
    def __init__(self, ):
        super().__init__()
        self.update_idletasks()

        self.title("tkCal")
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)

        self.setGeometry()

        self.mindate = datetime.today()
        self.maxdate = self.mindate + relativedelta(months=3)

        # self.var_date = StringVar()

        self.cal = Calendar(master=self, locale="de_DE",  # textvariable=self.var_date,
                            mindate=self.mindate, maxdate=self.maxdate)


        self.cal.calevent_create(date=self.mindate, text="karies", tags="karies")
        self.cal.tag_config(tag="karies", background="red")

        self.cal.grid(row=0, column=0, sticky="nsew")

    def setGeometry(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        initial_width = round(screen_width * 0.5)
        initial_height = round(screen_height * 0.5)

        startpos_x = round((screen_width / 2) - (initial_width / 2))
        startpos_y = round((screen_height / 2) - (initial_height / 2))

        self.geometry(f"{initial_width}x{initial_height}+{startpos_x}+{startpos_y}")


if __name__ == '__main__':
    app = CallApp()

    app.mainloop()