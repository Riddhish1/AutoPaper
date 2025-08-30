import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import webbrowser
import threading
import time
from pathlib import Path
import os

def create_research_dashboard(title: str, port: int = 8050) -> str:
    """
    Create an interactive research dashboard with flowcharts, graphs, and ratings.

    Args:
        title: Dashboard title
        port: Port to run the dashboard on

    Returns:
        URL of the running dashboard
    """

    app = dash.Dash(__name__)

    # Sample data generation based on config
    def generate_sample_data(chart_type):
        if chart_type == 'performance':
            return {
                'epochs': list(range(1, 101)),
                'training_loss': np.exp(-np.linspace(0, 3, 100)) + 0.1 * np.random.randn(100),
                'validation_loss': np.exp(-np.linspace(0, 2.8, 100)) + 0.15 * np.random.randn(100)
            }
        elif chart_type == 'comparison':
            return {
                'methods': ['Baseline', 'Method A', 'Method B', 'Proposed'],
                'accuracy': [0.75, 0.82, 0.78, 0.91],
                'precision': [0.73, 0.80, 0.76, 0.89],
                'recall': [0.77, 0.84, 0.80, 0.93]
            }
        elif chart_type == 'rating':
            return {
                'criteria': ['Novelty', 'Technical Quality', 'Clarity', 'Significance', 'Reproducibility'],
                'scores': [4.2, 4.5, 4.0, 4.3, 3.8],
                'max_score': 5.0
            }
        return {}

    # Create flowchart
    def create_flowchart():
        fig = go.Figure()

        # Define flowchart nodes
        nodes = [
            {'id': 'start', 'label': 'Data Collection', 'x': 1, 'y': 5},
            {'id': 'preprocess', 'label': 'Data Preprocessing', 'x': 1, 'y': 4},
            {'id': 'model', 'label': 'Model Training', 'x': 1, 'y': 3},
            {'id': 'evaluate', 'label': 'Evaluation', 'x': 1, 'y': 2},
            {'id': 'results', 'label': 'Results Analysis', 'x': 1, 'y': 1}
        ]

        # Add nodes
        for node in nodes:
            fig.add_shape(
                type="rect",
                x0=node['x']-0.3, y0=node['y']-0.2,
                x1=node['x']+0.3, y1=node['y']+0.2,
                fillcolor="lightblue",
                line=dict(color="darkblue", width=2)
            )
            fig.add_annotation(
                x=node['x'], y=node['y'],
                text=node['label'],
                showarrow=False,
                font=dict(size=12, color="black")
            )

        # Add arrows
        for i in range(len(nodes)-1):
            fig.add_annotation(
                x=nodes[i]['x'], y=nodes[i]['y']-0.3,
                ax=nodes[i+1]['x'], ay=nodes[i+1]['y']+0.3,
                arrowhead=2, arrowsize=1, arrowwidth=2,
                arrowcolor="darkblue"
            )

        fig.update_layout(
            title="Research Methodology Flowchart",
            xaxis=dict(range=[0, 2], showgrid=False, showticklabels=False),
            yaxis=dict(range=[0, 6], showgrid=False, showticklabels=False),
            showlegend=False,
            height=500
        )

        return fig

    # Create performance graph
    def create_performance_graph():
        data = generate_sample_data('performance')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data['epochs'],
            y=data['training_loss'],
            mode='lines',
            name='Training Loss',
            line=dict(color='blue', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=data['epochs'],
            y=data['validation_loss'],
            mode='lines',
            name='Validation Loss',
            line=dict(color='red', width=2)
        ))

        fig.update_layout(
            title="Model Performance Over Time",
            xaxis_title="Epochs",
            yaxis_title="Loss",
            hovermode='x unified',
            height=400
        )

        return fig

    # Create comparison chart
    def create_comparison_chart():
        data = generate_sample_data('comparison')

        fig = go.Figure()

        x = np.arange(len(data['methods']))
        width = 0.25

        fig.add_trace(go.Bar(
            x=[i - width for i in x],
            y=data['accuracy'],
            name='Accuracy',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            x=x,
            y=data['precision'],
            name='Precision',
            marker_color='lightgreen'
        ))
        fig.add_trace(go.Bar(
            x=[i + width for i in x],
            y=data['recall'],
            name='Recall',
            marker_color='lightcoral'
        ))

        fig.update_layout(
            title="Method Comparison",
            xaxis=dict(tickvals=x, ticktext=data['methods']),
            yaxis_title="Score",
            barmode='group',
            height=400
        )

        return fig

    # Create rating chart
    def create_rating_chart():
        data = generate_sample_data('rating')

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=data['scores'],
            theta=data['criteria'],
            fill='toself',
            name='Current Paper',
            line_color='blue'
        ))

        # Add maximum score reference
        fig.add_trace(go.Scatterpolar(
            r=[data['max_score']] * len(data['criteria']),
            theta=data['criteria'],
            fill='toself',
            name='Maximum Score',
            line_color='lightgray',
            opacity=0.3
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, data['max_score']]
                )
            ),
            title="Paper Quality Rating",
            height=500
        )

        return fig

    # Dashboard layout
    app.layout = html.Div([
        html.H1(title, style={'textAlign': 'center', 'marginBottom': 30}),

        # Tabs for different visualizations
        dcc.Tabs(id="tabs", value='flowchart', children=[
            dcc.Tab(label='Methodology Flowchart', value='flowchart'),
            dcc.Tab(label='Performance Analysis', value='performance'),
            dcc.Tab(label='Method Comparison', value='comparison'),
            dcc.Tab(label='Quality Rating', value='rating'),
        ]),

        html.Div(id='tab-content', style={'margin': 20})
    ])

    # Callback for tab content
    @app.callback(Output('tab-content', 'children'),
                  Input('tabs', 'value'))
    def render_content(tab):
        if tab == 'flowchart':
            return dcc.Graph(figure=create_flowchart())
        elif tab == 'performance':
            return dcc.Graph(figure=create_performance_graph())
        elif tab == 'comparison':
            return dcc.Graph(figure=create_comparison_chart())
        elif tab == 'rating':
            return dcc.Graph(figure=create_rating_chart())

    # Run the app
    def run_app():
        app.run_server(debug=False, port=port, host='127.0.0.1')

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_app)
    server_thread.daemon = True
    server_thread.start()

    # Wait a moment for server to start
    time.sleep(2)

    dashboard_url = f"http://127.0.0.1:{port}"

    # Open browser automatically
    webbrowser.open(dashboard_url)

    print(f"Research dashboard running at: {dashboard_url}")
    return dashboard_url

