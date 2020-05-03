import os
import pandas as pd

data = 'probe_data_map_matching'

def main():

    link_cols = ['']
    probe_cols = ['sampleID', 'dataTime']
    link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'))
    probe_data = pd.read_csv(os.path.join(data, 'Partition6467ProbePoints.csv'))



if __name__ == 'main':
    main()
