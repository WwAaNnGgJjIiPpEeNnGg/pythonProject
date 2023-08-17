import subprocess

def execute_adb_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode(), error.decode()

# 示例ADB命令：获取设备列表
device_list_command = 'adb devices'
output, error = execute_adb_command(device_list_command)
print(output)
print(error)
