import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    quote_count = 1
    file = open('quotes.txt', 'a', encoding='utf-8')
    start_urls = ['http://quotes.toscrape.com/page/1/', ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()
            self.file.write(str(self.quote_count) +
                            '*********************************************\n')
            self.file.write("Text: " + text + '\n')
            self.file.write("Author: " + author + '\n')
            self.file.write("Tags: " + str(tags) + '\n')
            self.quote_count += 1
        next_url = response.css('li.next a::attr(href)').get()

        if next_url is not None:
            next_url = "http: // quotes.toscrape.com" + next_url
            self.file.write("url::::::" next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)
        else:
            self.file.close()
