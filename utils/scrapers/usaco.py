from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

SAVE_PATH = dir_path + '/prescraped/usaco/'
scraped_problems = os.listdir(SAVE_PATH + "Problems")
scraped_editorials = os.listdir(SAVE_PATH + "Editorials")


def anti_scrape(soup):
    if soup.text == "Just a moment...Enable JavaScript and cookies to continue":
        print("Bypassing anti-scrap protection...")
        scr = soup.findAll("script")[-1].string
        scr = scr[scr.index("var a=toNumbers"):].split(';')
        line = scr[0]
        abc = []
        while "toNumbers" in line:
            i = line.index("toNumbers")
            line = line[i+11:]
            abc.append(line[:line.index('"')])
        from Crypto.Cipher import AES
        def to_numbers(x):
            return bytes(int(x[i:i+2], 16) for i in range(0, len(x), 2))
        key, iv, cipher = map(to_numbers, abc)
        aes = AES.new(key, AES.MODE_CBC, iv)
        rcpc = aes.decrypt(cipher).hex()
        print(f"RCPC = {rcpc}")
        url = scr[-2]
        url = url[url.index('"')+1:-1]
        r = requests.get(url, cookies={"RCPC": rcpc})
        s = r.text
        soup = BeautifulSoup(s, "html.parser")

def read(file_path):
    res = ""
    with open(file_path, 'r') as f:
        res = f.read()

    return res

def from_url(url):
    return url.split('/')[-1]

def problem(url):
    pid = from_url(url)
    if (pid in scraped_problems):
        statement = read(SAVE_PATH + "Problems/" + pid)
        if (len(statement)):
            return {"statement": statement}

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    soup = soup.find_all(class_='problem-text')[0]

    while soup.pre != None: # removes all code
        soup.pre.decompose()



    prob = soup.text

    prob = prob.split("SAMPLE INPUT")
    
    prob[-1] = prob[-1].split("SCORING:")


    prob = prob[0] + "SCORING:" +  prob[-1][-1]

    with open(SAVE_PATH + 'Problems/' + pid, 'w') as f:
        f.write(prob)
    scraped_problems.append(pid)

    return {"statement": prob}



def editorial(prob_url, edi_url, bot=None, query_func=None): # TODO: Fix random line breaks in the scrapes
    pid = from_url(edi_url)
    print(pid, scraped_editorials)
    if (pid in scraped_editorials):
        edi = read(SAVE_PATH + "Editorials/" + pid)
        if (len(edi)):
            return edi



    response = requests.get(edi_url)

    soup = BeautifulSoup(response.text, 'html.parser')

    while soup.pre != None: # removes all code
        soup.pre.decompose()

    edi = []

    for tag in soup.find_all(['p']):
        if (tag.parent.name != 'body'):
            continue

        latex_content = tag.text

        # print(tag.parent.name)

        # for elem in tag.descendants: # In case LaTeX doesn't render automatically with bs4

        #     if (elem.find_parent().name != 'p' and elem.find_parent().name != 'a' and elem.find_parent().name != 'center'):
        #         continue

        #     if isinstance(elem, str):
        #         latex_content += elem
        #     elif elem.name == "script" and elem.get("type") == "math/tex":
        #         latex_content += "$$$" + elem.string + "$$$"

        
        # if ("code:" in latex_content.lower()):
        #     continue
        edi.append(latex_content)

    edi = '\n'.join(edi)

    # print('bot', bot)

    # if (bot):
    #     edi = bot.chat(query_func(problem(prob_url), edi))


    with open(SAVE_PATH + 'Editorials/' + pid, 'w') as f:
        f.write(edi)
    scraped_editorials.append(pid)

    return edi

    

# print(editorial('https://usaco.org/current/data/sol_prob2_platinum_open24.html'))
# print(problem('https://usaco.org/index.php?page=viewproblem2&cpid=1428')['statement'])

