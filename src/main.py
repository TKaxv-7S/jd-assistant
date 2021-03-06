#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import CustomConfig
from jd_assistant import Assistant

if __name__ == '__main__':
    """
    启动前请先【安装chrome】并下载【与内核版本相同的chromedriver】，然后在config.ini中配置chromedriver_path
    如果需要指定chrome路径，则需要配置chrome_path
    chromedriver下载：https://sites.google.com/a/chromium.org/chromedriver/home
    """

    config = CustomConfig()
    config.sku_id = '100015521004'  # 商品id
    config.buy_time = '2020-12-13 16:59:59.950'  # 开始抢购时间，格式：'2020-11-28 12:59:59.950'，建议设置提前0.050秒，如果网络慢可根据自己网络情况适当修改

    # 配置【预约抢购，自动加入购物车】
    # 注意：一定要在抢购开始前手动清空购物车中此类无法勾选的商品！（因为脚本在执行清空购物车操作时，无法清空不能勾选的商品）
    config.is_pass_cart = False  # 是否跳过添加购物车，默认False

    # 配置【预约抢购，不会自动加入购物车】
    # area = '19_1607_3155_62117'  # 区域id
    # sku_buy_time = '2020-12-04 15:00:00.000'  # 商品抢购时间
    # buy_time = None  # 开始抢购时间，默认为None，自动提前0.050秒，网络通畅时不需要修改，如果网络慢可根据自己情况适当修改，格式：'2020-11-28 12:59:59.950'
    # fast_mode = True  # 快速模式：略过访问抢购订单结算页面这一步骤，默认为 True

    asst = Assistant()  # 初始化
    asst.login_by_QRcode()  # 扫码登陆

    # 执行【预约抢购，自动加入购物车】 手动清空自动添加到购物车的
    asst.exec_reserve_seckill_by_time(config)

    # 执行【预约抢购，不会自动加入购物车】
    # asst.exec_seckill_by_time(sku_ids=sku_id, buy_time=buy_time, sku_buy_time=sku_buy_time, retry=retry, interval=interval, num=num, fast_mode=fast_mode, sleep_interval=sleep_interval, fast_sleep_interval=fast_sleep_interval)















    # 根据商品是否有货自动下单
    # 6个参数：
    # sku_ids: 商品id。可以设置多个商品，也可以带数量，如：'1234' 或 '1234,5678' 或 '1234:2' 或 '1234:2,5678:3'
    # area: 地区id
    # wait_all: 是否等所有商品都有货才一起下单，可选参数，默认False
    # stock_interval: 查询库存时间间隔，可选参数，默认3秒
    # submit_retry: 提交订单失败后重试次数，可选参数，默认3次
    # submit_interval: 提交订单失败后重试时间间隔，可选参数，默认5秒
