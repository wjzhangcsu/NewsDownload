from pattern.web import URL

import os, os.path, sys, errno
import datetime

import urllib2 

def downloadPdf(urlStr, targetFile):
    url = URL(urlStr)
    f = open(targetFile, 'wb')
    f.write(url.download(timeout=50, cached=False))
    f.close()
    return True


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def urlexists(urlStr):
    url = URL(urlStr)
    existornot=url.exists
    return existornot


class Paper:
    baseDir = "./"
    baseUrl = ""

    def __init__(self):
        pass

    def download():
        pass



class Jfrb(Paper):
    baseUrl = "http://newspaper.jfdaily.com/jfrb/resfiles"
    def __init__(self, baseDir, date, max_page):
        self.baseDir = baseDir
        self.date = date
        self.max_page = max_page
        self.pdfDir = baseDir + "/"
        #self.jpgDir = baseDir + "/" + date + "/" + "img"

        #mkdir_p(self.jpgDir)
        mkdir_p(self.pdfDir)

    def download(self):
        date_list = self.date.split('-')

        nYear = date_list[0]
        #nYear ="2015"
        nMonth = date_list[1]
        #nMonth = "03"
        nDay = date_list[2]
        #nDay = "19"
        urlP = (self.baseUrl + "/%04s-%02s/%02s/" ) % (nYear, nMonth, nDay)
        
        for page in range(1, self.max_page+1):
            #j=0
            path = self.pdfDir + "/" + "0%d.pdf" % page;
            #pdf_file1 = "jf%02d-%02ss.pdf" % (page, nDay)
            pdf_files = ["jf%02d-%02ss.pdf" % (page, nDay), "jf%02d-%02sS.pdf" % (page, nDay), "JF%02d-%02sS.pdf" % (page, nDay), "JF%02d-%02ss.pdf" % (page, nDay)]
            #downloaded = False
            url=urlP+pdf_files[0]
            if urlexists(url):
                downloadPdf(url, path)
                print url, "downloaded successfully!"
            else:
                url=urlP+pdf_files[1]
                if urlexists(url):
                    downloadPdf(url, path)
                    print url, "downloaded successfully!"
                else:
                    url=urlP+pdf_files[2]
                    if urlexists(url):
                        downloadPdf(url, path)
                        print url, "downloaded successfully!"
                    else:
                        url=urlP+pdf_files[3]
                        if urlexists(url):
                            downloadPdf(url, path)
                            print url, "downloaded successfully!"
                        else:
                            print "Failed to download ", url
            

class Whb(Paper):
    baseUrl = "http://wenhui.news365.com.cn/resfiles"
    def __init__(self, baseDir, date, max_page):
        self.baseDir = baseDir
        self.date = date
        self.max_page = max_page
        self.pdfDir = baseDir + "/" 
        #self.jpgDir = baseDir + "/" + date + "/" + "img"

        #mkdir_p(self.jpgDir)
        mkdir_p(self.pdfDir)

    def download(self):
        date_list = self.date.split('-')

        nYear = int(date_list[0][-2:])
        nMonth = int(date_list[1])
        nDay = int(date_list[2])

        for page in range(1, self.max_page+1):
            pdf_file = "wh%02d%02d%02d%02d.pdf" % (nYear, nMonth, nDay, page)
            url = (self.baseUrl + "/%04s-%02d/%02d/" + pdf_file) % (date_list[0], nMonth, nDay)
            try:
                path = self.pdfDir + "/0%d.pdf" % page
                downloadPdf(url, path)
                print url, "downloaded successfully!"
            except:
                os.remove(path) 
                print "Failed to download ", url


class Qnb(Paper):
    baseUrl = "http://app.why.com.cn/epaper/qnb/images"
    def __init__(self, baseDir, date, max_page):
        self.baseDir = baseDir
        self.date = date
        self.max_page = max_page
        self.pdfDir = baseDir+"/"
        #self.jpgDir = baseDir + "/" + date + "/" + "img"

        #mkdir_p(self.jpgDir)
        mkdir_p(self.pdfDir)

    def download(self):
        date_list = self.date.split('-')

        nYear = int(date_list[0][-2:])
        nMonth = int(date_list[1])
        nDay = int(date_list[2])

        for page in range(1, self.max_page+1):
            pdf_file = "QNBA%02dB%01d%02dC.pdf" % (page, nMonth, nDay)
            url = (self.baseUrl + "/%04s-%02d/%02d/A%02d/" + pdf_file) % (date_list[0],nMonth,nDay,page)
            try:
                path = self.pdfDir + "/%02d.pdf" % page
                downloadPdf(url, path)
                print url, "downloaded successfully!"
            except:
                os.remove(path) 
                print "Failed to download ", url
	    
    

def main():
    ISOFORMAT='%Y-%m-%d'
    today =datetime.date.today().strftime(ISOFORMAT)
    date = today 



    print "Please choose a newspaper(Input the number):"
    print " 0 all"
    print " 1 jfrb"
    print " 2 whb"
    print " 3 qnb"

    paper = int(raw_input(":"))

    if(paper < 0 or paper > 3):
        print "Newspaper does not exist!"
        return
    
    elif paper == 0:
        qnb = Qnb("./paper/qnb/pdfDownload", date, 16)
        qnb.download()
        whb = Whb("./paper/whb/pdfDownload", date, 8)
        whb.download()
        
        jfrb = Jfrb("./paper/jfrb/pdfDownload", date, 8)
        jfrb.download()


    elif paper == 1:
        jfrb = Jfrb("./paper/jfrb/pdfDownload", date, 8)
        jfrb.download()

    elif paper == 2:
        whb = Whb("./paper/whb/pdfDownload", date, 8)
        whb.download()
    elif paper == 3:
        qnb = Qnb("./paper/qnb/pdfDownload", date, 16)
        qnb.download()


main()
