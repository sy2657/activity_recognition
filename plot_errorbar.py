# sept 13 plot 

# combine into 1 errorbar plot


fig, ax = plt.subplots(3, 1, figsize=(12, 6))


timevec = np.arange(smax_t)

# x
for a in activities:
    xseries_t = x_allperson_averaged[a]
    xstd_t = x_allperson_std[a]
    # uplims=True, lolims=True,
    ax[0].errorbar(timevec, xseries_t, yerr=xstd_t,alpha=0.5,capsize=3) #mark markersize=1) #uplims=True, lolims=True)
    yseries_t = y_allperson_averaged[a]
    ystd_t = y_allperson_std[a]
    zseries_t = z_allperson_averaged[a]
    zstd_t = z_allperson_std[a]
    ax[1].errorbar(timevec, yseries_t, yerr=ystd_t)# , marker=".", markersize=1)
    ax[2].errorbar(timevec, zseries_t, yerr=zstd_t)#, marker=".", markersize=1)
    
    
    #plt.scatter(timevec, xseries_t)

"""plt.legend(loc='lower right')

plt.xlabel("frame number")
plt.ylabel("x coordinate value")
plt.title("put back item")"""
ax[0].set_ylabel("x coordinate", fontsize=10)
ax[1].set_ylabel("y coordinate", fontsize=10)
ax[2].set_xlabel("frame number", fontsize=10)
ax[2].set_ylabel("z coordinate", fontsize=10)

plt.xlim((0, 1000))

labels = ["open/close fridge", "screen interaction"]

fig.legend(labels, loc='upper right')

plt.show()


