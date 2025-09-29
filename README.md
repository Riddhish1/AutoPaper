# AutoPaper 📝

An AI-powered research paper generation system that automatically searches for academic papers, analyzes research trends, and generates IEEE-formatted research papers with interactive visualizations.

## 🌟 Overview

AutoPaper is an intelligent research assistant that combines the power of large language models (Google Gemini) with academic databases (arXiv) to create comprehensive research papers. The system not only generates static PDF documents but also creates interactive dashboards and visualizations to complement the research findings.

## ✨ Key Features

### 🔍 **Intelligent Research**
- **ArXiv Integration**: Automatic paper search and retrieval from arXiv
- **PDF Analysis**: Extract and analyze text content from research papers
- **Research Gap Identification**: AI-powered analysis to identify promising research directions
- **Literature Review**: Automated synthesis of related work

### 📄 **Professional Paper Generation**
- **IEEE Format**: Proper IEEE conference paper formatting with LaTeX
- **Mathematical Equations**: Full LaTeX math support for complex formulas
- **Citation Management**: Automatic IEEE-style citation formatting
- **Structured Layout**: Complete paper sections (Abstract, Introduction, Methodology, Results, etc.)

### 📊 **Rich Visualizations**
- **Academic Plots**: Performance comparisons, distribution charts, timeline graphs
- **Interactive Dashboards**: Web-based dashboards with multiple visualization types
- **Custom Flowcharts**: Research methodology and process diagrams
- **LaTeX Figures**: Properly formatted figures with captions and labels

### 🎯 **Advanced Analytics**
- **Method Comparison**: Side-by-side performance analysis
- **Quality Assessment**: Radar charts for paper quality evaluation
- **Performance Tracking**: Training curves and convergence plots
- **Data Tables**: IEEE-formatted tables with professional styling

## 🏗️ Architecture

```
AutoPaper/
├── backend/
│   ├── ai_researcher.py      # Main AI research orchestrator with LangGraph
│   ├── arxiv_tool.py         # ArXiv search and paper retrieval
│   ├── read_pdf.py           # PDF text extraction and analysis
│   ├── write_pdf.py          # LaTeX PDF generation and rendering
│   ├── image_tools.py        # Research plot generation and image handling
│   ├── write_dash.py         # Interactive dashboard creation
│   ├── main.py               # Application entry point
│   ├── .env                  # Environment configuration
│   ├── pyproject.toml        # Project dependencies
│   └── output/               # Generated papers and visualizations
│       ├── images/           # Generated plots and figures
│       └── *.pdf             # Generated research papers
```

## 🚀 Installation

### Prerequisites
- Python 3.11+
- MiKTeX or TeX Live (for LaTeX compilation)
- Google Gemini API key

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AutoPaper/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Configure environment**
   Create a `.env` file in the backend directory:
   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

5. **Install LaTeX (Required for PDF generation)**
   - **Windows**: Install MiKTeX from https://miktex.org/
   - **Linux**: `sudo apt-get install texlive-full`
   - **Mac**: Install MacTeX from https://tug.org/mactex/

## 🎮 Usage

### Quick Start

1. **Run the main application**
   ```bash
   python ai_researcher.py
   ```

2. **Interactive Research Session**
   The AI will guide you through:
   - Topic selection and research focus
   - Paper discovery and analysis
   - Research gap identification
   - Paper generation with visualizations

### Example Workflow

```
User: I want to research machine learning in healthcare
AI: → Searches arXiv for recent papers
    → Presents top papers with summaries
    → Analyzes selected papers for research gaps
    → Proposes novel research directions
    → Generates IEEE-formatted paper with interactive dashboard
```

### Individual Tool Usage

#### ArXiv Search
```python
from arxiv_tool import arxiv_search
papers = arxiv_search("machine learning healthcare")
```

#### PDF Analysis
```python
from read_pdf import read_pdf
content = read_pdf("https://arxiv.org/pdf/2301.12345.pdf")
```

#### Generate Research Plots
```python
from image_tools import create_research_plot
plot_path = create_research_plot(
    data_type="comparison",
    title="Method Performance Comparison",
    filename="performance_plot"
)
```

#### Create Interactive Dashboard
```python
from write_dash import create_research_dashboard
dashboard_url = create_research_dashboard(
    title="ML Healthcare Research Dashboard"
)
```

