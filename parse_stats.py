#Parsing the DATA files into usable tables
#CB02Nov25

"""
parse_stats.py

Python script to parse Bcftools-stats (.vchk) files into per-section text 
outputs and always prints Summary Notes (SN) into the terminal.

Usage:
    python parse_stats.py "DATA\\data1.vchk" "output" -flags

Flags: 
    
    -tstv : Extracts only Transition/Transversion ratio section.
    -sis : Extracts only SNPs in Samples section.
    -af : Extracts only Allele Frequency Distribution section.
    -qual : Extracts only Quality Score Distribution section.
    -idd : Extracts only INDEL Length Distribution section.
    -str : Extracts only STR Length Distribution section.
    -dp : Extracts only Depth Distribution section.
    -psc : Extracts only Per Sample Counts section.
    -psi : Extracts only Per Sample Indels section.
    -hwe : Extracts only Hardy-Weinberg Equilibrium section.
    -all : Extracts all sections into separate files.
"""
    

import os, sys, argparse

all_tags = \
    ["ID", "SN", "TSTV", "SiS", "AF", "QUAL", "IDD", "ST", "DP", "PSC", "PSI", "HWE"]



def build_parser():
    """Build and return argument parser for command-line options."""
    p = argparse.ArgumentParser(
        description="Parse bcftools stats (.vchk) files into per-section text outputs and print Summary Numbers (SN) to terminal."
    )

    p.add_argument("input_file", help="Input .vchk file path.")
    p.add_argument("output_folder", help="Folder for combined.tsv, per-section text files and graphs.")
    
    # Add flags for each section (both short and long forms)
    for tag in all_tags:
        p.add_argument(
            f"-{tag.lower()}",
            f"--{tag.lower()}",
            action="store_true",
            help=f"Extract section {tag} only."
        )
        
    # Add flag for extracting all sections
    p.add_argument(
        "-all", "--all",
        action="store_true",
        help="Extract all sections into separate files."
    )
    
    return p

    

def read_vchk(path):
    """Read .vchk file and return tab-split lines, ignoring comments and empty lines."""
    
    rows = []
  
    with open(path, "r", encoding="utf-8", errors="ignore") as f: 
        # Used with open to avoid having to close the file manually
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            rows.append(parts)
            
    return rows
    

    
def print_sn(rows):
    """Print all Summary Numbers (SN) lines to the terminal."""
    print("=== Summary Numbers (SN) ===")
    found = False
    for r in rows:
        if r and r[0] == "SN":
            print("\t".join(r))
            found = True
    if not found:
        print("(No SN lines found)")



def write_combined_tsv(rows, output_path):
    """Write combined TSV file with padded rows."""

    # Find the widest line for formatting
    width = max(len(r) for r in rows)

    with open(output_path, "w") as out_f:
           # Write each row, padding to the same width
            for r in rows:
                padded_row = r + [""] * (width - len(r))
                out_f.write("\t".join(padded_row) + "\n")
                
def split_sections(rows):
    """Split rows into sections based on first column tag."""
    sections = {}
    for r in rows:
        if r:
            tag = r[0]
            sections.setdefault(tag, []).append(r)
    return sections

def write_section_files(sections, output_folder, selected_tags, input_name):
    """Write separate text files for each selected section."""
    for tag in selected_tags:
        tag_dir = os.path.join(output_folder, tag)
        os.makedirs(tag_dir, exist_ok=True)
       
        output_path = os.path.join(tag_dir, f"{input_name}_{tag}.txt")
        rows_tag = sections.get(tag, [])
        
        try:
            with open(output_path, "w") as out_f:
                if rows_tag:
                    for r in rows_tag:
                        out_f.write("\t".join(r) + "\n")
                        
        except Exception as e:
            raise RuntimeError(f"ERROR: could not write section file for {tag}: {e}")

def main():
    """Main entry point for parsing .vchk files into sections."""
    parser = build_parser()
    args = parser.parse_args()
    # Validate paths
    if not os.path.isfile(args.input_file):
        print(f"ERROR: file not found: {args.input_file}", file=sys.stderr)
        # Exit code 2: Input file not found
        sys.exit(2)

    try:
        os.makedirs(args.output_folder, exist_ok=True)
    except Exception as e:
        print(f"ERROR: could not create output folder: {args.output_folder}", file=sys.stderr)
        # Exit code 3: Output folder creation failed
        sys.exit(3)
        
    try:
        rows = read_vchk(args.input_file)
    except Exception as e:
        print(f"ERROR: could not read input file: {args.input_file}", file=sys.stderr)
        # Exit code 4: Input file read error
        sys.exit(4)
        
    """
    Print the Summary Numbers (SN) section in the terminal.
    """
    print_sn(rows)
    
    # Write combined TSV file - https://docs.python.org/3/library/os.path.html for os.path functions
    input_name = os.path.splitext(os.path.basename(args.input_file))[0]
    combined_tsv_path = os.path.join(args.output_folder, f"{input_name}_combined.tsv")
    write_combined_tsv(rows, combined_tsv_path)
   
    try:
        write_combined_tsv(rows, combined_tsv_path)
    except Exception as e:
        print(f"ERROR: could not write combined TSV file: {combined_tsv_path}", file=sys.stderr)
        # Exit code 5: Combined TSV file write error
        sys.exit(5)
    
    print(f"Combined TSV file written to: {combined_tsv_path}")
    
    # Split rows into sections

    sections = split_sections(rows)
    # Determine selected_tags based on args
    selected_tags = []
    for tag in all_tags:
        if getattr(args, tag.lower()):
            selected_tags.append(tag)
    if args.all:
        selected_tags = all_tags.copy()
    try:
        write_section_files(sections, args.output_folder, selected_tags, input_name)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        # Exit code 6: Section file write error
        sys.exit(6)

if __name__ == "__main__":
    main()
    
    
    