import xarray
import matplotlib.pyplot as plt
import scipy.misc
from xarray import Dataset

f_ = r"/external/b/HSAF_archive_bak_191212/h35_extract/h35_20190513_day_merged.grib2"

grbs= xarray.open_dataset(f_, engine='cfgrib')
print(grbs)
# # a_=xs.get("rssc")
# # x_show = plt.imshow(a_)


# scipy.misc.toimage(a_, cmin=0.0, cmax=).save('outfile.jpg')
