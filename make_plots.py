
# making plots from the parsed data
# CB04Nov25

"""
make_plots.py

Python script to create graphs from the parsed .txt files
and always prints Summary Notes (SN) into the terminal.

Usage:
    python make_plots.py "DATA\\data1.vchk" "output" -flags

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


import matplotlib.pyplot as plt, argparse, os, sys, pandas as pd

def read_section_txt(section_folder, section, basename):
    """Read section .txt files and return data as list of lists."""
    txt_path = os.path.join(section_folder, f"{basename}_{section}.txt") # path to section  file
    if not os.path.isfile(txt_path):
        print(f"WARNING: Section file not found: {txt_path}") 
        return []
    
    with open(txt_path) as f:
        return [line.strip().split('\t') for line in f if line.strip() and len(line.strip().split('\t')) > 1] # read non-empty lines with at least 2 columns
    
def plot_allele_frequency(data, output_path, title=None):
    """Create scatter plot of allele frequency distribution."""
    try:
        df = pd.DataFrame(data)[[2, 3]].astype(float).dropna()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(df[2], df[3], color='#4285F4', s=60) # Scatter plot customisation
        # Add labels to each point (rounded allele freq)
        for x, y in zip(df[2], df[3]):
            ax.text(x, y, f'{x:.2f}', fontsize=9, ha='center', 
                    va='bottom', color='#333333', rotation=45) # Label each point with allele frequency
        ax.set(title='Allele Frequency Distribution', xlabel='Non-reference Allele Frequency', ylabel='Number of Variant Sites')
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"Created: {output_path}")
    except Exception:
        print("Allele Frequency: Data format error, skipping plot.") # informative error message

def plot_depth_distribution(data, output_path, title="Depth Distribution"):
    """Create line plot of read depth distribution."""
    try:
        df = pd.DataFrame(data)[[2, 3]].copy() # Create a copy of the relevant columns 
        df = df[df[2].apply(lambda x: str(x)[0].isdigit() if str(x) else False)] # Filter rows where depth starts with a digit
        df[2] = pd.to_numeric(df[2], errors='coerce')  # Convert to numeric, replace invalid values with NaN
        df[3] = pd.to_numeric(df[3], errors='coerce')
        df = df.dropna() # Remove rows with NaN values
        ax = df.plot(x=2, y=3, kind='line', marker='o', markersize=4, linewidth=2, color='#2E86AB', legend=False, figsize=(10, 6))
        ax.fill_between(df[2], df[3], alpha=0.3, color='#2E86AB')
        ax.set(title=title, xlabel='Read Depth', ylabel='Number of Genotypes')
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.set_xlim(left=0)
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white') 
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("Depth Distribution: Data format error, skipping plot.")

def plot_quality_scores(data, output_path, title):
    """Create line plot of quality score distribution for SNPs and Indels."""
    try:
        
        df = pd.DataFrame(data)[[2, 3, 4]].astype(float).dropna()
        ax = df.plot(x=2, y=3, kind='line', marker='o', markersize=4, 
                     linewidth=2, label='SNPs', color='#A23B72', figsize=(14, 8))
        df.plot(x=2, y=4, kind='line', marker='s', markersize=4, 
                linewidth=2, label='Indels', color='#F18F01', ax=ax) # Add indels to same plot
        ax.set(xlabel='Quality Score', ylabel='Count', title=f'Quality Score Distribution - {title}')
        ax.legend(fontsize=12, frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim(left=0, right=400) # Set x-axis limits for better visualisation
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("Quality Scores: Data format error, skipping plot.")

def plot_indel_distribution(data, output_path, title):
    """Create bar plot of indel length distribution."""
    try:
        
        df = pd.DataFrame(data)[[2, 3]].astype(float).dropna()
        df[2] = df[2].astype(int) # Indel lengths should be integers
        colors = ['#C73E1D' if val < 0 else '#6A994E' for val in df[2]] 
        ax = df.plot.bar(x=2, y=3, color=colors, alpha=0.8, edgecolor='black', linewidth=0.5, legend=False, figsize=(14, 8))
        ax.set(xlabel='Indel Length (bp)', ylabel='Count', title=f'Indel Length Distribution - {title}')
        labels = [str(val) if i % 5 == 0 else '' for i, val in enumerate(df[2])] # Label every 5th bar for clarity
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=10) #
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("Indel Distribution: Data format error, skipping plot.")

def plot_tstv_ratio(data, output_path, title):
    """Create bar plot of transition/transversion statistics."""
    try:
        
        df = pd.DataFrame(data).dropna()
        ts, tv, ratio = int(df.iloc[0, 2]), int(df.iloc[0, 3]), float(df.iloc[0, 4])
        ax = pd.DataFrame({'Type': ['Transitions', 'Transversions'], 'Count': [ts, tv]}).plot.bar(
            x='Type', y='Count', color=['#6A4C93', '#F18F01'], alpha=0.8, edgecolor='black', linewidth=1.2, legend=False, figsize=(10, 6))
        [ax.text(i, val, f'{val:,}', ha='center', va='bottom', fontweight='bold', fontsize=12) for i, val in enumerate([ts, tv])] # Annotate bars with counts
        ax.set(ylabel='Count', title=f'Transition/Transversion Statistics - {title}')
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.legend([f'Ts/Tv ratio: {ratio:.2f}'], fontsize=12, frameon=True, shadow=True, loc='upper right')
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("TSTV Ratio: Data format error, skipping plot.")

def plot_substitution_types(data, output_path, title):
    """Create horizontal bar plot of substitution types."""
    try:
        
        df = pd.DataFrame(data)[[2, 3]].copy()
        df[3] = pd.to_numeric(df[3], errors='coerce') 
        df = df.dropna()
        colors = plt.cm.Set3(range(len(df)))
        ax = df.plot.barh(x=2, y=3, color=colors, alpha=0.8, edgecolor='black', linewidth=0.8, legend=False, figsize=(12, 8))
        ax.set_ylabel('Substitution Type', fontsize=14, fontweight='bold')
        ax.set_xlabel('Count', fontsize=14, fontweight='bold')
        ax.set_title(f'Substitution Types - {title}', fontsize=16, fontweight='bold', pad=20)
        ax.set_yticklabels(df[2], fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--', axis='x')
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("Substitution Types: Data format error, skipping plot.")

def plot_per_sample_counts(data, output_path, title):
    """Create grouped bar plot of SNP and indel counts per sample."""
    try:
        
        df = pd.DataFrame(data)
        snp = pd.to_numeric(df[3], errors='coerce')
        indel = pd.to_numeric(df[4], errors='coerce')
        snp_err = pd.to_numeric(df[5], errors='coerce') if df.shape[1] > 5 else None
        indel_err = pd.to_numeric(df[6], errors='coerce') if df.shape[1] > 6 else None
        samples = df[2]
        width = 0.35
        x = range(len(df))
        fig, ax = plt.subplots(figsize=(12, 8))
        # First set of bars (SNPs) - positioned to the LEFT
        # Second set of bars (Indels) - positioned to the RIGHT
        ax.bar([i - width/2 for i in x], snp, width, 
               label='SNPs', alpha=0.8, edgecolor='black', 
               linewidth=0.8, color='#A23B72', yerr=snp_err if snp_err is not None else None, capsize=5) #error bars
        ax.bar([i + width/2 for i in x], indel, width, 
               label='Indels', alpha=0.8, edgecolor='black', 
               linewidth=0.8, color='#F18F01', yerr=indel_err if indel_err is not None else None, capsize=5) #error bars
        ax.set_xlabel('Sample', fontsize=14, fontweight='bold')
        ax.set_ylabel('Count', fontsize=14, fontweight='bold')
        ax.set_title(f'Per Sample Counts - {title}', fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x) # Set the positions where labels appear
        ax.set_xticklabels(samples, rotation=45, ha='right', fontsize=11)
        ax.legend(fontsize=12, frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("Per Sample Counts: Data format error, skipping plot.")

def plot_per_sample_indels(data, output_path, title):
    """Create grouped bar plot of insertions and deletions per sample."""
    try:
        df = pd.DataFrame(data)[[2, 7, 8]].copy()
        df[7] = pd.to_numeric(df[7], errors='coerce')
        df[8] = pd.to_numeric(df[8], errors='coerce')
        df = df.dropna()
        width = 0.35
        x = range(len(df))
        fig, ax = plt.subplots(figsize=(10, 8))
        # First set of bars (Insertions) - positioned to the LEFT
        # Second set of bars (Deletions) - positioned to the RIGHT
        ax.bar([i - width/2 for i in x], df[7], width, 
               label='Heterozygous Indel Genotypes', alpha=0.8, edgecolor='black', linewidth=0.8, color='#6A994E')
        ax.bar([i + width/2 for i in x], df[8], width, 
               label='Homozygous Alternate Indel Genotypes', alpha=0.8, edgecolor='black', linewidth=0.8, color='#C73E1D')
        ax.set_xlabel('Sample', fontsize=14, fontweight='bold')
        ax.set_ylabel('Genotype counts', fontsize=14, fontweight='bold')
        ax.set_title(f'Per Sample Indels - {title}', fontsize=16, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(df[2], rotation=45, ha='right', fontsize=11)
        ax.legend(fontsize=12, frameon=True, shadow=True, loc='lower center', bbox_to_anchor=(0.5, -0.4)) #Legend positioning
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("Per Sample Indels: Data format error, skipping plot.")

def plot_hwe(data, output_path, title):
    """Create Hardy-Weinberg equilibrium plot with confidence intervals."""
    try:
        df = pd.DataFrame(data)
        af = df[2].astype(float)
        p25 = df[4].astype(float)
        median = df[5].astype(float)
        p75 = df[6].astype(float)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(af, median, color='#FF6B35', label='Median')
        ax.fill_between(af, p25, p75, color='#FF6B35', alpha=0.2, label='25-75th percentile')
        ax.set_xlabel('Allele Frequency', fontsize=14, fontweight='bold')
        ax.set_ylabel('Fraction of heterozygotes', fontsize=14, fontweight='bold')
        ax.legend(fontsize=12)
        plt.title(f'HWE - {title}', fontsize=15, fontweight='bold', pad=18)
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        plt.close()
        print(f"  Created: {output_path}")
    except Exception:
        print("HWE: Data format error, skipping plot.")

def plot_sis(data, output_path, title):
    """Create pie chart of singleton SNPs (SiS) with Ts/Tv ratio."""
    try:
        df = pd.DataFrame(data)
        row = df.iloc[0]
        snp_total = int(row[3])
        ts = max(0, int(row[4]))
        tv = max(0, int(row[5]))
        ratio = ts / tv if tv else float('inf')
        values, labels, colors = [ts, tv], ["Transitions (Ts)", "Transversions (Tv)"], ["#60a5fa", "#57f63b"]
        fig, ax = plt.subplots(figsize=(6, 6))
        explode = [0.12, 0]
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, 
               colors=colors, explode=explode, wedgeprops={"edgecolor": "white"}, 
               textprops={"fontsize": 12}, shadow=True) # Pie chart customisation
        ax.set_title(f"Singleton SNPs (SiS)\n{title}\nTotal SNP singletons: {snp_total:,}", fontsize=13, fontweight="bold", pad=16)
        ax.add_artist(plt.Circle((0, 0), 0.70, color='white', fc='white', linewidth=0)) # White circle to create donut chart effect
        ax.text(0, -1.15, f"Ts/Tv ratio: {ratio:.2f}", ha="center", va="center", fontsize=13, fontweight="bold") # Add Ts/Tv ratio below pie chart
        ax.axis("equal")
        plt.tight_layout()
        plt.savefig(output_path, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close(fig)
        print(f"  Created: {output_path}")
    except Exception:
        print(f"SiS: parse error in {title}")

def generate_plots_from_txt(output_folder, basename, sections=None):
    """
    Generate plots for specified sections from their .txt files.

    Parameters:
        output_folder: Path to the folder containing section subfolders and .txt files.
        basename: Base name for the files (e.g., 'data1').
        sections: List of section tags to plot (e.g., ['AF', 'DP']).
            If None, plots all available sections.

    Workflow:
        1. Determines which sections to plot based on the 'sections' argument.
        2. For each section, reads the corresponding .txt file from its subfolder.
        3. Calls the appropriate plotting function for each section.
        4. Saves each plot as a .png file in the corresponding section subfolder.
        5. Prints status messages for user feedback.
    """
    
    plot_functions = {
        'AF': plot_allele_frequency,
        'DP': plot_depth_distribution,
        'QUAL': plot_quality_scores,
        'IDD': plot_indel_distribution,
        'TSTV': plot_tstv_ratio,
        'ST': plot_substitution_types,
        'PSC': plot_per_sample_counts,
        'PSI': plot_per_sample_indels,
        'HWE': plot_hwe,
        'SiS': plot_sis,
    }
    if sections is None:
        sections_to_plot = [s for s in plot_functions.keys()]
    else:
        sections_to_plot = [s for s in sections if s in plot_functions]
    print(f"Generating plots for: {', '.join(sections_to_plot)}")
    failed_sections = []
    for section in sections_to_plot:
        section_folder = os.path.join(output_folder, section)
        os.makedirs(section_folder, exist_ok=True)
        data = read_section_txt(section_folder, section, basename)
        if not data:
            failed_sections.append(section)
            continue
        output_path = os.path.join(section_folder, f"{basename}_{section}.png")
        try:
            plot_functions[section](data, output_path, basename)
        except Exception:
            failed_sections.append(section)
    if failed_sections:
        print(f"\nWARNING: The following plots failed or had missing data: {', '.join(failed_sections)}")
    if len(failed_sections) < len(sections_to_plot):
        print(f"\nSUCCESS: All other plots saved to their section folders in: {output_folder}")
    else:
        print(f"\nNo plots were successfully created.")
    print(f"Output: {output_folder}/")

def main():
    """Main function for generating plots from parsed section .txt files."""
    
    section_tags = ["AF", "DP", "QUAL", "IDD", "TSTV", "ST", "PSC", "PSI", "HWE", "SiS"]
    parser = argparse.ArgumentParser(description="Generate plots from section .txt files")
    parser.add_argument("output_folder", help="Output folder containing section subfolders and .txt files")
    parser.add_argument("basename", nargs="?", default=None, help="Base name for the files (e.g., data1). If not provided, will try to auto-detect.")
    parser.add_argument("--sections", "-s", nargs='+', help="Specific sections to plot (default: all available). Accepts lowercase or uppercase (e.g., af dp qual)")
    parser.add_argument("-all", "--all", action="store_true", help="Generate all plots (default behavior)")
    for tag in section_tags:
        parser.add_argument(f"-{tag.lower()}", action="append_const", const=tag, dest="section_flags", help=f"Plot only {tag} section") # Add individual section flags
    args = parser.parse_args()
    # Auto-detect basename if not provided
    basename = args.basename
    if not basename:
        for section in section_tags:
            section_folder = os.path.join(args.output_folder, section)
            if os.path.isdir(section_folder): # only check existing folders
                for fname in os.listdir(section_folder): # list all files in the section folder
                    if fname.endswith(f"_{section}.txt"):# found a matching file 
                        basename = fname[:-(len(section)+5)] # strip _SECTION.txt
                        break
            if basename:
                break
        if not basename:
            print("ERROR: Could not auto-detect basename. Please specify it explicitly.")
            print("Usage: python make_plots.py <output_folder> [basename] [--sections ...]")
            sys.exit(7)
            
    # Collect all section flags
    sections = [] 
    if args.sections:
        sections += [s.upper() for s in args.sections]
    if getattr(args, "section_flags", None):
        sections += args.section_flags
    if not sections or args.all:
        sections = None
    generate_plots_from_txt(args.output_folder, basename, sections)
    
if __name__ == "__main__":
    main()

#cd "C:\PY\Python Project"
# python run_analysis.py "DATA\\data1.vchk" "output" -all
#