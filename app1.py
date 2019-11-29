import dash
import dash_table
import dash_core_components as dcc
import pandas as pd

df = pd.read_excel('output.xlsx')

app = dash.Dash(__name__)

	dcc.Slider(
		value=4, 
		min=-10, 
		max=20, step=0.5,
        marks={-5: '-5 Degrees', 0: '0', 10: '10 Degrees'})

if __name__ == '__main__':
    app.run_server(debug=True)
