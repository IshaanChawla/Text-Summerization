from bs4 import BeautifulSoup
import urllib.request
import threading
import re

destinationFolder = "../Corpus/"
class Scraper:
    ''' Scraper to scrape the NDTV news site '''
    def __init__(self,baseURL,baseCategories,pageURL,articlesToBeScraped):
        ''' Initializing the Scraper with basic info of the site to scrape '''
        self.baseURL = baseURL
        self.baseCategories = baseCategories
        self.pageURL = pageURL
        self.articlesToBeScraped = articlesToBeScraped
        self.articleNum = 1
        self.lock = threading.Lock()

    def __scrapeArticlePage(self,articleURL):
        ''' Function to scrape the pages which contain the articles '''
        print(articleURL)
        # Opening the Webpage and storing its contents in the page
        page = urllib.request.urlopen(articleURL).read()
        # Parsing the page using its DOM elements
        soup = BeautifulSoup(page,"html.parser")
        try:
            # Getting the Story Heading
            storyHeading = soup.find("div", attrs = {"class" : "ins_headline"}).get_text()
            # Getting Stroy Body and Cleaning it
            storyBody = soup.find("span",attrs = {"class" : "ins_storybody"}).get_text()
            storyBody = storyBody[0:storyBody.find("!func")]
        except:
            print("No Stroy Heading or Body Found")
        else:
            # Writing the Article if it doesnt contain any English word
            if not(re.search('[a-zA-Z]', storyBody) or re.search('[a-zA-Z]', storyHeading)):
                # Acquiring the lock. Reading the Number, Incrementing it and releasing the lock
                self.lock.acquire()
                filename = "Sample Text"
                try:
                    filename = "Sample Text " + str(self.articleNum)
                    self.articleNum = self.articleNum + 1
                finally:
                    self.lock.release()

                # Writing to the file the content of the article
                with open(destinationFolder + filename, "w") as fileDesc:
                    fileDesc.write(storyHeading + '\n' + storyBody)



    def __scrapeBaseCategory(self,baseCategory):
        ''' Function to scrape pages which contain list of articles '''
        # The page number from which the URL of the articles are being scraped
        pageNum = 1
        while self.articleNum < self.articlesToBeScraped and pageNum <=10:
            print(baseCategory + " " + str(pageNum))
            # Opening the Webpage and storing its contents in the page
            page = urllib.request.urlopen(self.baseURL + baseCategory + "/" + self.pageURL + str(pageNum)).read()
            # Parsing the page using its DOM elements
            soup = BeautifulSoup(page,"html.parser")
            # Finding all Divs on the page of class "nstory_header"
            storyDivs = soup.find_all("div", attrs = {"class" : "nstory_header"})
            for storyDiv in storyDivs:
                self.__scrapeArticlePage(storyDiv.a["href"])
            pageNum += 1


    def scrape(self):
        ''' Function to start the scraping of the website containing the articles '''
        baseCategoryThreads = []
        # Looping over all base categories and opening as threads
        for baseCategory in self.baseCategories:
            thread = threading.Thread(target = self.__scrapeBaseCategory, args = (baseCategory, ))
            thread.start()
            baseCategoryThreads.append(thread)

        # Waiting For the Threads to end
        for thread in baseCategoryThreads:
            thread.join()

if __name__ == "__main__":
    ''' Function which initializes all the contents on the webpage '''
    # Base URL of NDTV News
    baseURL = "http://khabar.ndtv.com/news/"
    # Base Categories under which news is divided on NDTV
    baseCategories = ["india","world","filmy","sports","cricket","zara-hatke","career","lifestyle","business","food","social"]
    # Page URL which contain list of the articles
    pageURL = "page-"
    # Total Number of pages to be scraped
    articlesToBeScraped = 10000

    # Initializing the Scraper
    ScraperNDTV = Scraper(baseURL,baseCategories,pageURL,articlesToBeScraped)
    # Start Scraping
    ScraperNDTV.scrape()