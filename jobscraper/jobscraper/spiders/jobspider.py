import scrapy
from jobscraper.items import JobItem

class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["www.reed.co.uk"]
    start_urls = ["https://www.reed.co.uk/jobs/data-analyst-jobs"]

    def parse(self, response):
        url = 'https://www.reed.co.uk/jobs/data-analyst-jobs'
        jobs = response.css('article.card.job-card_jobCard__MkcJD')

        for job in jobs:
            relative_url = job.css('h2 a ::attr(href)').get()
            job_url = 'https://www.reed.co.uk' + relative_url
            yield response.follow(job_url, callback=self.parse_all_job)
            
        next_page =  response.css('a.page-link.next ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.reed.co.uk' + next_page
            yield response.follow(next_page_url, callback= self.parse)
            
    def parse_all_job(self, response):
        job_item = JobItem()
        
        job_item['Detail_URL'] = response.url,
        job_item['Title'] = response.css('.col-xs-12 h1::text').get(),
        job_item['Salary'] = response.css('.salary.col-xs-12.col-sm-6.col-md-6.col-lg-6 span::text').get(),
        job_item['Contract_Type'] = response.css('.time.col-xs-12.col-sm-6.col-md-6.col-lg-6 a ::text').get(),
        job_item['Job_Type'] = response.css('.time.col-xs-12.col-sm-6.col-md-6.col-lg-6 a:last-child::text').get(),
        job_item['Location'] = response.css('.location.col-xs-12.col-sm-6.col-md-6.col-lg-6 a span::text').get(),  
        yield job_item