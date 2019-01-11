import cartopy
import numpy
import matplotlib.pyplot as plt

def xyz2ll(x,y,z):
    i_r = 1/numpy.sqrt(x*x + y*y + z*z)
    sinlat = z*i_r
    recip_coslat = 1/numpy.sqrt(1 - sinlat**2)
    sinlon = (y*i_r)*recip_coslat
    coslon = (x*i_r)*recip_coslat
    rad2deg = 180/numpy.pi
    lat = numpy.arcsin(sinlat)*rad2deg
    sgn = numpy.maximum(numpy.sign(coslon),0)
    lon0 = numpy.arcsin(sinlon)*rad2deg
    lon1 = 180-numpy.arcsin(sinlon)*rad2deg
    return (1-sgn)*lon1+sgn*lon0,lat
def ll2xyz(lon,lat):
    deg2rad = numpy.pi/180
    coslat = numpy.cos(deg2rad*lat)
    return coslat*numpy.cos(deg2rad*lon), coslat*numpy.sin(deg2rad*lon), numpy.sin(deg2rad*lat)
def roty(x,y,z,a):
    deg2rad = numpy.pi/180
    ca,sa = numpy.cos(deg2rad*a), numpy.sin(deg2rad*a)
    return ca*x-sa*z,y,ca*z+sa*x
def rotz(x,y,z,a):
    deg2rad = numpy.pi/180
    ca,sa = numpy.cos(deg2rad*a), numpy.sin(deg2rad*a)
    return ca*x-sa*y,ca*y+sa*x,z
def drw_circles(subplot, projection, w=0.23, lw=3):
    a = numpy.linspace(0,2*numpy.pi,32)
    x,y,z=1,w*numpy.cos(a),w*numpy.sin(a)
    ax=plt.subplot(subplot, projection=projection)
    ax.plot(*xyz2ll(x,y,z),transform=cartopy.crs.PlateCarree(),linewidth=lw)
    ax.plot(*xyz2ll(*roty(x,y,z,60)),transform=cartopy.crs.PlateCarree(),linewidth=lw)
    ax.plot(*xyz2ll(*roty(x,y,z,-60)),transform=cartopy.crs.PlateCarree(),linewidth=lw)
    ax.plot(*xyz2ll(*rotz(x,y,z,60)),transform=cartopy.crs.PlateCarree(),linewidth=lw)
    ax.plot(*xyz2ll(*rotz(x,y,z,-60)),transform=cartopy.crs.PlateCarree(),linewidth=lw)
    ax.plot(*xyz2ll(*rotz(x,y,z,-120)),transform=cartopy.crs.PlateCarree(),linewidth=lw)
    ax.plot(*xyz2ll(*rotz(x,y,z,120)),transform=cartopy.crs.PlateCarree(),linewidth=lw)
    ax.plot([-180,180,0,0],[0,0,89,-89],'w.',transform=cartopy.crs.PlateCarree())
    drw_lines(ax)
    ax.coastlines()
def drw_lines(ax, lon0=-70, lat0=-70, lon1=70, lat1=70, lw=2, ls='--', np=64):
    # Straight line in lat-lon space
    lons, lats = numpy.linspace(lon0, lon1, np), numpy.linspace(lat0, lat1, np)
    ax.plot(lons,lats,ls,transform=cartopy.crs.PlateCarree(),linewidth=lw)
    # Straight line in Mercator
    x0,y0 = cartopy.crs.Mercator().transform_point(lon0,lat0,cartopy.crs.PlateCarree())
    x1,y1 = cartopy.crs.Mercator().transform_point(lon1,lat1,cartopy.crs.PlateCarree())
    xs, ys = numpy.linspace(x0, x1, np), numpy.linspace(y0, y1, np)
    ax.plot(xs,ys,ls,transform=cartopy.crs.Mercator(),linewidth=lw)
    # Straight line in NearsidePerspective
    x0,y0,z0 = ll2xyz(lon0,lat0)
    x1,y1,z1 = ll2xyz(lon1,lat1)
    a = numpy.linspace(0,1,np)
    lons,lats = xyz2ll(x0 + (x1-x0)*a, y0 + (y1-y0)*a, z0 + (z1-z0)*a)
    ax.plot(lons,lats,ls,transform=cartopy.crs.PlateCarree(),linewidth=lw)
plt.figure(figsize=(10,10))
drw_circles(221, cartopy.crs.NearsidePerspective() ); plt.title('1a) Perspective')
drw_circles(222, cartopy.crs.PlateCarree() ); plt.title('1b) Equirectangular (Plate-Carrée)')
drw_circles(223, cartopy.crs.Robinson() ); plt.title('1c) Robinson')
drw_circles(224, cartopy.crs.Mercator() ); plt.title('1d) Mercator')

plt.tight_layout()
