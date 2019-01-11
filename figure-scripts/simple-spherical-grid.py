def drw_grid(subplot, projection, lw=1, dlon=30, dlat=30):
    ax=plt.subplot(subplot, projection=projection)
    z = numpy.linspace(0,1,128)
    lon0 = -int(180/dlon)*dlon
    # Grid lines
    for lon in range(lon0, 181, dlon):
        ax.plot(lon+0*z,-89+178*z,'k--',transform=cartopy.crs.PlateCarree(),linewidth=lw)
    lat0 = -int(89/dlon)*dlon
    for lat in range(lat0, 90, dlat):
        ax.plot(-180+360*z,lat+0*z,'k--',transform=cartopy.crs.PlateCarree(),linewidth=lw)
    # Dots for nodes
    for lat in range(lat0, 90, dlat):
        for lon in range(lon0, 181, dlon):
            ax.plot(lon,lat,'r.',transform=cartopy.crs.PlateCarree())
    ax.plot([-180,180,0,0],[0,0,89,-89],'w.',transform=cartopy.crs.PlateCarree())
    ax.coastlines()
plt.figure(figsize=(10,10))
drw_grid(221, cartopy.crs.NearsidePerspective() ); plt.title('Perspective')
drw_grid(222, cartopy.crs.PlateCarree() ); plt.title('Equirectangular (Plate-Carrée)')
drw_grid(223, cartopy.crs.NorthPolarStereo() ); plt.title('North Polar Stereographic')
w = 1e7; plt.xlim(-w,w); plt.ylim(-w,w)
drw_grid(224, cartopy.crs.Mercator() ); plt.title('Mercator')

