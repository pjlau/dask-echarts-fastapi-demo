# src/backend/data_processing.py
import dask.dataframe as dd
import pandas as pd

def load_and_process_data(file_path: str):
    # Load CSV with Dask
    df = dd.read_csv(file_path)
    
    # Compute unique nodes
    sources = df['source'].unique().compute().tolist()
    targets = df['target'].unique().compute().tolist()
    nodes = list(set(sources + targets))
    
    # Create node list for ECharts
    nodes_data = [{"name": node} for node in nodes]
    
    # Create links for Sankey
    links_data = df.groupby(['source', 'target'])['value'].sum().reset_index().compute()
    links_data = links_data.to_dict(orient='records')
    
    return {"nodes": nodes_data, "links": links_data}