# callbacks.py - Define all the callback functions for interactivity.

from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_leaflet as dl
from dash import html, dcc
import pandas as pd
from data_processing import get_data  # Import data processing function

# Register callbacks with the app
def register_callbacks(app):

    # Callback to update the data table based on the selected filter type
    @app.callback(
        Output('datatable-id', 'data'),         # Updates data displayed in the data table
        Output('datatable-id', 'columns'),      # Updates column structure of the data table
        [Input('filter-type', 'value')]         # Triggered by the filter selection dropdown
    )
    def update_datatable(filter_type):
        # Fetch data based on the selected filter type
        df = get_data(filter_type)
        
        # Define column headers for the data table
        columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
        
        # Convert DataFrame to a list of dictionaries for the data table
        data = df.to_dict('records')
        
        return data, columns

    # Callback to update the pie chart based on the data in the data table
    @app.callback(
        Output('graph-id', "children"),         # Updates the pie chart section of the app
        [Input('datatable-id', "derived_virtual_data")]  # Triggered by changes in the data table
    )
    def update_graphs(viewData):
        # Check if there is data to display; if not, show an empty pie chart
        if viewData is None or len(viewData) == 0:
            return [dcc.Graph(figure=px.pie(names=[], title='Preferred Animals'))]

        # Create a DataFrame from the data table's data
        dff = pd.DataFrame.from_dict(viewData)
        
        # If the DataFrame is empty, show an empty pie chart
        if dff.empty:
            return [dcc.Graph(figure=px.pie(names=[], title='Preferred Animals'))]

        # Count the occurrences of each breed in the data
        breed_counts = dff['breed'].value_counts()
        
        # Limit the chart to the top 10 breeds, grouping the rest as "Other"
        if len(breed_counts) > 10:
            top_breeds = breed_counts.nlargest(10)
            dff['breed'] = dff['breed'].apply(lambda x: x if x in top_breeds.index else 'Other')

        # Generate the pie chart
        fig = px.pie(dff, names='breed', title='Preferred Animals')
        return [dcc.Graph(figure=fig)]

    # Callback to update the map based on the selected row in the data table
    @app.callback(
        Output('map-id', "children"),           # Updates the map section of the app
        [Input('datatable-id', "derived_virtual_data"),   # Triggered by changes in data table data
         Input('datatable-id', "derived_virtual_selected_rows")]  # Triggered by row selection
    )
    def update_map(viewData, selected_rows):
        # If no data or row is selected, show the default map centered on Austin, TX
        if viewData is None or selected_rows is None or len(selected_rows) == 0:
            return [
                dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75, -97.48], zoom=10, children=[
                    dl.TileLayer(id="base-layer-id"),
                ])
            ]

        # Create a DataFrame from the data table's virtual data
        dff = pd.DataFrame.from_dict(viewData)
        
        # Get the index of the selected row
        row = selected_rows[0]

        # Ensure the required columns for map display exist in the DataFrame
        required_columns = ['location_lat', 'location_long', 'breed', 'name']
        if not all(col in dff.columns for col in required_columns):
            return [html.Div("Required data is missing from the DataFrame.")]

        # Retrieve the latitude, longitude, breed, and name of the selected animal
        lat = dff.loc[row, 'location_lat']
        lon = dff.loc[row, 'location_long']
        breed = dff.loc[row, 'breed']
        name = dff.loc[row, 'name']

        # Use default coordinates (Austin, TX) if lat/lon are missing or invalid
        if pd.isnull(lat) or pd.isnull(lon):
            lat, lon = 30.75, -97.48

        # Generate the map with a marker for the selected animal's location
        return [
            dl.Map(style={'width': '1000px', 'height': '500px'}, center=[lat, lon], zoom=10, children=[
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(position=[lat, lon], children=[
                    dl.Tooltip(breed),              # Tooltip with the animal breed
                    dl.Popup([                      # Popup with animal's name
                        html.H1("Animal Name"),
                        html.P(name)
                    ])
                ])
            ])
        ]

    # Callback to highlight selected columns in the data table
    @app.callback(
        Output('datatable-id', 'style_data_conditional'),  # Updates style based on selected columns
        [Input('datatable-id', 'selected_columns')]        # Triggered by column selection in data table
    )
    def update_styles(selected_columns):
        # Highlight selected columns with a light blue background color
        return [{
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        } for i in selected_columns]

