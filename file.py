def save_to_file(keyword, joblist):
  file = open(f"{keyword}.csv", "w")
  file.write("COMPANY, JOB TITLE, LOCATION, WORKING HOURS or SALARY, TO APPLY\n")

  for job in joblist:
    file.write(f"{job['company']}, {job['jobtitle']}, {job['location']},{job['jobinfo']}, {job['joblink']}\n")

  file.close()