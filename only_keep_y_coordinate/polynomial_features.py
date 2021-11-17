# https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html
from sklearn.preprocessing import PolynomialFeatures
# Generate a new feature matrix consisting of all polynomial combinations of the features with degree less than or equal to the specified degree

poly = PolynomialFeatures(2) # maximal degree of the polynomial feature
