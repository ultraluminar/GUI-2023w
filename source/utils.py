from bcrypt import hashpw, checkpw, gensalt
def mhash(plain: str) -> str:
    return hashpw(plain.encode(), gensalt()).decode()

def mcheck(user: str, pwd: str) -> bool:
    return checkpw(user.encode(), pwd.encode())