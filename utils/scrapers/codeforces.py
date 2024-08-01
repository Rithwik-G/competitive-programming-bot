from bs4 import BeautifulSoup
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

SAVE_PATH = dir_path + '/prescraped/codeforces/'
scraped_problems = os.listdir(SAVE_PATH + "Problems")
scraped_editorials = os.listdir(SAVE_PATH + "Editorials")


def anti_scrape(soup):
    if soup.text == "Just a moment...Enable JavaScript and cookies to continue":
        print("Bypassing anti-scrap protection...")
        scr = soup.findAll("script")[-1].string
        print(scr)
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
    pid = url.split('/')[-3:]
    pid.remove('problem')
    pid = ''.join(pid);
    return pid

def problem(url):

    pid = from_url(url)

    if (pid in scraped_problems):
        statement = read(SAVE_PATH + "Problems/" + pid)
        if (len(statement)):
            return {"statement": statement}


    chrome_options = Options()  
    chrome_options.add_argument("--headless") # Opens the browser up in background

    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        response = browser.page_source

    # response = requests.get(url)

    soup = BeautifulSoup(response, 'html.parser')

    # anti_scrape(soup)

    problem_statements = soup.find_all(class_='problem-statement')

    # print(p)
    for statement in problem_statements:
        # title
        title = statement.find(class_='title').text.strip()
        
        # time limit
        time_limit = statement.find(class_='time-limit').text.strip().replace('time limit per test', '')
        
        # memory limit
        memory_limit = statement.find(class_='memory-limit').text.strip().replace('memory limit per test', '')
        
        # Fails for interactives (and presumably output only's) 

        # # input format
        # input_spec = statement.find(class_='input-specification').text.strip().replace('Input', '')
        # # print("Input Specification:", input_spec)
        
        # # output format
        # output_spec = statement.find(class_='output-specification').text.strip().replace('Output', '')
        # # print("Output Specification:", output_spec)
        
        problem = ""
        for child in statement.children:
            if child.name == 'div' and ('input-specification' in child.get('class', [])):
                break

            if child.name == 'div' and ('header' not in child.get('class', [])):
                problem += child.text.strip()

        # sample inputs
        examples = statement.find(class_='sample-tests')
        input_tests = examples.find_all(class_='test-example-line')

        inputs = ""
        for i in input_tests: 
            input_example_lines = i.text.strip()
            inputs += input_example_lines
            inputs += '\n'
        
        # sample outputs
        output_tests = examples.find_all(class_='output')    
        outputs = ""

        # print(output_tests.text.strip())
        for i in output_tests:  
            output_example_lines = i.text.strip().replace('Output\n', '')
            outputs += output_example_lines
            outputs += '\n'
        
        note = statement.find(class_='note')
        notes = ""

        if note:
            note_text = note.text.strip().replace('Note', '')
            notes += note_text
            # print("Note:", note_text)
        
        data = {
            "title": title,
            "time_limit": time_limit,
            "memory_limit": memory_limit,
            # "input_format": input_spec,
            # "output_format": output_spec,
            "statement": problem,
            "sample_input": inputs,   
            "sample_outputs": outputs,
            "note": notes
        }

        with open(SAVE_PATH + 'Problems/' + pid, 'w') as f:
            f.write(data["statement"])
        scraped_problems.append(pid)

    return data



def editorial(prob_url, edi_url, bot=None, query_func=None):
    pid = from_url(prob_url)

    if (pid in scraped_editorials):
        edi = read(SAVE_PATH + "Editorials/" + pid)
        if (len(edi)):
            return edi

    domain = 'https://codeforces.com/'
    if (domain in prob_url):
        prob_url=prob_url[len(domain):]
    if ('problemset/problem/' in prob_url):
        # print(prob_url)
        prob_url=prob_url[len('problemset/problem/'):]
        # print(prob_url)
        prob_url = 'contest/' + '/problem/'.join(prob_url.split('/'))


    chrome_options = Options()  
    chrome_options.add_argument("--headless") # Opens the browser up in background

    with Chrome(options=chrome_options) as browser:
        browser.get(edi_url)
        response = browser.page_source

    soup = BeautifulSoup(response, 'html.parser')

    # anti_scrape(soup)

    soup = soup.find_all(class_='content')[0]


    while soup.pre != None: # removes all code
        soup.pre.decompose()

    edi = []

    on = False # checks what problem we're on

    contest_url = '/'.join(prob_url.split('/')[:-1])

    for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'center', 'b']):

        
        links = tag.find_all(href=True)

        # if (len(links)):
        #     print(links[0].prettify())
        #     print(prob_url)
        #     print(contest_url)
        if (len(links) > 0 and prob_url in links[0].prettify()):
            on=True
        elif len(links) > 0 and contest_url in links[0].prettify():
            on = False
        elif on:
            latex_content = ""

            for elem in tag.descendants: # In case LaTeX doesn't render automatically with bs4

                if (elem.find_parent().name != 'p' and elem.find_parent().name != 'a' and elem.find_parent().name !='b' and elem.find_parent().name != 'center'  and elem.find_parent().name != 'li'):
                    continue

                bold = elem.find_parent().name == 'b'
                if isinstance(elem, str):   
                    if ('code' in elem.lower() and bold):
                        continue
        
                    latex_content += '**' * bold + elem +  '**' * bold

                elif elem.name == "script" and elem.get("type") == "math/tex":
                    latex_content += "$$$" + elem.string + "$$$"

                

            edi.append(latex_content)

    edi = '\n'.join(edi)

    # print('bot', bot)

    # if (bot):
    #     edi = bot.chat(query_func(problem(prob_url), edi))


    with open(SAVE_PATH + 'Editorials/' + pid, 'w') as f:
        f.write(edi)
    scraped_editorials.append(pid)

    return edi


# print(problem('https://codeforces.com/problemset/problem/1985/G'))

