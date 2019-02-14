import * as request from "request-promise-native";
import * as fs from "fs";
//
const categories: any = [
  "FACE",
  "LIP",
  "EYE",
  "CHEEK",
  "SKINCARE",
  "TOOL",
  "NAIL",
  "ONLINE"
];

(async () => {
  let result: any[] = [];
  for (const categoryCode of categories) {
    const pageData = await request.post({
      url: `https://www.espoir.com/ko/shop/${categoryCode}/ALL/shop_prd_list_ajax.do?i_iPageSize=1000`,
      headers: {
        Referer: `https://www.espoir.com/ko/shop/${categoryCode}/shop_prd_list.do`
      },
      json: true
    });
    pageData.object.shopList.forEach((product: any) => {
      const category = product.v_ctg_nm.split(">")[
        product.v_ctg_nm.split(">").length - 1
      ];
      const brand = "espoir";
      const name = product.v_productnm; // 제품명,
      const image = product.v_img_path; // 제품 이미지,
      const originalPrice = product.n_list_price; // 가격,
      const salePrice = product.n_price; // 가격,
      const id = product.v_productcd; // 사이트 기준의 pid
      const url =
        "https://www.espoir.com/ko/shop/shop_prd_view.do?i_sProductcd=" + id; // - URL 추가
      if (product.v_opt_info && product.v_opt_info.includes("^")) {
        const option = (product.v_opt_info as string)
          .split("^^")
          .map((e: any) => {
            return e.split("^")[1];
          });
        option.forEach((c: any) => {
          if (c !== "1") {
            result.push({
              brand,
              name,
              image,
              category,
              originalPrice,
              salePrice,
              id,
              url,
              option: c
            });
          }
        });
      } else {
        result.push({
          brand,
          name,
          image,
          category,
          originalPrice,
          salePrice,
          id,
          url
        });
      }
    });
  }
  await fs.writeFileSync("./espoir.json", JSON.stringify(result));
})();
