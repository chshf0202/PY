from lxml import etree
import requests

from spider.errorHandler import is_gbk_encodable


def getBiliBili(kw, option):
    url_search = "https://search.bilibili.com/all?keyword=%s"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    tmp = ['', 'click', 'pubdate', 'dm', 'stow']
    metric = tmp[option - 1]
    url_metric = url_search % (kw)
    response = requests.get(url=url_metric, headers=headers)
    response.encoding = 'utf-8'
    et = etree.HTML(response.content)
    f_video_names = open("../load/dataSet/Bilibili/" + kw + "_video_names_" + metric + ".txt", "w", encoding='utf-8')
    video_names = []
    f_urls = open("../load/dataSet/Bilibili/" + kw + "_video_urls_" + metric + ".txt", "w", encoding='utf-8')
    urls = []
    if option == 1:
        video_names = et.xpath(
            '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/a/h3/@title | '
            '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/div/div/a/h3/@title |'
            '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[4]/div/div/div/div[2]/div/div/a/h3/@title')
        urls = et.xpath('//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/a/@href |'
                        '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[2]/div/div/a/@href |'
                        '//*[@id="i_cecream"]/div/div[2]/div[2]/div/div/div/div[4]/div/div/div/div[2]/div/div/a/@href')
        for i in range(len(video_names)):
            if (is_gbk_encodable(video_names[i])):
                print(video_names[i], file=f_video_names)

        for i in range(len(urls)):
            if (is_gbk_encodable(video_names[i])):
                print("https:" + urls[i], file=f_urls)

    else:
        url_metric += '&order=%s' % tmp[option - 1]
        headers[
            'Cookie'] = '_uuid=110A73486-6A54-9413-1D74-8BCD21110DAE816710infoc; b_nut=1665042819; buvid3=193EE7C1-50F6-594F-B219-87AD3C316BA218113infoc; i-wanna-go-back=-1; buvid_fp_plain=undefined; b_ut=5; LIVE_BUVID=AUTO6116652968723886; buvid4=A8502C2C-D223-F28F-FEED-9A9730A8127218113-022100615-PdJr0jKE6N6JrlIepfFQsWJeLXekQyQXBsnwxZtv%2BrwYAkk7MggfyQ%3D%3D; nostalgia_conf=-1; rpdid=0z9Zw2XGm2|3DPwNBVP|30W|3w1P1pJp; CURRENT_BLACKGAP=0; hit-new-style-dyn=0; hit-dyn-v2=1; CURRENT_FNVAL=4048; header_theme_version=CLOSE; is-2022-channel=1; CURRENT_PID=18355e60-ce36-11ed-aebf-d560dc9e86dc; FEED_LIVE_VERSION=V8; PVID=1; CURRENT_QUALITY=80; fingerprint=b9ce052db5ace4e829eb9485e3451397; buvid_fp=b9ce052db5ace4e829eb9485e3451397; home_feed_column=5; bsource=search_baidu; sid=55uketmo; bp_video_offset_1715207492=819659379914571800; browser_resolution=1495-716; innersign=0; b_lsid=CF793F58_1896910FE4E'
        response = requests.get(
            "https://api.bilibili.com/x/web-interface/wbi/search/type?&_extra=&context=&page=1&page_size=42&order=%s&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword=%s&qv_id=3IIo9p5R5g2qBQYCnvotJCEP16RrsG4a&ad_resource=5654&source_tag=3&gaia_vtoken=&category_id=&search_type=video" % (
                metric, kw), headers=headers)
        js = response.json()
        ans = js['data']['result']
        for dic in ans:
            video_names.append(dic['title'].replace('<em class="keyword">', '').replace('</em>', ''))
            urls.append(dic['arcurl'])

        for i in range(len(video_names)):
            if (is_gbk_encodable(video_names[i])):
                print(video_names[i], file=f_video_names)

        for i in range(len(urls)):
            if (is_gbk_encodable(video_names[i])):
                print(urls[i], file=f_urls)
