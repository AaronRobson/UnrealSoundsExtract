#!/usr/bin/python

import os

from typing import Sequence

#from: http://wiki.beyondunreal.com/Legacy:BatchExportCommandlet
#command example: "UCC batchexport Announcer.uax sound wav ..\\test"

#makeSubFolderForEachCollectionFile = True
MAKE_SUB_FOLDER_FOR_EACH_COLLECTION_FILE = True

#if UCC.exe exists: else if UT3.exe exists
EXTRACTOR_UTIL_FILENAME = 'UCC' # or 'UCC.exe'
#search batchexport in this for ut3 extract
#http://forums.epicgames.com/showthread.php?t=585103
#something like: UT3.exe Editor.BatchExport ...

title = 'Unreal Sounds Extractor'
author = 'Aaron Robson'
date = '21/10/2010'

description = """Must be run from the "System" folder of an unreal game which has "\\System\\UCC.exe"
(the original Unreal 1 does not).
Extracts the sounds from each sound file (\\Sounds\\*.uax) of an Unreal game.
"""

#up a directory from the CWD (CurrentWorkingDirectory (where the executable file is (in "System")))
rootDirectory = os.path.abspath('..')
#systemDirectory = os.path.join(rootDirectory, 'System')
soundsDirectory = os.path.join(rootDirectory, 'Sounds')
outputDirectory = os.path.join(rootDirectory, 'SoundsInWav') + os.path.sep

def raiseError(error):
    raise error

def WalkDir(directory: str):
    return list(os.walk(directory, onerror=raiseError))[0]

def GetFromDirectoryOtherFilesOrDirectories(directory: str, files: bool=True) -> Sequence[str]:
    if files:
        index = 2
    else:
        #directories
        index = 1

    try:
        return WalkDir(directory)[index]
    except IndexError:
        #no files/directories to report
        return []

def GetFoldersInDirectory(directory: str) -> Sequence[str]:
    return GetFromDirectoryOtherFilesOrDirectories(directory, False)

def GetFilenamesInDirectory(directory):
    #Old way: listdir takes a directory and returns the names of folders and files, folders must be removed from the list
    #filenames = [f for f in os.listdir(soundsDirectory) if os.path.isfile(os.path.join(soundsDirectory, f))]
    return GetFromDirectoryOtherFilesOrDirectories(directory)

def MakeFormatString(makeSubFolderForEachCollectionFile: str=MAKE_SUB_FOLDER_FOR_EACH_COLLECTION_FILE, extractorUtilFileName: str=EXTRACTOR_UTIL_FILENAME) -> str:
    return '%s batchexport {0} sound wav "{1}%s"' % (extractorUtilFileName, bool(makeSubFolderForEachCollectionFile) * '{0}')

def DoExtraction(directory: str=soundsDirectory) -> None:
    filenames = GetFilenamesInDirectory(directory)
    if filenames: #if there are files
        formatString = MakeFormatString();
        commands = [formatString.format(filename, outputDirectory) for filename in filenames]
        list(map(os.system, commands))
    else:
        raise OSError('No Files to Extract from in: {0}.'.format(repr(directory)))

def GetIntroductionString() -> str:
    return '{0}\nBy {1}\nVersion date: {2}\n\n{3}'.format(title, author, date, description)

if __name__ == "__main__":
    print(GetIntroductionString() + '\n')

    try:
        DoExtraction()
    except (UnrealSoundsExtractError) as e:
        print(e)
