def stats(d, dim=3):
	tmp = []
	for i in range(dim):
		tmp += [np.mean(d[:, i]), np.std(d[:, i]), np.min(d[:, i]), np.max(d[:, i]), np.max(d[:, i]) - np.min(d[:, i]),
		        skew(d[:, i]), kurtosis(d[:, i]), np.sum(d[:, i])] + list(
			np.quantile(d[:, i], q=[v * 0.01 for v in range(0, 100, 10)]))
	return tmp
