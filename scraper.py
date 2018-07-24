from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import time

from pokedex import Pokedex
from normalizer import Normalizer
import fileManager

x = 0
y = 1
charizardID = 6     

def parse(xOrY, pageNumber) :
    driver = initPGLWebsite()
    setPokemon(driver)
    setItem(driver, xOrY)
    submitQuery(driver)
    numOfResults = getNumResults(driver)
    
    
    #we can cache the images shown on the home screen
    # and if we can associate all the images with pokemon,
    # we don't have to check the party link to get the pokemon name
    imageCache = fileManager.getPokemonCache()
    pokedex = Pokedex()
    
    #so we can see the next button.
    #subsequent clicks don't require scrolling
    driver.execute_script("window.scrollTo(0, 700)")
    
    #since we are on the first page,
    #parse this first before looping
    if pageNumber == 1 :
        recordParties(driver, pokedex, imageCache, xOrY)
    
    
    for i in range(pageNumber-2) :
        toNextPage(driver)
        
    pageNumber = pageNumber - 1
    if pageNumber == 0 :
        pageNumber = 1
    
    numIterations = getPageCt(numOfResults) - 1
    for i in range(numIterations) :
        toNextPage(driver)
        pageNumber = pageNumber + 1
        filemanager.savePageNumber(str(pageNumber), xOrY)
        recordParties(driver, pokedex, imageCache, xOrY)
    
    driver.close()
    

def initPGLWebsite() :
    driver = webdriver.Chrome()
    driver.get("https://3ds.pokemon-gl.com/rentalteam/usum/search")
    return driver
    
def setPokemon(driver) :
    #there's a popup in the way so remove it first
    popupButton = driver.find_element_by_id("cookie-dismisser")
    popupButton.click()
    #set the pokemon (Charizard)
    pokemonSearchBox = driver.find_element_by_id("selectPokemon")
    pokemonSearchBox.click()
    #we can't see it so scroll down to it.
    #wait for page to load first
    absol = WebDriverWait(driver, 1000) .until(
        EC.presence_of_element_located((By.ID,"pokemon-359-0"))
    )
    #tab to scroll down
    cToD = driver.find_element_by_id("select-by-name").find_elements_by_css_selector("li.squeezed")[1]
    cToD.click()
    charizard = WebDriverWait(driver, 1000) .until(
        EC.presence_of_element_located((By.ID,"pokemon-6-0"))
    )
    charizard.click()
    enterButton = driver.find_element_by_class_name("btnCrSmall")
    enterButton.click()

    
def setItem(driver, xOrY) :
    itemSearchBox = driver.find_element_by_id("selectItem")
    itemSearchBox.click()
    charizarditeItemID = getCharizarditeItemID(xOrY)
    charizardite = WebDriverWait(driver, 1000) .until(
        EC.presence_of_element_located((By.ID,charizarditeItemID))
    )
    charizardite.click()
    enterButton = driver.find_element_by_class_name("btnCrSmall")
    enterButton.click()

def getCharizarditeItemID(xOrY) :
    if (xOrY == x) :
        return "item-660"
    elif (xOrY == y) :
        return "item-678"
    else :
        return ""
        
def submitQuery(driver):
    submitButton = driver.find_element_by_class_name("btnCrLarge")
    submitButton.click()
    
def getNumResults(driver):
    numResultsView = WebDriverWait(driver, 1000) .until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='templateValue template-count']"))
    )
    
    numResultsText = numResultsView.text
    numResultsText = numResultsText.replace(",","")
    
    return int(numResultsText)
    
def getPageCt(numOfResults):
    resultsPerPage = 5
    numOfIterations = int(numOfResults / resultsPerPage)
    #round up, not down
    if (numOfIterations * resultsPerPage < numOfResults) :
        numOfIterations = numOfIterations + 1
        
    return numOfIterations

