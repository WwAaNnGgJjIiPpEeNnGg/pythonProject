import time

from scapy.layers.inet import TCP, IP


def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # 将文件内容转换为集合，方便进行差集运算
    set1 = set(lines1)
    set2 = set(lines2)

    # 计算不同行的行号和行内容
    diff_lines = set1.symmetric_difference(set2)
    diff_lines = sorted(list(diff_lines))
    if file1 == file2:
        print("文件内容一致")

    # 输出不同行的行号和行内容
    for line in diff_lines:
        if line in lines1:
            print(f"Line {lines1.index(line) + 1} in {file1} is different: {line}")
        else:
            print(f"Line {lines2.index(line) + 1} in {file2} is different: {line}")


file1 = "C:\\py\\1.txt"
file2 = "C:\\py\\2.txt"
compare_files(file1, file2)


def timer(n):
    while n > 0:
        print(n)
        n = n - 1
        time.sleep(1)
    print('Time is up!')


timer(10)  # 10秒后打印 "Time is up!"

from scapy.all import *
import requests


def packet_callback(packet):
    if packet[TCP].payload:
        if packet[TCP].dport == 80 or packet[TCP].dport == 443:  # 检查目标端口是否为HTTP或HTTPS端口
            http_payload = str(packet[TCP].payload)

            # 检查载荷中是否存在APK文件的标识（可以根据实际情况进行修改）
            if ".apk" in http_payload.lower():
                print(f"Destination IP: {packet[IP].dst}")
                print(f"Destination Port: {packet[TCP].dport}")
                print(f"Payload: {http_payload}")

                # 提取APK下载链接
                apk_url = extract_apk_url(http_payload)

                # 下载APK文件
                download_apk(apk_url)


def extract_apk_url(payload):
    # 在实际情况下，您需要编写适合您的APK下载链接提取逻辑
    # 这里只是一个示例，提取方式可能因APK下载链接的格式而异
    apk_url_start = payload.lower().find("http")
    apk_url_end = payload.lower().find(".apk")
    apk_url = payload[apk_url_start:apk_url_end + 4]
    return apk_url


def download_apk(url):
    # 使用requests库下载APK文件
    response = requests.get(url)
    with open("downloaded.apk", "wb") as apk_file:
        apk_file.write(response.content)
    print("APK downloaded successfully.")


# 设置Npcap作为抓包引擎
conf.pcap_engine = pcapdnet

# 开始抓包
sniff(filter="tcp", prn=packet_callback, store=0)
