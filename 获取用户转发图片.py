import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
import json
import time

global host_uid
host_uid = "1687766935"  # 你想要查看的用户的uid

# 随机产生请求头
ua = UserAgent(verify_ssl=False)
# 随机切换请求头
def random_ua():
    headers = {
        "accept-encoding": "gzip",  # gzip压缩编码  能提高传输文件速率
        "user-agent": ua.random
    }
    return headers

def get_content(next_offset):
    # host_uid = "51030552"  
    print("uid:" + host_uid)
    urltwo = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid=1687766935&host_uid='+ host_uid +'&offset_dynamic_id=' + next_offset + '&need_top=1&platform=web'
    print("获取网址为" + urltwo)
#    try:
    r1 = requests.get(urltwo, headers=random_ua(), timeout=10)
    print("连接成功！")
    url_list = []
    data = json.loads(r1.content)
    next_offset = data['data']['next_offset']
    has_more = data['data']['has_more']
    for dict_data in data['data']['cards']:
        data2 = json.loads(dict_data['card'])
        # if (dict_data['card'][2] == 'i' or dict_data['card'][2] == 'c'):#i和c是具体读取到的数据的区分，我自己做的区分
        #     for item in data2['item']['pictures']:
        #         url_list.append(item['img_src'])
        # elif (dict_data['card'][2] == 'a'):
        #     continue  #这种情况发的是视频，没有图片所以直接略过了
        #     # print(data2['first_frame'])
        if not (dict_data['card'][2] == 'i' or dict_data['card'][2] == 'c' or dict_data['card'][2] == 'a'):
            if 'origin' in data2:
                orig = json.loads(data2['origin'])
                if 'item' in orig:
                    orit = orig['item']
                    if 'pictures' in orit:
                        for item in orit['pictures']:
                            url_list.append(item['img_src'])
    return url_list, next_offset, has_more
#    except Exception:
#        print(Exception)
#        print("链接网络过程中出错！")
#    finally:
#        print("连接网络后返回！")


#  创建文件夹
def path_creat():
    _path = "./bilibili/"
    if not os.path.exists(_path):
        os.mkdir(_path)
    return _path
# 根据url下载图片
def download(url, file_name):
    try:
        image = requests.get(url=url, headers=random_ua()).content  # 获取图片

    except Exception:
        print(Exception)
        print("网络请求出错！")
    try:
        with open(file_name, 'wb') as f:
            f.write(image)
            f.close()
    except Exception:
        f.close()
        print(Exception)
        print("保存文件过程出错！")



# 主函数
if __name__ == '__main__':
    time_start = time.time()
    path = path_creat()  # 创建保存B站封面的文件夹
    has_more = 1
    count = 0
    next_offset = "0"#初始化一些参数
    #具体的链接写在方法里面了，要在里面组合一下，可以随时修改
    #在初始化的第一页请求中，next_offset确实是等于0的
    while (has_more == 1):
        imageurl_lists, next_offset, has_more = get_content(str(next_offset))
        print("next=" + str(next_offset))
        print("has=" + str(has_more))
        # print(type(has_more))
        numb = len(imageurl_lists)
        if imageurl_lists == None:
            continue
        for it in imageurl_lists:
            strl = it.split("/")
            download(it, path + strl[5])#切割了一下，用来保存图片当成文件名，还可以防止图片格式不对
        count += 1
        print("循环结束！第" + str(count))
        time_end = time.time()  # 获取结束时间
        runtime = time_end - time_start  # 运行时间
        print('第' + str(count) + '轮运行结束,有' + str(numb) + '组数据，已用运行时间为', runtime)

    time_end = time.time()  # 获取结束时间
    runtime = time_end - time_start  # 运行时间
    # print('运行结束，总共运行'+str(count)+'轮，总使用运行时间为', runtime)
    print('finished')