def recordParties(driver, pokedex, cache, xOrY) :
    time.sleep(1)
    #get all the URLs for the parties on the page
    partyList = driver.find_element_by_xpath("//div[@class='battleteam-column-inner ranking-container battleTypeSingle']").find_elements_by_tag_name("a")
    for i in range(len(partyList)) :
        party = driver.find_element_by_xpath("//div[@class='battleteam-column-inner ranking-container battleTypeSingle']").find_elements_by_tag_name("a")[i]
        #first check if all the images are in our cache
        if allInExistingCache(driver, cache, i) :
            partyPokemonIDs = getPartyFromCache(driver, cache, i)
            fileManager.addRawParty(partyPokemonIDs, xOrY)
        else :
            partyURL = driver.find_element_by_xpath("//div[@class='battleteam-column-inner ranking-container battleTypeSingle']").find_elements_by_tag_name("a")[i].get_attribute("href")
            partyPokemonIDs = getPartyPokemonIDs(partyURL, pokedex, cache)
            fileManager.addRawParty(partyPokemonIDs, xOrY)


        
def allInExistingCache(driver, cache, partyIndex) :
    imageList = driver.find_element_by_xpath("//div[@class='battleteam-column-inner ranking-container battleTypeSingle']").find_elements_by_tag_name("a")[partyIndex].find_elements_by_tag_name("li")
    for i in range(len(imageList)) :
        imageCSS = driver.find_element_by_xpath("//div[@class='battleteam-column-inner ranking-container battleTypeSingle']").find_elements_by_tag_name("a")[partyIndex].find_elements_by_tag_name("li")[i].find_element_by_tag_name("img").value_of_css_property("background")
        imageURL = re.search('url\("(.*)"\)', imageCSS).group(1)
        imageURL = imageURL.replace("https://n-3ds-pgl-contents.pokemon-gl.com/share/images/pokemon/70/","")
        if imageURL not in cache :
            return False
        
    return True

def getPartyFromCache(driver, cache, partyIndex) :
    imageList = driver.find_element_by_xpath("//div[@class='battleteam-column-inner ranking-container battleTypeSingle']").find_elements_by_tag_name("a")[partyIndex].find_elements_by_tag_name("li")
    partyIDs = []
    for i in range(len(imageList)) :
        imageCSS = driver.find_element_by_xpath("//div[@class='battleteam-column-inner ranking-container battleTypeSingle']").find_elements_by_tag_name("a")[partyIndex].find_elements_by_tag_name("li")[i].find_element_by_tag_name("img").value_of_css_property("background")
        imageURL = re.search('url\("(.*)"\)', imageCSS).group(1)
        imageURL = imageURL.replace("https://n-3ds-pgl-contents.pokemon-gl.com/share/images/pokemon/70/","")
        id = cache[imageURL]
        if id != charizardID :
            partyIDs.append(id)
        
    return partyIDs
    
    
def getPartyPokemonIDs(url, pokedex, cache) :
    party = []
    
    #since this content is dynamic
    # use selenium
    driver = webdriver.Chrome()
    driver.get(url)
    
    nameList = driver.find_elements_by_xpath("//div[@class='name']")
    names = []
    for nameDiv in nameList :
        name = nameDiv.text
        names.append(name)
        
    images = []
    
    imageList = driver.find_elements_by_xpath("//div[@class='image']")
    for imageDiv in imageList :
        imageCSS = imageDiv.find_element_by_tag_name("img").value_of_css_property("background-image")
        imageURL = re.search('url\("(.*)"\)', imageCSS).group(1)
        imageURL = imageURL.replace("https://n-3ds-pgl-contents.pokemon-gl.com/share/images/pokemon/70/","")
        images.append(imageURL)
    
    assert len(names) == len(images)
    assert len(names) is not 0
    partyDict = dict(zip(images, names))
    for image, name in partyDict.items() :
        id = pokedex.convert(name, image)
        if image not in cache :
            fileManager.addPokemonToCache(image, id)
            cache[image] = id
        
        if id != charizardID :
            party.append(id)
    
    driver.close()
    return party

def toNextPage(driver) :
    nextButton = driver.find_element_by_class_name("btnArrowRight")
    nextButton.click()
    WebDriverWait(driver, 1000) .until(
        EC.presence_of_element_located((By.XPATH,"//div[@id='battleTeamColumn'][contains(@style, 'opacity: 1')]"))
    )


                    

#startingPageNumberX = fileManager.getPageNumber(x)    
#parse(x,startingPageNumberX)
#startingPageNumberY = fileManager.getPageNumber(y) 
#parse(y,startingPageNumberY)

