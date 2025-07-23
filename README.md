# 📦 Shipment Tracker Tool

A smart and automated desktop application to **track shipments**, extract **Bill of Lading (B/L)** numbers from PDFs, retrieve the **Estimated Time of Arrival (ETA)** from shipping websites using Selenium automation, and store the data in an organized **Excel file**.

Built using **Python**, **Tkinter GUI (ttkbootstrap)**, **Selenium**, and **Tesseract OCR**.

---

## 🛠 Features

- ✅ Upload and merge multiple PDF shipment documents.
- 🧠 Extract text using OCR (Optical Character Recognition).
- 🔎 Automatically detect Bill of Lading numbers.
- 🌐 Track shipment status and ETA from supported websites (e.g., MSC).
- 📅 Save container number and ETA to an Excel sheet.
- 🖥️ User-friendly graphical interface.
- 🕵️‍♂️ Supports both text-based and scanned (image) PDFs.

---

## 📁 Project Structure

```
ShipmentTracker/
│
├── main_gui.py              # GUI interface using ttkbootstrap
├── excel_utils.py           # Excel handling (update/save)
├── pdf_utils.py             # PDF merging, text extraction, B/L extraction
├── shipment_tracker.py      # Core logic: site tracking and automation
├── config.py                # Constants for default directories/files
├── requirements.txt         # List of required packages
└── README.md                # Project documentation (you are here)
```

---

## 🚀 How It Works

1. **Upload PDF files**: Click "Upload PDF Files" and select your shipment documents.
2. **Extract B/L Number**: The tool uses OCR to read text and locate the container or Bill of Lading number.
3. **Track Shipment Online**: The system uses Selenium to navigate to the shipping site, enter the tracking number, and extract the ETA.
4. **Store Data**: The container number and ETA are saved into a local Excel file.

---

## 📦 Supported Shipping Companies

- ✅ MSC (`MSDU`, `MEDU`, `MSKU`)
- 🛠️ MAERSK & COSCO: Placeholder ready, logic extendable via strategy pattern.

---

## 📌 Requirements

### Python Packages

Install all dependencies using:

```bash
pip install -r requirements.txt
```

### System Dependencies

- **Tesseract OCR**  
  Download and install: https://github.com/tesseract-ocr/tesseract  
  Make sure to update the `tesseract_cmd` path in `pdf_utils.py`:

  ```python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```

- **Poppler for Windows** (Required for `pdf2image`)  
  Install from: https://github.com/oschwartz10612/poppler-windows  
  Add the `bin` folder to your system PATH.

- **Google Chrome + ChromeDriver**  
  Ensure ChromeDriver version matches your installed Chrome browser version.  
  Download from: https://sites.google.com/a/chromium.org/chromedriver/

---

## 📂 Output Files

- **Merged PDF File**: Saved as `merged_shipment.pdf` inside `PDF_DIR`.
- **Excel File**: Automatically created if it doesn't exist. Default headers:
  - `رقم الحاوية` (Container Number)
  - `تاريخ الوصول` (ETA)

---

## 🖥️ Running the Application

```bash
python main_gui.py
```

Once the app launches:

- Upload your PDF documents
- (Optional) Provide a custom tracking site (currently only MSC is automated)
- Click **Track Shipment**

---

## 🔧 Customization

You can extend the app to support more shipping companies by updating:

- `self.tracking_strategies` inside `AdvancedShipmentTracker`
- Provide appropriate locators and ETA extraction patterns for each new carrier

---

## ✅ Future Improvements

- Add support for more carriers (e.g., MAERSK, COSCO)
- Support Excel column mapping from settings file
- Option to export results in CSV or JSON
- Headless mode for Selenium
- Multi-shipment batch processing

---

## 📄 License

This project is open-source and free to use under the [MIT License](LICENSE).
