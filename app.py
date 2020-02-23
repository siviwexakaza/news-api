from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

BASE_URL ='https://mg.co.za/section/'
news =[]
global page




@app.route('/business',methods=['GET'])
def getBusiness():
    page= requests.get(BASE_URL+'business').text
    return sendToClient(page)

@app.route('/health',methods=['GET'])
def getHealth():
    page= requests.get(BASE_URL+'health').text
    return sendToClient(page)

@app.route('/motoring',methods=['GET'])
def getMotoring():
    page= requests.get(BASE_URL+'motoring').text
    return sendToClient(page)


@app.route('/education',methods=['GET'])
def getEducation():
    page= requests.get(BASE_URL+'education').text
    return sendToClient(page)


def sendToClient(p):

    soup = BeautifulSoup(p,'lxml')

    for div_tag in soup.find_all('div',{'class':'tdb_module_loop'}):
        try:
            link = div_tag.find('a',{'class':'td-image-wrap'}).attrs['href']
            image = div_tag.find('span',{'class':'entry-thumb'}).attrs['style'][22:].split(')')[0]
            title = div_tag.find('h3',{'class':'entry-title'}).find('a').text.replace('      ',' ')
            description = div_tag.find('div',{'class':'td-excerpt'}).text

            item = {"Link":link,"Image":image,"title":title, "description":description}
            news.append(item)

            

        except Exception as identfier:
            pass

    return jsonify(news)

    


@app.route('/',methods=['GET'])
def index():
    return jsonify({"Message":"News API works!"})

if __name__ == '__main__':
    app.run(debug= True)