import scrapy

class CovidSpider(scrapy.Spider):
  name = "covid"
  start_urls = ['https://cv.nmhealth.org/newsroom/']

# Use this when testing to make sure we don't follow the "Older Entries" link
#  custom_settings = {
#    'DEPTH_LIMIT': 1
#  }

  def parse(self, response):
    for link in response.css('h2.entry-title a::attr(href)').getall():
      yield response.follow(link, self.parse)

    for content in response.css('div[class = "container"]'):
      yield {
        'newCases': content.css('li:contains("new cas")::text').getall(),
        'date': content.css('span[class=published]::text').get(),
      }

    next_page = response.css('div.alignleft a::attr(href)').get()
    if next_page is not None:
      yield scrapy.Request(next_page, callback=self.parse)

#    page = response.url.split("/")[-2]
#    filename = 'covid-%s.html' % page
#    with open(filename, 'wb') as f:
#      f.write(response.body)
#    self.log('Saved file %s' % filename)