def create_custom_flowchart(title: str = "Custom Flowchart", port: int = 8051) -> str:
    """
    Create a custom flowchart for research methodology.

    Args:
        title: Flowchart title
        port: Port to run the dashboard on

    Returns:
        URL of the dashboard
    """

    app = dash.Dash(__name__)

    def create_custom_flow():
        fig = go.Figure()

        # Define sample nodes for research methodology
        nodes = [
            {'id': 'problem', 'label': 'Problem Definition', 'x': 1, 'y': 6},
            {'id': 'literature', 'label': 'Literature Review', 'x': 1, 'y': 5},
            {'id': 'hypothesis', 'label': 'Hypothesis Formation', 'x': 1, 'y': 4},
            {'id': 'methodology', 'label': 'Methodology Design', 'x': 1, 'y': 3},
            {'id': 'experiment', 'label': 'Experimentation', 'x': 1, 'y': 2},
            {'id': 'analysis', 'label': 'Data Analysis', 'x': 1, 'y': 1},
            {'id': 'conclusion', 'label': 'Conclusions', 'x': 1, 'y': 0}
        ]

        connections = [
            ('problem', 'literature'),
            ('literature', 'hypothesis'),
            ('hypothesis', 'methodology'),
            ('methodology', 'experiment'),
            ('experiment', 'analysis'),
            ('analysis', 'conclusion')
        ]

        # Add nodes
        for node in nodes:
            fig.add_shape(
                type="rect",
                x0=node['x']-0.4, y0=node['y']-0.2,
                x1=node['x']+0.4, y1=node['y']+0.2,
                fillcolor="lightblue",
                line=dict(color="darkblue", width=2)
            )
            fig.add_annotation(
                x=node['x'], y=node['y'],
                text=node['label'],
                showarrow=False,
                font=dict(size=10, color="black")
            )

        # Add connections
        node_dict = {node['id']: node for node in nodes}
        for from_id, to_id in connections:
            from_node = node_dict[from_id]
            to_node = node_dict[to_id]

            fig.add_annotation(
                x=from_node['x'], y=from_node['y']-0.25,
                ax=to_node['x'], ay=to_node['y']+0.25,
                arrowhead=2, arrowsize=1, arrowwidth=2,
                arrowcolor="darkblue"
            )

        fig.update_layout(
            title=title,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            showlegend=False,
            height=600
        )

        return fig

    app.layout = html.Div([
        html.H1(title, style={'textAlign': 'center'}),
        dcc.Graph(figure=create_custom_flow())
    ])

    # Run the app
    def run_app():
        app.run_server(debug=False, port=port, host='127.0.0.1')

    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_app)
    server_thread.daemon = True
    server_thread.start()

    # Wait a moment for server to start
    time.sleep(2)

    dashboard_url = f"http://127.0.0.1:{port}"
    webbrowser.open(dashboard_url)

    print(f"Custom flowchart running at: {dashboard_url}")
    return dashboard_url

