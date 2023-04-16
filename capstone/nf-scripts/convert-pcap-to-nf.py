import sys, os
from pathlib import Path
import subprocess

def generateFileList(walk_dir):
    fileList = []
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            currentDirFile = os.path.join(root, filename)
            currentDir = os.path.basename(os.path.dirname(currentDirFile))
            fileList.append(currentDirFile)
    return fileList

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

if __name__ == "__main__":
    main()