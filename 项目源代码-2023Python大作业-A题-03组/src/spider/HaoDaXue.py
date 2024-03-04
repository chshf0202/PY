import requests

from spider.errorHandler import is_gbk_encodable


def getHDX(kw):
    f_video_names = open("../load/dataSet/HaoDaXue/" + kw + "_video_names.txt", "w", encoding='utf-8')
    f_video_urls = open("../load/dataSet/HaoDaXue/" + kw + "_video_urls.txt", "w", encoding='utf-8')
    f_video_teachers = open("../load/dataSet/HaoDaXue/" + kw + "_video_teachers.txt", "w", encoding='utf-8')
    f_video_schools = open("../load/dataSet/HaoDaXue/" + kw + "_video_schools.txt", "w", encoding='utf-8')

    url = 'https://www.cnmooc.org'
    headers = {
        'Referer': 'https://www.cnmooc.org/portal/frontCourseIndex/course.mooc?k=%s&n=course&f=0&t=&m=&e=all&l=all&c=all&p=1&s=' % kw.encode(
            'utf-8').decode('latin1'),
        'Cookie': 'moocvk=4878f313ab584ccd98763b9f34c9dfbd; cpstk=a291412a76f54473a5c84ac2f75fe075; JSESSIONID=B315AF4DBDD666BB29C3D57218CA92A5.tomcat-1; BEC=54af4961fbd3f6b0e2d88d786222fbd3; Hm_lvt_ed399044071fc36c6b711fa9d81c2d1c=1689737192,1689749957; Hm_lpvt_ed399044071fc36c6b711fa9d81c2d1c=1689749957',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
    }
    data = {
        'keyWord': kw,
        'openFlag': '0',
        'fromType': '',
        'learningMode': '0',
        'certType': '',
        'languageId': '',
        'categoryId': '',
        'menuType': 'course',
        'schoolId': '',
        'pageIndex': "1",
        'postoken': 'a291412a76f54473a5c84ac2f75fe075'
    }
    response = requests.post(
        'https://www.cnmooc.org/portal/ajaxCourseIndex.mooc',
        headers=headers,
        data=data
    )
    from lxml import etree
    et = etree.HTML(response.text)
    video_num = len(et.xpath('/html/body/ul/*'))
    video_names = []
    video_urls = []
    video_teachers = []
    video_schools = []
    for i in range(video_num):
        video_names += et.xpath('/html/body/ul/li[%d]/div/div[2]/h3/a/text()' % (i + 1))
        video_teachers += et.xpath('/html/body/ul/li[%d]/div/div[2]/div[3]/a/h3/text()' % (i + 1)) if len(
            et.xpath('/html/body/ul/li[%d]/div/div[2]/div[3]/a/h3/text()' % (i + 1))) != 0 else ['无']
        video_schools += et.xpath('/html/body/ul/li[%d]/div/div[2]/div[3]/a/h4/text()' % (i + 1)) if len(
            et.xpath('/html/body/ul/li[%d]/div/div[2]/div[3]/a/h4/text()' % (i + 1))) != 0 else ["无"]
        video_urls += [url + et.xpath('/html/body/ul/li[%d]/div/div[1]/div/@href' % (i + 1))[0]]

    for i in range(len(video_names)):
        if (is_gbk_encodable(video_names[i])):
            video_names[i] = video_names[i].replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '')

    for i in range(len(video_names)):
        if is_gbk_encodable(video_names[i]) and \
                is_gbk_encodable(video_urls[i]) and \
                is_gbk_encodable(video_teachers[i]) and \
                is_gbk_encodable(video_schools[i]):
            print(video_names[i], file=f_video_names)
            print(video_urls[i], file=f_video_urls)
            print(video_teachers[i], file=f_video_teachers)
            print(video_schools[i], file=f_video_schools)
