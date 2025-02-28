import os
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import glob
import geopandas as gpd

# 设置路径（使用原始字符串）
data_folder = r"E:\4_nc\ssp126_rsds\15-29_rsds_ssp126"  # 替换为你的SSP126数据文件夹路径
output_folder = r"E:\picture"  # 替换为保存图像和NetCDF文件的文件夹路径

# 定义时段（仅2015-2029）
period = "2015-2029"
time_slice = slice("2015-01-01", "2029-12-31")

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# 读取并处理数据
def process_data(data_folder, time_slice):
    # 查找文件
    file_pattern = "*.nc"
    file_path = os.path.join(data_folder, file_pattern)
    files = sorted(glob.glob(file_path))

    if not files:
        print(f"No files found for {period}. Files in directory:")
        for file in glob.glob(os.path.join(data_folder, "*")):
            print(file)
        return None

    try:
        # 读取数据，显式指定后端引擎
        ds = xr.open_mfdataset(files, combine="by_coords", engine="netcdf4")
        rsds = ds["rsds"].sel(time=time_slice)

        # 计算时段均值
        rsds_mean = rsds.mean(dim="time", skipna=True)

        # 保存时段均值为NetCDF文件
        output_nc_path = os.path.join(output_folder, f"rsds_mean_{period}.nc")
        rsds_mean.to_netcdf(output_nc_path)
        print(f"Saved {output_nc_path}")

        return rsds_mean
    except Exception as e:
        print(f"Error reading or processing data: {e}")
        return None

# 绘制空间分布图
def plot_spatial_distribution(rsds_mean, title, output_path):
    # 定义投影
    projn = ccrs.LambertConformal(central_longitude=105,
                                  central_latitude=40,
                                  standard_parallels=(25.0, 47.0))

    # 读取中国地图的GeoJSON文件
    geojson_path = r"E:\china_geo\中国_省.geojson"
    if not os.path.exists(geojson_path):
        print(f"文件 {geojson_path} 不存在")
        return

    china_shape = gpd.read_file(geojson_path)

    # 创建图形
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection=projn)

    # 设置地图范围
    extents = [73.4375, 135.3125, 17.75, 53.75]
    ax.set_extent(extents, crs=ccrs.PlateCarree())

    # 添加中国地图边界
    ax.add_geometries(china_shape["geometry"], crs=ccrs.PlateCarree(),
                      facecolor='none', edgecolor='k', linewidth=.6)

    # 绘制rsds均值
    rsds_mean.plot(ax=ax, transform=ccrs.PlateCarree(), cmap="viridis", cbar_kwargs={"label": "rsds (W/m²)"})

    # 设置标题
    ax.set_title(title)

    # 添加经纬网
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False  # 取消顶部标签
    gl.right_labels = False  # 取消右侧标签
    gl.xformatter = LongitudeFormatter()
    gl.yformatter = LatitudeFormatter()

    # 添加南海小地图
    # 其中 (0, 0) 是图形的左下角，(1, 1) 是图形的右上角
    ax2 = fig.add_axes([0.62, 0.17, 0.12, 0.25], projection=projn) # 设置小地图的坐标和比例
    ax2.set_extent([104.5, 125, 0, 26]) # 设置小地图的地理范围
    ax2.add_geometries(china_shape["geometry"], crs=ccrs.PlateCarree(),
                       facecolor='none', edgecolor='k', linewidth=.3)

    # 保存图像
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

# 主函数
def main():
    # 处理数据
    rsds_mean = process_data(data_folder, time_slice)

    if rsds_mean is not None:
        # 绘制空间分布图
        title = f"rsds Mean ({period}, SSP126)"
        output_path = os.path.join(output_folder, f"rsds_mean_{period}.png")
        plot_spatial_distribution(rsds_mean, title, output_path)

if __name__ == "__main__":
    main()