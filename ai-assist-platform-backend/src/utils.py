import sys


# Печатает оранжевое предупреждение в консоль и для удобства возвращает текст предупреждения
def warn(text: str) -> str:
    # ANSI escape code for a custom orange color (RGB: 255, 165, 0)
    orange = "\033[38;2;255;165;0m"
    reset = "\033[0m"
    print(f"{orange}{text}{reset}", file=sys.stderr)
    return text

def print_green_text(text: str):
    green = "\033[38;2;99;255;226m"
    reset = "\033[0m"
    print(f"{green}{text}{reset}", file=sys.stderr)
    return text