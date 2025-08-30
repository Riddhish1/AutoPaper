import requests
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image
import json

def download_image_from_url(url: str, filename: str, output_dir: str = "E:\\nothing\\AutoPaper\\output\\images") -> str:
    """
    Download an image from a URL and save it to the output directory.
    
    Args:
        url: URL of the image to download
        filename: Name to save the image as (with extension)
        output_dir: Directory to save the image in
    
    Returns:
        Path to the saved image file
    """
    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Download image
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Save image
        image_path = output_path / filename
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Image downloaded and saved to: {image_path}")
        return str(image_path)
        
    except Exception as e:
        print(f"Error downloading image: {e}")
        raise

def create_research_plot(data_type: str, title: str, filename: str, output_dir: str = "E:\\nothing\\AutoPaper\\output\\images") -> str:
    """
    Create various types of research plots commonly used in academic papers.
    
    Args:
        data_type: Type of plot ('comparison', 'performance', 'distribution', 'timeline')
        title: Title for the plot
        filename: Name to save the plot as (without extension)
        output_dir: Directory to save the plot in
    
    Returns:
        Path to the saved plot file
    """
    try:
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Set style for academic papers
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(8, 6))
        
        if data_type == 'comparison':
            # Create a comparison bar chart
            methods = ['Method A', 'Method B', 'Method C', 'Proposed Method']
            accuracy = [0.85, 0.88, 0.82, 0.92]
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            
            bars = ax.bar(methods, accuracy, color=colors, alpha=0.8)
            ax.set_ylabel('Accuracy')
            ax.set_title(title)
            ax.set_ylim(0.8, 0.95)
            
            # Add value labels on bars
            for bar, acc in zip(bars, accuracy):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                       f'{acc:.3f}', ha='center', va='bottom')
        
        elif data_type == 'performance':
            # Create a performance line plot
            x = np.linspace(0, 100, 50)
            baseline = 0.7 + 0.2 * np.exp(-x/30) + 0.05 * np.random.randn(50)
            proposed = 0.75 + 0.15 * np.exp(-x/25) + 0.03 * np.random.randn(50)
            
            ax.plot(x, baseline, 'o-', label='Baseline Method', linewidth=2)
            ax.plot(x, proposed, 's-', label='Proposed Method', linewidth=2)
            ax.set_xlabel('Training Epochs')
            ax.set_ylabel('Loss')
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        elif data_type == 'distribution':
            # Create a distribution plot
            np.random.seed(42)
            data1 = np.random.normal(100, 15, 1000)
            data2 = np.random.normal(110, 12, 1000)
            
            ax.hist(data1, bins=30, alpha=0.7, label='Group A', density=True)
            ax.hist(data2, bins=30, alpha=0.7, label='Group B', density=True)
            ax.set_xlabel('Value')
            ax.set_ylabel('Density')
            ax.set_title(title)
            ax.legend()
        
        elif data_type == 'timeline':
            # Create a timeline plot
            years = list(range(2015, 2025))
            values = [10, 15, 22, 35, 45, 52, 68, 75, 82, 90]
            
            ax.plot(years, values, 'o-', linewidth=3, markersize=8)
            ax.set_xlabel('Year')
            ax.set_ylabel('Performance Metric')
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save plot
        plot_path = output_path / f"{filename}.png"
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Plot saved to: {plot_path}")
        return str(plot_path)
        
    except Exception as e:
        print(f"Error creating plot: {e}")
        raise

def generate_latex_figure_code(image_path: str, caption: str, label: str, width: str = "0.8\\columnwidth") -> str:
    """
    Generate LaTeX code for including a figure in IEEE format.

    Args:
        image_path: Path to the image file (can be absolute or relative)
        caption: Figure caption
        label: Figure label for referencing
        width: Width specification for the figure

    Returns:
        LaTeX code for the figure
    """
    # Convert path to relative path from output directory for LaTeX
    image_path = Path(image_path)

    if image_path.is_absolute():
        # Check if it's in the AutoPaper output/images directory
        if "E:\\nothing\\AutoPaper\\output\\images" in str(image_path):
            relative_path = f"images/{image_path.name}"
        else:
            # For other absolute paths, just use the filename
            relative_path = f"images/{image_path.name}"
    else:
        # For relative paths, ensure they point to images directory
        if not str(image_path).startswith("images/"):
            relative_path = f"images/{image_path}"
        else:
            relative_path = str(image_path)

    latex_code = f"""\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width={width}]{{{relative_path}}}
\\caption{{{caption}}}
\\label{{{label}}}
\\end{{figure}}"""

    return latex_code

def create_table_latex(caption: str, label: str, table_type: str = "results") -> str:
    """
    Generate LaTeX code for a table in IEEE format with sample data.

    Args:
        caption: Table caption
        label: Table label for referencing
        table_type: Type of table ('results', 'comparison', 'parameters')

    Returns:
        LaTeX code for the table
    """

    if table_type == "results":
        headers = ["Method", "Accuracy", "Precision", "Recall", "F1-Score"]
        data = [
            ["Baseline", "0.75", "0.73", "0.77", "0.75"],
            ["Method A", "0.82", "0.80", "0.84", "0.82"],
            ["Method B", "0.78", "0.76", "0.80", "0.78"],
            ["Proposed", "0.91", "0.89", "0.93", "0.91"]
        ]
    elif table_type == "comparison":
        headers = ["Feature", "Previous Work", "Our Approach"]
        data = [
            ["Accuracy", "85.2\\%", "92.1\\%"],
            ["Speed", "2.3s", "1.1s"],
            ["Memory", "512MB", "256MB"],
            ["Complexity", "O(n²)", "O(n log n)"]
        ]
    elif table_type == "parameters":
        headers = ["Parameter", "Value", "Description"]
        data = [
            ["Learning Rate", "0.001", "Initial learning rate"],
            ["Batch Size", "32", "Training batch size"],
            ["Epochs", "100", "Maximum training epochs"],
            ["Dropout", "0.2", "Dropout probability"]
        ]
    else:
        # Default results table
        headers = ["Method", "Performance", "Notes"]
        data = [
            ["Baseline", "75.0\\%", "Standard approach"],
            ["Proposed", "91.0\\%", "Our novel method"]
        ]

    num_cols = len(headers)
    col_spec = "c" * num_cols

    # Create header row
    header_row = " & ".join(headers) + " \\\\"

    # Create data rows
    data_rows = []
    for row in data:
        data_rows.append(" & ".join(str(cell) for cell in row) + " \\\\")

    latex_code = f"""\\begin{{table}}[htbp]
\\centering
\\caption{{{caption}}}
\\label{{{label}}}
\\begin{{tabular}}{{{col_spec}}}
\\toprule
{header_row}
\\midrule
{chr(10).join(data_rows)}
\\bottomrule
\\end{{tabular}}
\\end{{table}}"""

    return latex_code
