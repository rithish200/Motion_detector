from detect import df

from bokeh.plotting import figure, show, output_file 
from bokeh.models import HoverTool, ColumnDataSource

df["st"] = df["Entry Time"]
df["en"] = df["Exit Time"]

cds = ColumnDataSource(df)

f = figure(height = 100, width = 500, x_axis_type = "datetime", title = "Detect-Motion", sizing_mode = "scale_both")

hover = HoverTool(tooltips = [("Object Visibility", ""),("From","@st"),("To","@en")])
f.add_tools(hover)

fig = f.quad(left = "Entry(for Plot)", right = "Exit(for Plot)", top = 1, bottom = 0, color = "red", source = cds)

f.yaxis.minor_tick_line_color = None
f.yaxis[0].ticker.desired_num_ticks = 1
f.xaxis.visible = False

output_file("plot.html")
show(f)