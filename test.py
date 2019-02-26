import os
import sys
import platform

if platform.system() == 'Windows':
    python_version = 'python '
    cmd_style = ' & '
else:
    python_version = 'python3 '
    cmd_style = ' ; '


def main(brand):
    if brand=='all':
        brandlist = next(os.walk('./crawling/'))[1]
        for brand in brandlist:
            update(brand)

    else:
        update(brand)

def update(brand):
    '''
    # crawling
    cmd = "cd crawling" + cmd_style +  python_version + "crawling.py "+ brand
    print('$',cmd)
    os.system(cmd)
    '''

    # cleansing
    cmd = "cd cleansing" + cmd_style + python_version + "cleansing.py "+ brand
    print('$',cmd)
    os.system(cmd)
    '''

    # compare
    cmd = "cd compare" + cmd_style + python_version + "compare.py "+ brand
    print('$',cmd)
    os.system(cmd)
    '''


if __name__ == "__main__":
    brand = sys.argv[1]
    main(brand)

