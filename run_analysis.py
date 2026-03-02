# Main script to parse .vchk files and generate plots in one go.
# CB04Nov25

"""
run_analysis.py

Main script to parse .vchk files and generate plots in one go.

Usage:
    python run_analysis.py "DATA\\data1.vchk" "output" -all
    
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

import subprocess
import argparse
import os
import sys

def main():
    """Main function to parse .vchk files and generate plots."""
    
    parser = argparse.ArgumentParser(description="Parse .vchk files and generate plots")
    parser.add_argument("input_file", help="Path to the input .vchk file")
    parser.add_argument("output_folder", help="Output folder for parsed data and plots")
    
    # Accept any extra flags for section selection
    parser.add_argument("flags", nargs=argparse.REMAINDER, help="Section flags (e.g., -af -qual -all)")
    args = parser.parse_args()
    if not os.path.isfile(args.input_file):
        print(f"ERROR: Input file not found: {args.input_file}")
        sys.exit(1)
    os.makedirs(args.output_folder, exist_ok=True)
    # Parse
    print("Parsing .vchk file...")
    result = subprocess.run(["python", "parse_stats.py", args.input_file, args.output_folder] + args.flags)
    if result.returncode != 0:
        print("\n Parsing failed")
        sys.exit(8)
        
    # Auto-detect basename
    basename = os.path.splitext(os.path.basename(args.input_file))[0]
    
    # Plot
    print("\nGenerating plots...")
    plot_cmd = ["python", "make_plots.py", args.output_folder, basename] + args.flags
    result = subprocess.run(plot_cmd)
    if result.returncode != 0:
        print("\n Plotting failed")
        sys.exit(9)
    print("\n COMPLETE!")
    print(f"Output: {args.output_folder}/")

if __name__ == "__main__":
    main()
