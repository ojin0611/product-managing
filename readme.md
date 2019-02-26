# 상품 관리 자동화 시스템
- Amazon EC2 : 자동화
- Amazon S3  : 결과 데이터 저장
- Amazon DynamoDB : Admin DB Table 저장
- Amazon Athena : S3에 저장된 데이터 쿼리

## 2가지 process
1. 주기적으로 전체 브랜드 크롤링 
2. 요청시 특정 브랜드 크롤링 
- 과정 : 특정 브랜드 크롤링>비교>클렌징>DB

* * *

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

## modules
[자세히 보기](./modules)

* * *

## Requirements
### git
- sudo yum install git
- 정리 링크 : https://medium.com/sunhyoups-story/ec2-git-ac275a4e789c

### python3
- sudo yum install python36

### pip3
```
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py --user
```
이후 모듈 설치 : `pip3 install modulename --user`

### Google Chrome (+chromedriver)
- [한 방에 정리!] (https://medium.com/@praneeth.jm/running-chromedriver-and-selenium-in-python-on-an-aws-ec2-instance-2fb4ad633bb5)

- Install chromedriver
```
cd/tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
chromedriver --version
```
- Install Google Chrome
```
curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
google-chrome --version && which google-chrome
```



### Node.js / npm
- Port 설정 : 인스턴스 > 보안 그룹 생성(또는 변경) > Custon TCP Rule  / PORT 3000
- 설치방법 링크 : https://gist.github.com/nrollr/325e9bc4c35a0523d290b38cfa3c5142
- 로컬 노드 버전 탐색 : https://nodejs.org/dist/
- 로컬 노드 버전 확인 : ```node --version```

```
// Ctrl + Insert : 복사, Shift + Insert : 붙여넣기
sudo yum update -y
sudo yum install -y gcc gcc-c++ make openssl-devel

cd /tmp
curl -O https://nodejs.org/dist/v9.9.0/node-v9.9.0.tar.gz
tar -xvf node-v9.9.0.tar.gz && rm node-v9.9.0.tar.gz

cd node-v9.9.0
./configure
make
sudo make install

sudo ln -s /usr/local/bin/node /usr/bin/node
sudo ln -s /usr/local/lib/node /usr/lib/node
sudo ln -s /usr/local/bin/npm /usr/bin/npm
```

### AWS CLI 설치 (EC2에는 install 돼있습니다.)
- [pip install](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/install-windows.html#awscli-install-windows-path) 
- [AWS Guide](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/cli-chap-tutorial.html)

AWS CLI 설치 후 setting
```
$ aws configure
AWS Access Key ID [None]: AccessKeyID
AWS Secret Access Key [None]: SecretAccessKey
Default region name [None]: ap-northeast-2
Default output format [None]: ENTER
```

### Linux 시간 변경
- [리눅스 시간 UTC에서 KST로 변경하는 방법](https://ithub.tistory.com/227)
```
sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
date
```
* * *

### crontab 사용
- 크론탭 편집
```
crontab -e
* * * * * cd /home/ec2-user/product-managing ; git pull ; python3 update_brand all
```
분 시 일 월 요일

- 크론탭 목록 확인
`crontab -l`

- 크론탭 목록 제거
`crontab -r`

## 부록
- [Python으로 Bash 명령 실행](https://www.journaldev.com/16140/python-system-command-os-subprocess-call)





- Created by [Jingoo Kim](https://github.com/Kimjingoo), [Youngjin Yang](https://github.com/ojin0611), [Jungbin Im](https://github.com/dlawjdqls10), [Seoyoung Jang](https://github.com/Seoyoung1202) -
