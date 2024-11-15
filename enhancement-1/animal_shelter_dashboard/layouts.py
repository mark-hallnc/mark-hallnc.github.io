# layouts.py - Define the layout of the application.

import base64
from dash import Dash, dcc, html, dash_table

# Read the logo image file and encode it to base64
image_filename = 'Grazioso Salvare Logo.png'  
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Initialize the Dash app with a custom title
app = Dash(__name__)
app.title = "Grazioso Salvare"  # Sets the browser tab title to "Grazioso Salvare"

# Define the layout structure of the application
app_layout = html.Div([

    # Header Section with aligned image and title
    html.Div([
        # Inner div to align logo image and title horizontally
        html.Div([
            html.Img(  # Logo image
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={'width': '80px', 'height': 'auto', 'margin-right': '20px'}  # Logo styling
            ),
            html.H1('Animal Shelter Dashboard', style={'margin': '0', 'color': '#2c3e50'}),  # Dashboard title styling
        ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),  # Flex styling for horizontal alignment
        html.Hr(),  # Horizontal line separator
    ], style={'backgroundColor': '#f8f9fa', 'padding': '10px'}),  # Header section styling

    # Filter Section with dropdown for rescue type selection
    html.Div([
        # Label for the filter dropdown
        html.Label('Filter by Rescue Type:', style={'font-weight': 'bold', 'font-size': '16px', 'color': '#2c3e50'}),
        # Dropdown menu for filter selection
        dcc.Dropdown(
            id='filter-type',
            options=[  # Dropdown options
                {'label': 'Water Rescue', 'value': 'Water Rescue'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain or Wilderness Rescue'},
                {'label': 'Disaster or Individual Tracking', 'value': 'Disaster or Individual Tracking'},
                {'label': 'Reset', 'value': 'Reset'}
            ],
            value='Reset',  # Default value
            placeholder="Select a filter",
            style={'width': '100%', 'margin-top': '10px'}  # Dropdown styling
        )
    ], style={'padding': '20px', 'backgroundColor': '#e9ecef', 'border-radius': '8px', 'margin': '10px'}),  # Filter section styling

    # Data Table Section
    html.Div([
        dash_table.DataTable(
            id='datatable-id',  
            columns=[],  # Placeholder for columns, to be set dynamically
            data=[],     # Placeholder for data, to be set dynamically
            row_selectable='single',  # Allows single row selection
            selected_rows=[0],        # Default selected row
            page_size=10,             # Number of rows per page
            sort_action="native",     # Enables data sorting
            style_table={'overflowX': 'auto', 'border': '1px solid #dee2e6', 'border-radius': '8px'},  # Table styling
            style_header={
                'backgroundColor': '#2c3e50',  # Header background color
                'color': 'white',              # Header text color
                'fontWeight': 'bold'           # Header font weight
            },
            style_cell={
                'textAlign': 'left',           # Cell text alignment
                'padding': '8px',              # Cell padding
                'backgroundColor': '#f8f9fa',  # Cell background color
                'border': '1px solid #dee2e6'  # Cell border styling
            },
            # Conditional styling to alternate row colors
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},  # Style for odd rows
                    'backgroundColor': '#e9ecef'
                }
            ]
        )
    ], style={'padding': '20px', 'margin': '10px'}),  # Data table section styling

    # Graph and map section
    html.Div(className='row', style={'display': 'flex', 'padding': '20px'}, children=[
        # Graph container with styling
        html.Div(
            id='graph-id',
            className='col s12 m6',  # Column styling for responsive layout
            style={
                'flex': '1', 
                'padding': '10px', 
                'backgroundColor': '#f8f9fa', 
                'border-radius': '8px', 
                'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'  # Shadow effect for card-like appearance
            }
        ),
        # Map container with styling
        html.Div(
            id='map-id',
            className='col s12 m6',  # Column styling for responsive layout
            style={
                'flex': '1', 
                'padding': '10px', 
                'backgroundColor': '#f8f9fa', 
                'border-radius': '8px', 
                'box-shadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'  # Shadow effect for card-like appearance
            }
        )
    ])
])

# Assign the layout to the app
app.layout = app_layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)  # Start the Dash app in debug mode



