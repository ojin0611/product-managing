import os
import sys
import platform

if platform.system() == 'Windows':
    python_version = ' & python '
else:
    python_version = ' ; python3 '

def main():
    brand = sys.argv[1]
    cmd = "cd crawling" + python_version + "crawling.py "+ brand
    print(cmd)
#    cmd = "cd "+brand+" & python "+brand+".py"
    os.system(cmd)


if __name__ == "__main__":
    main()

