# -*- coding:utf-8 -*-
import json
import time

from log import logger


def get_user_address(main_obj):
    address_url = 'https://cd.jd.com/usual/address'
    address_params = {
        '_': str(int(time.time() * 1000))
    }
    address_headers = {
        'DNT': '1',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'upgrade-insecure-requests': '1',
        'Referer': 'https://item.jd.com/',
        'User-Agent': main_obj.user_agent
    }
    default_address_json = None
    ipLocation = None
    province_id = None
    address_count = 0
    while True:
        try:
            address_resp = main_obj.sess.get(url=address_url, params=address_params,
                                             headers=address_headers, allow_redirects=False)
            default_address_json = json.loads(address_resp.text)[0]
            province_id = default_address_json['provinceId']
            break
        except Exception as e:
            address_count += 1
            logger.error('获取地址信息失败 %s', e)
            if address_count > 2:
                exit(-1)
        finally:
            time.sleep(0.05)

    area_url = 'https://d.jd.com/area/get'
    area_params = {
        'fid': '0'
    }
    area_headers = {
        'DNT': '1',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'script',
        'upgrade-insecure-requests': '1',
        'Referer': 'https://item.jd.com/',
        'User-Agent': main_obj.user_agent
    }
    address_count = 0
    while True:
        try:
            area_resp = main_obj.sess.get(url=area_url, params=area_params,
                                          headers=area_headers, allow_redirects=False)
            area_json = json.loads(area_resp.text)
            for area in area_json:
                if area['id'] == province_id:
                    ipLocation = str(area['name'].encode('unicode_escape'), encoding="utf-8").replace('\\u', '%u')
                    break
            break
        except Exception as e:
            address_count += 1
            logger.error('获取地址信息失败 %s', e)
            if address_count > 2:
                exit(-1)
    cookies = main_obj.sess.cookies
    # print(cookies.items())
    if province_id is not None and ipLocation is not None:
        cookies.set('ipLoc-djd',
                    f'{province_id}-{default_address_json["cityId"]}-{default_address_json["countyId"]}-{default_address_json["townId"]}.{default_address_json["id"]}',
                    domain='.jd.com', path='/')
        cookies.set('ipLocation', ipLocation, domain='.jd.com', path='/')
        return True
    else:
        return False
