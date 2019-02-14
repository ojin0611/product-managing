import json
import sys
from glob import glob
import os
import subprocess
import crawling_module
import platform

sys.path.append("../modules")
import io_module


if platform.system() == 'Windows':
    python_version = 'python '
    cmd_style = ' & '
else:
    python_version = 'python3 '
    cmd_style = ' ; '

def main():
    with open('brandlist.json', encoding='UTF-8') as brandlist:
        brand_dict = json.load(brandlist)

    brand = sys.argv[1]
    print('--- brand :', brand,'---')
    for key, value in brand_dict.items():
        if brand in value:
            print('--- crawling method :',key,'--- ')
            print('--- directory :',brand,'--- ')
            if key=='python':
                # file name considering
                cmd = "cd " + brand + cmd_style +  python_version + brand + ".py"
                print(cmd)
                os.system(cmd)

            elif key=='js':
                cmd = "cd " + brand + cmd_style + "npm install" + cmd_style + "npm start"
                print(cmd)
                print(os.getcwd())
                os.system(cmd)

            elif key=='manual':
                pass

            else:
                print('---',brand + ' crawler is not prepared! ---')

            break


if __name__ == "__main__":
    main()

