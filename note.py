def main():
    while True:
        print("\n1. 写入记事本")
        print("2. 读取记事本")
        print("3. 退出")

        choice = input("请选择操作：")

        if choice == '1':
            write_note()
        elif choice == '2':
            read_note()
        elif choice == '3':
            print("感谢使用记事本！")
            break
        else:
            print("无效的选项，请重新输入。")


def write_note():
    filename = input("请输入文件名：")
    content = input("请输入要写入的内容：")

    with open(filename, 'w') as file:
        file.write(content)

    print(f"内容已写入 {filename}。")


def read_note():
    filename = input("请输入要读取的文件名：")

    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"文件内容：\n{content}")
    except FileNotFoundError:
        print("文件不存在，请检查文件名是否正确。")


if __name__ == "__main__":
    main()
