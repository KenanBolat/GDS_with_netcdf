
import glob
from datetime import timedelta
import os
import h5py
import numpy as np
import datetime
import pandas as pd

# region constants: Same with h_10
SNOW = 0
CLOUD = 42
LAND = 85
SEA = 170
NODATA = 255
# endregion

start = datetime.datetime.now()
mode = "HSAF_34"


if mode == 'HSAF_34':
    # Looks for the merged product
    working_path = r'/external/b/HSAF_archive_bak_191212/h34_extract'
elif mode == "TSMS":
    # Looks for the Mountainous product (Unmerged TSMS produced)
    working_path = r'/external/b/TSMS_archive/h10_HDF'

start_day = datetime.datetime.strptime("20190425", "%Y%m%d")
end_day = datetime.datetime.strptime("20191209", "%Y%m%d")
date_list_h34 = [start_day + timedelta(n) for n in range(int((end_day - start_day).days) + 1)]

d_s_format = "%Y%m%d"
H5_files = [file_ for file_ in glob.glob1(working_path, "*.H5")]
result = []

important_values = [0, 42, 85]

for en, date_ in enumerate(date_list_h34):
    print(datetime.datetime.now() - start)
    merge = 0
    date_in = date_.strftime(d_s_format)
    try:
        match = list(filter(lambda x: x.find(date_in) != -1, H5_files))
        if len(match) > 0:
            hf_h34= h5py.File(os.path.join(working_path, match[0]), 'r')
            data_h34 = hf_h34['SC']
            test_points = [data_h34[585, 2876],
                           data_h34[594, 2861],
                           data_h34[579, 2777],
                           data_h34[410, 2087],
                           data_h34[441, 2029]]
            if all(item in important_values for item in test_points):
                a = np.unique(data_h34, return_counts=True)
                unique, counts = np.unique(data_h34, return_counts=True)
                b = dict(zip(unique, counts / data_h34.size * 100))

                data_count = data_h34.size
                merge = 1
            else:
                print("There is problem in merging")
            c = ['H34', date_in, merge, b[SNOW], b[CLOUD], b[LAND], b[SEA], b[NODATA], data_h34.size]
            c.extend(test_points)
            result.append(c)
        else:
            result.append(['H34', date_in, merge, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    except BaseException as be:
        print("Problem")
        merge = be
        result.append(['H34', date_in, merge, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        continue

print(datetime.datetime.now() - start)

data_frame = pd.DataFrame(result,
                          columns=['Product', "Date", "MERGE", "SNOW %", "CLOUD %", "LAND %", "SEA %", "NODATA %",
                                   "DATA Count", "Test_P_1" , "Test_P_2", "Test_P_3", "Test_P_4", "Test_P_5"])
data_frame.to_csv(datetime.datetime.now().strftime(d_s_format) +"_"+mode+ ".csv")

# düzgün çalışıyor sıkıntı yok