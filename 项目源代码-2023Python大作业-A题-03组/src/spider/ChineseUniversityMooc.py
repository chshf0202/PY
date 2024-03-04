from spider.errorHandler import is_gbk_encodable


def getMooc(kw):
    f_video_names = open("../load/dataSet/Mooc/" + kw + "_video_names.txt", "w", encoding='utf-8')
    f_population = open("../load/dataSet/Mooc/" + kw + "_population.txt", "w", encoding='utf-8')
    f_urls = open("../load/dataSet/Mooc/" + kw + "_video_urls.txt", "w", encoding='utf-8')
    f_special = open("../load/dataSet/Mooc/" + kw + "_video_special.txt", "w", encoding='utf-8')
    url = 'https://www.icourse163.org/search.htm?search=%s#/' % kw
    import requests
    from lxml import etree
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Cookie': 'EDUWEBDEVICE=ac524ec757a34e5695f740ab39e7fc6c; __yadk_uid=CNi0NMD5zMyisoBtoBvwkEE0eBg1bnvZ; WM_TID=Ik4HWgeFnz1FAEQUBQbVgKv1XqoRyGpw; hb_MA-A976-948FFA05E931_source=cn.bing.com; NTESSTUDYSI=d0a628efdc214c7388d2b9bd76d28e39; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1689730524,1689733642,1689736935,1689742610; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1689742610; WM_NI=Bc4LVVAfEBAJX6Rk9V2CByyozK%2Bchw%2FVcbndJQ6wW4tqMiiic%2BYKjblvYtMYa3bZpcuxvxLomicV938IoDxeSJmQBvk%2BHN9utTeCbhOE508iiil8vtNp81i3Bhg8%2BT%2FZQnI%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee91e43df4f1ffd5c63eaa968ea7d85a979a9f82c83cbbb200d1d47d93b09fb7ef2af0fea7c3b92a82bdfcadd55e83ba8ba3c4429cea9e8cbc5ef29d8e9afc65ba95e584eb7ded8aad83ed708a8ffa98d640b8af838aec63a1f597ace96ab0aa9795d053a3edaebbf369b7a8ba99cf65afb7adb7bc39fc97a1a5fb6f9196a3b2c17ea9f588afbc7fb88caba4e1648d9bfbd1bb63abb7a4d9f5808eb0f8d2ec3982b8a9d9aa60ed869f8fcc37e2a3'
    }
    data = {
        "mocCourseQueryVo": '{"keyword":"%s","pageIndex":1,"highlight":"true","orderBy":0,"stats":10,"pageSize":20}' % kw
    }
    response = requests.post(
        url='https://www.icourse163.org/web/j/mocSearchBean.searchCourse.rpc?csrfKey=d0a628efdc214c7388d2b9bd76d28e39',
        headers=headers, data=data)
    import re
    p = re.compile('"mocCourseCardDto":{"id":(.*?),"shortName":".*?","name":"(.*?)"')
    ls = p.findall(response.text)
    video_names = [a[1] for a in ls]
    video_urls = ['https://www.icourse163.org/course/CCIT-%s' % a[0] for a in ls]
    p = re.compile('"orderPrice":null,"enrollCount":(.*?),"price"')
    video_enroll_cnt = p.findall(response.text)
    p = re.compile('"mocTagDtos":\[(.*?)],"firstPublishTime')
    video_tags = p.findall(response.text)
    p = re.compile('"name":"(.*?)","colour"')
    for i in range(len(video_tags)):
        if len(video_tags[i]) == 0 or p.search(video_tags[i]) == None:
            video_tags[i] = "无"
        else:
            video_tags[i] = p.search(video_tags[i]).group(1)

    for i in range(len(video_names)):
        if is_gbk_encodable(video_names[i]) and \
                is_gbk_encodable(video_urls[i]) and \
                is_gbk_encodable(video_enroll_cnt[i]) and \
                is_gbk_encodable(video_tags[i]):
            print(video_names[i], file=f_video_names)
            print(video_urls[i], file=f_urls)
            print(video_enroll_cnt[i], file=f_population)
            print(video_tags[i], file=f_special)
