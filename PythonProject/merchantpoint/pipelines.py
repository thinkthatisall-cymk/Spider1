from itemadapter import ItemAdapter


class CuCrawlingPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # address: убираем префикс "  —  "
        address = adapter.get("address")
        if isinstance(address, str):
            prefix = "  —  "
            if address.startswith(prefix):
                adapter["address"] = address.replace(prefix, "")

        # org_description: убираем переносы строк и лишние пробелы
        org_description = adapter.get("org_description")
        if isinstance(org_description, str):
            adapter["org_description"] = org_description.replace("\n", " ").strip()

        # merchant_name: тоже подчищаем пробелы
        merchant_name = adapter.get("merchant_name")
        if isinstance(merchant_name, str):
            adapter["merchant_name"] = merchant_name.strip()

        return item
