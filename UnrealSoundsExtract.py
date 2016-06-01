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

#Helped by: http://en.wikibooks.org/wiki/Python_Programming/Exceptions
class UnrealSoundsExtractError(Exception): #generic attributes for all my custom exceptions
	value = 'Default Custom UnrealSoundsExtract Error Message' #would define this as abstract but object hiding isn't a strongpoint of python

	def __init__(self, value):
		'''Optional text used to help the user identify the specific cause of the error.
		'''
		self.parameter = value

	def __str__(self):
		if self.parameter:
			return "Error %s; '%s'" % (repr(self.value), self.parameter)
		else:
			return repr(self.value) # __repr__ defaults to the value of __str__ when missing

class NoFilesError(UnrealSoundsExtractError):
	value = 'No Files to Extract from'

class DirectoryDoesNotExistError(UnrealSoundsExtractError):
	value = 'Directory not found'

def WalkDir(directory: str):
	if os.path.exists(directory):
		#os.walk returns a 3-tuple of (the given full directory, the sub-directories, the files)
		#put into list() then out again by accessing the first index: [0] (otherwise gets stuck as confusing generator)
		#may need to take this into account http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
		return list(os.walk(directory))[0]
	else:
		raise DirectoryDoesNotExistError(directory)

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
		raise NoFilesError(directory)

def GetIntroductionString() -> str:
	return '{0}\nBy {1}\nVersion date: {2}\n\n{3}'.format(title, author, date, description)

if __name__ == "__main__":
	print(GetIntroductionString() + '\n')

	try:
		DoExtraction()
	except (UnrealSoundsExtractError) as e:
		print(e)

	#keep the window open
	input('\nPress Enter to Exit:')
