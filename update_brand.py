import os
import sys

def main():
    brand = sys.argv[1]
    cmd = "cd crawling & python crawling.py "+brand
#    cmd = "cd "+brand+" & python "+brand+".py"
    os.system(cmd)


if __name__ == "__main__":
    main()

