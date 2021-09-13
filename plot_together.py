#minhui plot


fig, ax = plt.subplots(3, 1, figsize=(12, 6))

people = [1, 2, 3, 4, 5, 7, 8, 9]

for p in people:
    xseries_total = x_tot[p]
    yseries_total = y_tot[p]
    zseries_total = z_tot[p]
    ax[0].plot(timevec, xseries_total, marker=".", markersize=3)
    ax[1].plot(timevec, yseries_total, marker=".", markersize=3)
    ax[2].plot(timevec, zseries_total, marker=".", markersize=3)

ax[0].set_ylabel("x coordinate", fontsize=10)
ax[1].set_ylabel("y coordinate", fontsize=10)
ax[2].set_xlabel("frame number", fontsize=10)
ax[2].set_ylabel("z coordinate", fontsize=10)

labels = ["person 1", "person 2", "person 3", "person 4", "person 5", "person 7", "person 8",
          "person 9"]
# labels_first5 = ["person 1", "person 2", "person 3", "person 4", "person 5"]
fig.legend(labels, loc='upper right')
fig.suptitle("put back item")
