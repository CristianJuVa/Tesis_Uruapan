import pygmt
import pandas as pd

# firstly we need to import the coodinates of the stations
data = pd.read_csv("estaciones_decimal.txt", sep = " ", names=["name","latitude", "longitude", "Alt"])

#Earthquakes Mw>4.0
sismos = pd.read_csv("sismos.txt", sep = " ", names=["latitude", "longitude", "depth_km"])

#Map generation wit PYGMT
#KWARGS = dict(grid='etopo1_bedrock.grd', region=[-105,-98,16,23.5], projection='M10i', 
 #                     cmap='verde.cpt', frame=0)

#txt legend
#leyend = b.read_csv("estaciones_decimal.txt", sep = " ",
                   
# Set the region of the map
 #region = [xmin,xmax,ymin,ymax]
region = [
    int(data.longitude.min()) - 0.6, #izquierda
    int(data.longitude.min()) + 6.7, #derecha
    int(data.latitude.min()), #- 0.1, #para abajo
    21,#int(data.latitude.max())+ 1.5,#21 menos una estación, #arriba
]


topo_data = '@earth_relief_15s' #30 arc second global relief (SRTM15+V2.1 @ 1.0 km)



fig = pygmt.Figure()

# make color pallets
pygmt.makecpt(
    cmap='topo',
    series='-8000/8000/1000',
    continuous=True
)

#plot high res topography
fig.grdimage(
    grid=topo_data,
    region=region, 
    projection='M4i',
    shading=True,
    frame=True
    )
# plot coastlines
fig.coast(
    region=region, 
    projection='M4i', 
    shorelines=True,
    frame=True
    )
# plot topo contour lines
fig.grdcontour(
    grid=topo_data,
    interval=4000,
    annotation="4000+f6p",
    # annotation="1000+f6p",
    limit="-8000/0",
    pen="a0.10p"
    )


# plot stations 
fig.plot(
    x=data.longitude, y=data.latitude, style='"t0.2c"', 
    color='red', pen='black',label='Estaciones sismológicas',
    )

#Plotting earthquakes
fig.plot(x=sismos.longitude, y=sismos.latitude, style="a0.2c", fill="yellow", pen="black", label='Sismos Mw=4.0')

## Plot colorbar
# Default is horizontal colorbar
fig.colorbar(position="JMB+005C/0c+w5c/0.2c+",frame=["x+lTopografía", "y+lm"])
#text of Mw>4.0
fig.text(x=-102.33, y=19.36,position=None,text='4.0', angle=0,
        font='4.5p,Helvetica-Bold,black', justify='LM')

#station names
fig.text(textfiles=None,x=data.longitude-0.1, y=data.latitude+0.13, position=None,text=data.name,  
 angle=0, font='3p,Helvetica-Bold,black', justify='LM')

#Legend
fig.legend()

#rose and scale of the map
with pygmt.config(FONT_TITLE=8):
    fig.basemap(rose="jTL+w1.3c+lO,W,N,N+o-0.1c/3c", map_scale="jBL+w100k+o0.5c/0.5c+f") 
            #   rose="jTL+w1.3c+lO,W,N,N+o-0.1c/3c"
# save figure as pdf
#fig.savefig("map.jpg", crop=True, dpi=720)

#save figure as png
fig.savefig("estaciones.jpg")