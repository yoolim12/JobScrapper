from bs4 import BeautifulSoup
import requests

def extract_rmok_jobs(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  joblist = []
  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    # write your ✨magical✨ code here
    jobs = soup.find_all('tr', class_='job')
    
    for job in jobs:
      location = ""
      salary = ""
      a = job.find('a', class_='preventLink')
      joblink = a['href']
      if a.find('img') != None:
        jobimg = a.find('img')['data-src']
      else:
        jobimg = ""
      company = job.find('h3', {'itemprop': 'name'})
      jobtitle = job.find('h2', {'itemprop': 'title'})
      location_and_salary = job.find_all('div', class_='location')
      
      isSalary = location_and_salary.pop(-1)
      if '$' in isSalary.string:
        salary = isSalary.string
      else:
        location_and_salary.append(isSalary)

      if(len(location_and_salary) == 0):
        location = "Not Indicated"
      else:
        for el in location_and_salary:
          location += el.string + '/'
        location = location.rstrip('/')

      if not joblink.startswith('https://remoteok.com'):
        joblink = 'https://remoteok.com' + joblink

      job_info = {
        'joblink' : joblink.strip('\n'),
        'company' : company.string.strip('\n').replace(',','&'),
        'jobtitle' : jobtitle.string.strip('\n').replace(',','&'),
        'location' : location.strip('\n').replace(',','&'),
        'jobinfo' : salary.strip('\n').replace(',','&'),
        'jobimg' : jobimg.strip('\n')
      }
      joblist.append(job_info)
  
  return joblist