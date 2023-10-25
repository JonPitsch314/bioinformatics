## Vim Commands

The list of commands below is not comprehensive. See Additional Resources below to find information about other commands that Vim employs.

### Command Mode

* esc - changes document to 'command mode'

From Command Mode, you can execute the following commands to modify the document:

* :w -> save changes made in the document
* :w filename.type -> essentially a save-as command. ':w new_csv.csv' will copy the contents of the current document and save them in a new file called new_csv.csv. Useful if you want to make an exact copy of a file.
* :q -> quit out of the saved document
* :q! -> quit out of the document without saving
* :!reset -> resets vim if the arrow keys stop working
* '#' -> highlight all instances of the word/character that the cursor is on. Pressing # on the word 'the' will highlight all instances of the word 'the'.
* :noh -> will unhighlight any highlighted text
* dd -> will delete the line that cursor is located on
* INT dd -> Example: 5 dd - will delete the line that the cursor is on and the INT-1 lines beneath it. The example will delete the current line and the four lines beneath it.
* w -> skip to the end of the current word
* INT w -> Example: 20 w - will skip to the end of the 20th word from where the cursor is located. Useful for making changes to long commands.
* b -> skip to the end of the previous word
* INT b -> Example: 10 b - will move the cursor backwards to the end of the 10th word behind the cursor
* g -> jump to the first line of the file
* shift + g -> jump to the last line of the file 
* a -> moves cursor over 1 character and changes document from command mode to insert mode. Press esc to change back to command mode.
* shift + a -> moves cursor to the end of the current line and changes document from command mode to insert mode. Press esc to change back to command mode.

### Insert Mode

* i -> changes document to Insert Mode. After pressing i, you will be able to type text into the document. 

### Additional Resources

* Search and Replace: https://vim.fandom.com/wiki/Search_and_replace
* Comprehensive list of commands: https://vim.rtorr.com/
* Interactive Vim tutorial: https://www.openvim.com/
