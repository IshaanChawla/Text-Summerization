import os

if __name__ == '__main__':
    ''' The Function Helps to preprocess Multiple Text Files in a single run '''
    # Destination to save all the Preprocessed Files
    destinationFolder = '../../Preprocessed_Corpus/'
    # List of all Folders that contain files to be preprocessed
    sourceFolders = ['../../Dummy_Corpus/']
    # Fetching all files from all the folders
    for folder in sourceFolders:
        files = os.listdir(folder)
        # Iterating over all files
        for file in files:
            # Replacing any spaces in the name of the File with '\ '
            file = file.replace(' ','\ ')
            # Putting Content of the File in hindi.input.txt so that it can be preprocessed
            os.system('cat ' + folder + '/' + file + ' > hindi.input.txt')
            # Running the command so that Stemmer and Tagger can work on hindi.input.txt
            os.system('make tag')
            # Creating a new file
            os.system('touch ' + destinationFolder + file)
            # Writing the output to the destination
            os.system('cat hindi.output > ' + destinationFolder + '/' + file)
            # To close the terminal on which commands are running
            os.system('exit')