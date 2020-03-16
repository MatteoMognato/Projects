# Convert From DOCX to Anki Deck

#### Prerequisite

You need python installed in the pc and the following libraries installed:

- Mammoth
-  Genanki

#### Step by Step procedure

1. First you need to create your word document based on a prefixed framework:

   ```
   ask (enter) 
   
   answer(enter) 
   
   { image (enter) }
   ```

   Note that the image is between 2 graph bracket because is not necessary.

   That is the card schema and then you can repeat it. Note that you can separate 2 cards without any empty line just repeating the schema or you can insert some empty line between 2 (future) cards

2. Than from the cmd prompt you have to execute  

   ```
   mammoth input.docx --output-dir=out
   ```

   where input is the word file you have created and out is the folder created for storing the html and pictures. 

3. In the out folder or the folder you have choose for the html and images you have to put the py code and execute.

4. An output anki deck is made

5. Double click on it and all the new deck would be imported into your anki profile.