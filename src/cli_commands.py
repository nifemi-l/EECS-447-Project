import os

# Every single function must accept active_user and args as parameters. args may be None type

def library_help(active_user, args):
    helper_text = """
    help : show this helper text
    logout : clear the active user
    quit : close the session and exit
    """
    print(helper_text)

def clear(active_user, args):
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")