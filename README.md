# BCFtools Stats Parser & Plotter

A Python toolkit for parsing `bcftools stats` output files (`.vchk`) and generating publication-quality plots for each statistics section.

---

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Data Download](#data-download)
- [Usage](#usage)
  - [Option 1 – Run everything at once (recommended)](#option-1--run-everything-at-once-recommended)
  - [Option 2 – Parse only](#option-2--parse-only)
  - [Option 3 – Plot only](#option-3--plot-only)
- [Flags / Sections](#flags--sections)
- [Output Structure](#output-structure)

---

## Overview

This project provides three scripts:

| Script | Purpose |
|---|---|
| `run_analysis.py` | **Main entry point** – parses a `.vchk` file and generates plots in one step |
| `parse_stats.py` | Parses a `.vchk` file into per-section `.txt` files and prints Summary Numbers to the terminal |
| `make_plots.py` | Reads the parsed `.txt` files and creates plots for each section |

---

## Requirements

- Python 3.8+
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)

Install dependencies with:

```bash
pip install pandas matplotlib
```

---

## Setup

1. Clone or download this repository.
2. Create a `DATA/` folder in the project root (it is excluded from version control):

```bash
mkdir DATA
```

3. Place your `.vchk` data file(s) inside the `DATA/` folder (see [Data Download](#data-download)).

Your project directory should look like this:

```
Python-Project/
├── DATA/
│   └── data1.vchk
├── output/
├── parse_stats.py
├── make_plots.py
└── run_analysis.py
```

---

## Data Download

> **Download the sample data from:** [PLACEHOLDER LINK]

Once downloaded, move the `.vchk` file(s) into the `DATA/` folder:

```bash
# Example
mv ~/Downloads/data1.vchk DATA/
```

---

## Usage

### Option 1 – Run everything at once (recommended)

Use `run_analysis.py` to parse the data **and** generate plots in a single command:

```bash
python run_analysis.py "DATA/data1.vchk" "output" -all
```

This will:
1. Parse `DATA/data1.vchk` and write per-section `.txt` files to the `output/` folder.
2. Generate a `.png` plot for each section inside its own subfolder under `output/`.

To extract and plot only specific sections, replace `-all` with the relevant flags (see [Flags / Sections](#flags--sections)):

```bash
python run_analysis.py "DATA/data1.vchk" "output" -af -dp -qual
```

---

### Option 2 – Parse only

```bash
python parse_stats.py "DATA/data1.vchk" "output" -all
```

Summary Numbers (SN) are always printed to the terminal. Per-section `.txt` files are written to `output/`.

---

### Option 3 – Plot only

If you have already parsed the data, you can regenerate plots without re-parsing:

```bash
python make_plots.py "output" data1 -all
```

The second argument (`data1`) is the base name of your input file (without the `.vchk` extension). It is optional – the script will try to auto-detect it if omitted.

---

## Flags / Sections

Use these flags with any of the three scripts to select which sections to process:

| Flag | Section |
|---|---|
| `-tstv` | Transition / Transversion ratio |
| `-sis` | SNPs in Samples |
| `-af` | Allele Frequency Distribution |
| `-qual` | Quality Score Distribution |
| `-idd` | INDEL Length Distribution |
| `-str` | STR Length Distribution |
| `-dp` | Depth Distribution |
| `-psc` | Per Sample Counts |
| `-psi` | Per Sample Indels |
| `-hwe` | Hardy–Weinberg Equilibrium |
| `-all` | **All** of the above sections |

---

## Output Structure

After running the analysis, the `output/` folder will contain:

```
output/
├── data1_combined.tsv      # All sections in one tab-separated file
├── AF/
│   ├── data1_AF.txt
│   └── data1_AF.png
├── DP/
│   ├── data1_DP.txt
│   └── data1_DP.png
├── QUAL/
│   ├── data1_QUAL.txt
│   └── data1_QUAL.png
└── ...                     # One subfolder per section
```
