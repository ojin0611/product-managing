import * as request from "request-promise-native";
import * as fs from "fs";

const result: any = [];
const baseUrl = "https://www.drjart.com/api/prd/mng/";
const sleep = (ms: number) =>
  new Promise(resolve => {
    setTimeout(resolve, ms);
  });
const getData = (prdNtcmList: any, param: string) => {
  return prdNtcmList.find((e: any) => e.prd_ntcm_nm === param);
};

(async () => {
  const prodList = await request.get({
    url:
      "https://www.drjart.com/api/prd/mng/list?pageNumber=1&rows=10000&catSeqs%5B%5D=2&catSeqs%5B%5D=4&catSeqs%5B%5D=58&catSeqs%5B%5D=61&order=002&_=1545629129148",
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
    },
    json: true
  });
  const prodNumList = prodList.page.list.map((e: any) => e.prd_mng_seq);
  for (const prod of prodNumList) {
    try {
      await sleep(100);
      console.log(prod);
      const prodData = await request.get({
        url: baseUrl + prod,
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        },
        json: true
      });
      const brand = "drjart";
      const category = (prodData.prdMngview.full_cat_ko_nm as string)
        .split(">")
        .map(e => e.trim()); // 그 사이트 기준의 카테고리,
      const url = "https://www.drjart.com/ko/prd/view/" + prod; // - URL 추가
      const ingredient = getData(prodData.prdNtcmList, "전성분")
        ? getData(prodData.prdNtcmList, "전성분").prd_ntcm_cont
        : null; // - 주요성분
      const companyOfManufacturer = getData(
        prodData.prdNtcmList,
        "제조자 및 책임판매업자"
      )
        ? getData(prodData.prdNtcmList, "제조자 및 책임판매업자").prd_ntcm_cont
        : null;

      const countryOfManufacturer = getData(prodData.prdNtcmList, "제조국")
        ? getData(prodData.prdNtcmList, "제조국").prd_ntcm_cont
        : null;

      const expirationDate = getData(
        prodData.prdNtcmList,
        "사용기한 또는 개봉 후 사용기간"
      )
        ? getData(prodData.prdNtcmList, "사용기한 또는 개봉 후 사용기간")
            .prd_ntcm_cont
        : null;

      const specifications = getData(prodData.prdNtcmList, "제품 주요 사양")
        ? getData(prodData.prdNtcmList, "제품 주요 사양").prd_ntcm_cont
        : null;

      const volume = getData(prodData.prdNtcmList, "용량(중량) 또는 중량")
        ? getData(prodData.prdNtcmList, "용량(중량) 또는 중량").prd_ntcm_cont
        : null;

      const functionalCosmetics = getData(
        prodData.prdNtcmList,
        "기능성 화장품 심사 필 유무"
      )
        ? getData(prodData.prdNtcmList, "기능성 화장품 심사 필 유무")
            .prd_ntcm_cont
        : null;

      const id = prod; // 사이트 기준의 pid
      if (
        Array.isArray(prodData.attchList) ||
        Array.isArray(prodData.prdList)
      ) {
        prodData.prdList.forEach((prod: any, index: number) => {
          const originalPrice = prod.stdprc_prc;
          const name = prod.prd_ko_nm; // 제품명,
          const image = prodData.attchList[index]
            ? prodData.attchList[index].attch_url
            : prodData.attchList[0].attch_url; // 제품 이미지,
          const salePrice = prod.sal_prc;

          result.push({
            brand,
            category,
            companyOfManufacturer,
            countryOfManufacturer,
            expirationDate,
            id,
            image,
            ingredient,
            name,
            originalPrice,
            salePrice,
            specifications,
            url,
            functionalCosmetics,
            volume
          });
        });
      } else {
        const name = prodData.prdMngview.prd_ko_nm; // 제품명,
        const image = prodData.prdMngview.attch_url; // 제품 이미지,
        const originalPrice = prodData.prdMngview.stdprc_prc; // 가격,
        const salePrice = prodData.prdMngview.sal_prc; // 가격,
        result.push({
          brand,
          category,
          companyOfManufacturer,
          countryOfManufacturer,
          expirationDate,
          id,
          image,
          ingredient,
          name,
          originalPrice,
          salePrice,
          specifications,
          url,
          functionalCosmetics,
          volume
        });
      }
    } catch (e) {
      console.log(e);
      console.log("ERROR: ", prod);
    }
  }

  await fs.writeFileSync("./drjart.json", JSON.stringify(result));
})();
