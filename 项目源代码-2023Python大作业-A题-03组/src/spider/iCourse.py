from spider.errorHandler import is_gbk_encodable


def getIcourse(kw):
    global s
    url = 'https://www.icourses.cn/web//sword/portalsearch/searchPage'
    f_video_names = open("../load/dataSet/iCourse/" + kw + "_video_names.txt", "w", encoding='utf-8')
    f_video_urls = open("../load/dataSet/iCourse/" + kw + "_video_urls.txt", "w", encoding='utf-8')
    f_video_teachers = open("../load/dataSet/iCourse/" + kw + "_video_teachers.txt", "w", encoding='utf-8')
    f_video_schools = open("../load/dataSet/iCourse/" + kw + "_video_schools.txt", "w", encoding='utf-8')
    f_video_types = open("../load/dataSet/iCourse/" + kw + "_video_types.txt", "w", encoding='utf-8')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Cookie': 'JSESSIONID=66C47D82DAAA41DEEADBF5B956DEE345-n1; acw_tc=2760820116897357166916542e116ad37c3e8cccbc567c940999bf3b937799; Hm_lvt_787dbcb72bb32d4789a985fd6cd53a46=1689735717; Hm_lpvt_787dbcb72bb32d4789a985fd6cd53a46=1689735717; portaltikerviewcookiesys=e959f338052547c49a2fbdc138f8426e'
    }
    data = {
        'kw': kw,
        'curPage': '1'
    }
    import requests
    response = requests.post(url=url, headers=headers, data=data)
    response.encoding = "utf-8"
    import re
    p = re.compile('<a class="icourse-desc-title" href="(.*?)" title="(.*?)" target="_blank">')
    ls = p.findall(response.text)
    names = [a[1] for a in ls]
    video_urls = ['https:' + a[0] if not a[0].__contains__('https') else a[0] for a in ls]
    video_names = [tmp.replace('<b>', '').replace('</b>', '') for tmp in names]
    from lxml import etree
    et = etree.HTML(response.text)
    tmp = et.xpath('/html/body/section/div/div[1]/ul/li/div/div[2]/p[3]/span/text()')
    video_authors = [a.split('|')[0] for a in tmp]
    video_schools = []
    for a in tmp:
        s = a.split('|')
        if len(s) == 1:
            video_schools.append(s[0])
        else:
            video_schools.append(s[1])

    video_types = et.xpath('/html/body/section/div/div[1]/ul/li/div/div[2]/p[2]/span/text()')
    for i in range(len(video_names)):
        if is_gbk_encodable(video_schools[i]) and \
                is_gbk_encodable(video_authors[i]) and \
                is_gbk_encodable(video_names[i]) and \
                is_gbk_encodable(video_urls[i]) and \
                is_gbk_encodable(video_types[i]):
            print(video_schools[i], file=f_video_schools)
            print(video_authors[i], file=f_video_teachers)
            print(video_names[i], file=f_video_names)
            print(video_urls[i], file=f_video_urls)
            print(video_types[i], file=f_video_types)