def save_dashboard_plots_as_images(title: str = "Research Dashboard") -> list:
    """
    Save dashboard plots as static images for LaTeX inclusion.

    Args:
        title: Base title for the plots

    Returns:
        List of saved image file paths
    """

    # Ensure output directory exists
    output_dir = Path("E:\\nothing\\AutoPaper\\output\\images")
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    # Sample data generation
    def generate_sample_data(chart_type):
        if chart_type == 'performance':
            return {
                'epochs': list(range(1, 101)),
                'training_loss': np.exp(-np.linspace(0, 3, 100)) + 0.1 * np.random.randn(100),
                'validation_loss': np.exp(-np.linspace(0, 2.8, 100)) + 0.15 * np.random.randn(100)
            }
        elif chart_type == 'comparison':
            return {
                'methods': ['Baseline', 'Method A', 'Method B', 'Proposed'],
                'accuracy': [0.75, 0.82, 0.78, 0.91],
                'precision': [0.73, 0.80, 0.76, 0.89],
                'recall': [0.77, 0.84, 0.80, 0.93]
            }
        elif chart_type == 'rating':
            return {
                'criteria': ['Novelty', 'Technical Quality', 'Clarity', 'Significance', 'Reproducibility'],
                'scores': [4.2, 4.5, 4.0, 4.3, 3.8],
                'max_score': 5.0
            }
        return {}

    # 1. Save Performance Graph
    data = generate_sample_data('performance')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['epochs'],
        y=data['training_loss'],
        mode='lines',
        name='Training Loss',
        line=dict(color='blue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=data['epochs'],
        y=data['validation_loss'],
        mode='lines',
        name='Validation Loss',
        line=dict(color='red', width=2)
    ))
    fig.update_layout(
        title="Model Performance Over Time",
        xaxis_title="Epochs",
        yaxis_title="Loss",
        width=800,
        height=500
    )

    performance_path = output_dir / "performance_analysis.png"
    fig.write_image(str(performance_path), width=800, height=500, scale=2)
    saved_files.append(str(performance_path))

    # 2. Save Comparison Chart
    data = generate_sample_data('comparison')
    fig = go.Figure()

    x = np.arange(len(data['methods']))
    width = 0.25

    fig.add_trace(go.Bar(
        x=[i - width for i in x],
        y=data['accuracy'],
        name='Accuracy',
        marker_color='lightblue'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=data['precision'],
        name='Precision',
        marker_color='lightgreen'
    ))
    fig.add_trace(go.Bar(
        x=[i + width for i in x],
        y=data['recall'],
        name='Recall',
        marker_color='lightcoral'
    ))

    fig.update_layout(
        title="Method Comparison",
        xaxis=dict(tickvals=x, ticktext=data['methods']),
        yaxis_title="Score",
        barmode='group',
        width=800,
        height=500
    )

    comparison_path = output_dir / "method_comparison.png"
    fig.write_image(str(comparison_path), width=800, height=500, scale=2)
    saved_files.append(str(comparison_path))

    # 3. Save Rating Chart
    data = generate_sample_data('rating')
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=data['scores'],
        theta=data['criteria'],
        fill='toself',
        name='Current Paper',
        line_color='blue'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[data['max_score']] * len(data['criteria']),
        theta=data['criteria'],
        fill='toself',
        name='Maximum Score',
        line_color='lightgray',
        opacity=0.3
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, data['max_score']]
            )
        ),
        title="Paper Quality Rating",
        width=600,
        height=600
    )

    rating_path = output_dir / "quality_rating.png"
    fig.write_image(str(rating_path), width=600, height=600, scale=2)
    saved_files.append(str(rating_path))

    print(f"Saved {len(saved_files)} dashboard plots as images:")
    for file_path in saved_files:
        print(f"  - {file_path}")

    return saved_files