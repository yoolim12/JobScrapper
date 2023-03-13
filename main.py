from flask import Flask, render_template, request, redirect, send_file
from extractor.wwr import extract_wwr_jobs
from extractor.rmok import extract_rmok_jobs
from file import save_to_file

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
  return render_template('home.html')

@app.route("/search")
def search():
  keyword = request.args.get('keyword')
  if keyword == None or keyword == "":
    return redirect("/")
  if keyword in db:
    result = db[keyword]
  else:
    wwr = extract_wwr_jobs(keyword)
    rmok = extract_rmok_jobs(keyword)
    result = wwr + rmok
    db[keyword] = result
  return render_template('search.html', keyword=keyword, result=result, cnt=len(result))

@app.route("/export")
def export():
  keyword = request.args.get('keyword')
  if keyword == None or keyword == "":
    return redirect("/")
  if keyword not in db:
    return redirect(f'/search?keyword={keyword}')
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0")