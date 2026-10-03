import streamlit as st
import matplotlib.pyplot as plt
import csv
import io
from collections import Counter
from difflib import SequenceMatcher


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DNA → RNA → Protein Analyzer",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# COLOR PALETTE
# ============================================================

BG = "#0E1119"
SURFACE = "#161B27"
SURFACE_2 = "#1D2330"
YELLOW = "#E9CC5A"
VIOLET = "#C1BBE9"
BLUE = "#78A3D7"
CINNAMON = "#BA7462"
BORDER = "#4C5261"
TEXT = "#FFFFFF"
MUTED = "#AEB3C0"
GREEN = "#72C79A"


# ============================================================
# GLOBAL THEME
# ============================================================

st.markdown(
    f"""
<style>

.stApp {{
    background: {BG};
}}

.main .block-container {{
    max-width: 1400px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}}

/* ---------------------------------------------------------
   GENERAL TEXT
--------------------------------------------------------- */

p, label, span {{
    color: {TEXT};
}}

[data-testid="stCaptionContainer"] {{
    color: {MUTED} !important;
}}

h1 {{
    color: {TEXT} !important;
    font-size: 34px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}}

h2 {{
    color: {YELLOW} !important;
    font-weight: 750 !important;
}}

h3 {{
    color: {VIOLET} !important;
    font-weight: 700 !important;
}}

/* ---------------------------------------------------------
   HEADER
--------------------------------------------------------- */

.hero {{
    background:
        linear-gradient(
            135deg,
            rgba(233,204,90,0.10),
            rgba(193,187,233,0.08),
            rgba(120,163,215,0.08)
        );
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 30px 34px;
    margin-bottom: 24px;
}}

.hero-title {{
    font-size: 36px;
    font-weight: 800;
    color: {TEXT};
    margin-bottom: 8px;
}}

.hero-title span {{
    color: {YELLOW};
}}

.hero-description {{
    color: {MUTED};
    font-size: 16px;
    line-height: 1.6;
    max-width: 900px;
}}

.badge-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 18px;
}}

.badge {{
    border: 1px solid {BORDER};
    background: {SURFACE};
    border-radius: 999px;
    padding: 6px 13px;
    color: {TEXT};
    font-size: 13px;
    font-weight: 600;
}}

.badge.yellow {{
    border-color: {YELLOW};
    color: {YELLOW};
}}

.badge.violet {{
    border-color: {VIOLET};
    color: {VIOLET};
}}

.badge.blue {{
    border-color: {BLUE};
    color: {BLUE};
}}

/* ---------------------------------------------------------
   METRIC CARDS
--------------------------------------------------------- */

[data-testid="stMetric"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 16px;
}}

[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
}}

[data-testid="stMetricValue"] {{
    color: {YELLOW} !important;
}}

[data-testid="stMetricDelta"] {{
    color: {BLUE} !important;
}}

/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */

.stButton > button {{
    background: {YELLOW} !important;
    color: #111111 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 750 !important;
    min-height: 42px;
}}

.stButton > button:hover {{
    background: {VIOLET} !important;
    color: #111111 !important;
}}

.stDownloadButton > button {{
    background: {SURFACE_2} !important;
    color: {YELLOW} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
}}

.stDownloadButton > button:hover {{
    border-color: {YELLOW} !important;
    color: {YELLOW} !important;
}}

/* ---------------------------------------------------------
   INPUTS
--------------------------------------------------------- */

[data-testid="stTextArea"] textarea {{
    background: {SURFACE} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}

[data-testid="stTextArea"] textarea:focus {{
    border-color: {YELLOW} !important;
}}

[data-baseweb="select"] > div {{
    background: {SURFACE} !important;
    border-color: {BORDER} !important;
    color: {TEXT} !important;
}}

[data-baseweb="select"] * {{
    color: {TEXT} !important;
}}

[data-testid="stNumberInput"] input {{
    background: {SURFACE} !important;
    color: {TEXT} !important;
    border-color: {BORDER} !important;
}}

[data-testid="stFileUploader"] {{
    background: {SURFACE} !important;
    border: 1px dashed {BORDER} !important;
    border-radius: 12px !important;
}}

[data-testid="stRadio"] label {{
    color: {TEXT} !important;
}}

/* ---------------------------------------------------------
   TABS
--------------------------------------------------------- */

button[data-baseweb="tab"] {{
    color: {MUTED} !important;
    font-weight: 600 !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: {YELLOW} !important;
    font-weight: 750 !important;
}}

/* ---------------------------------------------------------
   EXPANDERS
--------------------------------------------------------- */

[data-testid="stExpander"] {{
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}

[data-testid="stExpander"] summary {{
    color: {TEXT} !important;
}}

/* ---------------------------------------------------------
   CODE
--------------------------------------------------------- */

[data-testid="stCode"] {{
    background: #0A0D13 !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
}}

/* ---------------------------------------------------------
   DATAFRAME
--------------------------------------------------------- */

[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

/* ---------------------------------------------------------
   ALERTS
--------------------------------------------------------- */

[data-testid="stAlert"] {{
    border-radius: 10px;
}}

/* ---------------------------------------------------------
   DIVIDERS
--------------------------------------------------------- */

hr {{
    border-color: {BORDER} !important;
}}

/* ---------------------------------------------------------
   CUSTOM CARDS
--------------------------------------------------------- */

.info-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px;
    height: 100%;
}}

.info-card-title {{
    color: {VIOLET};
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 8px;
}}

.info-card-value {{
    color: {TEXT};
    font-size: 22px;
    font-weight: 800;
}}

.info-card-small {{
    color: {MUTED};
    font-size: 13px;
    margin-top: 5px;
}}

.sequence-box {{
    background: #0A0D13;
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 16px;
    font-family: monospace;
    line-height: 2;
    overflow-x: auto;
}}

.codon-box {{
    display: inline-block;
    min-width: 58px;
    text-align: center;
    padding: 7px 5px;
    margin: 3px;
    border: 1px solid {BORDER};
    border-radius: 8px;
    background: {SURFACE_2};
    color: {TEXT};
    font-family: monospace;
    font-weight: 700;
}}

.codon-start {{
    border-color: {YELLOW};
    color: {YELLOW};
}}

.codon-stop {{
    border-color: {CINNAMON};
    color: {CINNAMON};
}}

.frame-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}}

.frame-title {{
    color: {YELLOW};
    font-size: 20px;
    font-weight: 800;
}}

.frame-subtitle {{
    color: {MUTED};
    font-size: 13px;
}}

.orf-complete {{
    color: {GREEN};
    font-weight: 750;
}}

.orf-incomplete {{
    color: {CINNAMON};
    font-weight: 750;
}}

.footer {{
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid {BORDER};
    color: {MUTED};
    text-align: center;
    font-size: 13px;
}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# GENETIC CODE
# ============================================================

CODON_TABLE = {
    "UUU": "F", "UUC": "F", "UUA": "L", "UUG": "L",
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "UAU": "Y", "UAC": "Y", "UAA": "*", "UAG": "*",
    "UGU": "C", "UGC": "C", "UGA": "*", "UGG": "W",

    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "CAU": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",

    "AUU": "I", "AUC": "I", "AUA": "I", "AUG": "M",
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "AAU": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "AGU": "S", "AGC": "S", "AGA": "R", "AGG": "R",

    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "GAU": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
}


AA_NAMES = {
    "A": "Alanine",
    "R": "Arginine",
    "N": "Asparagine",
    "D": "Aspartic acid",
    "C": "Cysteine",
    "E": "Glutamic acid",
    "Q": "Glutamine",
    "G": "Glycine",
    "H": "Histidine",
    "I": "Isoleucine",
    "L": "Leucine",
    "K": "Lysine",
    "M": "Methionine",
    "F": "Phenylalanine",
    "P": "Proline",
    "S": "Serine",
    "T": "Threonine",
    "W": "Tryptophan",
    "Y": "Tyrosine",
    "V": "Valine"
}


AA_THREE_LETTER = {
    "A": "Ala",
    "R": "Arg",
    "N": "Asn",
    "D": "Asp",
    "C": "Cys",
    "E": "Glu",
    "Q": "Gln",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "L": "Leu",
    "K": "Lys",
    "M": "Met",
    "F": "Phe",
    "P": "Pro",
    "S": "Ser",
    "T": "Thr",
    "W": "Trp",
    "Y": "Tyr",
    "V": "Val"
}


# Average residue molecular masses in Da
AA_MASSES = {
    "A": 89.09,
    "R": 174.20,
    "N": 132.12,
    "D": 133.10,
    "C": 121.16,
    "E": 147.13,
    "Q": 146.15,
    "G": 75.07,
    "H": 155.16,
    "I": 131.17,
    "L": 131.17,
    "K": 146.19,
    "M": 149.21,
    "F": 165.19,
    "P": 115.13,
    "S": 105.09,
    "T": 119.12,
    "W": 204.23,
    "Y": 181.19,
    "V": 117.15
}


HYDROPHOBIC = set("AVILMFWY")
POLAR = set("STNQCG")
POSITIVELY_CHARGED = set("KRH")
NEGATIVELY_CHARGED = set("DE")


STOP_CODONS = {"UAA", "UAG", "UGA"}
START_CODON = "AUG"


# ============================================================
# SEQUENCE FUNCTIONS
# ============================================================

def clean_sequence(sequence):
    """Remove whitespace and FASTA header lines."""

    lines = []

    for line in sequence.splitlines():
        line = line.strip()

        if line and not line.startswith(">"):
            lines.append(line)

    return "".join(lines).upper()


def validate_dna(sequence):
    """Return an error message or None."""

    if not sequence:
        return "The sequence is empty."

    invalid = sorted(set(sequence) - set("ATGC"))

    if invalid:
        return "Invalid characters: " + ", ".join(invalid)

    return None


def reverse_complement(sequence):
    return sequence.translate(
        str.maketrans("ATGC", "TACG")
    )[::-1]


def transcribe_coding(sequence):
    return sequence.replace("T", "U")


def transcribe_template(sequence):
    mapping = {
        "A": "U",
        "T": "A",
        "G": "C",
        "C": "G"
    }

    return "".join(
        mapping[base]
        for base in sequence
    )


# ============================================================
# TRANSLATION
# ============================================================

def translate_rna(
    rna,
    offset=0,
    stop_at_stop=False
):
    protein = []

    for i in range(
        offset,
        len(rna) - 2,
        3
    ):

        codon = rna[i:i + 3]
        amino_acid = CODON_TABLE.get(codon)

        if amino_acid is None:
            continue

        if amino_acid == "*":

            if not stop_at_stop:
                protein.append("*")

            break

        protein.append(amino_acid)

    return "".join(protein)


def codons_in_frame(
    rna,
    offset=0
):
    return [
        rna[i:i + 3]
        for i in range(
            offset,
            len(rna) - 2,
            3
        )
    ]


# ============================================================
# SIX READING FRAMES
# ============================================================

def get_six_frames(coding_dna):

    forward_rna = transcribe_coding(
        coding_dna
    )

    reverse_dna = reverse_complement(
        coding_dna
    )

    reverse_rna = transcribe_coding(
        reverse_dna
    )

    frames = {}

    for offset in range(3):

        plus_label = f"+{offset + 1}"
        minus_label = f"-{offset + 1}"

        plus_codons = codons_in_frame(
            forward_rna,
            offset
        )

        minus_codons = codons_in_frame(
            reverse_rna,
            offset
        )

        frames[plus_label] = {
            "strand": "+",
            "offset": offset,
            "dna": coding_dna[offset:],
            "rna": forward_rna[offset:],
            "codons": plus_codons,
            "protein": translate_rna(
                forward_rna,
                offset
            ),
            "oriented_rna": forward_rna
        }

        frames[minus_label] = {
            "strand": "-",
            "offset": offset,
            "dna": reverse_dna[offset:],
            "rna": reverse_rna[offset:],
            "codons": minus_codons,
            "protein": translate_rna(
                reverse_rna,
                offset
            ),
            "oriented_rna": reverse_rna
        }

    return frames


# ============================================================
# ORF DETECTION
# ============================================================

def find_orfs_in_rna(
    rna,
    strand,
    coding_reference_length
):

    results = []

    for offset in range(3):

        codons = codons_in_frame(
            rna,
            offset
        )

        for codon_index, codon in enumerate(codons):

            if codon != START_CODON:
                continue

            start_index = (
                offset
                + codon_index * 3
            )

            stop_end_index = None
            protein = []
            stop_found = False

            for j in range(
                start_index,
                len(rna) - 2,
                3
            ):

                current = rna[j:j + 3]

                if current in STOP_CODONS:
                    stop_end_index = j + 3
                    stop_found = True
                    break

                amino_acid = CODON_TABLE.get(
                    current
                )

                if amino_acid:
                    protein.append(
                        amino_acid
                    )

            if stop_found:

                oriented_end_exclusive = (
                    stop_end_index
                )

            else:

                oriented_end_exclusive = (
                    start_index
                    + len(protein) * 3
                )

            if oriented_end_exclusive <= start_index:
                continue

            if strand == "+":

                genomic_start = (
                    start_index + 1
                )

                genomic_end = (
                    oriented_end_exclusive
                )

            else:

                genomic_start = (
                    coding_reference_length
                    - oriented_end_exclusive
                    + 1
                )

                genomic_end = (
                    coding_reference_length
                    - start_index
                )

            results.append({
                "strand": strand,
                "frame": (
                    f"{strand}{offset + 1}"
                ),
                "start": genomic_start,
                "end": genomic_end,
                "oriented_start": (
                    start_index + 1
                ),
                "oriented_end": (
                    oriented_end_exclusive
                ),
                "length_nt": (
                    oriented_end_exclusive
                    - start_index
                ),
                "length_aa": len(protein),
                "protein": "".join(protein),
                "complete": stop_found
            })

    return results


def find_all_orfs(coding_dna):

    forward_rna = transcribe_coding(
        coding_dna
    )

    reverse_rna = transcribe_coding(
        reverse_complement(coding_dna)
    )

    orfs = (
        find_orfs_in_rna(
            forward_rna,
            "+",
            len(coding_dna)
        )
        +
        find_orfs_in_rna(
            reverse_rna,
            "-",
            len(coding_dna)
        )
    )

    return sorted(
        orfs,
        key=lambda x: (
            x["start"],
            x["end"],
            x["strand"]
        )
    )


# ============================================================
# STATISTICS
# ============================================================

def get_statistics(dna):

    counts = Counter(dna)
    length = len(dna)

    gc = (
        100
        * (
            counts["G"]
            + counts["C"]
        )
        / length
        if length
        else 0
    )

    at = (
        100
        * (
            counts["A"]
            + counts["T"]
        )
        / length
        if length
        else 0
    )

    return {
        "length": length,
        "A": counts["A"],
        "T": counts["T"],
        "G": counts["G"],
        "C": counts["C"],
        "GC": gc,
        "AT": at
    }


def gc_windows(
    dna,
    window_size
):

    results = []

    for start in range(
        0,
        len(dna),
        window_size
    ):

        window = dna[
            start:start + window_size
        ]

        if not window:
            continue

        gc = (
            100
            * (
                window.count("G")
                + window.count("C")
            )
            / len(window)
        )

        results.append({
            "start": start + 1,
            "end": start + len(window),
            "length": len(window),
            "gc": gc
        })

    return results


# ============================================================
# CODON USAGE
# ============================================================

def get_codon_usage(
    rna,
    offset
):

    codons = codons_in_frame(
        rna,
        offset
    )

    counts = Counter(codons)
    total = len(codons)

    rows = []

    for codon, count in sorted(
        counts.items()
    ):

        rows.append({
            "Codon": codon,
            "Amino acid": (
                "Stop"
                if CODON_TABLE[codon] == "*"
                else AA_NAMES[
                    CODON_TABLE[codon]
                ]
            ),
            "Count": count,
            "Frequency (%)": (
                round(
                    count / total * 100,
                    2
                )
                if total
                else 0
            )
        })

    return rows


# ============================================================
# SEQUENCE COMPARISON
# ============================================================

def compare_sequences(
    reference,
    query
):

    matcher = SequenceMatcher(
        None,
        reference,
        query,
        autojunk=False
    )

    differences = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":
            continue

        if tag == "replace":

            ref_part = reference[i1:i2]
            query_part = query[j1:j2]

            if len(ref_part) == len(query_part):

                for k, (
                    ref_base,
                    query_base
                ) in enumerate(
                    zip(
                        ref_part,
                        query_part
                    )
                ):

                    differences.append({
                        "Type": "Substitution",
                        "Reference position": (
                            i1 + k + 1
                        ),
                        "Reference": ref_base,
                        "Query": query_base
                    })

            else:

                differences.append({
                    "Type": (
                        "Replacement / complex variant"
                    ),
                    "Reference position": (
                        f"{i1 + 1}-{i2}"
                    ),
                    "Reference": (
                        ref_part or "-"
                    ),
                    "Query": (
                        query_part or "-"
                    )
                })

        elif tag == "delete":

            differences.append({
                "Type": "Deletion",
                "Reference position": (
                    f"{i1 + 1}-{i2}"
                ),
                "Reference": reference[i1:i2],
                "Query": "-"
            })

        elif tag == "insert":

            differences.append({
                "Type": "Insertion",
                "Reference position": (
                    f"after {i1}"
                ),
                "Reference": "-",
                "Query": query[j1:j2]
            })

    return differences


# ============================================================
# PROTEIN ANALYSIS
# ============================================================

def protein_molecular_weight(protein):

    if not protein:
        return 0

    total = sum(
        AA_MASSES.get(aa, 0)
        for aa in protein
    )

    # Add one water molecule for the complete peptide
    return total + 18.015


def protein_classes(protein):

    counts = {
        "Hydrophobic": 0,
        "Polar": 0,
        "Positively charged": 0,
        "Negatively charged": 0,
        "Other": 0
    }

    for aa in protein:

        if aa in HYDROPHOBIC:
            counts["Hydrophobic"] += 1

        elif aa in POLAR:
            counts["Polar"] += 1

        elif aa in POSITIVELY_CHARGED:
            counts["Positively charged"] += 1

        elif aa in NEGATIVELY_CHARGED:
            counts["Negatively charged"] += 1

        else:
            counts["Other"] += 1

    return counts


def get_protein_composition(protein):

    counts = Counter(protein)
    total = len(protein)

    rows = []

    for aa, count in sorted(
        counts.items()
    ):

        rows.append({
            "Code": aa,
            "3-letter": AA_THREE_LETTER.get(
                aa,
                ""
            ),
            "Amino acid": AA_NAMES.get(
                aa,
                aa
            ),
            "Count": count,
            "Percentage": round(
                count / total * 100,
                2
            )
        })

    return rows


# ============================================================
# VALIDATION TESTS
# ============================================================

def run_validation_tests():

    tests = []

    def check(
        name,
        condition,
        details
    ):

        tests.append({
            "Test": name,
            "Result": (
                "PASS"
                if condition
                else "FAIL"
            ),
            "Details": details
        })

    check(
        "Valid DNA accepted",
        validate_dna("ATGC") is None,
        "ATGC contains only valid DNA bases."
    )

    check(
        "Invalid DNA rejected",
        validate_dna("ATGX") is not None,
        "Sequences containing X must be rejected."
    )

    check(
        "Empty DNA rejected",
        validate_dna("") is not None,
        "An empty sequence must not be analyzed."
    )

    check(
        "Reverse complement",
        reverse_complement("ATGC") == "GCAT",
        "Reverse complement of ATGC is GCAT."
    )

    check(
        "Coding transcription",
        transcribe_coding("ATGGCC") == "AUGGCC",
        "Coding DNA is transcribed by replacing T with U."
    )

    check(
        "Template transcription",
        transcribe_template("TACCGG") == "AUGGCC",
        "Template TACCGG produces AUGGCC."
    )

    check(
        "Known translation",
        translate_rna(
            "AUGGCCUGA",
            0,
            True
        ) == "MA",
        "AUG GCC UGA translates to MA."
    )

    check(
        "Stop codon handling",
        translate_rna(
            "AUGUAA",
            0,
            True
        ) == "M",
        "Translation terminates at UAA."
    )

    check(
        "Incomplete codon ignored",
        translate_rna(
            "AUGGC",
            0
        ) == "M",
        "Final incomplete codon is ignored."
    )

    stats = get_statistics("ATGC")

    check(
        "GC percentage",
        abs(stats["GC"] - 50.0) < 0.001,
        "ATGC has 50% GC content."
    )

    check(
        "AT percentage",
        abs(stats["AT"] - 50.0) < 0.001,
        "ATGC has 50% AT content."
    )

    orfs = find_all_orfs(
        "ATGAAATAA"
    )

    complete = [
        orf
        for orf in orfs
        if orf["strand"] == "+"
        and orf["frame"] == "+1"
        and orf["complete"]
    ]

    check(
        "Complete ORF detected",
        any(
            orf["protein"] == "MK"
            and orf["length_nt"] == 9
            for orf in complete
        ),
        "ATG AAA TAA should produce a complete ORF."
    )

    incomplete_orfs = find_all_orfs(
        "ATGAAA"
    )

    check(
        "Incomplete ORF reported",
        any(
            orf["strand"] == "+"
            and orf["frame"] == "+1"
            and not orf["complete"]
            for orf in incomplete_orfs
        ),
        "ATG AAA has no in-frame stop codon."
    )

    variants = compare_sequences(
        "ATGC",
        "ATGA"
    )

    check(
        "Substitution detected",
        any(
            v["Type"] == "Substitution"
            and v["Reference"] == "C"
            and v["Query"] == "A"
            for v in variants
        ),
        "ATGC versus ATGA contains a substitution."
    )

    variants = compare_sequences(
        "ATGC",
        "ATGGC"
    )

    check(
        "Insertion detected",
        any(
            v["Type"] == "Insertion"
            for v in variants
        ),
        "The query contains an additional base."
    )

    variants = compare_sequences(
        "ATGGC",
        "ATGC"
    )

    check(
        "Deletion detected",
        any(
            v["Type"] == "Deletion"
            for v in variants
        ),
        "The query is missing a base."
    )

    return tests


# ============================================================
# VISUALIZATION HELPERS
# ============================================================

def show_base_composition(stats):

    bases = ["A", "T", "G", "C"]

    counts = [
        stats[base]
        for base in bases
    ]

    fig, ax = plt.subplots(
        figsize=(6, 3)
    )

    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    bars = ax.bar(
        bases,
        counts,
        width=0.5,
        color=[
            YELLOW,
            BLUE,
            VIOLET,
            CINNAMON
        ]
    )

    maximum = max(
        counts
    ) if counts else 0

    ax.set_ylim(
        0,
        max(
            maximum * 1.25,
            1
        )
    )

    ax.tick_params(
        colors=TEXT,
        length=0
    )

    ax.grid(
        axis="y",
        color=BORDER,
        alpha=0.35
    )

    ax.set_axisbelow(True)

    for bar, count in zip(
        bars,
        counts
    ):

        ax.text(
            bar.get_x()
            + bar.get_width() / 2,
            count
            + max(maximum, 1) * 0.03,
            str(count),
            ha="center",
            color=TEXT,
            fontsize=10,
            fontweight="bold"
        )

    ax.set_xticks(
        range(4)
    )

    ax.set_xticklabels(
        [
            "A",
            "T",
            "G",
            "C"
        ],
        color=TEXT
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)


def show_codon_boxes(codons):

    if not codons:

        st.info(
            "No complete codons in this reading frame."
        )

        return

    for start in range(
        0,
        len(codons),
        10
    ):

        group = codons[
            start:start + 10
        ]

        html = ""

        for codon in group:

            if codon == "AUG":
                css_class = "codon-start"

            elif codon in STOP_CODONS:
                css_class = "codon-stop"

            else:
                css_class = ""

            html += (
                f'<span class="codon-box {css_class}">'
                f"{codon}"
                f"</span>"
            )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


def show_sequence_viewer(
    dna,
    rna,
    selected_frame
):

    st.markdown(
        f"**Selected frame: `{selected_frame}`**"
    )

    frame_number = int(
        selected_frame[-1]
    )

    offset = frame_number - 1

    if selected_frame.startswith("-"):

        oriented_dna = reverse_complement(
            dna
        )

        oriented_rna = transcribe_coding(
            oriented_dna
        )

    else:

        oriented_dna = dna
        oriented_rna = transcribe_coding(
            dna
        )

    codons = codons_in_frame(
        oriented_rna,
        offset
    )

    if not codons:

        st.info(
            "The sequence is too short for a complete codon "
            "in this frame."
        )

        return

    st.markdown(
        "**DNA / RNA codon alignment**"
    )

    dna_codons = [
        oriented_dna[
            offset + i * 3:
            offset + i * 3 + 3
        ]
        for i in range(len(codons))
    ]

    dna_html = ""
    rna_html = ""

    for dna_codon, rna_codon in zip(
        dna_codons,
        codons
    ):

        if rna_codon == START_CODON:
            css_class = "codon-start"

        elif rna_codon in STOP_CODONS:
            css_class = "codon-stop"

        else:
            css_class = ""

        dna_html += (
            f'<span class="codon-box {css_class}">'
            f"{dna_codon}"
            f"</span>"
        )

        rna_html += (
            f'<span class="codon-box {css_class}">'
            f"{rna_codon}"
            f"</span>"
        )

    st.markdown(
        f"""
        <div style="
            color:{MUTED};
            font-weight:700;
            margin-top:12px;
        ">
            DNA
        </div>
        <div style="
            overflow-x:auto;
            white-space:nowrap;
        ">
            {dna_html}
        </div>

        <div style="
            color:{MUTED};
            font-weight:700;
            margin-top:12px;
        ">
            RNA
        </div>
        <div style="
            overflow-x:auto;
            white-space:nowrap;
        ">
            {rna_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Yellow = start codon (AUG). "
        "Warm red = stop codon."
    )


# ============================================================
# HEADER / HERO SECTION
# ============================================================

st.markdown(
    """
<div class="hero">

<div class="hero-title">
🧬 DNA → RNA → <span>Protein Analyzer</span>
</div>

<div class="hero-description">
An interactive bioinformatics application for exploring DNA
sequences through transcription, translation, six reading
frames, ORF detection, codon usage, protein composition,
sequence comparison and GC-content analysis.
</div>

<div class="badge-row">

<div class="badge yellow">
Python
</div>

<div class="badge violet">
Streamlit
</div>

<div class="badge blue">
Bioinformatics
</div>

<div class="badge">
DNA Analysis
</div>

<div class="badge">
RNA Translation
</div>

<div class="badge">
ORF Detection
</div>

</div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

input_column, settings_column = st.columns(
    [2, 1]
)

with input_column:

    st.subheader(
        "📄 Sequence Input"
    )

    input_method = st.radio(
        "Input method",
        [
            "Paste DNA sequence",
            "Upload FASTA file"
        ],
        horizontal=True
    )

    raw_dna = ""

    if input_method == "Paste DNA sequence":

        raw_dna = st.text_area(
            "Paste DNA sequence",
            placeholder=(
                "Example: ATGAAATAA"
            ),
            height=130
        )

    else:

        uploaded_file = st.file_uploader(
            "Upload FASTA file",
            type=[
                "fasta",
                "fa",
                "fna",
                "txt"
            ]
        )

        if uploaded_file is not None:

            raw_dna = (
                uploaded_file
                .getvalue()
                .decode(
                    "utf-8",
                    errors="replace"
                )
            )

            st.success(
                "Sequence file loaded."
            )


with settings_column:

    st.subheader(
        "⚙️ Analysis Settings"
    )

    strand_type = st.selectbox(
        "Sequence entered is",
        [
            "Coding strand",
            "Template strand"
        ]
    )

    selected_frame = st.selectbox(
        "Protein translation frame",
        [
            "+1",
            "+2",
            "+3",
            "-1",
            "-2",
            "-3"
        ]
    )

    window_size = st.number_input(
        "GC window size (bp)",
        min_value=10,
        max_value=10000,
        value=100,
        step=10
    )


st.caption(
    "For a template strand, enter the sequence in the "
    "3′ → 5′ direction."
)


# ============================================================
# EXAMPLE SEQUENCE
# ============================================================

example_col1, example_col2 = st.columns(
    [1, 4]
)

with example_col1:

    if st.button(
        "🧬 Load Example",
        use_container_width=True
    ):

        st.session_state["example_sequence"] = (
            "ATGAAACCCGGGTTTTAA"
        )

with example_col2:

    if "example_sequence" in st.session_state:

        st.info(
            "Example sequence loaded. "
            "Click Analyze Sequence below."
        )

        raw_dna = st.session_state[
            "example_sequence"
        ]


# ============================================================
# OPTIONAL COMPARISON
# ============================================================

with st.expander(
    "🧬 Optional: Compare with another DNA sequence"
):

    raw_query = st.text_area(
        "Paste query / comparison DNA",
        placeholder=(
            "Enter a second sequence to compare "
            "with the reference."
        ),
        height=90
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🔬 Analyze Sequence",
    type="primary",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    dna = clean_sequence(
        raw_dna
    )

    query_dna = clean_sequence(
        raw_query
    )

    error = validate_dna(
        dna
    )

    if error:

        st.error(error)
        st.stop()

    query_error = None

    if query_dna:

        query_error = validate_dna(
            query_dna
        )

    if query_error:

        st.error(
            "Comparison sequence: "
            + query_error
        )

        st.stop()

    # --------------------------------------------------------
    # CONVERT INPUT INTO CODING-ORIENTED REFERENCE
    # --------------------------------------------------------

    if strand_type == "Template strand":

        coding_dna = reverse_complement(
            dna
        )

        rna = transcribe_template(
            dna
        )

    else:

        coding_dna = dna

        rna = transcribe_coding(
            dna
        )

    coding_rna = transcribe_coding(
        coding_dna
    )

    reverse_dna = reverse_complement(
        coding_dna
    )

    reverse_rna = transcribe_coding(
        reverse_dna
    )

    stats = get_statistics(
        dna
    )

    frames = get_six_frames(
        coding_dna
    )

    orfs = find_all_orfs(
        coding_dna
    )

    selected_data = frames[
        selected_frame
    ]

    selected_rna = selected_data[
        "oriented_rna"
    ]

    selected_offset = selected_data[
        "offset"
    ]

    selected_protein = translate_rna(
        selected_rna,
        selected_offset,
        stop_at_stop=True
    )

    selected_codons = codons_in_frame(
        selected_rna,
        selected_offset
    )

    aa_counts = Counter(
        selected_protein
    )

    codon_rows = get_codon_usage(
        selected_rna,
        selected_offset
    )

    complete_orfs = [
        orf
        for orf in orfs
        if orf["complete"]
    ]

    incomplete_orfs = [
        orf
        for orf in orfs
        if not orf["complete"]
    ]

    longest_orf = max(
        complete_orfs,
        key=lambda x: x["length_aa"],
        default=None
    )

    longest_orf_length = (
        longest_orf["length_aa"]
        if longest_orf
        else 0
    )

    # Protein properties

    molecular_weight = (
        protein_molecular_weight(
            selected_protein
        )
    )

    protein_classes_count = (
        protein_classes(
            selected_protein
        )
    )

    protein_composition = (
        get_protein_composition(
            selected_protein
        )
    )

    st.success(
        "Sequence analysis completed successfully."
    )


    # ========================================================
    # OVERVIEW DASHBOARD
    # ========================================================

    st.markdown(
        "## 📊 Sequence Overview"
    )

    overview_1, overview_2, overview_3, overview_4 = st.columns(
        4
    )

    overview_1.metric(
        "🧬 DNA Length",
        f"{stats['length']} bp"
    )

    overview_2.metric(
        "GC Content",
        f"{stats['GC']:.2f}%"
    )

    overview_3.metric(
        "🧬 Protein",
        f"{len(selected_protein)} aa"
    )

    overview_4.metric(
        "🧪 Complete ORFs",
        len(complete_orfs)
    )

    overview_5, overview_6, overview_7, overview_8 = st.columns(
        4
    )

    overview_5.metric(
        "RNA Length",
        f"{len(coding_rna)} nt"
    )

    overview_6.metric(
        "Total ORFs",
        len(orfs)
    )

    overview_7.metric(
        "Longest ORF",
        f"{longest_orf_length} aa"
    )

    overview_8.metric(
        "Selected Frame",
        selected_frame
    )

    st.caption(
        f"Input strand: {strand_type} · "
        f"Translation frame: {selected_frame} · "
        f"Complete ORFs: {len(complete_orfs)} · "
        f"Incomplete ORFs: {len(incomplete_orfs)}"
    )


    # ========================================================
    # ANALYSIS PIPELINE
    # ========================================================

    st.markdown(
        "### 🧬 Analysis Pipeline"
    )

    pipeline_1, pipeline_2, pipeline_3, pipeline_4 = st.columns(
        4
    )

    with pipeline_1:

        st.markdown(
            """
<div class="info-card">
<div class="info-card-title">STEP 1</div>
<div class="info-card-value">DNA</div>
<div class="info-card-small">
Sequence validation and base composition
</div>
</div>
""",
            unsafe_allow_html=True
        )

    with pipeline_2:

        st.markdown(
            """
<div class="info-card">
<div class="info-card-title">STEP 2</div>
<div class="info-card-value">RNA</div>
<div class="info-card-small">
Transcription into coding-oriented RNA
</div>
</div>
""",
            unsafe_allow_html=True
        )

    with pipeline_3:

        st.markdown(
            """
<div class="info-card">
<div class="info-card-title">STEP 3</div>
<div class="info-card-value">6 Frames</div>
<div class="info-card-small">
Three forward and three reverse frames
</div>
</div>
""",
            unsafe_allow_html=True
        )

    with pipeline_4:

        st.markdown(
            """
<div class="info-card">
<div class="info-card-title">STEP 4</div>
<div class="info-card-value">Protein</div>
<div class="info-card-small">
Translation, ORFs and amino-acid analysis
</div>
</div>
""",
            unsafe_allow_html=True
        )


    st.divider()


    # ========================================================
    # TABS
    # ========================================================

    tab_names = [
        "📊 Statistics",
        "🧬 DNA / RNA",
        "🔬 Reading Frames",
        "🧪 ORFs",
        "🧬 Protein",
        "🧮 Codon Usage",
        "🧬 Comparison",
        "📈 GC Windows",
        "🧪 Validation",
        "💾 Downloads"
    ]

    (
        statistics_tab,
        dna_rna_tab,
        frames_tab,
        orfs_tab,
        protein_tab,
        codon_tab,
        comparison_tab,
        gc_tab,
        validation_tab,
        downloads_tab
    ) = st.tabs(
        tab_names
    )


    # ========================================================
    # STATISTICS
    # ========================================================

    with statistics_tab:

        chart_col, summary_col = st.columns(
            [1.2, 1]
        )

        with chart_col:

            st.subheader(
                "🧬 Base Composition"
            )

            show_base_composition(
                stats
            )

        with summary_col:

            st.subheader(
                "📄 Sequence Summary"
            )

            summary_1, summary_2 = st.columns(
                2
            )

            summary_1.metric(
                "Length",
                f"{stats['length']} bp"
            )

            summary_2.metric(
                "GC",
                f"{stats['GC']:.2f}%"
            )

            summary_1.metric(
                "AT",
                f"{stats['AT']:.2f}%"
            )

            summary_2.metric(
                "Complete ORFs",
                len(complete_orfs)
            )

            summary_1.metric(
                "Incomplete ORFs",
                len(incomplete_orfs)
            )

            summary_2.metric(
                "Protein",
                f"{len(selected_protein)} aa"
            )

        st.divider()

        st.subheader(
            "🧬 Base Counts"
        )

        base_columns = st.columns(
            4
        )

        base_names = {
            "A": "Adenine",
            "T": "Thymine",
            "G": "Guanine",
            "C": "Cytosine"
        }

        for column, base in zip(
            base_columns,
            ["A", "T", "G", "C"]
        ):

            column.metric(
                f"{base} — {base_names[base]}",
                stats[base]
            )


    # ========================================================
    # DNA / RNA
    # ========================================================

    with dna_rna_tab:

        st.subheader(
            "🧬 Sequence Viewer"
        )

        show_sequence_viewer(
            coding_dna,
            coding_rna,
            selected_frame
        )

        st.divider()

        st.subheader(
            "Input DNA"
        )

        st.code(
            dna
        )

        st.subheader(
            "Coding-Oriented Reference DNA"
        )

        st.code(
            coding_dna
        )

        st.subheader(
            "Reverse Complement"
        )

        st.code(
            reverse_dna
        )

        st.subheader(
            "RNA Transcribed from Input"
        )

        st.code(
            rna
        )

        st.subheader(
            "Coding-Oriented RNA"
        )

        st.code(
            coding_rna
        )

        st.info(
            "For template-strand input, the template is assumed "
            "to be written 3′ → 5′. The coding-oriented sequence "
            "is used for six-frame analysis."
        )


    # ========================================================
    # READING FRAMES
    # ========================================================

    with frames_tab:

        st.subheader(
            "🔬 Six Reading Frames"
        )

        st.caption(
            "Forward frames (+1, +2, +3) are calculated from "
            "the coding-oriented sequence. Reverse frames "
            "(-1, -2, -3) are calculated from its reverse complement."
        )

        frame_summary = []

        for frame_name in [
            "+1",
            "+2",
            "+3",
            "-1",
            "-2",
            "-3"
        ]:

            frame_data = frames[
                frame_name
            ]

            protein_without_stop = (
                frame_data["protein"]
                .replace("*", "")
            )

            frame_summary.append({
                "Frame": frame_name,
                "Strand": (
                    "Forward"
                    if frame_data["strand"] == "+"
                    else "Reverse"
                ),
                "Codons": len(
                    frame_data["codons"]
                ),
                "Protein length": len(
                    protein_without_stop
                ),
                "Selected": (
                    "✓"
                    if frame_name == selected_frame
                    else ""
                )
            })

        st.dataframe(
            frame_summary,
            hide_index=True,
            use_container_width=True
        )

        st.divider()

        for frame_name in [
            "+1",
            "+2",
            "+3",
            "-1",
            "-2",
            "-3"
        ]:

            frame_data = frames[
                frame_name
            ]

            protein = (
                frame_data["protein"]
                .replace("*", "")
            )

            with st.expander(
                f"{'⭐ ' if frame_name == selected_frame else ''}"
                f"Frame {frame_name} · "
                f"{len(frame_data['codons'])} codons · "
                f"{len(protein)} aa",
                expanded=(
                    frame_name
                    == selected_frame
                )
            ):

                st.markdown(
                    f"""
<div class="frame-card">

<div class="frame-title">
Frame {frame_name}
</div>

<div class="frame-subtitle">
{
    "Forward strand"
    if frame_data["strand"] == "+"
    else "Reverse-complement strand"
}
</div>

</div>
""",
                    unsafe_allow_html=True
                )

                st.markdown(
                    "**Codon visualization**"
                )

                show_codon_boxes(
                    frame_data["codons"]
                )

                st.markdown(
                    "**Translated protein**"
                )

                st.code(
                    frame_data["protein"]
                    or "No amino acids"
                )

                fc1, fc2, fc3 = st.columns(
                    3
                )

                fc1.metric(
                    "Complete codons",
                    len(
                        frame_data["codons"]
                    )
                )

                fc2.metric(
                    "Amino acids",
                    len(protein)
                )

                fc3.metric(
                    "Stops",
                    frame_data["protein"].count("*")
                )


    # ========================================================
    # ORFs
    # ========================================================

    with orfs_tab:

        st.subheader(
            "🧪 Open Reading Frames"
        )

        if longest_orf:

            st.markdown(
                f"""
<div class="info-card">

<div class="info-card-title">
LONGEST COMPLETE ORF
</div>

<div class="info-card-value">
{longest_orf["length_aa"]} aa
</div>

<div class="info-card-small">
Frame {longest_orf["frame"]} ·
Position {longest_orf["start"]}–{longest_orf["end"]} ·
Protein: {longest_orf["protein"]}
</div>

</div>
""",
                unsafe_allow_html=True
            )

            st.write("")

        else:

            st.info(
                "No complete AUG-to-stop ORF was detected."
            )

        if not orfs:

            st.info(
                "No AUG-initiated ORFs were detected."
            )

        else:

            orf_table = []

            for index, orf in enumerate(
                orfs,
                start=1
            ):

                orf_table.append({
                    "ORF": f"ORF {index}",
                    "Strand": orf["strand"],
                    "Frame": orf["frame"],
                    "Start": orf["start"],
                    "End": orf["end"],
                    "Length (nt)": orf["length_nt"],
                    "Length (aa)": orf["length_aa"],
                    "Status": (
                        "Complete"
                        if orf["complete"]
                        else "Incomplete"
                    )
                })

            st.dataframe(
                orf_table,
                hide_index=True,
                use_container_width=True
            )

            st.divider()

            for index, orf in enumerate(
                orfs,
                start=1
            ):

                status = (
                    "Complete"
                    if orf["complete"]
                    else "Incomplete"
                )

                status_class = (
                    "orf-complete"
                    if orf["complete"]
                    else "orf-incomplete"
                )

                with st.expander(
                    f"ORF {index} · "
                    f"{orf['frame']} · "
                    f"{status} · "
                    f"{orf['length_aa']} aa"
                ):

                    st.markdown(
                        f"""
<span class="{status_class}">
● {status}
</span>
""",
                        unsafe_allow_html=True
                    )

                    c1, c2, c3, c4 = st.columns(
                        4
                    )

                    c1.metric(
                        "Frame",
                        orf["frame"]
                    )

                    c2.metric(
                        "Start",
                        orf["start"]
                    )

                    c3.metric(
                        "End",
                        orf["end"]
                    )

                    c4.metric(
                        "Protein length",
                        f"{orf['length_aa']} aa"
                    )

                    st.write(
                        f"**Nucleotide length:** "
                        f"{orf['length_nt']} bp"
                    )

                    st.write(
                        f"**Stop codon found:** "
                        f"{'Yes' if orf['complete'] else 'No'}"
                    )

                    st.markdown(
                        "**Protein sequence**"
                    )

                    st.code(
                        orf["protein"]
                        or "No amino acids"
                    )


    # ========================================================
    # PROTEIN
    # ========================================================

    with protein_tab:

        st.subheader(
            "🧬 Protein Analysis"
        )

        protein_col, property_col = st.columns(
            [1.2, 1]
        )

        with protein_col:

            st.markdown(
                f"**Selected reading frame:** `{selected_frame}`"
            )

            st.metric(
                "Amino acid count",
                len(selected_protein)
            )

            st.markdown(
                "**Protein sequence**"
            )

            st.code(
                selected_protein
                or "No amino acids detected"
            )

        with property_col:

            st.markdown(
                "**Protein properties**"
            )

            pc1, pc2 = st.columns(
                2
            )

            pc1.metric(
                "Molecular weight",
                (
                    f"{molecular_weight:.2f} Da"
                    if selected_protein
                    else "—"
                )
            )

            pc2.metric(
                "Hydrophobic",
                protein_classes_count[
                    "Hydrophobic"
                ]
            )

            pc1.metric(
                "Polar",
                protein_classes_count[
                    "Polar"
                ]
            )

            pc2.metric(
                "Positive",
                protein_classes_count[
                    "Positively charged"
                ]
            )

            pc1.metric(
                "Negative",
                protein_classes_count[
                    "Negatively charged"
                ]
            )

            pc2.metric(
                "Other",
                protein_classes_count[
                    "Other"
                ]
            )

        st.divider()

        st.subheader(
            "🧪 Amino Acid Composition"
        )

        if protein_composition:

            st.dataframe(
                protein_composition,
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "No amino acids detected in this frame."
            )

        st.caption(
            "Molecular weight is an approximate theoretical "
            "value calculated from average amino-acid residue "
            "masses. It is not a measured experimental mass."
        )


    # ========================================================
    # CODON USAGE
    # ========================================================

    with codon_tab:

        st.subheader(
            "🧮 Codon Usage"
        )

        if codon_rows:

            st.dataframe(
                codon_rows,
                hide_index=True,
                use_container_width=True
            )

            usage_counts = {
                row["Codon"]: row["Count"]
                for row in codon_rows
            }

            fig, ax = plt.subplots(
                figsize=(10, 3.5)
            )

            fig.patch.set_facecolor(
                BG
            )

            ax.set_facecolor(
                BG
            )

            ax.bar(
                list(
                    usage_counts.keys()
                ),
                list(
                    usage_counts.values()
                ),
                color=BLUE
            )

            ax.tick_params(
                axis="x",
                rotation=90,
                colors=TEXT
            )

            ax.tick_params(
                axis="y",
                colors=TEXT
            )

            ax.set_ylabel(
                "Count",
                color=TEXT
            )

            ax.grid(
                axis="y",
                color=BORDER,
                alpha=0.35
            )

            ax.set_axisbelow(True)

            for spine in ax.spines.values():
                spine.set_visible(False)

            plt.tight_layout()

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

        else:

            st.info(
                "No complete codons available "
                "in the selected frame."
            )


    # ========================================================
    # COMPARISON
    # ========================================================

    with comparison_tab:

        st.subheader(
            "🧬 Reference vs Query Comparison"
        )

        if not query_dna:

            st.info(
                "Enter a second DNA sequence above and "
                "click Analyze Sequence."
            )

        else:

            differences = compare_sequences(
                dna,
                query_dna
            )

            c1, c2, c3, c4 = st.columns(
                4
            )

            substitutions = sum(
                item["Type"] == "Substitution"
                for item in differences
            )

            insertions = sum(
                item["Type"] == "Insertion"
                for item in differences
            )

            deletions = sum(
                item["Type"] == "Deletion"
                for item in differences
            )

            c1.metric(
                "Reference",
                f"{len(dna)} bp"
            )

            c2.metric(
                "Query",
                f"{len(query_dna)} bp"
            )

            c3.metric(
                "Differences",
                len(differences)
            )

            c4.metric(
                "Similarity",
                f"{SequenceMatcher(None, dna, query_dna).ratio() * 100:.1f}%"
            )

            if not differences:

                st.success(
                    "The sequences are identical."
                )

            else:

                d1, d2, d3 = st.columns(
                    3
                )

                d1.metric(
                    "Substitutions",
                    substitutions
                )

                d2.metric(
                    "Insertions",
                    insertions
                )

                d3.metric(
                    "Deletions",
                    deletions
                )

                st.dataframe(
                    differences,
                    hide_index=True,
                    use_container_width=True
                )

                st.warning(
                    "This is a simple sequence comparison, "
                    "not a clinical variant caller."
                )


    # ========================================================
    # GC WINDOWS
    # ========================================================

    with gc_tab:

        st.subheader(
            "📈 GC Content Across the Sequence"
        )

        windows = gc_windows(
            coding_dna,
            int(window_size)
        )

        if windows:

            midpoints = [
                (
                    row["start"]
                    + row["end"]
                ) / 2
                for row in windows
            ]

            values = [
                row["gc"]
                for row in windows
            ]

            fig, ax = plt.subplots(
                figsize=(10, 3.5)
            )

            fig.patch.set_facecolor(
                BG
            )

            ax.set_facecolor(
                BG
            )

            ax.plot(
                midpoints,
                values,
                marker="o",
                linewidth=1.8,
                color=YELLOW
            )

            ax.set_xlabel(
                "Position (bp)",
                color=TEXT
            )

            ax.set_ylabel(
                "GC content (%)",
                color=TEXT
            )

            ax.set_ylim(
                0,
                100
            )

            ax.tick_params(
                colors=TEXT
            )

            ax.grid(
                color=BORDER,
                alpha=0.35
            )

            for spine in ax.spines.values():
                spine.set_visible(False)

            plt.tight_layout()

            st.pyplot(
                fig,
                use_container_width=True
            )

            plt.close(fig)

            st.dataframe(
                [
                    {
                        "Start (bp)": row["start"],
                        "End (bp)": row["end"],
                        "Length (bp)": row["length"],
                        "GC (%)": round(
                            row["gc"],
                            2
                        )
                    }
                    for row in windows
                ],
                hide_index=True,
                use_container_width=True
            )

        else:

            st.info(
                "Not enough sequence data "
                "to calculate GC windows."
            )


    # ========================================================
    # VALIDATION
    # ========================================================

    with validation_tab:

        st.subheader(
            "🧪 Built-in Validation Tests"
        )

        test_results = run_validation_tests()

        passed = sum(
            result["Result"] == "PASS"
            for result in test_results
        )

        failed = (
            len(test_results)
            - passed
        )

        a, b, c = st.columns(
            3
        )

        a.metric(
            "Tests",
            len(test_results)
        )

        b.metric(
            "Passed",
            passed
        )

        c.metric(
            "Failed",
            failed
        )

        st.dataframe(
            test_results,
            hide_index=True,
            use_container_width=True
        )

        if failed == 0:

            st.success(
                "All built-in checks passed."
            )

        else:

            st.error(
                "One or more validation checks failed."
            )

        with st.expander(
            "What do these tests verify?"
        ):

            st.markdown(
                """
                - DNA alphabet validation
                - Empty input handling
                - Reverse-complement calculation
                - Coding transcription
                - Template transcription
                - Translation
                - Stop-codon handling
                - GC and AT percentages
                - Complete ORF detection
                - Incomplete ORF detection
                - Substitution detection
                - Insertion detection
                - Deletion detection

                These are regression tests for selected examples,
                not a replacement for validation against trusted
                bioinformatics software and reference sequences.
                """
            )


    # ========================================================
    # DOWNLOADS
    # ========================================================

    with downloads_tab:

        st.subheader(
            "💾 Download Results"
        )

        # ----------------------------------------------------
        # TXT REPORT
        # ----------------------------------------------------

        txt = io.StringIO()

        txt.write(
            "DNA → RNA → Protein Analyzer\n"
        )

        txt.write(
            "====================================\n\n"
        )

        txt.write(
            f"Input strand: {strand_type}\n"
        )

        txt.write(
            f"DNA length: {stats['length']} bp\n"
        )

        txt.write(
            f"GC content: {stats['GC']:.2f}%\n"
        )

        txt.write(
            f"AT content: {stats['AT']:.2f}%\n"
        )

        txt.write(
            f"Selected frame: {selected_frame}\n"
        )

        txt.write(
            f"Protein length: "
            f"{len(selected_protein)} aa\n"
        )

        txt.write(
            f"Protein molecular weight: "
            f"{molecular_weight:.2f} Da\n\n"
        )

        txt.write(
            f"Input DNA:\n{dna}\n\n"
        )

        txt.write(
            f"Coding-oriented DNA:\n"
            f"{coding_dna}\n\n"
        )

        txt.write(
            f"Reverse complement:\n"
            f"{reverse_dna}\n\n"
        )

        txt.write(
            f"RNA:\n{rna}\n\n"
        )

        txt.write(
            f"Selected protein:\n"
            f"{selected_protein}\n\n"
        )

        txt.write(
            f"Complete ORFs: "
            f"{len(complete_orfs)}\n"
        )

        txt.write(
            f"Incomplete ORFs: "
            f"{len(incomplete_orfs)}\n\n"
        )

        txt.write(
            "ORF details:\n"
        )

        for index, orf in enumerate(
            orfs,
            start=1
        ):

            txt.write(
                f"{index}. "
                f"Frame={orf['frame']}, "
                f"start={orf['start']}, "
                f"end={orf['end']}, "
                f"length={orf['length_aa']} aa, "
                f"complete={orf['complete']}, "
                f"protein={orf['protein']}\n"
            )

        st.download_button(
            "📄 Download TXT Report",
            data=txt.getvalue(),
            file_name=(
                "dna_rna_protein_report.txt"
            ),
            mime="text/plain"
        )

        # ----------------------------------------------------
        # CSV SUMMARY
        # ----------------------------------------------------

        csv_buffer = io.StringIO()

        writer = csv.writer(
            csv_buffer
        )

        writer.writerow(
            [
                "Parameter",
                "Value"
            ]
        )

        summary_rows = [
            ("Input strand", strand_type),
            ("DNA length", stats["length"]),
            ("A", stats["A"]),
            ("T", stats["T"]),
            ("G", stats["G"]),
            ("C", stats["C"]),
            ("GC content", stats["GC"]),
            ("AT content", stats["AT"]),
            ("Selected frame", selected_frame),
            ("Protein length", len(selected_protein)),
            ("Protein molecular weight", molecular_weight),
            ("Complete ORFs", len(complete_orfs)),
            ("Incomplete ORFs", len(incomplete_orfs)),
            ("Input DNA", dna),
            ("Coding-oriented DNA", coding_dna),
            ("RNA", rna),
            ("Reverse complement", reverse_dna),
            ("Selected protein", selected_protein)
        ]

        for key, value in summary_rows:

            writer.writerow(
                [
                    key,
                    value
                ]
            )

        st.download_button(
            "📊 Download CSV Summary",
            data=csv_buffer.getvalue(),
            file_name=(
                "dna_rna_protein_summary.csv"
            ),
            mime="text/csv"
        )

        # ----------------------------------------------------
        # ORF TABLE
        # ----------------------------------------------------

        orf_buffer = io.StringIO()

        orf_fields = [
            "strand",
            "frame",
            "start",
            "end",
            "length_nt",
            "length_aa",
            "complete",
            "protein"
        ]

        orf_writer = csv.DictWriter(
            orf_buffer,
            fieldnames=orf_fields
        )

        orf_writer.writeheader()

        for orf in orfs:

            orf_writer.writerow({
                field: orf[field]
                for field in orf_fields
            })

        st.download_button(
            "🧪 Download ORF Table",
            data=orf_buffer.getvalue(),
            file_name="dna_orf_results.csv",
            mime="text/csv"
        )

        # ----------------------------------------------------
        # CODON USAGE
        # ----------------------------------------------------

        codon_buffer = io.StringIO()

        codon_writer = csv.DictWriter(
            codon_buffer,
            fieldnames=[
                "Codon",
                "Amino acid",
                "Count",
                "Frequency (%)"
            ]
        )

        codon_writer.writeheader()

        codon_writer.writerows(
            codon_rows
        )

        st.download_button(
            "🧮 Download Codon Usage",
            data=codon_buffer.getvalue(),
            file_name="codon_usage.csv",
            mime="text/csv"
        )

        # ----------------------------------------------------
        # PROTEIN COMPOSITION
        # ----------------------------------------------------

        protein_buffer = io.StringIO()

        protein_writer = csv.DictWriter(
            protein_buffer,
            fieldnames=[
                "Code",
                "3-letter",
                "Amino acid",
                "Count",
                "Percentage"
            ]
        )

        protein_writer.writeheader()

        protein_writer.writerows(
            protein_composition
        )

        st.download_button(
            "🧬 Download Protein Composition",
            data=protein_buffer.getvalue(),
            file_name="protein_composition.csv",
            mime="text/csv"
        )

        # ----------------------------------------------------
        # SEQUENCE COMPARISON
        # ----------------------------------------------------

        if query_dna:

            variant_buffer = io.StringIO()

            differences = compare_sequences(
                dna,
                query_dna
            )

            variant_fields = [
                "Type",
                "Reference position",
                "Reference",
                "Query"
            ]

            variant_writer = csv.DictWriter(
                variant_buffer,
                fieldnames=variant_fields
            )

            variant_writer.writeheader()

            variant_writer.writerows(
                differences
            )

            st.download_button(
                "🧬 Download Sequence Differences",
                data=variant_buffer.getvalue(),
                file_name=(
                    "sequence_comparison.csv"
                ),
                mime="text/csv"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">

🧬 DNA → RNA → Protein Analyzer

Interactive bioinformatics sequence analysis application

Python · Streamlit · Computational Biology

</div>
""",
    unsafe_allow_html=True
)