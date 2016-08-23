import requests
from bs4 import BeautifulSoup
import os.path


class Zhihu():
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                        'Host': 'www.zhihu.com'}
        self.cookie = {
            'z_c0': 'Mi4wQUJDTVpzcWVmUWdBRU1EcGc1S2lDUmNBQUFCaEFsVk5LVTNkVndDaUl3NFdyLW9GS09zWXdNak9kbVdMVWtUT2pR|1471529339|4be0f2588f3ce36b105e8e753000fdfe600cc67b'}
        self.session = requests.session()
        self.title = ''

    def getImage(self, pageUrl):
        response = self.session.get(pageUrl, headers=self.headers)
        html = BeautifulSoup(response.text, 'lxml')
        self.title = html.find('span', class_='zm-editable-content').string
        answers = html.find_all('div', class_='zm-item-answer')
        for answer in answers:
            if answer.find('img', class_='origin_image zh-lightbox-thumb lazy'):
                self.parse(answer, self.title)
            else:
                pass

    def parse(self, item, title):
        author = item.find('a', class_='author-link').string
        images = item.find_all('img', class_='origin_image zh-lightbox-thumb lazy')
        image_list = [n.get('data-actualsrc') for n in images]
        self.Download(image_list, author, title)

    def Download(self, list, author, title):
        num = 0
        for i in list:
            num = num + 1
            print('正在下载《%s》问题下的%s的第%d张图片' % (title, author, num))
            temp = i.split('/')
            content = self.session.get(i)
            if not os.path.exists('E:\\Python3\\Crawler\\爬取知乎图片\pic\\' + title + '\\' + author):
                os.makedirs('E:\\Python3\\Crawler\\爬取知乎图片\pic\\' + title + '\\' + author)
            with open('E:\\Python3\\Crawler\\爬取知乎图片\pic\\' + title + '\\' + author + '\\' + str(temp[3]),
                      'wb+') as file:
                file.write(content.content)

        print('《%s》问题下答主%s的图片已下载结束，共%d张图片' % (title, author, num))


if __name__ == "__main__":
    answer = input('输入问题编号：')
    url = 'https://www.zhihu.com/question/' + str(answer)
    image=Zhihu()
    image.getImage(url)

