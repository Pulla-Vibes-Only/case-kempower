# ui.py

class UI:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"

def mainTitle(mainTxt, color=UI.CYAN):
    starline = "*" * (len(mainTxt) + 2)
    print(color + "*" + starline + "*")
    print(f"* {mainTxt} *")
    print("*" + starline + "*" + UI.RESET)

def title(text, color=UI.CYAN):
    line = "═" * (len(text) + 2)
    print(color + "╔" + line + "╗")
    print(f"║ {text} ║")
    print("╚" + line + "╝" + UI.RESET)

def breadcrumb(path_list):
    print(UI.BLUE + " > ".join(path_list) + UI.RESET + "\n")

def success(msg):
    print(UI.GREEN + msg + UI.RESET)

def warning(msg):
    print(UI.YELLOW + msg + UI.RESET)

def error(msg):
    print(UI.RED + msg + UI.RESET)
