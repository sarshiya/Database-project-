# Opioid Database Project (OpioGeneDB)

##  Overview

**OpioGeneDB** is a web-based application developed to streamline the exploration and interpretation of RNA-seq data from placental cells, particularly in the context of opioid exposure. This tool allows researchers to analyze gene expression patterns, visualize differential expression, and explore metadata filters interactively.

Developed as part of the BF768 Spring 2024 course at Boston University School of Medicine, under the mentorship of **Dr. Huiping Zhang** and course instructor **Dr. Gary Benson**.

---

##  Features

- **Interactive Metadata Search**:
  - Search by `SampleID`
  - Filter data by `Batch`, `OPIOIDCONTROL`, `SEX`, `RACE`, `ETHNICITY`, and `OPIOIDTYPE`
  - Real-time table generation based on filters
  - Reset and help buttons for each filter
  - Client-server interaction via AJAX

- **Gene Expression Analysis**:
  - Differential Gene Expression (DEG) results with DESeq2
  - GSEA visualizations
  - CNA and other genomic insights

- **Designed For**:
  - Researchers studying the effects of opioids on placental gene expression
  - Public health professionals analyzing maternal-fetal outcomes
  - Bioinformatics and data science students learning interactive web data tools

---

## Repository Structure

```
├── Opio_gene.html              # Main interactive frontend page (HTML + JS)
├── metadata.py                # Backend Python script to handle AJAX queries
├── counts.py                  # Python script for gene count data processing
├── Initial_Downstream_Deseq2.R # R script for DESeq2 differential expression analysis
├── LOGO.jpg                   # Project logo
├── README.md                  # You're here 📄
└── instruction.txt            # Original project brief / assignment
```

---

##  How It Works

### Frontend (`Opio_gene.html`)
- Built using HTML5, jQuery, and Google Charts.
- Users interact via form inputs and radio buttons.
- JavaScript sends AJAX requests to the Python backend.

### Backend (`metadata.py`)
- Receives AJAX queries with either:
  - SampleID search
  - Column filters (e.g., SEX, ETHNICITY)
- Responds with JSON-formatted data for table generation.

### Data Processing
- RNA-seq counts and metadata are processed in `counts.py`
- `Initial_Downstream_Deseq2.R` handles downstream differential expression using DESeq2.

## 🔒 Data Availability

Due to the sensitive and confidential nature of the RNA-seq and metadata used in this project, the dataset is **not publicly available** in this repository.

However, the repository **includes all frontend and backend code** required to reproduce the functionality using similar datasets. Interested collaborators with appropriate data access credentials can integrate their data into the provided codebase by:

- Modifying `metadata.py` and `counts.py` to point to your own database or `.csv`/`.tsv` files
- Ensuring DESeq2-compatible count matrices are used with `Initial_Downstream_Deseq2.R`

---

##  Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/opioid-database.git
   cd opioid-database
   ```

2. **Ensure backend setup**:
   - Python 3.x installed
   - Required libraries: `pandas`, `json`, `cgi` (or Flask for extended use)
   - R + DESeq2 installed for running the R script

3. **Run metadata server**:
   (If using CGI)
   - Place in your `cgi-bin/` directory
   - Ensure proper execution permissions (`chmod +x metadata.py`)

4. **Open `Opio_gene.html`** in your browser and interact with the platform

---

## 👩‍🔬 Authors

- Abhiuday Singh Parihar  
- Arshiya Saxena  
- Simran Singh  
- Faculty Advisor: Dr. Huiping Zhang  
- Course: BF768, Boston University School of Medicine (Spring 2024)

---

## 📄 License

MIT License — free to use, distribute, and modify with proper attribution.

---

## 🧠 Acknowledgements

Thanks to the **Boston University Bioinformatics Department**, and our mentors **Dr. Zhang** and **Dr. Benson**, for their invaluable guidance and support.
```
