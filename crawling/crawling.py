import json
import sys
from glob import glob
import os
import subprocess
import crawling_module

def main():
    with open('brandlist.json', encoding='UTF-8') as brandlist:
        brand_dict = json.load(brandlist)

    brand = sys.argv[1]
    for key, value in brand_dict.items():
        if brand in value:
            print('crawling method :',key)
            if key=='python':
                filelist = glob("./"+brand+"/*.py") # 모든 python file 실행할것! 추후에 crawler로 이름 바꿔도 됨.

                for file in filelist:
                    cmd = "cd "+brand+" & python "+brand+".py"

                    os.system(cmd) # 이 때 current directory 변경됨
                pass

            if key=='js':
                # do something
                pass

            if key=='manual':
                pass

            break

    try:
        print('directory :',sys.argv[1])
    except Exception as e:
        print("Error :", e)


if __name__ == "__main__":
    main()

