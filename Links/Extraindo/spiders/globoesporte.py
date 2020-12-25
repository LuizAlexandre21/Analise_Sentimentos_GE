import scrapy

clubes = ['athletico-pr','atletico-go','bahia','botafogo','bragantino','ceara','corinthians',
            'coritiba','flamengo','fluminense','fortaleza','goias','gremio','internacional','palmeiras',
            'sao-paulo','sport','vasco','atletico-mg']

class GloboesporteSpider(scrapy.Spider):
    name = 'globoesporte'
    allowed_domains = ['globoesporte.com']
    start_urls = ['http://globoesporte.com/']

    def start_requests(self):
        for i in clubes:
            if i == 'athletico-pr':
                url = 'https://globoesporte.globo.com/pr/futebol/times/'+i
            else:
                url = 'https://globoesporte.globo.com/futebol/times/'+i
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for i in response.xpath("//div[starts-with('bstn-hls xlarge-22 xlarge-offset-1 theme model-3')]"):
            print(i)
