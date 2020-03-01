from background_task import background
from products.models import Product
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from bs4.element import NavigableString
import json


@background(schedule=3600)
def crawl_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
    }
    req = Request(url=url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    name = soup.find(
        "span", {"class": "base", "data-ui-id": "page-title-wrapper"}
    ).contents[0]
    price = soup.find("span", {"class": "price"}).contents[0]
    description = ""
    main_image = ""
    scripts = soup.find_all("script")
    image_list = []
    is_nav_string = isinstance(
        soup.find("div", id="description").contents[0], NavigableString
    )
    description = (
        "<p>" + soup.find("div", id="description").contents[0] + "</p>"
        if is_nav_string
        else soup.find("div", id="description").contents
    )
    for script in scripts:
        if script.contents is not None:
            result = search_image_list(script.contents)
            description = (
                result["description"]
                if "description" in result and result["description"] != ""
                else description
            )
            image_list = (
                result["images"]["image_list"]
                if "images" in result and result["images"]["image_list"] != []
                else image_list
            )
            main_image = (
                result["images"]["main_image"]
                if "images" in result and result["images"]["main_image"] != ""
                else main_image
            )

    product = Product(
        name=name,
        description=description,
        url=url,
        price=price,
        image_list=image_list,
        main_image=main_image,
    )
    product.save()


def search_image_list(contents):
    result = {}
    for content in contents:
        if (
            "Magento_Swatches/js/swatch-renderer" in content
            and "data-role=swatch-options" in content
            and "jsonConfig" in content
        ):
            json_config = json.loads(content)["[data-role=swatch-options]"][
                "Magento_Swatches/js/swatch-renderer"
            ]["jsonConfig"]
            product_id = list(json_config["descriptions"].keys())[0]
            result["description"] = json_config["descriptions"][product_id]
            result["images"] = parse_image_data(json_config["images"][product_id])
        elif (
            "mage/gallery/gallery" in content
            and "data-gallery-role=gallery-placeholder" in content
            and "data" in content
        ):
            image_datas = json.loads(content)[
                "[data-gallery-role=gallery-placeholder]"
            ]["mage/gallery/gallery"]["data"]
            result["images"] = parse_image_data(image_datas)
    return result


def parse_image_data(image_datas):
    main_image = ""
    image_list = []
    for image_data in image_datas:
        image_list.append(image_data["img"])
        main_image = image_data["img"] if image_data["isMain"] else main_image
    return {"image_list": image_list, "main_image": main_image}
