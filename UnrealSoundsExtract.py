#!/usr/bin/python

import argparse
import os

# from: http://wiki.beyondunreal.com/Legacy:BatchExportCommandlet
# command example: "UCC batchexport Announcer.uax sound wav ..\\test"

# if UCC.exe exists: else if UT3.exe exists
EXTRACTOR_FILENAME = 'UCC'  # or 'UCC.exe'
# search batchexport in this for ut3 extract
# http://forums.epicgames.com/showthread.php?t=585103
# something like: UT3.exe Editor.BatchExport ...


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
        extractorFilepath,
        subFolderPerCollectionFile):
    return '%s batchexport {0} sound wav "{1}%s"' % (
        extractorFilepath,
        bool(subFolderPerCollectionFile) * '{0}')


def DoExtraction(input, output, flatten):
    soundsDirectory = os.path.join(input, 'Sounds')
    systemDirectory = os.path.join(input, 'System')
    extractorFilepath = os.path.join(systemDirectory, EXTRACTOR_FILENAME)
    filenames = GetFilenamesInDirectory(soundsDirectory)
    if filenames:  # if there are files
        formatString = MakeFormatString(
            extractorFilepath=extractorFilepath,
            subFolderPerCollectionFile=not flatten)
        commands = [
            formatString.format(
                filename,
                os.path.join(os.path.abspath(output), ''))
            for filename in filenames]
        for command in commands:
            os.system(command)
    else:
        raise OSError(
            'No Files to Extract from in: {0}.'.format(repr(soundsDirectory)))


INPUT_DEFAULT = '.'
OUTPUT_DEFAULT = os.path.join('.', 'SoundsInWav')


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
        default=INPUT_DEFAULT,
        dest='input',
        help='the install directory of the game',
    )
    parser.add_argument(
        '-o', '--output',
        default=OUTPUT_DEFAULT,
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
        DoExtraction(
            input=args.input,
            output=args.output,
            flatten=args.flatten
        )
    except Exception as e:
        print(e)
