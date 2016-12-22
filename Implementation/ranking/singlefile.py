import os


def fun(path, file, destinationFolder):
    file = file.replace(' ', '\ ')
    path = path.replace(' ','\ ')
    destinationFolder = destinationFolder.replace(' ','\ ')

    os.chdir("/mnt/Semester/Major Final/Implementation/Preprocessor/tagger-stemmer/")

    os.system('cat ' + path + file + ' > hindi.input.txt')
    os.system('make tag')

    os.system('touch ' + destinationFolder + 'tagged\ ' + file)
    os.system('cat hindi.output > ' + destinationFolder + 'tagged\ ' + file)

    os.system('exit')
