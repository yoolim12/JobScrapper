from bs4 import BeautifulSoup
from requests import get

def extract_wwr_jobs(term):
  base_url = f"https://weworkremotely.com/remote-{term}-jobs"
  response = get(base_url)
  jobres = []
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find('section', class_='jobs')
    jobs2 = jobs.find('ul')
    joblist = jobs2.find_all('li', recursive=False)
    del joblist[-1]

    for job in joblist:
      company = job.find_all('span', class_='company')[0]
      jobtitle = job.find('span', class_='title')
      jobtime = job.find_all('span', class_='company')[1]
      location = job.find('span', class_='region company')
      joblink = job.find_all('a')[1]['href']

      isImage = job.find('div', class_='flag-logo')
      if isImage != None:
        jobimg = isImage['style'].strip('background-image:url()')
      else:
        jobimg = ""

      if not joblink.startswith('https://weworkremotely.com/'):
        joblink = 'https://weworkremotely.com/' + joblink
      job_info = {
        'company' : company.string.strip('\n').replace(',','&'),
        'jobtitle' : jobtitle.string.strip('\n').replace(',','&'),
        'jobinfo' : jobtime.string.strip('\n').replace(',','&'),
        'location' : location.string.strip('\n').replace(',','&'),
        'joblink' : joblink.strip('\n'),
        'jobimg' : jobimg.strip('\n')
      }

      jobres.append(job_info)

  return jobres