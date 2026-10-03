
import bioinformatics as app


def test_clean_sequence():
    assert app.clean_sequence("atgc\natgc") == "ATGCATGC"


def test_clean_sequence_removes_fasta_header():
    assert app.clean_sequence(">sequence1\nATGC\nATGA") == "ATGCATGA"


def test_valid_dna():
    assert app.validate_dna("ATGC")[0] is True


def test_invalid_dna():
    valid, message = app.validate_dna("ATGX")
    assert valid is False
    assert "X" in message


def test_empty_dna():
    valid, message = app.validate_dna("")
    assert valid is False
    assert message


def test_reverse_complement():
    assert app.reverse_complement("ATGC") == "GCAT"


def test_coding_transcription():
    assert app.transcribe("ATGGCC") == "AUGGCC"


def test_template_transcription():
    coding_dna, rna = app.dna_to_rna(
        "TACCGG", "Template strand (5' → 3')"
    )
    assert coding_dna == "CCGGTA"
    assert rna == "CCGGUA"


def test_translation():
    assert app.translate_rna("AUGGCCCUGUAA") == "MAL"


def test_translation_stops_at_stop_codon():
    assert app.translate_rna("AUGUAA") == "M"


def test_incomplete_codon_is_ignored():
    assert app.translate_rna("AUGGC") == "M"


def test_gc_content():
    assert app.calculate_gc("ATGC") == 50.0


def test_empty_gc_content():
    assert app.calculate_gc("") == 0.0


def test_base_composition():
    assert app.base_composition("AATGC") == {
        "A": 2, "T": 1, "G": 1, "C": 1
    }


def test_six_reading_frames():
    frames = app.get_six_frames("ATGGCCCTGTAA")
    assert len(frames) == 6
    assert all(
        frame in frames
        for frame in ["+1", "+2", "+3", "-1", "-2", "-3"]
    )


def test_complete_orf():
    orfs = app.find_orfs("ATGAAATAA")
    assert any(
        orf["Frame"] == "+1"
        and orf["Stop found"] == "Yes"
        and orf["Protein"] == "MK"
        and orf["Length (nt)"] == 9
        for orf in orfs
    )


def test_incomplete_orf():
    orfs = app.find_orfs("ATGAAA")
    assert any(
        orf["Frame"] == "+1"
        and orf["Stop found"] == "No"
        and orf["Protein"] == "MK"
        for orf in orfs
    )


def test_gc_windows():
    windows = app.gc_windows("ATGCATGC", 4, 4)
    assert len(windows) == 2
    assert windows.iloc[0]["GC (%)"] == 50.0
    assert windows.iloc[1]["GC (%)"] == 50.0


def test_identical_sequences():
    assert app.compare_sequences("ATGC", "ATGC").empty


def test_substitution_detection():
    differences = app.compare_sequences("ATGC", "ATGA")
    assert not differences.empty
    assert "Substitution" in differences.iloc[0]["Change"]


def test_insertion_detection():
    differences = app.compare_sequences("ATGC", "ATGGC")
    assert any(
        "Insertion" in change
        for change in differences["Change"]
    )


def test_deletion_detection():
    differences = app.compare_sequences("ATGGC", "ATGC")
    assert any(
        "Deletion" in change
        for change in differences["Change"]
    )
PY