# 상품 관리 자동화 시스템

## 2가지 process
1. 주기적으로 전체 브랜드 크롤링 
2. 요청시 특정 브랜드 크롤링 

과정 : 특정 브랜드 크롤링>비교>클렌징>DB

## 사용법
```
$ python update_brand.py <brand>
```

## crawling
[자세히 보기](./crawling)

## cleansing
[자세히 보기](./cleansing)


## compare
[자세히 보기](./compare)



## AWS 연동
- product-managing > EC2로 이동
- data 디렉토리 > S3 디렉토리로 이동
- S3 > compare 최종 결과를 DynamoDB로 push 
- athena로 S3 볼 수 있도록 설정


## Requirements
### git
- sudo yum install git
- 정리 링크 : https://medium.com/sunhyoups-story/ec2-git-ac275a4e789c

### AWS CLI 설치 
- [Python 설치](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/install-windows.html#awscli-install-windows-path) 
- [AWS Guide](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-chap-tutorial.html)
- AWS CLI 설치 후 setting
```
$ aws configure
AWS Access Key ID [None]: AccessKeyID
AWS Secret Access Key [None]: SecretAccessKey
Default region name [None]: ap-northeast-2
Default output format [None]: ENTER
```

### python3
- sudo yum install python36

### pip3
- curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
- python3 get-pip.py --user
- 이후 모듈 설치 : pip3 install modulename --user
- node.js 설치

### Google Chrome (+chromedriver) + selenium
- 한 방에 정리 링크! : https://medium.com/@praneeth.jm/running-chromedriver-and-selenium-in-python-on-an-aws-ec2-instance-2fb4ad633bb5


## 부록
- [Python으로 Bash 명령 실행](https://www.journaldev.com/16140/python-system-command-os-subprocess-call)
