import requests, time,random,re
import logging
import json
import os
import sys
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
def get_bili_cookie():
    if "bili_cookie" in os.environ:
        bili_cookies = os.environ['bili_cookie'].split('&')
        if len(bili_cookies) > 0:
            return bili_cookies
        else:
            logger.info("bili_cookie变量未启用")
            sys.exit(1)
    else:
        logger.info("未添加bili_cookie变量")
        sys.exit(0)

def get_next(cookie):
    s = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
        'cookie': cookie,
        }
    url = "https://api.bilibili.com/x/credit/v2/jury/case/next"
    r = s.get(url,headers=headers)
    if(r.json()['code']== 0):
        return r.json()['data']['case_id']
    else:
        return r.json()['code']

def vote(cookie,case_id):
    s = requests.Session()
    url = "https://api.bilibili.com/x/credit/v2/jury/vote"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
        'cookie': cookie,
        }
    data = {
        "case_id": case_id,
        "vote": '12',
        "csrf": csrf
        }
    r = s.post(url, data=data, headers=headers, timeout=5)
    if(r.json()['code']== 0):
        return 1
    else:
        return 0


def toubi(cookie):
    s = requests.Session()
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?type_list=8,512,4097,4098,4099,4100,4101"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/76.0',
        'cookie': cookie,
        "referer": "https://www.bilibili.com/video/"
        }
    r = s.get(url,headers=headers)
    list = r.json()['data']['cards']
    num = range(0, 19)
    nums = random.sample(num, 5)
    for i in nums:
        bv=list[i]['desc']['bvid']
        rid=list[i]['desc']['rid']
        logger.info("正在给"+bv+"投币\n")
        url_add ="https://api.bilibili.com/x/web-interface/coin/add"
        data = {
        "aid": rid,
        "multiply": '1',
        "select_like": "1",
        "cross_domain":"true",
        "csrf": csrf
        }
        r = s.post(url_add, data=data, headers=headers, timeout=5)
        if(r.json()['code']== 0):
            logger.info("投币成功\n")
        else:
            logger.info("投币失败\n")
        time.sleep(1)


if __name__ == '__main__':
    logger.info("\n--------------------\n")
    bili_cookies = get_bili_cookie() 
    zh_sx=1
    for cookie in bili_cookies:
        try:
            i=1
            logger.info("第"+str(zh_sx)+"个账户\n--------------------")
            csrf=re.search(r"(?<=bili_jct=).*(?=;)", cookie, flags=0).group()
            while(1):
                case_id = get_next(cookie)
                if(case_id == 25014):
                    logger.info("风纪委员任务执行完毕\n")
                    break
                elif(case_id==25005):
                    logger.info("请先成为风纪委员\n")
                    break
                logger.info("正在执行第"+str(i)+"个任务\n")
                logger.info("case id 为"+case_id+"\n")
                i=i+1
                vote(cookie,case_id)
                time.sleep(15)
            toubi(cookie)
            zh_sx = zh_sx+1
            logger.info("--------------------\n")
        except:
            logger.info("第"+str(zh_sx)+"个账户出现错误--------------------\n")
            continue
    logger.info("执行完成\n--------------------")
    sys.exit(0)
