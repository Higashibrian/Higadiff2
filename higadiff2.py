#!/usr/bin/ python
#Import Required Packages
from PIL import Image, ImageDraw, ImageChops, ImageFilter,ImageOps
import PIL
import os,csv,time, BHTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from slacker import Slacker
import multiprocessing
import threading
import datetime



var_crawl=True
con_crawl=True


threads=6
timetorun=0
#set a variable to equal current date and time
#add two minutes to that variable
#timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
intwominutes=datetime.datetime.now() + datetime.timedelta(0,0,0,0,2,0,0)
url_list=[]
navs_list=[]
page_info_list=[]
slack_message=''

timein=datetime.datetime.now()
cwd=os.getcwd()
timedir=str(timein.strftime('%m%d_%H%M'))
slack = Slacker('xoxp-3224245812-6395256785-7719710624-411e26')
con_time_dir=timedir
var_time_dir=timedir

condom=raw_input('enter the URL for your control site:\n\thttp://')
vardom=raw_input('enter the URL for your updated site:\n\thttp://')

conauth=raw_input(condom+' auth?\n')
varauth=raw_input(vardom+' auth?\n')

conpw=raw_input('Con Password?\n')
varpw=raw_input('Var Password?\n')

conbase='http://'+conauth+condom
varbase='http://'+varauth+vardom

if not con_crawl:
    con_time_dir=raw_input('Enter the Time Code for the first set of images')
if not var_crawl:
    var_time_dir=raw_input('Enter the Time Code for the second set of images')

condom=condom.replace('.','_')
vardom=vardom.replace('.','_')
compdom='comparisons/'+condom+'_V_'+vardom

condom='sites/'+condom
vardom='sites/'+vardom
#########
#for root in os.listdir(os.getcwd()+'/'+condom):
#    print root
#########

condom=condom+'/'+str(timedir)
vardom=vardom+'/'+str(timedir)
compdom=compdom+'/'+str(timedir)

try:
    os.makedirs(compdom+'/passed')
except:
    pass

try:
    os.makedirs(compdom+'/failed')
except:
    pass
try:
    os.makedirs(condom+'/pictures')
except:
    pass
try:
    os.makedirs(vardom+'/pictures')
except:
    pass
