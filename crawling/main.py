import json
import sys

def main():
    with open('brandlist.json', encoding='UTF-8') as brandlist:
        brand_dict = json.load(brandlist)

    brand = sys.argv[1]
    for key, value in brand_dict.items():
        if brand in value:
            print('crawling method :',key)
            if key=='html':
                print(sys.path)
                break

            if key=='api':
                pass
            if key=='manual':
                break

            break

    try:
        print('directory :',sys.argv[1])
    except Exception as e:
        print("Error :", e)


if __name__ == "__main__":
    main()
