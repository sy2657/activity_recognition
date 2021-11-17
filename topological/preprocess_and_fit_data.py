hist_file="history_wrists" #nov 13

hist_wrist = load_file(hist_file)

# manually random split
dataset, users, activities, raw_files = hist_wrist['_1.mp4']

dataset2, users2, activities2, raw_files2 = hist_wrist['_2.mkv']

dataset3, users3, activities3, raw_files3 = hist_wrist['_3.mp4']

# create point cloud array 

pt_cloud_array = []

nrows = 100 
for i in range(nrows):
    series = dataset[i]
    x_ser = series[::3]
    y_ser = series[1::3]
    z_ser = series[2::3]
    pt_cloud_current = np.stack((x_ser, y_ser, z_ser), axis=-1)
    pt_cloud_array.append(pt_cloud_current)
    
# print shape
print(np.shape(pt_cloud_array))

# plot one of its rows
pt_cloud = pt_cloud_array[1]
plot_point_cloud(pt_cloud)

# fit
from gtda.homology import VietorisRipsPersistence

# Track connected components, loops, and voids
homology_dimensions = [0, 1, 2]

# Collapse edges to speed up H2 persistence calculation!
persistence = VietorisRipsPersistence(
    metric="euclidean",
    homology_dimensions=homology_dimensions,
    n_jobs=6,
    collapse_edges=True,
)

diagrams_basic = persistence.fit_transform(pt_cloud_array)

# plot
from gtda.plotting import plot_diagram

# Circle
plot_diagram(diagrams_basic[0])

# map to less # of pts
from gtda.diagrams import PersistenceEntropy

persistence_entropy = PersistenceEntropy()

# calculate topological feature matrix
X_basic = persistence_entropy.fit_transform(diagrams_basic)

# expect shape - (n_point_clouds, n_homology_dims)

print(X_basic.shape)

# train classifier, evaluate on same set

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(oob_score=True)
rf.fit(X_basic, activities100)

print(f"OOB score: {rf.oob_score_:.3f}")
