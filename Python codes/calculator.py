"""
╔══════════════════════════════════════════════════════╗
║         Calculator GUI  —  Python + CustomTkinter    ║
║  Run: python calculator.py                           ║
║  Requires: pip install customtkinter                 ║
╚══════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
import tkinter as tk

# ══════════════════════════════════════════════════════
#  CORE LOGIC  (your original functions — unchanged)
# ══════════════════════════════════════════════════════

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    else:
        return "Division by zero is not allowed"


# ══════════════════════════════════════════════════════
#  THEME
# ══════════════════════════════════════════════════════

BG          = "#0D0D0D"
SURFACE     = "#1A1A1A"
SURFACE2    = "#222222"
ACCENT      = "#00E5FF"       # electric cyan
ACCENT_DIM  = "#008FA3"
NUM_BG      = "#1E1E1E"
NUM_HOV     = "#2A2A2A"
OP_BG       = "#002B33"
OP_HOV      = "#004D5C"
EQ_BG       = "#00E5FF"
EQ_HOV      = "#00B8CC"
EQ_FG       = "#0D0D0D"
CLEAR_BG    = "#2A0A0A"
CLEAR_HOV   = "#4A1010"
CLEAR_FG    = "#FF4D4D"
TEXT_PRI    = "#F0F0F0"
TEXT_SEC    = "#888888"
TEXT_ACC    = "#00E5FF"


# ══════════════════════════════════════════════════════
#  CALCULATOR APP
# ══════════════════════════════════════════════════════

class CalculatorApp:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Calculator")
        self.root.geometry("400x680")
        self.root.resizable(False, False)
        self.root.configure(fg_color=BG)

        # State
        self._expr   = ""          # what's being built
        self._result = None        # last computed result
        self._just_calculated = False
        self._history: list[str] = []
        self._show_history = False

        self._build_ui()
        self._bind_keys()
        self._center()

    # ── UI ───────────────────────────────────────────

    def _build_ui(self):
        self._build_display()
        self._build_history_panel()
        self._build_buttons()

    def _build_display(self):
        disp = ctk.CTkFrame(self.root, fg_color=SURFACE, corner_radius=18)
        disp.pack(fill="x", padx=18, pady=(18, 10))

        # Top row: history toggle + mode label
        top = ctk.CTkFrame(disp, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(12, 0))

        ctk.CTkLabel(
            top, text="CALCULATOR",
            font=ctk.CTkFont(family="Courier", size=10, weight="bold"),
            text_color=TEXT_SEC,
        ).pack(side="left")

        self.btn_hist_toggle = ctk.CTkButton(
            top, text="History ▾", width=75, height=22,
            corner_radius=6,
            font=ctk.CTkFont(size=10),
            fg_color="transparent",
            border_width=1,
            border_color=TEXT_SEC,
            text_color=TEXT_SEC,
            hover_color=SURFACE2,
            command=self._toggle_history,
        )
        self.btn_hist_toggle.pack(side="right")

        # Expression (small, secondary line)
        self.lbl_expr = ctk.CTkLabel(
            disp, text="",
            font=ctk.CTkFont(family="Courier", size=14),
            text_color=TEXT_SEC,
            anchor="e",
        )
        self.lbl_expr.pack(fill="x", padx=20, pady=(8, 0))

        # Main display number
        self.lbl_display = ctk.CTkLabel(
            disp, text="0",
            font=ctk.CTkFont(family="Courier", size=48, weight="bold"),
            text_color=TEXT_PRI,
            anchor="e",
        )
        self.lbl_display.pack(fill="x", padx=20, pady=(0, 16))

    def _build_history_panel(self):
        self.history_frame = ctk.CTkFrame(
            self.root, fg_color=SURFACE2, corner_radius=12,
        )
        # Not packed yet — shown on toggle

        ctk.CTkLabel(
            self.history_frame,
            text="  Recent Calculations",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_ACC,
            anchor="w",
        ).pack(fill="x", padx=12, pady=(10, 4))

        self.history_scroll = ctk.CTkScrollableFrame(
            self.history_frame,
            fg_color="transparent",
            height=110,
        )
        self.history_scroll.pack(fill="x", padx=8, pady=(0, 8))

        self.lbl_no_hist = ctk.CTkLabel(
            self.history_scroll,
            text="No calculations yet.",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_SEC,
        )
        self.lbl_no_hist.pack(pady=10)

    def _build_buttons(self):
        grid = ctk.CTkFrame(self.root, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        # Button layout: text, col, row, colspan, style
        # styles: num | op | eq | clear | fn
        layout = [
            # Row 0 — functions
            ("AC",  0, 0, 1, "clear"),
            ("+/-", 1, 0, 1, "fn"),
            ("%",   2, 0, 1, "fn"),
            ("÷",   3, 0, 1, "op"),
            # Row 1
            ("7",   0, 1, 1, "num"),
            ("8",   1, 1, 1, "num"),
            ("9",   2, 1, 1, "num"),
            ("×",   3, 1, 1, "op"),
            # Row 2
            ("4",   0, 2, 1, "num"),
            ("5",   1, 2, 1, "num"),
            ("6",   2, 2, 1, "num"),
            ("−",   3, 2, 1, "op"),
            # Row 3
            ("1",   0, 3, 1, "num"),
            ("2",   1, 3, 1, "num"),
            ("3",   2, 3, 1, "num"),
            ("+",   3, 3, 1, "op"),
            # Row 4
            ("0",   0, 4, 2, "num"),   # wide zero
            (".",   2, 4, 1, "num"),
            ("=",   3, 4, 1, "eq"),
        ]

        STYLE_MAP = {
            "num":   (NUM_BG,   NUM_HOV,   TEXT_PRI,  ctk.CTkFont(size=20)),
            "op":    (OP_BG,    OP_HOV,    TEXT_ACC,  ctk.CTkFont(size=22, weight="bold")),
            "eq":    (EQ_BG,    EQ_HOV,    EQ_FG,     ctk.CTkFont(size=22, weight="bold")),
            "clear": (CLEAR_BG, CLEAR_HOV, CLEAR_FG,  ctk.CTkFont(size=18, weight="bold")),
            "fn":    (SURFACE2, NUM_HOV,   TEXT_PRI,  ctk.CTkFont(size=18)),
        }

        # Configure grid columns/rows equally
        for c in range(4):
            grid.columnconfigure(c, weight=1, uniform="col")
        for r in range(5):
            grid.rowconfigure(r, weight=1, uniform="row")

        for (txt, col, row, span, style) in layout:
            bg, hov, fg, font = STYLE_MAP[style]
            btn = ctk.CTkButton(
                grid,
                text=txt,
                font=font,
                fg_color=bg,
                hover_color=hov,
                text_color=fg,
                corner_radius=14,
                border_width=0,
                command=lambda t=txt: self._on_button(t),
            )
            btn.grid(
                row=row, column=col,
                columnspan=span,
                padx=5, pady=5,
                sticky="nsew",
            )

    # ── Button Handler ───────────────────────────────

    def _on_button(self, val: str):
        if val == "AC":
            self._clear()
        elif val == "=":
            self._calculate()
        elif val == "+/-":
            self._negate()
        elif val == "%":
            self._percent()
        elif val in ("÷", "×", "−", "+"):
            self._append_operator(val)
        else:
            self._append_digit(val)

    def _append_digit(self, d: str):
        if self._just_calculated:
            self._expr = ""
            self._just_calculated = False

        # Prevent multiple decimal points in the current number
        parts = self._expr.replace("÷", "+").replace("×", "+") \
                          .replace("−", "+").split("+")
        if d == "." and "." in (parts[-1] if parts else ""):
            return

        self._expr += d
        self._update_display(self._expr)

    def _append_operator(self, op: str):
        self._just_calculated = False
        if self._expr and self._expr[-1] in "÷×−+":
            # Replace last operator instead of stacking
            self._expr = self._expr[:-1] + op
        elif self._expr:
            self._expr += op
        self._update_display(self._expr)

    def _calculate(self):
        if not self._expr:
            return

        # Map display symbols to Python operators for eval
        raw = (self._expr
               .replace("÷", "/")
               .replace("×", "*")
               .replace("−", "-"))

        # Parse and call original functions
        result = self._evaluate(raw)

        if result is None:
            return

        entry = f"{self._expr} = {self._fmt(result)}"
        self._history.append(entry)
        self._update_history_panel()

        self._lbl_expr_set(self._expr + " =")
        self._expr = self._fmt(result)
        self._result = result
        self._just_calculated = True
        self._update_display(self._fmt(result))

    def _evaluate(self, expr: str) -> float | str | None:
        """
        Parses a simple a OP b expression and routes to
        the original add / subtract / multiply / divide functions.
        """
        # Try each operator (right to left so we handle negatives safely)
        for op_char, fn in [("/", divide), ("*", multiply),
                             ("-", subtract), ("+", add)]:
            # Find last occurrence so we handle e.g. -3 + -2 correctly
            idx = expr.rfind(op_char)
            # Skip if it's just a leading minus
            if idx <= 0:
                continue
            try:
                a = float(expr[:idx])
                b = float(expr[idx + 1:])
                res = fn(a, b)
                if isinstance(res, str):
                    self._lbl_expr_set("Error")
                    self._update_display("÷ 0 Error")
                    self._expr = ""
                    return None
                return res
            except ValueError:
                continue

        # Single number — just return it
        try:
            return float(expr)
        except ValueError:
            return None

    def _clear(self):
        self._expr = ""
        self._result = None
        self._just_calculated = False
        self._lbl_expr_set("")
        self._update_display("0")

    def _negate(self):
        if not self._expr:
            return
        try:
            val = float(self._expr)
            val = -val
            self._expr = self._fmt(val)
            self._update_display(self._expr)
        except ValueError:
            pass

    def _percent(self):
        if not self._expr:
            return
        try:
            val = float(self._expr)
            val = val / 100
            self._expr = self._fmt(val)
            self._update_display(self._expr)
        except ValueError:
            pass

    # ── Display Helpers ──────────────────────────────

    def _update_display(self, text: str):
        # Shrink font for long numbers
        n = len(str(text))
        size = 48 if n <= 9 else (36 if n <= 13 else 26)
        self.lbl_display.configure(
            text=text if text else "0",
            font=ctk.CTkFont(family="Courier", size=size, weight="bold"),
        )

    def _lbl_expr_set(self, text: str):
        self.lbl_expr.configure(text=text)

    @staticmethod
    def _fmt(val) -> str:
        """Format number: remove .0 for whole numbers."""
        if isinstance(val, float) and val == int(val):
            return str(int(val))
        # Limit to 10 significant figures
        return f"{val:.10g}"

    # ── History Panel ────────────────────────────────

    def _toggle_history(self):
        self._show_history = not self._show_history
        if self._show_history:
            self.history_frame.pack(fill="x", padx=18, pady=(0, 8),
                                     after=self.root.winfo_children()[0])
            self.btn_hist_toggle.configure(text="History ▴")
        else:
            self.history_frame.pack_forget()
            self.btn_hist_toggle.configure(text="History ▾")

    def _update_history_panel(self):
        for w in self.history_scroll.winfo_children():
            w.destroy()

        if not self._history:
            ctk.CTkLabel(
                self.history_scroll, text="No calculations yet.",
                font=ctk.CTkFont(size=11), text_color=TEXT_SEC,
            ).pack(pady=10)
            return

        for entry in reversed(self._history[-10:]):
            ctk.CTkLabel(
                self.history_scroll,
                text=entry,
                font=ctk.CTkFont(family="Courier", size=12),
                text_color=TEXT_PRI,
                anchor="e",
            ).pack(fill="x", padx=4, pady=1)

    # ── Keyboard Support ─────────────────────────────

    def _bind_keys(self):
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, event):
        k = event.keysym
        c = event.char

        if c in "0123456789.":
            self._append_digit(c)
        elif c == "+":
            self._append_operator("+")
        elif c == "-":
            self._append_operator("−")
        elif c == "*":
            self._append_operator("×")
        elif c == "/":
            self._append_operator("÷")
        elif k in ("Return", "KP_Enter", "equal"):
            self._calculate()
        elif k == "BackSpace":
            self._expr = self._expr[:-1]
            self._update_display(self._expr if self._expr else "0")
        elif k == "Escape" or c.lower() == "c":
            self._clear()
        elif c == "%":
            self._percent()

    # ── Launch ───────────────────────────────────────

    def _center(self):
        self.root.update_idletasks()
        w, h = 400, 680
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def run(self):
        self.root.mainloop()


# ══════════════════════════════════════════════════════
#  LAUNCH
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    CalculatorApp().run()
