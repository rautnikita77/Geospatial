# from Slope_Estimation.utils import load_pickle
#
# data = load_pickle('/Users/anupamtripathi/PycharmProjects/Geospatial/Slope_Estimation/data/probe_dict_128_zones_10000_samples.pkl')
# print(data[14350])


from sklearn.metrics import r2_score

print(r2_score([0.3, 0.6], [0.3, 0.6]))
print(r2_score([0.2, 0.5], [0.4, 0.7]))
print(r2_score([0.3, 0.6, 0.2, 0.5], [0.3, 0.6, 0.4, 0.7]))