####open internal_all.csv and create list of pages to visit.
with open ('internal_all.csv','rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
for x in range(2,len(your_list)):
    visit_me = your_list[x][0]
    url_list.append(visit_me)
###^open internal_all.csv^###

for url in url_list:
    nav=''
    url_split=url.split('/')
    for x in range (3,len(url_split)):
        nav=nav+'/'+url_split[x]
    navs_list.append(nav)

##open file for code
try:
    f=open(os.getcwd()+'/loopcode.txt')
    loopcode=(f.read())
    print 'I found some code'
except:
    loopcode='pass'
    print 'not running any code today'
##
try:
    g=open(os.getcwd()+'/headcode.txt')
    headcode=(g.read())
    print 'I found some code'
except:
    headcode='pass'
    print 'not running any code today'

conselect=raw_input('condriver?\n\t1)PhantomJS\n\t2)Firefox\n\t3)Chrome\n\t4)IE9')
varselect=raw_input('vardriver?\n\t1)PhantomJS\n\t2)Firefox\n\t3)Chrome\n\t4)IE9')

def set_browser(select):
    if select=='1':
        driver=webdriver.PhantomJS()
    elif select =='2':
        driver = webdriver.Firefox()
    elif select =='3':
        driver = webdriver.Chrome()
    elif select =='4':
        driver = webdriver.DesiredCapabilities.ie
    return driver

def run():
    print 'run just started'
    global navs_list
    global timetorun
    global pw
    global url_list
    global page_info_list
    #####
    print 'get webdrivers'
    condriver = set_browser(conselect)
    vardriver = set_browser(varselect)
    condirect=''
    vardirect=''
    print 'got webdrivers'
    condriver.set_window_size('1080','1080')
    vardriver.set_window_size('1080','1080')
    condriver.get(conbase)
    vardriver.get(varbase)
    print 'bases loaded'
    try:
        condriver.find_element_by_css_selector("#password_protected_pass").send_keys(conpw)
        condriver.find_element_by_css_selector("#password_protected_pass").send_keys(Keys.RETURN)
        condriver.find_element_by_css_selector("#menu-secondary > li:nth-child(6) > a").click()
    except:
        pass

    try:
        vardriver.find_element_by_css_selector("#password_protected_pass").send_keys(varpw)
        vardriver.find_element_by_css_selector("#password_protected_pass").send_keys(Keys.RETURN)
        vardriver.find_element_by_css_selector("#menu-secondary > li:nth-child(6) > a").click()
    except:
        pass
    print 'passed password protect'
    exec(headcode)
    print 'executed headcode'
    while timetorun < len(url_list):
        print 'start while'
        this=timetorun
        
        timetorun+=1
        print varbase+navs_list[this]

        print '---'
        condriver.get(conbase+navs_list[this])
        vardriver.get(varbase+navs_list[this])



        direct=navs_list[this]
        print 'driver.get'
        time.sleep(2)
        try:
            exec(loopcode)
        except:
            print 'error in loopcode'
        print (conbase+navs_list[this])+'\t'+(varbase+navs_list[this])
        a=condriver.get_screenshot_as_base64()
        b=vardriver.get_screenshot_as_base64()
        
        f = open(condom+"/pictures/"+str(this)+".png", "wb")
        f.write(a.decode('base64'))
        f.close()

        f = open(vardom+"/pictures/"+str(this)+".png", "wb")
        f.write(b.decode('base64'))
        f.close()        
        page_info_list.append((this,conbase+navs_list[this],varbase+navs_list[this]))


        print str(this)
    condriver.quit()
    vardriver.quit()

start_time = time.time()
##
time.sleep(2)

for x in range (0,threads):
    time.sleep(1)
    exec('mult'+str(x)+' = threading.Thread(target=run, args=())')
    exec('print mult'+str(x))
    exec('mult'+str(x)+'.start()')
    time.sleep(0)



for x in range (0,threads):
   exec('mult'+str(x)+'.join()')
##
this=os.getcwd()
page_info_list.sort()
slack_massage=[]#
for x in range (0,len(url_list)):
    time.sleep(.2)
    print 'comparing '+str(x)
    con = Image.open(condom+'/pictures/'+str(x)+'.png')
    var = Image.open(vardom+'/pictures/'+str(x)+'.png')
    con.load()
    var.load()
    filename=str(page_info_list[x][1]).replace('.','_')
    filename=filename.replace('/',':')
    varg=ImageOps.grayscale(var)
    cong=ImageOps.grayscale(con)

    diffo = ImageChops.difference(varg,cong)
    diffpic = ImageChops.difference(var,con)
    imgstats=sum(i * n for i, n in enumerate(diffo.histogram()))

    new_img_width=var.size[0]+var.size[0]+var.size[0]
    if var.size[1]>=con.size[1]:
        new_img_height=var.size[1]
    else:
        new_img_height=con.size[1]
    new_img_height=var.size[1]
    img_two_thirds=var.size[0]+var.size[0]
    concated=Image.new('RGB',(new_img_width,new_img_height),'white')
    visual_fails=0
    text_fails=0

    concated.paste(con,(0,0))
    concated.paste(diffpic,(var.size[0],0))
    concated.paste(var,(img_two_thirds,0))

    if imgstats>0:
        concated.save(compdom+'/failed/'+str(x)+filename+'.png')
        slack_massage.append('\n '+str(x)+'\t'+page_info_list[x][1]+'\t'+page_info_list[x][2])
        if len(slack_massage)%25==0:
            for item in slack_massage:
                slack_message=slack_message+item
            slack.chat.post_message('#automation_log',slack_message)
            slack_massage=[]
            slack_message=''
        #slack_message=slack_message+'\n'+str(x)+'\t'+page_info_list[x][1]+'\t'+page_info_list[x][2]

    else:
        con.save(compdom+'/passed/'+str(x)+filename+'.png')
    
print "---"+str(time.time()-start_time)+" seconds ---"

if len(slack_massage)>0:
    for item in slack_massage:
        slack_message=slack_message+item
    slack.chat.post_message('#automation_log', slack_message)

slack.chat.post_message('#automation_log', 'The visual comparison has completed for '+conbase+ '_v_' + varbase+'\n '+str())

