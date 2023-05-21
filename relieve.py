import pygmt 
import pandas as pd

# firstly we need to import the coodinates of the stations
data = pd.read_csv("estaciones.txt", sep = " ", names=["name","latitude", "longitude"])

#Earthquakes Mw>4.0
sismos = pd.read_csv("sismos.txt", sep = " ", names=["latitude", "longitude", "km"])

# Load sample earth relief data
grid = pygmt.datasets.load_earth_relief(resolution="01m", region=[-102.65, -101.75, 19.30, 19.65])

fig = pygmt.Figure()

#Color

fig.grdimage(
   grid=grid,
    cmap="haxby",
    projection="Y35/30/15c",
    frame=True,
)

fig.grdcontour(
    annotation=500,
    interval=100,
    grid=grid,
    limit=[1000, 3200],
    frame=True,
)



# plot stations 
fig.plot(
    x=data.longitude, y=data.latitude, style='"t0.2c"', 
    color='red', pen='black',
    )

#station names
fig.text(textfiles=None,x=data.longitude-0.015, y=data.latitude+0.0095, position=None,text=data.name,  
 angle=0, font='6p,Helvetica-Bold,black', justify='LM')




pygmt.makecpt(cmap="viridis",
    series=[sismos.km.min(), 
            sismos.km.max()])

#Plotting earthquakes
fig.plot(x=sismos.longitude, y=sismos.latitude,
         fill=sismos.km,
         cmap=True,
         style="c0.15c", pen="black")


with pygmt.config(FONT_TITLE=8):
    fig.basemap(rose="jTL+w1.3c+lO,W,N,N+o-0.01c/3c", map_scale="jBL+w10k+o0.5c/0.5c+f") 



fig.savefig("relieve.jpg")