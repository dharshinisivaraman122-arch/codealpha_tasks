"""
=============================================================
  Task 2 — Stock Portfolio Tracker
  Tech  : Python 3 + Tkinter (standard library, no installs)
  Author: Dharshini
=============================================================

README
------
A GUI-based stock portfolio tracker that calculates total
investment value based on manually defined (hardcoded) prices.

Demonstrates the following core Python concepts:

  1. Dictionary      — STOCK_PRICES stores symbol → price mapping
  2. Input / Output  — GUI entry widgets + result display area
  3. Basic Arithmetic — quantity × price = investment value
  4. File Handling   — save portfolio report as .txt or .csv

HOW TO RUN
----------
  python stock_tracker.py      (Python 3.8 or newer)

No third-party libraries needed — only the Python standard library.

FEATURES
--------
  • Hardcoded stock price dictionary (easily extendable)
  • Add multiple stocks with name + quantity
  • Live portfolio table showing stock, qty, price, value
  • Running total investment displayed prominently
  • Save report as .txt or .csv file
  • Clear portfolio to start fresh
  • Input validation with helpful error messages
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv
import os


# ─────────────────────────────────────────────────────────────
#  STOCK PRICE DICTIONARY  (Key Concept: dictionary)
#  Format: { "SYMBOL": price_in_USD }
#  Add or change any stock here to extend the tracker.
# ─────────────────────────────────────────────────────────────
STOCK_PRICES = {
    "AAPL":  180.00,   # Apple Inc.
    "TSLA":  250.00,   # Tesla Inc.
    "GOOGL": 140.00,   # Alphabet (Google)
    "MSFT":  415.00,   # Microsoft Corp.
    "AMZN":  185.00,   # Amazon.com Inc.
    "NVDA":  875.00,   # NVIDIA Corp.
    "META":  500.00,   # Meta Platforms
    "NFLX":  620.00,   # Netflix Inc.
    "RELIANCE": 2900.00,  # Reliance Industries (INR)
    "TCS":   3800.00,  # Tata Consultancy Services (INR)
    "INFY":  1500.00,  # Infosys Ltd. (INR)
    "WIPRO":  450.00,  # Wipro Ltd. (INR)
}


# ─────────────────────────────────────────────────────────────
#  HELPER: Calculate investment for one stock entry
#  Key Concept: basic arithmetic (quantity × price)
# ─────────────────────────────────────────────────────────────
def calculate_investment(symbol: str, quantity: int) -> float:
    """Return total value for a given stock symbol and quantity."""
    price = STOCK_PRICES.get(symbol.upper(), 0)
    return price * quantity                          # Basic arithmetic


# ─────────────────────────────────────────────────────────────
#  MAIN APPLICATION CLASS
# ─────────────────────────────────────────────────────────────
class StockTrackerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("780x620")
        self.root.configure(bg="#0f172a")
        self.root.resizable(False, False)

        # Portfolio data: list of dicts {symbol, qty, price, value}
        self.portfolio: list[dict] = []

        self._build_header()
        self._build_input_section()
        self._build_table_section()
        self._build_summary_section()
        self._build_buttons()
        self._build_footer()

    # ── Layout builders ──────────────────────────────────────

    def _build_header(self):
        header = tk.Frame(self.root, bg="#1e293b", height=62)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="📈  STOCK PORTFOLIO TRACKER",
            font=("Helvetica", 18, "bold"),
            bg="#1e293b",
            fg="#f8fafc",
        ).pack(pady=16)

    def _build_input_section(self):
        """Input area: stock symbol dropdown + quantity entry."""
        frame = tk.LabelFrame(
            self.root,
            text="  Add Stock  ",
            font=("Arial", 11, "bold"),
            bg="#0f172a",
            fg="#94a3b8",
            bd=1,
            relief=tk.GROOVE,
        )
        frame.pack(fill=tk.X, padx=16, pady=(12, 6))

        inner = tk.Frame(frame, bg="#0f172a")
        inner.pack(padx=10, pady=10, fill=tk.X)

        # ── Stock symbol dropdown ─────────────────────────────
        tk.Label(inner, text="Stock Symbol:", font=("Arial", 11),
                 bg="#0f172a", fg="#cbd5e1").grid(row=0, column=0, padx=(0, 8), sticky="w")

        self.symbol_var = tk.StringVar(value="AAPL")
        symbol_menu = ttk.Combobox(
            inner,
            textvariable=self.symbol_var,
            values=sorted(STOCK_PRICES.keys()),
            font=("Arial", 12),
            width=12,
            state="readonly",
        )
        symbol_menu.grid(row=0, column=1, padx=(0, 20))
        symbol_menu.bind("<<ComboboxSelected>>", self._update_price_preview)

        # ── Price preview (read-only) ─────────────────────────
        tk.Label(inner, text="Current Price:", font=("Arial", 11),
                 bg="#0f172a", fg="#cbd5e1").grid(row=0, column=2, padx=(0, 8), sticky="w")

        self.price_preview = tk.StringVar(value=f"₹/$ {STOCK_PRICES['AAPL']:,.2f}")
        tk.Label(
            inner,
            textvariable=self.price_preview,
            font=("Arial", 12, "bold"),
            bg="#0f172a",
            fg="#22c55e",
            width=16,
            anchor="w",
        ).grid(row=0, column=3, padx=(0, 20))

        # ── Quantity entry ────────────────────────────────────
        tk.Label(inner, text="Quantity:", font=("Arial", 11),
                 bg="#0f172a", fg="#cbd5e1").grid(row=0, column=4, padx=(0, 8), sticky="w")

        self.qty_var = tk.StringVar()
        qty_entry = tk.Entry(
            inner,
            textvariable=self.qty_var,
            font=("Arial", 12),
            bg="#1e293b",
            fg="#f8fafc",
            insertbackground="white",
            relief=tk.FLAT,
            width=8,
        )
        qty_entry.grid(row=0, column=5, ipady=6, padx=(0, 16))
        qty_entry.bind("<Return>", self._add_stock)

        # ── Add button ────────────────────────────────────────
        tk.Button(
            inner,
            text="＋ Add",
            font=("Arial", 11, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            relief=tk.FLAT,
            cursor="hand2",
            width=8,
            command=self._add_stock,
        ).grid(row=0, column=6)

    def _build_table_section(self):
        """Treeview table to display portfolio rows."""
        frame = tk.Frame(self.root, bg="#0f172a")
        frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=6)

        cols = ("Symbol", "Company / Note", "Qty", "Price", "Total Value")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Portfolio.Treeview",
                         background="#1e293b",
                         foreground="#f8fafc",
                         rowheight=28,
                         fieldbackground="#1e293b",
                         font=("Arial", 11))
        style.configure("Portfolio.Treeview.Heading",
                         background="#334155",
                         foreground="#94a3b8",
                         font=("Arial", 11, "bold"))
        style.map("Portfolio.Treeview", background=[("selected", "#2563eb")])

        self.tree = ttk.Treeview(frame, columns=cols, show="headings",
                                  style="Portfolio.Treeview", height=10)

        # Column widths
        widths = [80, 200, 70, 120, 130]
        anchors = ["center", "w", "center", "e", "e"]
        for col, w, a in zip(cols, widths, anchors):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor=a)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        sb = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)

    def _build_summary_section(self):
        """Shows total portfolio value prominently."""
        frame = tk.Frame(self.root, bg="#1e293b")
        frame.pack(fill=tk.X, padx=16, pady=6)

        tk.Label(frame, text="Total Portfolio Value:",
                 font=("Arial", 13, "bold"), bg="#1e293b", fg="#94a3b8").pack(side=tk.LEFT, padx=14, pady=10)

        self.total_var = tk.StringVar(value="0.00")
        tk.Label(frame, textvariable=self.total_var,
                 font=("Helvetica", 20, "bold"), bg="#1e293b", fg="#22c55e").pack(side=tk.LEFT)

        self.stock_count_var = tk.StringVar(value="(0 holdings)")
        tk.Label(frame, textvariable=self.stock_count_var,
                 font=("Arial", 10), bg="#1e293b", fg="#64748b").pack(side=tk.LEFT, padx=10)

    def _build_buttons(self):
        """Action buttons: Save TXT, Save CSV, Remove selected, Clear all."""
        frame = tk.Frame(self.root, bg="#0f172a")
        frame.pack(fill=tk.X, padx=16, pady=(4, 8))

        buttons = [
            ("💾 Save as TXT",  "#3b82f6", "#2563eb", self._save_txt),
            ("📊 Save as CSV",  "#8b5cf6", "#7c3aed", self._save_csv),
            ("🗑 Remove Selected", "#f59e0b", "#d97706", self._remove_selected),
            ("✖ Clear All",    "#ef4444", "#dc2626", self._clear_all),
        ]

        for text, bg, active, cmd in buttons:
            tk.Button(
                frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=bg,
                fg="white",
                activebackground=active,
                activeforeground="white",
                relief=tk.FLAT,
                cursor="hand2",
                padx=10,
                pady=6,
                command=cmd,
            ).pack(side=tk.LEFT, padx=(0, 8))

    def _build_footer(self):
        tk.Label(
            self.root,
            text="Task 2 — Stock Portfolio Tracker  |  Python & Tkinter  |  Prices are hardcoded for demo purposes",
            font=("Arial", 8),
            bg="#1e293b",
            fg="#475569",
            pady=5,
        ).pack(fill=tk.X, side=tk.BOTTOM)

    # ── Core Logic ───────────────────────────────────────────

    def _update_price_preview(self, event=None):
        """Update price label when symbol changes."""
        sym = self.symbol_var.get().upper()
        price = STOCK_PRICES.get(sym, 0)
        self.price_preview.set(f"₹/$ {price:,.2f}")

    def _add_stock(self, event=None):
        """
        Read symbol + quantity, calculate value, add row to table.
        Key Concepts: dictionary lookup, arithmetic, input/output.
        """
        symbol = self.symbol_var.get().upper().strip()
        qty_text = self.qty_var.get().strip()

        # ── Input validation ──────────────────────────────────
        if not qty_text:
            messagebox.showwarning("Missing Quantity", "Please enter a quantity.")
            return

        if not qty_text.isdigit() or int(qty_text) <= 0:
            messagebox.showerror("Invalid Quantity", "Quantity must be a positive whole number.")
            return

        if symbol not in STOCK_PRICES:
            messagebox.showerror("Unknown Symbol", f"'{symbol}' is not in the stock list.")
            return

        quantity = int(qty_text)                             # Input
        price    = STOCK_PRICES[symbol]                      # Dictionary lookup
        value    = calculate_investment(symbol, quantity)    # Arithmetic

        # Company name labels (a small reference dict for display)
        labels = {
            "AAPL": "Apple Inc.", "TSLA": "Tesla Inc.", "GOOGL": "Alphabet",
            "MSFT": "Microsoft", "AMZN": "Amazon", "NVDA": "NVIDIA",
            "META": "Meta Platforms", "NFLX": "Netflix",
            "RELIANCE": "Reliance Ind.", "TCS": "Tata Consultancy",
            "INFY": "Infosys", "WIPRO": "Wipro",
        }
        label = labels.get(symbol, symbol)

        # Add to internal list
        self.portfolio.append({
            "symbol": symbol, "label": label,
            "qty": quantity, "price": price, "value": value,
        })

        # Add row to table (Output)
        self.tree.insert("", tk.END, values=(
            symbol,
            label,
            quantity,
            f"{price:,.2f}",
            f"{value:,.2f}",
        ))

        self._refresh_total()
        self.qty_var.set("")   # Clear quantity field

    def _refresh_total(self):
        """Recalculate and display total portfolio value."""
        total = sum(row["value"] for row in self.portfolio)   # Arithmetic
        self.total_var.set(f"{total:,.2f}")
        n = len(self.portfolio)
        self.stock_count_var.set(f"({n} holding{'s' if n != 1 else ''})")

    def _remove_selected(self):
        """Remove the highlighted row from the table."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Nothing Selected", "Click a row to select it first.")
            return
        for item in selected:
            idx = self.tree.index(item)
            self.tree.delete(item)
            self.portfolio.pop(idx)
        self._refresh_total()

    def _clear_all(self):
        """Clear the entire portfolio."""
        if not self.portfolio:
            return
        if messagebox.askyesno("Clear Portfolio", "Remove all holdings?"):
            self.tree.delete(*self.tree.get_children())
            self.portfolio.clear()
            self._refresh_total()

    # ── File Handling (Key Concept: file handling) ───────────

    def _save_txt(self):
        """Save portfolio report as a plain .txt file."""
        if not self.portfolio:
            messagebox.showinfo("Nothing to Save", "Add some stocks first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            title="Save Portfolio as TXT",
        )
        if not path:
            return

        total = sum(r["value"] for r in self.portfolio)
        now   = datetime.now().strftime("%d-%m-%Y  %I:%M %p")

        with open(path, "w", encoding="utf-8") as f:        # File handling
            f.write("=" * 52 + "\n")
            f.write("       STOCK PORTFOLIO REPORT\n")
            f.write(f"       Generated: {now}\n")
            f.write("=" * 52 + "\n\n")
            f.write(f"{'Symbol':<10} {'Qty':>6}  {'Price':>12}  {'Value':>14}\n")
            f.write("-" * 48 + "\n")
            for r in self.portfolio:
                f.write(
                    f"{r['symbol']:<10} {r['qty']:>6}  "
                    f"{r['price']:>12,.2f}  {r['value']:>14,.2f}\n"
                )
            f.write("-" * 48 + "\n")
            f.write(f"{'TOTAL':>36}  {total:>14,.2f}\n\n")
            f.write("Prices are hardcoded for demo purposes.\n")

        messagebox.showinfo("Saved", f"Report saved to:\n{os.path.basename(path)}")

    def _save_csv(self):
        """Save portfolio as a .csv file (spreadsheet-compatible)."""
        if not self.portfolio:
            messagebox.showinfo("Nothing to Save", "Add some stocks first.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Save Portfolio as CSV",
        )
        if not path:
            return

        total = sum(r["value"] for r in self.portfolio)

        with open(path, "w", newline="", encoding="utf-8") as f:   # File handling
            writer = csv.writer(f)
            writer.writerow(["Symbol", "Company", "Quantity", "Price", "Total Value"])
            for r in self.portfolio:
                writer.writerow([r["symbol"], r["label"], r["qty"],
                                  f"{r['price']:.2f}", f"{r['value']:.2f}"])
            writer.writerow([])
            writer.writerow(["", "", "", "TOTAL", f"{total:.2f}"])

        messagebox.showinfo("Saved", f"CSV saved to:\n{os.path.basename(path)}")


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    StockTrackerApp(root)
    root.mainloop()
