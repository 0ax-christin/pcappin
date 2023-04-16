import sys, os
from pathlib import Path
import subprocess
import generatePCAPwoPayload.generateFileList

def main():
    #walk_dir = '{}/'.format(basedir.baseDir)
    walk_dir = '/mnt/capstone_pcaps/'
    fileList = generateFileList(walk_dir)
    for file in fileList:
        currentDir = os.path.dirname(file)
        fileName = (os.path.basename(file)).split('.')[0]
        Path(f"{currentDir}/netflows").mkdir(parents=True, exist_ok=True)
        Path(f"{currentDir}/netflows/{file}").mkdir(parents=True, exist_ok=True)
        Path(f"{currentDir}/csv-flows").mkdir(parents=True, exist_ok=True)
        subprocess.run('nfpcapd', '-r', f'{file}', '-l', f"{currentDir}/netflows/{fileName}/")
        subprocess.run('nfdump', '-R', f"{currentDir}/netflows/{fileName}", '-o', 'extended', '-o', 'csv', '>', f'{fileName}.csv')

    main()