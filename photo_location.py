from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from coordTransform_utils import wgs84_to_gcj02, gcj02_to_wgs84


def get_exif_data(image_path):
    with Image.open(image_path) as img:
        if hasattr(img, '_getexif'):
            exif_data = img._getexif()
            if exif_data:
                return {TAGS.get(tag): value for tag, value in exif_data.items() if tag in TAGS}


def get_gps_info(exif_data):
    gps_info = {}
    if 'GPSInfo' in exif_data:
        for tag, value in exif_data['GPSInfo'].items():
            tag_name = GPSTAGS.get(tag, tag)
            gps_info[tag_name] = value
        return gps_info
    return None


def get_capture_time(exif_data):
    if exif_data:
        capture_time = exif_data.get('DateTimeOriginal') or exif_data.get('DateTimeDigitized')
        return capture_time
    return None


def convert_to_degrees(degrees, minutes, seconds):
    return degrees + (minutes / 60.0) + (seconds / 3600.0)


def get_lat_lon(gps_info):
    lat = gps_info.get('GPSLatitude')
    lon = gps_info.get('GPSLongitude')
    if lat and lon:
        lat_ref = gps_info.get('GPSLatitudeRef')
        lon_ref = gps_info.get('GPSLongitudeRef')
        lat_degrees, lat_minutes, lat_seconds = lat[0], lat[1], lat[2]
        lon_degrees, lon_minutes, lon_seconds = lon[0], lon[1], lon[2]
        latitude = convert_to_degrees(lat_degrees, lat_minutes, lat_seconds)
        longitude = convert_to_degrees(lon_degrees, lon_minutes, lon_seconds)
        if lat_ref in ['S', 's']:
            latitude = -latitude
        if lon_ref in ['W', 'w']:
            longitude = -longitude
        return latitude, longitude
    return None, None


if __name__ == '__main__':

    # image_path = 'test_data/DJI_0043.JPG'
    # image_path = 'test_data/input/0001.jpg'
    # image_path = r'C:\Users\ENFI\Desktop\gopro\GPAG0489.JPG'
    image_path = r'F:\项目\裂缝监测\【训练资料】\井盖测试数据\images\00002.jpg'
    # image_path = r'C:\Users\ENFI\Desktop\gopro\00000.jpg'
    exif_data = get_exif_data(image_path)
    gps_info = get_gps_info(exif_data)
    capture_time = get_capture_time(exif_data)
    print("拍摄时间：", capture_time)

    # 如果gps存在的话
    if gps_info:
        latitude, longitude = get_lat_lon(gps_info)
        print(f'WGS84:Latitude: {latitude}, Longitude: {longitude}')
        print(f'{longitude}, {latitude}')

        # 从gps映射到高德地图
        longitude, latitude = wgs84_to_gcj02(longitude, latitude)

        print(f'高德:Latitude: {latitude}, Longitude: {longitude}')
        print(f'{longitude}, {latitude}')
