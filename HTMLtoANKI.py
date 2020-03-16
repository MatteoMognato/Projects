#library import
from html.parser import HTMLParser #a library for navigating/parsing HTML file
import codecs # library for coding in html
import genanki #per generare anki deck and cards
'''
legenda
sp = started paragrapher
fp = finish paragrapher
si = start image
fi = finish image
'''
# array that will contain all tags and data
allTag=[]
#the print is used for testing
class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if(tag=='p'): #is a paragrapher
            allTag.append('sp') 
            #print("Encountered a start tag:", tag)
        elif(tag=='img'): #is an image
            allTag.append('si')
            print(attrs)
            if(len(attrs)<2): allTag.append(attrs[0][1]) #cot
            else: allTag.append(attrs[1][1])
            #print(attrs[0][1])
        else: allTag.append("<"+tag+">")
        #might be a font caratheristics
    def handle_endtag(self, tag):
        if(tag=='p'):
            allTag.append('fp') 
            #print("Encountered an end tag :", tag)
        elif(tag=='img'):
            allTag.append('fi')
        else: allTag.append("</"+tag+">")    
    def handle_data(self, data):
        allTag.append(data)
        #print(data)

def generateArray():
    """
    A class used to create the array with all the tags and data in the
    html file 
    
    """
    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    #open html and read
    file = codecs.open("input.html", "r", "utf-8")
    html = file.read()
    #call the parser that I've previsusly defined
    parser.feed(html)
    
def createImgNames():
    """
    create an array With all the imgages' names and extensions

    """
    listImg=[]
    isImg = False
    for i in allTag:
        if(isImg == True): listImg.append(i) #se mi viene indicato che è un'immagine 
        isImg = (i=='si')
    return listImg

generateArray() #generate de Array with the tags
print(allTag)

'''
let's create our anki cards' models
'''
#model with the picture after the answer
model_picture = genanki.Model(
  1,
  'Provo a metter na foto',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'MyMedia'},                                  
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '<div style="font-family: Arial; text-align: center; font-size: 20px; padding: 20px"> {{Question}} </div>',              
      'afmt': '<div style="font-family: Arial; text-align: center; font-size: 20px; padding: 20px"> {{FrontSide}}<hr id="answer">{{Answer}}</div> <br>{{MyMedia}}',
    },
  ])
#model without any picture (the basic one ask and answer)
model = genanki.Model(
  2,
  'Prova senza foto',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},                               
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '<div style="font-family: Arial; text-align: center; font-size: 20px; padding: 20px"> {{Question}} </div>',              
      'afmt': '<div style="font-family: Arial; text-align: center; font-size: 20px; padding: 20px"> {{FrontSide}}<hr id="answer">{{Answer}} </div>',
    },
  ])

#generate the deck with is code and name
my_deck = genanki.Deck(
  222222222222,
  'New cards from docx')

def create():
    """
    The create method is used to generate all the cards and add them to
    the deck my_deck that has been created before
    """
    l = len(allTag) #allTag lenght
    v=0 #is a indicator used to navigate the allTag list
    
    while(v<l): #while there is other element to visit
        
        d="" #question (domanda)
        if(allTag[v] == 'sp' and allTag[v+1] != 'si'): 
            v=v+1
            while(allTag[v]!='fp'): #this part will reconstruct all the text
                d = d + allTag[v]
                print(d)
                v=v+1
        v=v+1
        
        r="" #answer (risposta)
        if(allTag[v]== 'sp' and allTag[v+1] != 'si' ):
            v=v+1
            while(allTag[v]!='fp'):  #this part will reconstruct all the text
                r = r + allTag[v]
                v=v+1
        v=v+1
        
        img=""
        isCardWithImg=False #is True if there is a image in the answer
        
        if(v<l): #to prevent IndexOutOfBoundException if is the last answer of the document 
            if (allTag[v]== 'sp' and (v+1)<l): #controll if start a paragrapher and control to prevent IndexOutOfBoundException
                if(allTag[v+1] == 'si' ): #start an immagine
                    isCardWithImg=True #set that there is a img
                    img="<img src='"+allTag[v+2]+"'/>"
                    v=v+5
                    #print(d, r, img)
                    #generate the card with picture
                    my_note = genanki.Note(
                          model=model_picture,
                          fields=[d, r, img])
                    
                    my_deck.add_note(my_note)
                    
        if(not isCardWithImg):
            #print(d, r)
            #generate card without picture
            my_note = genanki.Note(
                  model=model,
                  fields=[d, r])
            
            my_deck.add_note(my_note)
            
create() #call the method for creating the cards and put into the deck
my_package = genanki.Package(my_deck) 
my_package.media_files = createImgNames() #insert on the generator the location of all the images
my_package.write_to_file('output.apkg') #create the anki's deck