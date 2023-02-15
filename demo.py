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
