# UnrealSoundsExtract
To extract game sound effects from Unreal games.

[![Build Status](https://travis-ci.org/AaronRobson/UnrealSoundExtract.svg?branch=master)](https://travis-ci.org/AaronRobson/UnrealSoundExtract)

## Instructions

### Windows
* Install a game which uses the Unreal Engine.
* Check that the game has this file present `\\System\\UCC.exe` (Unreal Tournament and UT2004 but not Unreal 1 for example).
* `git clone https://github.com/AaronRobson/UnrealSoundsExtract.git`
* Place the `UnrealSoundsExtract.py` in the `System` folder of the game.
* Run `UnrealSoundsExtract.py`.
* Each package from `\\Sounds\\*.uax` should have been converted and placed into `\\SoundsInWav\\*.uax\\*.wav` (grouped by sound package and then by sub-song).
