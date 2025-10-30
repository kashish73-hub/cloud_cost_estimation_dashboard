import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Use seaborn theme
sns.set(style="whitegrid")

class CloudCostDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("☁️Cloud Cost Estimation Dashboard")
        self.root.state("zoomed")  # Full screen
        self.root.configure(bg="#dff6ff")

        # --- Header ---
        header = tk.Label(self.root, text="☁️Cloud Cost Estimation Dashboard☁️",
                          bg="#007acc", fg="white",
                          font=("Segoe UI", 26, "bold"), pady=18)
        header.pack(fill="x")

        # --- Input Frame ---
        form_frame = tk.Frame(self.root, bg="#c7e2ec")
        form_frame.pack(pady=20)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 12, "bold"), padding=8)
        style.map("TButton",
                  background=[("active", "#005f99"), ("!disabled", "#0088cc")],
                  foreground=[("active", "white")])

        tk.Label(form_frame, text="Enter VM Count:", bg="#dff6ff", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, padx=15, pady=10, sticky="e")
        self.vm_entry = tk.Entry(form_frame, font=("Segoe UI", 14), width=12, relief="solid", borderwidth=1)
        self.vm_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Hours Used:", bg="#dff6ff", font=("Segoe UI", 14, "bold")).grid(row=1, column=0, padx=15, pady=10, sticky="e")
        self.hours_entry = tk.Entry(form_frame, font=("Segoe UI", 14), width=12, relief="solid", borderwidth=1)
        self.hours_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Rate per Hour (₹):", bg="#dff6ff", font=("Segoe UI", 14, "bold")).grid(row=2, column=0, padx=15, pady=10, sticky="e")
        self.rate_entry = tk.Entry(form_frame, font=("Segoe UI", 14), width=12, relief="solid", borderwidth=1)
        self.rate_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        ttk.Button(form_frame, text="💰 Calculate", command=self.calculate_cost).grid(row=3, column=0, padx=15, pady=15)
        ttk.Button(form_frame, text="📊 Show Graph", command=self.show_graph).grid(row=3, column=1, padx=15, pady=15)
        ttk.Button(form_frame, text="🧹 Clear", command=self.clear_all).grid(row=3, column=2, padx=15, pady=15)

        # --- Output Frame ---
        output_frame = tk.LabelFrame(self.root, text="Cost Summary", font=("Segoe UI", 14, "bold"),
                                     bg="#f2f9ff", fg="#005f99", padx=10, pady=10)
        output_frame.pack(padx=20, pady=15, fill="x")

        self.output_text = tk.Text(output_frame, height=7, font=("Consolas", 12), wrap="word",
                                   bg="#ffffff", relief="solid", borderwidth=1)
        self.output_text.pack(fill="x", padx=10, pady=10)

        # --- Table Frame ---
        table_frame = tk.LabelFrame(self.root, text="Recent Cost Records", font=("Segoe UI", 14, "bold"),
                                    bg="#f2f9ff", fg="#005f99")
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ("vm", "hours", "rate", "cost")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col.upper(), anchor="center")
            self.tree.column(col, width=200, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # --- Stats Frame ---
        self.stats_label = tk.Label(self.root, text="", bg="#b8c5ca", font=("Segoe UI", 14, "bold"), fg="#004466")
        self.stats_label.pack(pady=10)

        self.records = []

    def calculate_cost(self):
        try:
            vms = int(self.vm_entry.get())
            hours = float(self.hours_entry.get())
            rate = float(self.rate_entry.get())

            cost = np.round(vms * hours * rate, 2)
            monthly = np.round(cost * 30, 2)

            self.output_text.insert(tk.END, f"\n➡️ {vms} VMs × {hours} hrs × ₹{rate}/hr = ₹{cost}\n")
            self.output_text.insert(tk.END, f"📅 Estimated Monthly Cost: ₹{monthly}\n{'-'*70}\n")

            record = {"VMs": vms, "Hours": hours, "Rate": rate, "Cost": cost}
            self.records.append(record)
            self.tree.insert("", "end", values=(vms, hours, rate, cost))

            self.update_stats()

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values!")

    def update_stats(self):
        if not self.records:
            self.stats_label.config(text="")
            return

        costs = np.array([r["Cost"] for r in self.records])
        avg_cost = np.mean(costs)
        max_cost = np.max(costs)
        min_cost = np.min(costs)

        self.stats_label.config(text=f"📊 Avg: ₹{avg_cost:.2f}   |   🔼 Max: ₹{max_cost:.2f}   |   🔽 Min: ₹{min_cost:.2f}")

    def show_graph(self):
        if not self.records:
            messagebox.showwarning("No Data", "No records to display!")
            return

        vms = np.array([r["VMs"] for r in self.records])
        cost = np.array([r["Cost"] for r in self.records])

        plt.figure(figsize=(10, 6))
        plt.title("Cloud Cost Analysis Trend", fontsize=16, fontweight="bold", color="#004466")
        sns.barplot(x=vms, y=cost, palette="coolwarm", alpha=0.8)
        sns.lineplot(x=vms, y=cost, marker="o", color="black", label="Cost Line")
        plt.xlabel("Number of VMs", fontsize=12)
        plt.ylabel("Total Cost (₹)", fontsize=12)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def clear_all(self):
        self.vm_entry.delete(0, tk.END)
        self.hours_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.output_text.delete("1.0", tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.stats_label.config(text="")
        self.records.clear()


# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CloudCostDashboard(root)
    root.mainloop()
