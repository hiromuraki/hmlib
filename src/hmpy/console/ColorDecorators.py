def red(x: str) -> str:
    return f"\033[31m{x}\033[0m"


def green(x: str) -> str:
    return f"\033[32m{x}\033[0m"


def yellow(x: str) -> str:
    return f"\033[33m{x}\033[0m"


def blue(x: str) -> str:
    return f"\033[34m{x}\033[0m"


def magenta(x: str) -> str:
    return f"\033[35m{x}\033[0m"


def cyan(x: str) -> str:
    return f"\033[36m{x}\033[0m"


def white(x: str) -> str:
    return f"\033[37m{x}\033[0m"


def black(x: str) -> str:
    return f"\033[30m{x}\033[0m"
