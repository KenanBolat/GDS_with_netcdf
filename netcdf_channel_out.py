#!/usr/bin/python3
from __future__ import print_function
from netCDF4 import Dataset
import h5py
import xarray
import os
import glob
import datetime
import numpy as np
import multiprocessing as mp
s = datetime.datetime.now()
import os
import sys 
import mode_selector as mode_selector

def resample_it(lat, lon, data, file_str, channel,  output_path = "/external/b/HSAF/OFFLINE/H35/input"):

    date_ = datetime.datetime.strptime(file_str.split("_")[4],"%Y%m%d%H%M%S")
    date_str =date_.strftime("%Y%m%d")
    time_str =date_.strftime("%H%M")
    from pyresample import kd_tree, image, geometry
    _p_type = 'M01'

    area_def = geometry.AreaDefinition('a', 'b', 'c', {'proj': 'longlat'}, 35999, 8999, [-180, 0, 180, 90]);
    swath_def = geometry.SwathDefinition(lons=lon, lats=lat)
    swath_con = image.ImageContainerNearest(data, swath_def, radius_of_influence=5000)
    area_con = swath_con.resample(area_def)
    # area_con = kd_tree.resample_nearest(swath_def, data.ravel(), area_def, radius_of_influence = 5000, nprocs = 10)
    im_data = area_con.image_data
    with h5py.File(os.path.join(output_path,
                                "eps_" + _p_type + "_" +
                                date_str + "_" +
                                time_str + "_" +
                                time_str + '__' +
                                str(channel) + '.hdf'), 'w') as h5file:
        h5file.create_dataset('/' + str(channel), shape=im_data.shape, dtype=im_data.dtype, data=im_data)


process_path = r"/home/knn/Desktop/somedata"
# start = datetime.datetime.now()


# for en, row in enumerate(glob.glob1(process_path, "*.nc")):
#     lat = []
#     lon = []
#
#     print(row)
#     f = xarray.open_dataset(os.path.join(process_path, row))
#     # if row == 'W_XX-EUMETSAT-Darmstadt,HIRES+RADIOMETER,METOPA+AVHR_C_EUMP_20200111051133_68641_eps_o_l1b.nc':
#
#     lat = np.vstack((f.lat.data))
#     lon = np.vstack((f.lon.data))
#     data = np.vstack((f.scene_radiances1.data))
#     resample_it(lat, lon, np.array(data * 100, dtype="int16"))
#
#     print(f.lat.shape)



def resampleAll(file):
    channels = ['1', '2', 'a', '4', '5']
    for i in channels:
        flag = ''
        if i == 'a':
            flag = '3'
        start = datetime.datetime.now()
        print(" {} started at {}".format(file, start))
        f = xarray.open_dataset(os.path.join(process_path, file))
        lat = np.vstack((f.lat.data))
        lon = np.vstack((f.lon.data))
        data = np.vstack((f['scene_radiances{}'.format(flag + i)].data))
        resample_it(lat, lon, np.array(data * 100, dtype="int16"), file_str=file, channel=i)
        end = datetime.datetime.now()
        print(" {} ended at {} and took {}".format(file, end, end - start))


if __name__ == "__main__":
    # process_path = r"/home/off/HSAF_SRC/offline/H35/input"
    process_path = r"/external/b/HSAF/OFFLINE/H35/raw"
    # input_path = "/external/b/HSAF/OFFLINE/H35/input/"
    input_path = r"/external/b/HSAF/OFFLINE/H35/input"
    incr = 4
    for compressed in mode_selector.working_date:
        files = glob.glob1(process_path, "*_C_EUMP_{}*.nc".format(compressed))
        for f in range(0, len(files), incr):
            files_in = files[f:f+incr]
            N = mp.cpu_count()
            with mp.Pool(processes=N) as p:
                results = p.map(resampleAll, [file for file in files_in])
        os.chdir(input_path)
        cmd = "tar -czvf "+"{}_avhrr_h35_extent.tar.gz".format(compressed)+" eps_M01_"+compressed+"_*.hdf --remove-files";
        print(cmd)
        os.system(cmd);

