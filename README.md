# Fake Data Generator – Pattern-Preserving Anonymisation

This project is a **Python-based fake data generator** that masks sensitive information in a CSV file while keeping the **overall format and structure** of the data.

It is useful for:

- Sharing datasets safely (for demos, interviews, blog posts)
- Creating realistic test data for applications
- Practising data engineering / data privacy concepts

---

## ✨ Features

- Supports masking of the following columns:

  - `email address`
  - `pancard`
  - `Phone Number`
  - `IFSC Code`
  - `credit-card`

- **Pattern-preserving masking**

  - The script learns a simple pattern from each original value  
  - It then generates fake data that *looks similar* (same length / character types)
  - The first **two characters are kept** to mimic the original format  
    (example: `SBIN0001234` → `SBXZ7482913`)

- Email generation:

  - Uses the `name` column to generate realistic local parts
  - Adds optional digits
  - Uses common domains (gmail, yahoo, etc.)

- Works on any CSV with the expected column names

---

## 🛠 Tech Stack

- Python 3
- pandas
- faker
- regex (`re`)
- random / string (standard library)

---

## 📁 Project Structure

```text
fake-data-generator-/
├── fake_data_generator.py   # Core masking logic
├── run_masking.py           # Script to run the masking on a CSV
├── pwc_check_1000.csv       # Example input data (1000 rows of synthetic PII)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
