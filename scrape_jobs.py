import requests
import xlsxwriter
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# function for creating soup object from web page content
def create_soup(url, headers=None):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

# coursera
def get_coursera_jobs(headers=None):
    r = requests.get("https://api.lever.co/v0/postings/coursera", headers=headers)
    jobs = {}
    for job in r.json():
        jobs[job["text"]] = job["hostedUrl"]
    return jobs

# khan academy
def get_khanacademy_jobs(headers=None):
    soup = create_soup("https://www.khanacademy.org/careers")
    jobs_html = soup.find_all(class_="span4")
    jobs = {}
    for tags in jobs_html:
        a_tags = tags.find_all("a")
        for job in a_tags:
            title = job.get_text().strip()
            jobs[title] = job["href"]
    return jobs

# udemy
def get_udemy_jobs(headers=None):
    r = requests.get("https://api.lever.co/v0/postings/udemy?&group=department&mode=json",
                     headers=headers)
    jobs = {}
    for depts in r.json():
        for job in depts["postings"]:
            title = job["text"].strip()
            jobs[title] = job["hostedUrl"]
    return jobs

# edx
def get_edx_jobs(headers=None):
    soup = create_soup("https://www.edx.org/careers")
    jobs_html = soup.find_all(class_="job-link")
    jobs = {}
    for job in jobs_html:
        title = job.get_text().strip()
        jobs[title] = job["href"]
    return jobs

# duolingo
def get_duolingo_jobs(headers=None):
    r = requests.get("https://boards-api.greenhouse.io/v1/boards/duolingo/departments",
                     headers=headers)
    jobs = {}
    for depts in r.json()["departments"]:
        if depts["jobs"] != []:
            for job in depts["jobs"]:
                title = job["title"].strip()
                jobs[title] = job["absolute_url"]
    return jobs
            
# teachers pay teachers
def get_tpt_jobs(headers=None):
    r = requests.get("https://api.greenhouse.io/v1/boards/teacherspayteachers/jobs?content=trues",
                     headers=headers)
    jobs = {}
    for job in r.json()["jobs"]:
        title = job["title"].strip()
        jobs[title] = job["absolute_url"]
    return jobs
 
# newsela
def get_newsela_jobs(headers=None):
    soup = create_soup("https://boards.greenhouse.io/embed/job_board?for=newsela&b=https%3A%2F%2Fnewsela.com%2Fabout%2Fcompany%2Fcareers%2Fpost%2F")
    jobs = {}
    for job in soup.find_all("a"):
        title = job.get_text().strip()
        jobs[title] = job["href"]
    return jobs

# code for america
def get_cfa_jobs(headers=None):
    soup = create_soup("https://boards.greenhouse.io/embed/job_board?for=codeforamerica&b=https%3A%2F%2Fwww.codeforamerica.org%2Fjobs")
    jobs = {}
    for job in soup.find_all("a"):
        title = job.get_text().strip()
        jobs[title] = job["href"]
    return jobs

# codecademy
def get_codecademy_jobs(headers=None):
    r = requests.get("https://api.greenhouse.io/v1/boards/codeacademy/jobs?content=true",
                     headers=headers)
    jobs = {}
    for job in r.json()["jobs"]:
        title = job["title"].strip()
        jobs[title] = job["absolute_url"]
    return jobs

# code.org
def get_codeorg_jobs(headers=None):
    r = requests.get("https://api.lever.co/v0/postings/code.org?group=team&mode=json",
                     headers=headers)
    jobs = {}
    for dept in r.json():
        for job in dept["postings"]:
            title = job["text"].strip()
            jobs[title] = job["hostedUrl"]
    return jobs


if __name__ == "__main__":
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
    jobs = {
        "Coursera": get_coursera_jobs(headers),
        "Khan Academy": get_khanacademy_jobs(headers),
        "EdX": get_edx_jobs(headers),
        "Duolingo": get_duolingo_jobs(headers),
        "Teachers Pay Teachers": get_tpt_jobs(headers),
        "Newsela": get_newsela_jobs(headers),
        "Code for America": get_cfa_jobs(headers),
        "Codecademy": get_codecademy_jobs(headers),
        "Code.org": get_codeorg_jobs(headers)
    }
    # create workbook/worksheet
    date_today = datetime.date(datetime.now())
    workbook = xlsxwriter.Workbook(f"Job Postings {date_today}.xlsx")
    worksheet = workbook.add_worksheet()

    # formatting
    header_format = workbook.add_format({
        "bold": True,
        "bg_color": "#DCE6F1"
    })
    green_format = workbook.add_format({"bg_color": "#C6EFCE"})

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 1, 97)
    worksheet.set_column(2, 2, 63)

    # write data to worksheet
    worksheet.write(0, 0, "Company", header_format)
    worksheet.write(0, 1, "Job Title", header_format)
    worksheet.write(0, 2, "Application Link", header_format)
    row_num = 1
    for company, data in jobs.items():
        for title, link in data.items():
            worksheet.write(row_num, 0, company)
            worksheet.write(row_num, 1, title)
            worksheet.write(row_num, 2, link)
            row_num += 1

    #conditional formatting
    worksheet.conditional_format(1, 0, row_num, 2, {"type": "formula",
                                                    "criteria": '=SEARCH("data", $B2)>0',
                                                    "format": green_format})
    worksheet.conditional_format(1, 0, row_num, 2, {"type": "formula",
                                                    "criteria": '=SEARCH("analy", $B2)>0',
                                                    "format": green_format})
    workbook.close()

