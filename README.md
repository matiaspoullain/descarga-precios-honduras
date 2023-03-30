# Automatic download, extraction and process SIMPAH PDF files

- [Automatic download, extraction and process SIMPAH PDF files](#automatic-download-extraction-and-process-simpah-pdf-files)
  - [1. Introduction](#1-introduction)
  - [2. Setup](#2-setup)
  - [3. Data description](#3-data-description)
  - [4. How to use](#4-how-to-use)
    - [4.1. Download PDFs](#41-download-pdfs)
    - [4.2. Extract tables from downloaded PDFs](#42-extract-tables-from-downloaded-pdfs)
    - [4.3. Process extracted excel files](#43-process-extracted-excel-files)


## 1. Introduction
This repository allows to automatically download and process PDF files from the Honduras' SIMPAH data.
Last month PDF files are downloaded from **San Pedro Sula** and **Tegucigalpa** regions. Those files contain tables that are then extracted and formatted for delivery.

## 2. Setup
1. Create a new virtual environment: `conda create --name descarga-precios-honduras python=3.9`
2. Activate virtual environment: `conda activate descarga-precios-honduras`
3. Install *camelot* and *tabula*: `pip install camelot-py[cv] tabula-py`
4. Installl *python-tk*: `sudo apt-get install python-tk`
5. Install *ghostscript*: `conda install -c conda-forge ghostscript`
6. Install requirements: `pip install requirements.txt`

## 3. Data description
All files are stored in data[data] in one of these directories:
- /pdfs[data/pdfs]: Raw PDF files are stored here. Subdirectories are created by the Year-Month (last month), region and zone.
- /excels[data/excels]: Raw extraced tables from the PDFs are sotred here. The subdirectories structure is the same as for *data/pdfs*.
- /processed_excels[data/processed_excels]: The raw excels are filtered and formatted. The output tables are stored here with the same subdirectories structures

## 4. How to use
### 4.1. Download PDFs
Running `python -m src.scrap` will download all last month available PDFs from SIMPAH webpage. If a PDF file is already downloaded, it's download will be omitted.
Regions and zones that will be downloaded are specified in src/diccionario_reportes.py[src/diccionario_reportes.py].

### 4.2. Extract tables from downloaded PDFs
Once all PDFs files are downloaded, running `python -m src.pdf_to_excel` will extract tables from the PDF files and store them as .xlsx files in data/excels[data/excels].

### 4.3. Process extracted excel files
Once all tables are extracted from the PDFs, running `python -m src.excel_to_processed_excels` will filter, format and store the tables as .xlsx files in data/processed_excels[data/processed_excels]