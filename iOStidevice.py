
from tidevice import Usbmux
from tidevice import Device
from tidevice import Usbmux
for info in Usbmux().watch_device():
    print(info)

print(Usbmux().device_list())


# 内容会比cmd 全很多， 但是需要理解每个字段的含义
#Device("00008020-001D05892223002E").device_info()