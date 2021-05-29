
# ffmpeg -start_number 1 -r 35 -f image2 -s 1920x1080 -i %08d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -vcodec libx264 -preset veryslow -crf 15 -pix_fmt yuv420p OUTPUT_PATH.mp4 
# https://scitools.org.uk/cartopy/docs/latest/matplotlib/intro.html

imagery = cimgt.GoogleTiles() 
imagery = OSM()

ptsNum = len(track)
xy = fun.getRouteArray(route).T
for tix in range(1, ptsNum):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_axes([0, 0, 0.5, 0.5], projection=ccrs.PlateCarree())
    
    ax.set_facecolor("black")
    ax.imshow(plt.imread(pth), extent=[cLon-pad, cLon+pad, cLat-pad, cLat+pad])
    ax.set_extent(
        [cLon-pad, cLon+pad, cLat-pad, cLat+pad], 
        crs=ccrs.PlateCarree()
    )
    plt.plot(
        xy[0][:tix], xy[1][:tix],
        color=cmap(norm(xy[3][tix])) , 
        alpha=.5,
        linewidth=1, solid_capstyle='round',
        transform=ccrs.Geodetic()
    )
    if POINTS:
        for c in range(1, tix):
            plt.plot(
                xy[0][c], xy[1][c],
                color=cmap(norm(xy[3][c])), 
                alpha=1,
                marker='o', markersize=.75,
                transform=ccrs.Geodetic()
            )
    tixPad = str(tix).zfill(4)
    fimgName = path.join(PATH, 'img', '{}-{}.png'.format(fName, tixPad))
    fig.savefig(fimgName, dpi=250, bbox_inches='tight', pad_inches=0)
    plt.cla() 
    plt.clf() 
    plt.close(fig)
    plt.gcf()

tix = ptsNum
fig = plt.figure(figsize=(12, 12))
ax = fig.add_axes([0, 0, 0.5, 0.5], projection=ccrs.PlateCarree())
# ax.set_facecolor("black")
ax.set_extent(
    [cLon-pad, cLon+pad, cLat-pad, cLat+pad], 
    crs=ccrs.PlateCarree()
)
plt.plot(
    xy[0], xy[1],
    color=cmap(meanRoute['speed']) , 
    alpha=.5,
    linewidth=1, solid_capstyle='round',
    transform=ccrs.Geodetic()
)
if POINTS:
    for c in range(1, tix):
        plt.plot(
            xy[0][c], xy[1][c],
            color=cmap(norm(xy[3][c])), 
            alpha=1,
            marker='o', markersize=.75,
            transform=ccrs.Geodetic()
        )
tixPad = str(tix).zfill(4)
fimgName = path.join(PATH, 'img', '{}-{}.png'.format(fName, 'final'))
fig.savefig(fimgName, dpi=250, bbox_inches='tight', pad_inches=0, transparent=True)
plt.close(fig)