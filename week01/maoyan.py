import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

#请求头部
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'   

header = {'user-agent':user_agent}
#访问地址
myurl = 'https://maoyan.com/films?showType=3'   
#设置爬取的数量
NUM = 10   

response = requests.get(myurl,headers=header)  

bs_info = bs(response.text, 'html.parser')

#写入通过验证后的cookie
COOKIE = '__mta=88971940.1593317584685.1593335526097.1593335539540.5; uuid_n_v=v1; uuid=A9EE5A90B8F511EAAD7CEBC74F78E0F979100B34E57C4AFE9E109609807D065C; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593317584,1593317712,1593335488,1593335685; _lxsdk_cuid=172f920ec0ec8-09c6ab6b8443ca8-4c302c7d-144000-172f920ec0ec8; _lxsdk=A9EE5A90B8F511EAAD7CEBC74F78E0F979100B34E57C4AFE9E109609807D065C; __mta=88971940.1593317584685.1593335539540.1593335685308.6; mojo-uuid=6e090b86b2b0a7594465eb35d437c9a5; _csrf=4986367c1ecbc235204d4ecefe231aa1fea0570d319953334465042cd821b9e1; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593335685; _lxsdk_s=172fac8ce4e-2bf-225-049%7C%7C1'


result_list = []

for i, movie_tags in enumerate(bs_info.find_all('div', attrs={'class': 'movie-hover-info'})):
    if i == NUM:
        break
    #movie_name = None
    #movie_type = None
    #movie_time = None
    for movie_info in movie_tags.find_all('div'):
        movie_name = movie_info.get('title')
        span = movie_info.find('span')
        if span.text == '类型:':
            movie_type = movie_info.text.split()[-1]
        elif span.text == '上映时间:':
            movie_time = movie_info.text.split()[-1]
    result = {'movie_name':movie_name, 'movie_type': movie_type, 'movie_time': movie_time}
    result_list.append(result)

movie1 = pd.DataFrame(result_list)
movie1.to_csv('./movie1_result.csv', index=False)

print('myurl: ' + response.url)
print('Status code: {}'.format(response.status_code))
print('Done')