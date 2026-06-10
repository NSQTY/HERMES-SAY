from system.CommunicationAndExamples.HY_Register import RegisterVPT

@RegisterVPT(abbreviation='read_file', document="读一个文件内容，但是注意告诉用户你准备读哪个文件")
def read_file(file_path, mode='r', code='utf-8'):
    with open(file_path, mode, encoding=code) as file:
        content = file.read()
        return content
    
    
@RegisterVPT(abbreviation='write_file', document="写一个文件内容，但是注意告诉用户你准备写哪个文件")
def write_file(file_path, content, mode='w', code='utf-8'):
    with open(file_path, mode, encoding=code) as file:
        file.write(content)
        return True