# 🧬 DNA → RNA → Protein Analyzer

An interactive bioinformatics web application built with **Python and Streamlit** for exploring DNA sequences through transcription, translation, reading-frame analysis, ORF detection, codon usage, sequence comparison, and GC-content analysis.

The application provides a simple interface where users can paste a DNA sequence or upload a FASTA file and perform multiple sequence-level analyses in one place.

---

## 🔬 Overview

The **DNA → RNA → Protein Analyzer** takes a DNA sequence as input and provides a collection of computational biology analyses.

The application supports both:

- **Coding-strand DNA**
- **Template-strand DNA**

For template-strand input, the sequence is assumed to be provided in the **3′ → 5′ direction**.

The application converts the input into a coding-oriented reference sequence and performs downstream DNA, RNA, protein, ORF, codon, and GC-content analyses.

---

## ✨ Features

### 🧬 1. DNA Sequence Input

The application accepts DNA sequences through:

- Direct sequence input
- FASTA file upload
- `.fasta`
- `.fa`
- `.fna`
- `.txt`

FASTA headers and whitespace are automatically removed before analysis.

The application validates the sequence and accepts the standard DNA bases:

```text
A
T
G
C

Invalid characters are detected and reported before analysis.

📊 2. Sequence Statistics

The application calculates:

DNA sequence length
Adenine (A) count
Thymine (T) count
Guanine (G) count
Cytosine (C) count
GC content
AT content

The statistics are displayed using interactive Streamlit metrics and visualizations.

Example:

DNA Length
GC Content
AT Content
Longest Complete ORF
🔄 3. DNA → RNA Transcription

The application supports transcription from both DNA orientations.

Coding Strand

For coding-strand DNA:

DNA: ATGGCC
RNA: AUGGCC

The transcription is performed by replacing:

T → U
Template Strand

For template-strand DNA, the sequence is assumed to be written:

3′ → 5′

and is converted into RNA written:

5′ → 3′

The application also generates the coding-oriented reference sequence and reverse complement.

🔬 4. Six Reading Frames

The application analyzes all six possible reading frames:

+1
+2
+3
-1
-2
-3

The positive frames are calculated from the coding-oriented sequence.

The negative frames are calculated from its reverse complement.

Each frame provides:

Oriented DNA
RNA codons
Translated protein
Number of complete codons

Users can select a specific frame for detailed protein analysis.

🧪 5. ORF Detection

The application detects open reading frames (ORFs) across all six reading frames.

ORFs are identified using:

Start codon: AUG
Stop codons: UAA, UAG, UGA

The application reports:

Strand
Reading frame
Start position
End position
Nucleotide length
Protein length
Protein sequence
Complete or incomplete status

Both complete and incomplete ORFs are reported.

Complete ORF

A start codon is followed by an in-frame stop codon.

Incomplete ORF

A start codon is detected, but no in-frame stop codon occurs before the sequence ends.

ORF coordinates are reported as 1-based inclusive coordinates relative to the coding-oriented reference DNA sequence.

🧬 6. Protein Translation

The selected reading frame can be translated into a protein sequence.

The application uses the standard nuclear genetic code.

For example:

RNA:
AUG GCC UGA

Protein:
MA

Stop codons are handled during translation, and translation terminates at the first stop codon for the selected protein analysis.

🧪 7. Amino Acid Composition

For the selected protein sequence, the application calculates amino acid composition.

The results include:

One-letter amino acid code
Amino acid name
Count
Percentage

Example:

Code | Amino acid | Count | Percentage

This provides a simple overview of the composition of the translated protein.

🧮 8. Codon Usage Analysis

The application calculates codon usage for the selected reading frame.

For each codon, it reports:

Codon
Amino acid
Count
Frequency (%)

A codon usage visualization is also provided.

Stop codons are included when they occur within the analyzed codon sequence.

🧬 9. DNA Sequence Comparison

The application allows users to compare a reference DNA sequence with a second query sequence.

The comparison can identify:

Substitutions
Insertions
Deletions
Replacement / complex variants

The results include the reference position, reference sequence, and query sequence.

The comparison uses Python's SequenceMatcher.

Important: This is a simple sequence comparison tool and is not a clinical variant caller or a replacement for specialized sequence-alignment or variant-calling software.

📈 10. GC Content Window Analysis

The application calculates GC content across successive sequence windows.

Users can select the window size in base pairs.

The application displays:

Window start
Window end
Window length
GC percentage

A GC-content plot is generated to visualize how GC composition changes across the sequence.

The final window can be shorter than the selected window size.

🧪 11. Built-in Validation Tests

The application includes built-in validation tests for important functions.

The tests cover:

DNA alphabet validation
Empty sequence handling
Reverse-complement calculation
Coding-strand transcription
Template-strand transcription
RNA translation
Stop-codon handling
Incomplete codon handling
GC percentage
AT percentage
Complete ORF detection
Incomplete ORF detection
Substitution detection
Insertion detection
Deletion detection

The application displays:

Total Tests
Passed
Failed

and provides details for each validation test.

These are regression-style checks for selected examples and do not cover every possible biological edge case.

💾 12. Downloadable Results

The application provides downloadable analysis results.

Available downloads include:

📄 TXT Report

Contains:

Input strand
DNA length
GC content
AT content
Base counts
Input DNA
Coding-oriented DNA
Reverse complement
RNA
Selected reading frame
Selected protein
ORF information
📊 CSV Summary

Contains sequence statistics and major analysis results.

🧪 ORF Table

Contains:

Strand
Frame
Start
End
Nucleotide length
Protein length
Complete status
Protein sequence
🧮 Codon Usage

Contains:

Codon
Amino acid
Count
Frequency
🧬 Sequence Differences

When a comparison sequence is provided, sequence differences can also be downloaded as CSV.

🖥️ Application Interface

The application is organized into several analysis sections:

📊 Statistics
🧬 DNA / RNA
🔬 Reading Frames
🧪 ORFs
🧬 Protein
🧮 Codon Usage
🧬 Comparison
📈 GC Windows
🧪 Validation
💾 Downloads

The interface is designed using Streamlit with a clean, interactive layout.

🛠️ Technologies Used
Programming Language
Python
Web Application Framework
Streamlit
Data Visualization
Matplotlib
Python Libraries
streamlit
matplotlib
csv
io
re
collections
difflib

The application uses Python's built-in libraries for sequence processing, counting, comparison, and file generation.

📁 Project Structure
Web-application_DNA-RNA-Protein-Analyzer/
│
├── streamlit_app.py
├── app3.py
├── tests/
│   └── test_bioinformatics.py
├── .gitignore
└── README.md
⚙️ Installation
1. Clone the repository
git clone https://github.com/sudharshini-kannan/Web-application_DNA-RNA-Protein-Analyzer.git
2. Move into the project directory
cd Web-application_DNA-RNA-Protein-Analyzer
3. Install the required Python packages
pip install streamlit matplotlib pytest
▶️ Run the Application

Start the Streamlit application using:

streamlit run streamlit_app.py

Streamlit will provide a local URL, typically:

http://localhost:8501

Open the URL in your web browser.

🧪 Run Tests

The project also contains a test suite under:

tests/

Run the tests with:

pytest

The application additionally contains built-in validation checks that can be run from the 🧪 Validation section after analyzing a sequence.

🧬 Example Input

A simple example sequence:

ATGAAATAA

This sequence contains:

ATG AAA TAA

which represents:

AUG AAA UAA

and produces the amino acid sequence:

MK

The application can identify this as a complete ORF.

🔍 Example Workflow

A typical analysis can be performed as follows:

1. Enter DNA sequence
        ↓
2. Validate DNA sequence
        ↓
3. Calculate sequence statistics
        ↓
4. Generate coding-oriented DNA
        ↓
5. Transcribe DNA → RNA
        ↓
6. Analyze six reading frames
        ↓
7. Detect ORFs
        ↓
8. Translate selected frame
        ↓
9. Analyze amino acid composition
        ↓
10. Analyze codon usage
        ↓
11. Calculate GC content across windows
        ↓
12. Optionally compare another DNA sequence
        ↓
13. Download results
⚠️ Scope and Limitations

This application is designed as an educational and exploratory bioinformatics tool.

It does not replace specialized bioinformatics software for research or clinical analysis.

In particular:

Sequence comparison is a simple computational comparison.
It is not a clinical variant caller.
ORF detection is based on the standard start and stop codons implemented in the application.
Built-in validation tests cover selected examples rather than every biological edge case.
Results should be independently validated when used for research purposes.
For research workflows, results should be compared with trusted bioinformatics tools and appropriate reference sequences.
🚀 Future Development

Possible future improvements include:

Additional sequence analysis tools
More advanced sequence alignment
Additional visualization options
Protein property analysis
Support for larger biological datasets
Integration with external bioinformatics resources
Expanded automated testing
Additional FASTA/sequence-processing functionality
👩‍💻 Author

Sudharshini Kannan

Computational Biology / Bioinformatics