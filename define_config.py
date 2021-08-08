import os

if __name__ == '__main__':
    files_list = [el.split('.')[0] for el in os.listdir(os.path.join('Data EAF','materials','G01','V01')) if el.endswith('.eaf')]
    print(os.getcwd(),files_list)
    with open('config_file.txt','w+') as file:
        file.write('\n'.join(files_list))
        file.close()