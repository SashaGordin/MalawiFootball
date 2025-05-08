import pandas as pd
import numpy as np
import plotly.express as px
from preswald import Workflow, text, table, plotly, connect, get_df
import os

# Create a workflow instance
workflow = Workflow()

@workflow.atom()
def load_data():
    connect()
    data_folder = 'data'  # Folder where your dataset is located
    file_path = os.path.join(data_folder, 'Dataset_Malawi_National_Football_Team_Matches.csv')
    
    # Load the dataset using pandas
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        text(f"Error loading data: {str(e)}")
        return None

@workflow.atom(dependencies=['load_data'])
def analyze_data(load_data):
    df = load_data
    if df is not None:
        # Log data structure
        text("## Data Analysis of Malawi National Football Team Matches")
        text(f"Columns in the dataset: {df.columns.tolist()}")
        text("Dataset shape: " + str(df.shape))
        text("Column types:\n" + df.dtypes.to_string())
        text("First 10 rows of the data:")
        table(df.head(10))
        
        # Convert scores if they're not already numeric
        df['Team Score'] = pd.to_numeric(df['Team Score'], errors='coerce')
        df['Opponent Score'] = pd.to_numeric(df['Opponent Score'], errors='coerce')
        
        # Create a count of matches for each score combination
        score_counts = df.groupby(['Team Score', 'Opponent Score']).size().reset_index(name='Count')

        wins = df[df['Result'] == 'Win']
        text("**Filtered Data (Wins)**")
        table(wins)
        
        return df  # Return the original dataframe for visualization
    else:
        text("Data is None, cannot proceed with analysis.")
        return None

@workflow.atom(dependencies=['analyze_data'])
def visualize_data(analyze_data):
    df = analyze_data
    if df is not None:
        try:          
            # Add jitter to scores to avoid overplotting identical points
            jitter_amount = 0.1
            df['Team Score Jittered'] = df['Team Score'] + (np.random.rand(len(df)) * jitter_amount - jitter_amount/2)
            df['Opponent Score Jittered'] = df['Opponent Score'] + (np.random.rand(len(df)) * jitter_amount - jitter_amount/2)
            
            # Create the scatter plot
            fig = px.scatter(
                df,
                x='Opponent Score Jittered',
                y='Team Score Jittered',
                hover_data={
                    'Team Score': True,
                    'Opponent Score': True,
                    'Team Score Jittered': False,
                    'Opponent Score Jittered': False,
                    'Opponent': True,
                    'Date': True,
                    'Result': True
                },
                color='Result',
                title='Malawi National Football Team Scores',
                labels={
                    'Team Score Jittered': 'Team Score',
                    'Opponent Score Jittered': 'Opponent Score'
                },
                size_max=15
            )
            
            # Add a diagonal line representing equal scores (draws)
            score_max = max(df['Team Score'].max(), df['Opponent Score'].max()) + 1
            fig.add_shape(
                type="line",
                x0=0, y0=0,
                x1=score_max, y1=score_max,
                line=dict(color="gray", dash="dash"),
                opacity=0.5
            )
            
            # Add annotations for regions
            fig.add_annotation(
                x=score_max*0.75, y=score_max*0.25,
                text="Losses",
                showarrow=False,
                font=dict(size=14)
            )
            fig.add_annotation(
                x=score_max*0.25, y=score_max*0.75,
                text="Wins",
                showarrow=False,
                font=dict(size=14)
            )
            
            # Improve layout
            fig.update_layout(
                xaxis_title="Opponent Score",
                yaxis_title="Team Score",
                xaxis=dict(range=[-0.5, score_max]),
                yaxis=dict(range=[-0.5, score_max]),
                legend_title="Match Result"
            )
            
            try:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                # Filter out rows with invalid dates
                df_time = df.dropna(subset=['Date'])
                
                if not df_time.empty:
                    # Create a time series plot
                    fig_time = px.line(
                        df_time.sort_values('Date'),
                        x='Date',
                        y='Team Score',
                        title='Malawi Team Scores Over Time',
                        markers=True
                    )
                    
                    # Add opponent scores for comparison
                    fig_time.add_scatter(
                        x=df_time.sort_values('Date')['Date'],
                        y=df_time.sort_values('Date')['Opponent Score'],
                        mode='lines+markers',
                        name='Opponent Score'
                    )
                    
                    plotly(fig_time)
            except Exception as e:
                text(f"Could not create time series plot: {str(e)}")
            
            # Display the main scatter plot
            plotly(fig)
            
            # Create a bar chart of results
            result_counts = df['Result'].value_counts().reset_index()
            result_counts.columns = ['Result', 'Count']
            
            fig_results = px.bar(
                result_counts,
                x='Result',
                y='Count',
                title='Match Results Summary',
                color='Result'
            )
            
            plotly(fig_results)
            
        except Exception as e:
            text(f"Error creating or displaying the plot: {str(e)}")
            import traceback
            text(traceback.format_exc())
    else:
        text("Data is None, cannot create the plot.")

# Execute the workflow
workflow.execute()
