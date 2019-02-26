import json, sys, os, platform

sys.path.append("../modules")
import io_module


if platform.system() == 'Windows':
    python_version = 'python '
    cmd_style = ' & '
else:
    python_version = 'python3 '
    cmd_style = ' ; '

def main():

    brand = sys.argv[1]
    print('--- brand :', brand,'---')
    filelist = os.listdir('./'+brand)

    # find crawling style
    if 'package.json' in filelist:
        crawling_type = 'npm' 
    else:
        for filename in filelist:
            if '.py' in filename: 
                crawling_type = 'python'
                break
        else:
            crawling_type = None # npm도 아니고 python도 아닌 애들은 crawling_type이 없다.
    print('--- crawling type :',crawling_type,'---') 



    # crawling with its style
    if crawling_type=='python':
        # file name considering
        cmd = "cd " + brand + cmd_style +  python_version + brand + ".py"
        print(cmd)
        os.system(cmd)

    elif crawling_type=='npm':
        cmd = "cd " + brand + cmd_style + "npm install" + cmd_style + "npm start"
        print(cmd)
        print(os.getcwd())
        os.system(cmd)

    

    # crawling type이 있다면, local에 저장된 크롤링 결과 파일을 s3에 업로드한다.
    if crawling_type is not None:
        crawled_data = io_module.get_json(brand, brand, 'local')
        io_module.upload_json(crawled_data, brand, 'crawling')

    else: # crawler not exists
        print('---',brand + ' crawler is not prepared! ---')



if __name__ == "__main__":
    main()

