import os
import threading
from tkinter import filedialog, messagebox
from config import EXCEL_FILE, PDF_DIR
from pdf_utils import merge_pdfs, extract_text_from_pdf, extract_bill_of_lading
from excel_utils import update_excel
from trackers.tracker_core import AdvancedShipmentTracker
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class ShipmentTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shipment Tracker")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.pdf_directory = PDF_DIR
        self.excel_file = EXCEL_FILE
        if not os.path.exists(self.pdf_directory):
            os.makedirs(self.pdf_directory)
        if not os.path.exists(self.excel_file):
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(["رقم الحاوية", "تاريخ الوصول"])
            wb.save(self.excel_file)
        self.tracker = AdvancedShipmentTracker()
        self.pdf_files = []
        self.create_widgets()

    def create_widgets(self):
        frame = tb.Frame(self.root, padding=30)
        frame.pack(fill=BOTH, expand=True)

        tb.Label(frame, text="Shipment Tracking System", font=("Arial", 22, "bold")).pack(pady=(0, 25))

        site_frame = tb.Frame(frame)
        site_frame.pack(pady=10, fill=X)
        tb.Label(site_frame, text="Tracking Website:", font=("Arial", 12)).pack(side=LEFT, padx=(0, 10))
        self.site_entry = tb.Entry(site_frame, width=50, font=("Arial", 12))
        self.site_entry.pack(side=LEFT, fill=X, expand=True)
        self.site_entry.insert(0, "")

        self.upload_button = tb.Button(frame, text="Upload PDF Files", bootstyle=PRIMARY, command=self.upload_pdf, width=25)
        self.upload_button.pack(pady=15)

        self.status_label = tb.Label(frame, text="", font=("Arial", 11), bootstyle=INFO)
        self.status_label.pack(pady=5)

        self.search_button = tb.Button(frame, text="Track Shipment", bootstyle=SUCCESS, command=self.search_shipment, width=25)
        self.search_button.pack(pady=20)

        self.result_label = tb.Label(frame, text="", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=10)

    def upload_pdf(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if file_paths:
            self.pdf_files = list(file_paths)
            self.status_label.config(text=f"{len(self.pdf_files)} PDF files uploaded.", bootstyle=SUCCESS)
            print("PDF files uploaded successfully.")

    def search_shipment(self):
        thread = threading.Thread(target=self._search_shipment_worker)
        thread.start()

    def _search_shipment_worker(self):
        tracking_site = self.site_entry.get().strip()
        if not tracking_site:
            self.root.after(0, lambda: messagebox.showerror("Error", "Please enter the tracking website!"))
            self.root.after(0, lambda: self.status_label.config(text="Tracking website is required.", bootstyle=DANGER))
            return

        if not self.pdf_files:
            self.root.after(0, lambda: messagebox.showerror("Error", "Please upload PDF files first!"))
            self.root.after(0, lambda: self.status_label.config(text="No PDF files uploaded.", bootstyle=DANGER))
            return

        self.root.after(0, lambda: self.status_label.config(text="Processing...", bootstyle=INFO))
        self.root.after(0, lambda: self.result_label.config(text=""))

        merged_pdf_path = os.path.join(self.pdf_directory, "merged_shipment.pdf")
        merge_pdfs(self.pdf_files, merged_pdf_path)

        text = extract_text_from_pdf(merged_pdf_path)
        if not text.strip():
            self.root.after(0, lambda: messagebox.showerror("Error", "No text extracted from PDF files!"))
            self.root.after(0, lambda: self.status_label.config(text="No text extracted from PDF files.", bootstyle=DANGER))
            return

        bl_number = extract_bill_of_lading(text)
        if bl_number:
            print(f"Bill of Lading number: {bl_number}")
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", "Bill of Lading number not found in PDF files!"))
            self.root.after(0, lambda: self.status_label.config(text="Bill of Lading number not found.", bootstyle=DANGER))
            return

        self.root.after(0, lambda: self.status_label.config(text="Tracking shipment online...", bootstyle=INFO))
        eta = self.tracker.track_shipment(bl_number)
        if eta:
            print(f"ETA found: {eta}")
            update_excel(self.excel_file, bl_number, eta)
            self.root.after(0, lambda: self.result_label.config(text=f"ETA: {eta}", bootstyle=SUCCESS))
            self.root.after(0, lambda: self.status_label.config(text="Shipment tracked and saved.", bootstyle=SUCCESS))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"ETA found: {eta}"))
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", "Shipment not found on website!"))
            self.root.after(0, lambda: self.status_label.config(text="Shipment not found on website.", bootstyle=DANGER))



def main():
    root = tb.Window(themename="superhero")
    app = ShipmentTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()