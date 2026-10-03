 rotein stops at the first stop codon."
                )

    # ========================================================
    # ORFs
    # ========================================================

    with orfs_tab:
        st.subheader("🧪 ORFs in All Six Frames")

        st.caption(
            "Coordinates are 1-based and inclusive on the "
            "coding-oriented reference DNA. Reverse-strand coordinates "
            "are mapped back to that reference."
        )

        if not orfs:
            st.info("No AUG-initiated ORFs were detected.")
        else:
            st.write(
                f"**{len(complete_orfs)} complete** and "
                f"**{len(incomplete_orfs)} incomplete** ORFs detected."
            )

            for index, orf in enumerate(orfs, start=1):
                status = "Complete" if orf["complete"] else "Incomplete"

                with st.expander(
                    f"ORF {index} · {orf['frame']} · "
                    f"{status} · {orf['length_aa']} aa"
                ):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Frame", orf["frame"])
                    c2.metric("Start", orf["start"])
                    c3.metric("End", orf["end"])
                    c4.metric("Protein length", f"{orf['length_aa']} aa")

                    st.write(
                        f"**Nucleotide length:** {orf['length_nt']} bp"
                    )
                    st.write(
                        f"**Stop codon found:** "
                        f"{'Yes' if orf['complete'] else 'No'}"
                    )
                    st.markdown("**Protein sequence**")
                    st.code(orf["protein"] or "No amino acids")

    # ========================================================
    # PROTEIN
    # ========================================================

    with protein_tab:
        protein_col, composition_col = st.columns(2)

        with protein_col:
            st.subheader("🧬 Selected Protein")
            st.caption(f"Reading frame: {selected_frame}")
            st.metric("Amino acid count", len(selected_protein))
            st.code(selected_protein or "No amino acids detected")

        with composition_col:
            st.subheader("🧪 Amino Acid Composition")

            if aa_counts:
                rows = []

                for aa, count in sorted(aa_counts.items()):
                    rows.append({
                        "Code": aa,
                        "Amino acid": AA_NAMES.get(aa, aa),
                        "Count": count,
                        "Percentage": round(
                            count / len(selected_protein) * 100, 2
                        )
                    })

                st.dataframe(
                    rows,
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No amino acids detected in this frame.")

    # ========================================================
    # CODON USAGE
    # ========================================================

    with codon_tab:
        st.subheader("🧮 Codon Usage")
        st.caption(
            f"Codon counts for frame {selected_frame}, including a "
            "stop codon if it occurs before the end of the sequence."
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

            fig, ax = plt.subplots(figsize=(10, 3.5))
            fig.patch.set_facecolor("#0b1b2e")
            ax.set_facecolor("#0b1b2e")
            ax.bar(
                list(usage_counts.keys()),
                list(usage_counts.values()),
                color="#46d0c1"
            )
            ax.tick_params(axis="x", rotation=90, colors="#dce8f5")
            ax.tick_params(axis="y", colors="#dce8f5")
            ax.set_ylabel("Count", color="#dce8f5")
            ax.grid(axis="y", alpha=0.25)
            ax.set_axisbelow(True)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.info("No complete codons available in the selected frame.")

    # ========================================================
    # SEQUENCE COMPARISON
    # ========================================================

    with comparison_tab:
        st.subheader("🧬 Reference vs Query Comparison")

        if not query_dna:
            st.info(
                "Open 'Optional: Compare with another DNA sequence' "
                "above and enter a second DNA sequence, then click "
                "'Analyze Sequence' again."
            )
        else:
            st.write(f"**Reference length:** {len(dna)} bp")
            st.write(f"**Query length:** {len(query_dna)} bp")

            differences = compare_sequences(dna, query_dna)

            if not differences:
                st.success("The sequences are identical.")
            else:
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

                a, b, c = st.columns(3)
                a.metric("Substitutions", substitutions)
                b.metric("Insertions", insertions)
                c.metric("Deletions", deletions)

                st.dataframe(
                    differences,
                    hide_index=True,
                    use_container_width=True
                )

                st.warning(
                    "This is a simple sequence comparison, not a "
                    "clinical variant caller. Repetitive regions and "
                    "complex variants can have ambiguous alignments. "
                    "Both sequences should use the same orientation."
                )

    # ========================================================
    # GC WINDOW ANALYSIS
    # ========================================================

    with gc_tab:
        st.subheader("📈 GC Content Across the Sequence")

        windows = gc_windows(coding_dna, int(window_size))

        if windows:
            st.caption(
                f"Window size: {window_size} bp. The final window "
                "may be shorter than the selected window size."
            )

            fig, ax = plt.subplots(figsize=(10, 3.5))
            fig.patch.set_facecolor("#0b1b2e")
            ax.set_facecolor("#0b1b2e")

            midpoints = [
                (row["start"] + row["end"]) / 2
                for row in windows
            ]
            values = [row["gc"] for row in windows]

            ax.plot(
                midpoints,
                values,
                marker="o",
                linewidth=1.8,
                color="#46d0c1"
            )
            ax.set_xlabel("Position (bp)", color="#dce8f5")
            ax.set_ylabel("GC content (%)", color="#dce8f5")
            ax.set_ylim(0, 100)
            ax.tick_params(colors="#dce8f5")
            ax.grid(alpha=0.25)
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

            st.dataframe(
                [
                    {
                        "Start (bp)": row["start"],
                        "End (bp)": row["end"],
                        "Length (bp)": row["length"],
                        "GC (%)": round(row["gc"], 2)
                    }
                    for row in windows
                ],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Not enough sequence data to calculate GC windows.")

    # ========================================================
    # VALIDATION
    # ========================================================

    with validation_tab:
        st.subheader("🧪 Built-in Validation Tests")

        test_results = run_validation_tests()
        passed = sum(
            result["Result"] == "PASS"
            for result in test_results
        )
        failed = len(test_results) - passed

        a, b, c = st.columns(3)
        a.metric("Tests", len(test_results))
        b.metric("Passed", passed)
        c.metric("Failed", failed)

        st.dataframe(
            test_results,
            hide_index=True,
            use_container_width=True
        )

        if failed == 0:
            st.success(
                "All built-in checks passed. These tests cover selected "
                "examples, not every biological edge case."
            )
        else:
            st.error(
                "One or more checks failed. Review the test details "
                "before relying on the corresponding analysis."
            )

        with st.expander("What do these tests verify?"):
            st.markdown("""
            - DNA alphabet validation and empty input handling
            - Reverse-complement calculation
            - Coding and template transcription
            - Translation and stop-codon handling
            - GC and AT percentages
            - Complete and incomplete ORF detection
            - Simple substitution, insertion and deletion detection

            These are small regression tests. For research use, also
            validate results against trusted bioinformatics software
            and known reference sequences.
            """)

    # ========================================================
    # DOWNLOADS
    # ========================================================

    with downloads_tab:
        st.subheader("💾 Download Results")

        txt = io.StringIO()
        txt.write("DNA → RNA → Protein Analyzer\n\n")
        txt.write(f"Input strand: {strand_type}\n")
        txt.write(f"DNA length: {stats['length']} bp\n")
        txt.write(f"GC content: {stats['GC']:.2f}%\n")
        txt.write(f"AT content: {stats['AT']:.2f}%\n")
        txt.write(f"A: {stats['A']}\nT: {stats['T']}\n")
        txt.write(f"G: {stats['G']}\nC: {stats['C']}\n\n")
        txt.write(f"Input DNA:\n{dna}\n\n")
        txt.write(f"Coding-oriented DNA:\n{coding_dna}\n\n")
        txt.write(f"Reverse complement:\n{reverse_dna}\n\n")
        txt.write(f"RNA transcribed from input:\n{rna}\n\n")
        txt.write(f"Selected frame: {selected_frame}\n")
        txt.write(f"Selected protein:\n{selected_protein}\n\n")
        txt.write(f"Complete ORFs: {len(complete_orfs)}\n")
        txt.write(f"Incomplete ORFs: {len(incomplete_orfs)}\n\n")

        txt.write("ORF details:\n")
        for index, orf in enumerate(orfs, start=1):
            txt.write(
                f"{index}. Frame={orf['frame']}, "
                f"start={orf['start']}, end={orf['end']}, "
                f"length={orf['length_aa']} aa, "
                f"complete={orf['complete']}, "
                f"protein={orf['protein']}\n"
            )

        st.download_button(
            "📄 Download TXT Report",
            data=txt.getvalue(),
            file_name="dna_rna_protein_report.txt",
            mime="text/plain"
        )

        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Parameter", "Value"])

        for key, value in stats.items():
            writer.writerow([key, value])

        writer.writerow(["Input strand", strand_type])
        writer.writerow(["Selected frame", selected_frame])
        writer.writerow(["Input DNA", dna])
        writer.writerow(["Coding-oriented DNA", coding_dna])
        writer.writerow(["RNA", rna])
        writer.writerow(["Reverse complement", reverse_dna])
        writer.writerow(["Selected protein", selected_protein])
        writer.writerow(["Complete ORFs", len(complete_orfs)])
        writer.writerow(["Incomplete ORFs", len(incomplete_orfs)])

        st.download_button(
            "📊 Download CSV Summary",
            data=csv_buffer.getvalue(),
            file_name="dna_rna_protein_summary.csv",
            mime="text/csv"
        )

        orf_buffer = io.StringIO()
        orf_fields = [
            "strand", "frame", "start", "end",
            "length_nt", "length_aa", "complete", "protein"
        ]
        orf_writer = csv.DictWriter(
            orf_buffer,
            fieldnames=orf_fields
        )
        orf_writer.writeheader()

        for orf in orfs:
            orf_writer.writerow({
                field: orf[field] for field in orf_fields
            })

        st.download_button(
            "🧪 Download ORF Table",
            data=orf_buffer.getvalue(),
            file_name="dna_orf_results.csv",
            mime="text/csv"
        )

        codon_buffer = io.StringIO()
        codon_writer = csv.DictWriter(
            codon_buffer,
            fieldnames=["Codon", "Amino acid", "Count", "Frequency (%)"]
        )
        codon_writer.writeheader()
        codon_writer.writerows(codon_rows)

        st.download_button(
            "🧮 Download Codon Usage",
            data=codon_buffer.getvalue(),
            file_name="codon_usage.csv",
            mime="text/csv"
        )

        if query_dna:
            variant_buffer = io.StringIO()
            differences = compare_sequences(dna, query_dna)
            variant_fields = [
                "Type", "Reference position", "Reference", "Query"
            ]
            variant_writer = csv.DictWriter(
                variant_buffer,
                fieldnames=variant_fields
            )
            variant_writer.writeheader()
            variant_writer.writerows(differences)

            st.download_button(
                "🧬 Download Sequence Differences",
                data=variant_buffer.getvalue(),
                file_name="sequence_comparison.csv",
                mime="text/csv"
            )