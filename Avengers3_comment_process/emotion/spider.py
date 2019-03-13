import requests
from bs4 import BeautifulSoup
import pandas as pd
#导入外部cookies
raw_cookies = 'Cookie: bid=N1KCEpjnAsM; __yadk_uid=bcrWROPbwyaIwQCosFcJhCe3pYBdusof; ll="118204"; _vwo_uuid_v2=DAE6A6312D891660B7ED1B9B76FA6AF70|cb663de30fa369527b074247cd396e05; __utmc=30149280; ap=1; ps=y; push_noty_num=0; push_doumail_num=0; __utma=30149280.281089888.1510583746.1528372468.1528376090.16; __utmz=30149280.1528376090.16.13.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; dbcl2="179605616:gutKLa6LaO0"; ck=x5EZ; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1528376145%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%22%5D; _pk_id.100001.8cb4=a59a15cef77b5575.1510583742.15.1528376145.1528359283.; _pk_ses.100001.8cb4=*; __utmt=1; __utmv=30149280.17960; __utmb=30149280.2.10.1528376090'
cookies = {}
def savedata(texts):
    wirte_flag = True
    path = 'fulian_content.txt'
    with open(path, 'a', encoding='utf-8') as f:
        f.writelines(texts+'\n')
        f.close()
for line in raw_cookies.split(';'):
        key, value = line.split('=', 1)  # 1代表只分一次，得到两个数据
        cookies[key] = value
for i in range(0,400,20):
    url = "https://movie.douban.com/subject/24773958/comments?start="+str(i)+"&limit=20&sort=new_score&status=P"
    req = requests.get(url,cookies=cookies)
    bf = BeautifulSoup(req.content,"html.parser")
    bf_div = bf.find_all('div',class_="comment")
    for each in range(len(bf_div)):
        content = str(bf_div[each].find('p').text).strip()
        #username = bf_div[each].find('span',class_="comment-info").find('a').text
        #comment_time = str(bf_div[each].find('span',class_="comment-time").text).strip()
        #votes = bf_div[each].find('span',class_='votes').text
        #texts = username+","+content+","+comment_time+","+votes
        #print(texts)
        savedata(content)


