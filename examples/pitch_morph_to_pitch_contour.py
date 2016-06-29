'''
Created on Jun 29, 2016

This file shows an example of morphing to a pitch tier.
In f0_morph.py, the target pitch contour is extracted in the
script from another file.  In this example, the pitch tier
could come from any source (hand sculpted or generated).

WARNING: If you attempt to morph to a pitch track that has
few sample points, the morph process will fail.

@author: Tim
'''

from os.path import join

from praatio import pitch_and_intensity
from praatio import dataio

from promo import f0_morph
from promo.morph_utils import utils
from promo.morph_utils import interpolation


# Define the arguments for the code
# Windows paths
path = r"C:\Users\Tim\Dropbox\workspace\prosodyMorph\examples\files"
praatEXE = r"C:\Praat.exe"

# Mac paths
path = "/Users/tmahrt/Dropbox/workspace/prosodyMorph/examples/files"
praatEXE = "/Applications/Praat.app/Contents/MacOS/Praat"

minPitch = 50
maxPitch = 350
stepList = utils.generateStepList(3)

fromName = "mary1"
fromWavFN = fromName + ".wav"
fromPitchFN = fromName + ".txt"
fromTGFN = join(path, fromName + ".TextGrid")

toName = "mary1_stylized"
toPitchFN = toName + ".PitchTier"

# Prepare the data for morphing
# 1st load it into memory
fromPitchList = pitch_and_intensity.audioToPI(path, fromWavFN, path,
                                              fromPitchFN, praatEXE, minPitch,
                                              maxPitch, forceRegenerate=False)
fromPitchList = [(time, pitch) for time, pitch, _ in fromPitchList]

# Load in the target pitch contour
pitchTier = dataio.open2DPointObject(join(path, toPitchFN))
toPitchList = [(time, pitch) for time, pitch in pitchTier.pointList]

# The target contour doesn't contain enough sample points, so interpolate
# over the provided samples
# (this step can be skipped if there are enough sample points--a warning
# will be issued if there are any potential problems)
toPitchList = interpolation.quadraticInterpolation(toPitchList, 4, 1000, 0)

# 3rd select which sections to align.
# We'll use textgrids for this purpose.
tierName = "PhonAlign"
fromPitch = f0_morph.getPitchForIntervals(fromPitchList, fromTGFN, tierName)
toPitch = f0_morph.getPitchForIntervals(toPitchList, fromTGFN, tierName)

# Run the morph process
f0_morph.f0Morph(fromWavFN=join(path, fromWavFN),
                 pitchPath=path,
                 stepList=stepList,
                 outputName="%s_%s_f0_morph" % (fromName, toName),
                 doPlotPitchSteps=True,
                 fromPitchData=fromPitch,
                 toPitchData=toPitch,
                 outputMinPitch=minPitch,
                 outputMaxPitch=maxPitch,
                 praatEXE=praatEXE)
