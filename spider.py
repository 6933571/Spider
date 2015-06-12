import httplib2
import re


class Record():
    def __init__(self):
        self.url = ''
        self.charset = 'utf-8'
        self.title = ''
        self.length = 0


class Spider():
    def __init__(self, url, depth):
        self.client = httplib2.Http()
        self.url = url
        self.depth = depth
        self.info = []

    def run(self):
        self.crawl(self.url, 0)

    def get(self, url):
        record = Record()
        try:
            header, body = self.client.request(url, redirections=5)
            data = re.search(r'<title>(.*)</title>', body)
            if data:
                record.title = data.group(1)
            data = re.search(r'text/html;\s*charset\s*=(.*)', header['content-type'])
            if data:
                record.charset = data.group(1)
            record.length = header['content-length']
            if record.length:
                self.info.append(record)
        except Exception, e:
            print e
            return None

        return body

    def crawl(self, url, depth):
        print('get:', url)
        print('depth:', depth)
        body = self.get(url)
        if not body:
            return

        if depth < self.depth:
            url = re.findall('<a.*?href="(http://[^<>]*?)".*?>[^<>]*?</a>', body)
            for item in url:
                self.crawl(item, depth + 1)

if __name__ == "__main__":
    spider = Spider('http://www.zhihu.com', 1)
    spider.run()


