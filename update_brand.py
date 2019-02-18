import os
import sys
import platform

if platform.system() == 'Windows':
    python_version = 'python '
    cmd_style = ' & '
else:
    python_version = 'python3 '
    cmd_style = ' ; '

def main():
    brand = sys.argv[1]
    # crawling
    cmd = "cd crawling" + cmd_style +  python_version + "crawling.py "+ brand
    print('$',cmd)
    os.system(cmd)

    cmd = "cd cleansing" + cmd_style + python_version + "cleansing.py "+ brand
    print('$',cmd)
    os.system(cmd)

    cmd = "cd compare" + cmd_style + python_version + "compare.py "+ brand
    print('$',cmd)
    os.system(cmd)

    cmd = "cd complete" + cmd_style + python_version + "complete.py "+ brand
    print('$',cmd)
    os.system(cmd)


if __name__ == "__main__":
    main()

