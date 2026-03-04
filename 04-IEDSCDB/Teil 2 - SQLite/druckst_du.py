import sys

try:
    # Windows
    import msvcrt

    def wait_for_keypress():
        """
        Windows: Wartet auf einen beliebigen Tastendruck (ohne Enter).
        """
        print("Drücke eine beliebige Taste, um fortzufahren …")
        msvcrt.getch()

except ImportError:
    # Unix/Linux/macOS
    import tty
    import termios

    def wait_for_keypress():
        """
        Unix: Wartet auf einen beliebigen Tastendruck (ohne Enter).
        """
        print("Drücke eine beliebige Taste, um fortzufahren …")
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            # Setzt das Terminal in den „rohen“ Modus
            tty.setraw(fd)
            # Liest genau ein Zeichen
            sys.stdin.read(1)
        finally:
            # Stellt den ursprünglichen Terminal-Zustand wieder her
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)