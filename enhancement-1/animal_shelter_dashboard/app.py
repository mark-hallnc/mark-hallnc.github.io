# app.py - Initialize the Dash app and set up the server. This file is the entry point for the application.

from dash import Dash
import dash_html_components as html
from layouts import app_layout
from callbacks import register_callbacks

app = Dash(__name__)
server = app.server  

app.layout = app_layout

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)