#!/usr/bin/python

import argparse
import os

# from: http://wiki.beyondunreal.com/Legacy:BatchExportCommandlet
# command example: "UCC batchexport Announcer.uax sound wav ..\\test"

SUB_FOLDER_PER_COLLECTION_FILE = True

# if UCC.exe exists: else if UT3.exe exists
EXTRACTOR_UTIL_FILENAME = 'UCC'  # or 'UCC.exe'
# search batchexport in this for ut3 extract
# http://forums.epicgames.com/showthread.php?t=585103
# something like: UT3.exe Editor.BatchExport ...

# up a directory from the CWD (CurrentWorkingDirectory
# (where the executable file is (in "System")))
rootDirectory = os.path.abspath('..')
# systemDirectory = os.path.join(rootDirectory, 'System')
soundsDirectory = os.path.join(rootDirectory, 'Sounds')
outputDirectory = os.path.join(rootDirectory, 'SoundsInWav') + os.path.sep


def raiseError(error):
    raise error


def WalkDir(directory):
    return list(os.walk(directory, onerror=raiseError))[0]


def GetFromDirectoryOtherFilesOrDirectories(directory, files=True):
    if files:
        index = 2
    else:
        # directories
        index = 1

    try:
        return WalkDir(directory)[index]
    except IndexError:
        # no files/directories to report
        return []


def GetFoldersInDirectory(directory):
    return GetFromDirectoryOtherFilesOrDirectories(directory, False)


def GetFilenamesInDirectory(directory):
    return GetFromDirectoryOtherFilesOrDirectories(directory)


def MakeFormatString(
        subFolderPerCollectionFile=SUB_FOLDER_PER_COLLECTION_FILE,
        extractorUtilFileName=EXTRACTOR_UTIL_FILENAME):
    return '%s batchexport {0} sound wav "{1}%s"' % (
        extractorUtilFileName,
        bool(subFolderPerCollectionFile) * '{0}')


def DoExtraction(directory=soundsDirectory):
    filenames = GetFilenamesInDirectory(directory)
    if filenames:  # if there are files
        formatString = MakeFormatString()
        commands = [
            formatString.format(filename, outputDirectory)
            for filename in filenames]
        list(map(os.system, commands))
    else:
        raise OSError(
            'No Files to Extract from in: {0}.'.format(repr(directory)))


def produce_parser():
    '''Produce command-line parser.
    '''
    parser = argparse.ArgumentParser(
        description='Extracts the sounds from each sound file '
                    '(/Sounds/*.uax) of games that use the Unreal Engine. '
                    'Requires an unreal game which has "/System/UCC.exe" '
                    '(for example Unreal 1 does not have this file).'
    )
    parser.add_argument(
        '-i', '--input',
        required=True,
        dest='input',
        help='the install directory of the game',
    )
    parser.add_argument(
        '-o', '--output',
        default='./SoundsInWav/',
        dest='output',
        help='the output directory for the extracted sound files',
    )
    parser.add_argument(
        '-f', '--flatten',
        action='store_true',
        help='all sub-sounds are extracted directly to the output directory',
    )
    return parser


if __name__ == "__main__":
    parser = produce_parser()
    args = parser.parse_args()

    try:
        DoExtraction()
    except Exception as e:
        print(e)
