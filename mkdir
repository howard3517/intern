import os 
dir = 'name'
now_path = os.getcwd()
path = f'{now_path}\\{dir}'
if not os.path.exists(path):
    os.mkdir(path)
else:
    for file in os.listdir(path):
        os.remove(f'{path}\\{file}')
