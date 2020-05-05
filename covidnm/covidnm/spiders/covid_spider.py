import scrapy

counties = ['Bernalillo','Catron','Chaves','Cibola','Colfax','Curry','De Baca','Dona Ana','Eddy','Grant','Guadalupe','Harding','Hidalgo','Lea','Lincoln','Los Alamos','Luna','McKinley','Mora','Otero','Quay','Rio Arriba','Roosevelt','Sandoval','San Juan','San Miguel','Santa Fe','Sierra','Socorro','Taos','Torrance','Union','Valencia']

class CovidSpider(scrapy.Spider):
  name = "covid"
  start_urls = ['https://cv.nmhealth.org/newsroom/']

# Use this when testing to make sure we don't follow the "Older Entries" link
#  custom_settings = {
#    'DEPTH_LIMIT': 5
#  }

  def parse(self, response):
    for link in response.css('h2.entry-title a::attr(href)').getall():
      yield response.follow(link, self.parse)

    for content in response.css('div[class = "container"]'):
      for county in counties:
        countyM = county + 'M'
        countyS = county + 'S'
        county_mult_msg = 'new cases in ' + county + ' County'
        county_single_msg = 'new case in ' + county + ' County'
        yield {
          'date': content.xpath('//div[@class="container"]//span[@class="published"]/text()').get(),
          'county': county,
          'countyM': content.xpath('//div[@class="container"]//li[contains(text(), $msg)]', msg=county_mult_msg).getall(),
          'countyS': content.xpath('//div[@class="container"]//li[contains(text(), $msg)]', msg=county_single_msg).getall(),

        #'BernalilloCountyM': content.css('li:contains("new cases in Bernalillo County")::text').getall(),
        #'BernalilloCountyS': content.css('li:contains("new case in Bernalillo County")::text').getall(),
        #'McKinleyCountyM': content.css('li:contains("new cases in McKinley County")::text').getall(),
        #'McKinleyCountyS': content.css('li:contains("new case in McKinley County")::text').getall(),
        }
        # print(countyM)

    next_page = response.css('div.alignleft a::attr(href)').get()
    if next_page is not None:
      yield scrapy.Request(next_page, callback=self.parse)

#    page = response.url.split("/")[-2]
#    filename = 'covid-%s.html' % page
#    with open(filename, 'wb') as f:
#      f.write(response.body)
#    self.log('Saved file %s' % filename)
