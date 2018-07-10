import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_summary_from_result(soup): 
  summaries = []
  spans = soup.findAll('span', attrs={'class': 'summary'})
  for span in spans:
    summaries.append(span.text.strip())
  return summaries


def extract_salary_from_result(soup): 
  salaries = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    if div.find('nobr') is not None:
      salaries.append(div.find('nobr').text)
    else:
      div_two = div.find(name="div", attrs={"class": "sjcl"})
      if div_two is not None and div_two.find("div") is not None:
        salaries.append(div_two.find("div").text.strip())
      else:
        salaries.append("Nothing_found")
  return salaries


def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll('span', attrs={'class': 'location'})
  for span in spans:
    locations.append(span.text)
  return locations

def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    company = div.find_all(name="span", attrs={"class":"company"})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
        companies.append(span.text.strip())
  return companies

def extract_job_title_from_result(soup): 
  jobs = []
  for div in soup.find_all(name="div", attrs={"class":"row"}):
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
      jobs.append(a["title"])
  return jobs


def main():
  max_results_per_city = 100
  num_results_per_page = 10
  city_set = ['New+York', 'Chicago', 'San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']
  columns = ['city', 'job_title', 'company_name', 'location', 'salary', 'summary']


  # scraping code:
  for city in city_set:
    sample_df = pd.DataFrame(columns=columns)
    for start in range(0, max_results_per_city, num_results_per_page):
      page = requests.get("https://www.indeed.com/jobs?q=translator&l={city}&start={start}".format(city=city, start=start))
      time.sleep(1)  # ensuring at least 1 second between page grabs
      soup = BeautifulSoup(page.text, "html.parser")
      job_titles =  extract_job_title_from_result(soup)
      companies = extract_company_from_result(soup)
      locations =  extract_location_from_result(soup)
      salaries = extract_salary_from_result(soup)
      summaries =  extract_summary_from_result(soup)

      for i in range(len(job_titles)):
        job_post = [city, job_titles[i], companies[i], locations[i], salaries[i], summaries[i]]
        sample_df.loc[len(sample_df) + 1] = job_post
    sample_df.to_csv('results/{city}.csv'.format(city=city), encoding='utf-8')


if __name__ == '__main__':
    main()
