import zipfile
name = '0573'
while True:
    fz = zipfile.ZipFile(name + '.zip', 'r')
    fz.extractall(pwd=bytes(name, 'utf-8'))
    name = fz.filelist[0].filename[0:4]
    fz.close()
