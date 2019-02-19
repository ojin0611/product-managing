import * as request from "request-promise-native";
import * as fs from "fs";

const categories: any = {
  "20": "클렌저",
  "21": "스크럽&마스크",
  "22": "페이스오일",
  "23": "토너&미스트",
  "24": "세럼",
  "25": "모이스처라이저",
  "26": "아이케어",
  "27": "선케어",
  "28": "립케어",
  "29": "화장솜&액세서리",
  "30": "남성스킨케어",
  "72": "기획세트",
  "32": "대용량바디케어",
  "33": "배쓰&샤워",
  "34": "바디스크럽",
  "35": "바디모이스처라이저",
  "36": "바디오일",
  "37": "바디미스트",
  "38": "데오도란트",
  "39": "풋케어",
  "40": "핸드케어",
  "41": "비누",
  "42": "액세서리",
  "43": "기획세트",
  "74": "트래블 에센셜",
  "45": "클렌저&쉐이브",
  "46": "스크럽&마스크",
  "47": "모이스처라이저",
  "48": "선케어",
  "49": "향수&바디미스트",
  "51": "파우더&팩트&쿠션",
  "52": "아이",
  "53": "립",
  "54": "스킨&메이크업브러쉬",
  "55": "액세서리",
  "57": "FOR HIM",
  "58": "FOR HER",
  "59": "FOR EVERYONE",
  "61": "샴푸&스크럽",
  "62": "컨디셔너&트리트먼트",
  "64": "헤어오일&스타일링",
  "65": "액세서리"
};
function* makeRangeIterator(start = 1, end = Infinity, step = 1) {
  let n = 0;
  for (let i = start; i < end; i += step) {
    n++;
    yield i;
  }
  return n;
}
(async () => {
  let result: any[] = [];
  for (const category of Object.keys(categories)) {
    const pageSize = await request.get({
      url: `https://www.thebodyshop.co.kr/display/category/list?_format=json&pageNo=1&dpCateId=${category}&refDpCateId=60&dpCateCd=&sortKey=1`,
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
      },
      json: true
    });
    for (const page of makeRangeIterator(
      1,
      pageSize.totalCount / pageSize.pageSize + 1
    )) {
      const prodList = await request.get({
        url: `https://www.thebodyshop.co.kr/display/category/list?_format=json&pageNo=${page}&dpCateId=${category}&refDpCateId=60&dpCateCd=&sortKey=1`,
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        },
        json: true
      });
      result = result.concat(
        prodList.list.map((prod: any) => {
          return {
            brand: "thebodyshop",
            id: prod.item.itemCd, // 사이트 기준의 pid
            name: prod.item.itemNm,
            category: categories[category as any],
            image: `https://www.thebodyshop.co.kr/files/public/item/${
              prod.item.itemCd
            }/${prod.item.itemCd}-represent.jpg`,
            originalPrice: prod.item.itemPrice.rgurPrc,
            salePrice: prod.item.itemPrice.sellPrc,
            url: `https://www.thebodyshop.co.kr/item/${prod.item.itemCd}`
          };
        })
      );
    }
  }
  await fs.writeFileSync("./thebodyshop.json", JSON.stringify(result));
})();
