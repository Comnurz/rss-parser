from typing import Any, Dict, List

import requests
from requests_html import HTMLSession


def parse_rss(url: str) -> List[Dict[str, Any]]:
    """
    Parse rss
    :param url: str
    :return: Dict[str, Any]
    """
    try:
        session = HTMLSession()
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        raise e

    res = []
    items = response.html.find("item", first=False)

    for item in items:
        title = item.find("title", first=True).text
        pub_date = item.find("pubDate", first=True).text
        guid = item.find("guid", first=True).text
        description = item.find("description", first=True).text

        res.append(
            {
                "title": title,
                "pubDate": pub_date,
                "guid": guid,
                "description": description,
            }
        )

    return res
