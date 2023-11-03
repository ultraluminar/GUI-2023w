from test.classes.app import App
from json import load

# load json
with open("test/pwd.json", mode="r") as filestream:
    pwds: dict = load(filestream)

app = App(pwds=pwds)
app.mainloop()