## 📊 Visualization Types

### Static Plots
- **Comparison Charts**: Bar charts comparing different methods
- **Performance Graphs**: Line plots showing training/validation curves
- **Distribution Plots**: Histograms and density plots
- **Timeline Charts**: Progress over time visualizations

### Interactive Dashboards
- **Multi-tab Interface**: Organized visualization sections
- **Methodology Flowcharts**: Step-by-step research process
- **Performance Analysis**: Dynamic training curves
- **Quality Ratings**: Radar charts for paper assessment

### LaTeX Integration
- **Figure Generation**: Automatic LaTeX figure code generation
- **Table Creation**: IEEE-formatted tables with professional styling
- **Caption Management**: Proper figure and table referencing

## 🔧 Configuration

### LaTeX Setup
The system requires pdflatex for PDF generation. Update the path in `write_pdf.py`:

```python
# Update this path to your pdflatex installation
pdflatex_path = r"C:\Users\bonde\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"
```

### Output Directories
- **Papers**: `backend/output/paper_YYYYMMDD_HHMMSS.pdf`
- **Images**: `backend/output/images/`
- **Dashboards**: Running on `http://localhost:8050`

## 🧠 AI Research Engine

### LangGraph Architecture
The system uses LangGraph for orchestrating the research workflow:

```python
# State management for multi-step research
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Tool integration
tools = [
    arxiv_search,           # Paper discovery
    read_pdf,              # Content analysis
    render_latex_pdf,      # PDF generation
    create_research_plot,  # Visualization
    # ... more tools
]
```

### Available Research Tools
1. **Literature Search**: `arxiv_search()` - Find relevant papers
2. **Content Analysis**: `read_pdf()` - Extract and analyze paper content
3. **PDF Generation**: `render_latex_pdf()` - Create IEEE-formatted papers
4. **Image Tools**: Download and generate research figures
5. **Visualization**: Create plots, tables, and interactive dashboards

## 📋 Dependencies

### Core Libraries
- **LangChain**: AI orchestration and tool integration
- **LangGraph**: State management for complex workflows
- **Google Gemini**: Large language model for research analysis
- **PyPDF2**: PDF text extraction
- **Requests**: HTTP requests for arXiv API

### Visualization
- **Matplotlib**: Static plot generation
- **Seaborn**: Statistical visualizations
- **Plotly**: Interactive charts and graphs
- **Dash**: Web-based dashboard framework
- **Pandas/NumPy**: Data manipulation and analysis

### Document Generation
- **LaTeX**: Professional document formatting
- **Python-dotenv**: Environment variable management

## 🎯 Research Domains

The system is optimized for research in:
- **Physics & Mathematics**
- **Computer Science & AI**
- **Quantitative Biology**
- **Quantitative Finance**
- **Statistics & Data Science**
- **Electrical Engineering**
- **Systems Science**
- **Economics**

## 📄 Output Examples

### Generated Papers
- IEEE-formatted research papers with proper structure
- Mathematical equations and formulas
- Professional figures and tables
- Comprehensive bibliography and citations

### Interactive Components
- Performance analysis dashboards
- Research methodology flowcharts
- Method comparison visualizations
- Quality assessment radar charts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Review existing GitHub issues
3. Create a new issue with detailed description

## 🔧 Troubleshooting

### Common Issues

**LaTeX Compilation Errors**
- Ensure MiKTeX/TeX Live is properly installed
- Check the pdflatex path in `write_pdf.py`
- Verify all required LaTeX packages are available

**API Rate Limiting**
- ArXiv API has rate limits - add delays between requests
- Google Gemini API quota limits may apply

**Dashboard Not Loading**
- Check if port 8050 is available
- Ensure all Dash dependencies are installed
- Try a different port if conflicts occur

**PDF Extraction Issues**
- Some PDFs may have complex layouts
- Try different papers if extraction fails
- Check network connectivity for PDF downloads

## 🔮 Future Enhancements

- Support for additional academic databases (PubMed, IEEE Xplore)
- Multi-language paper generation
- Collaborative research features
- Advanced citation analysis
- Integration with reference managers (Zotero, Mendeley)
- Real-time collaboration on research papers

---

**AutoPaper** - Transforming academic research with AI-powered automation 🚀