#!/usr/bin/env python
"""
Colored by Group Example
===============
Generating a word cloud that assigns colors to words based on
a predefined mapping from colors to words
"""

from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt


class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [(get_single_color_func(color), set(words))
                                    for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(color_func
                              for (color_func, words) in self.color_func_to_words
                              if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


text = """SignalP
SIFT
TargetP
PolyPhen
MutationTaster
WoLF-PSORT
FOLDEF
MaxEnt
Dmutant
CADD
FoldX
PROVEAN
PolyPhen2
FIS
Mutationassessor.org 
SNAP2 
PMUT
AGGRESCAN
SNPs3D 
MutPred
A-GVGD
 SNPinfo/FuncPred 
Mupro
CHASM
Waltz
TANGO
CUPSAT
Eris
DFIRE
 PantherPSEC
MAPP
Zyggregator
PAGE
EGAD
SDM
PopMuSic
VAAST
PROFcon
CanPredict
FOLD-RATE
GWAVA 
SNPeffect
Scpred
nsSNPAnalyzer 
FoldAmyloid
Scide
KGGSeq
DBD-Hunter
PPT-DB
PON-P
Skippy
Saunders&Baker
TransComp
UMD-predictor
K-Fold
SAPred
LS-SNP/PDB
BeAtMuSiC
CoVEC 
Parepro
FATHmm
PASTA2
MutPredSplice
SNPdbe
transFIC 
VAAST2
SAAPdb
LocTree2
VEST
MultiMutate
SIFT-indel
Phen-Gen
AutoMute
MuStab
ASP/ASPex
SNPs&GO
PhD-SNP
DANN
FunSAV
MuX-48
MuX-S
HOPE
SInBaD
Eigen
EIGEN
Re-ID
NETdiseaseSNP
ProA
VEST-indel
Exomiser
CoDP
VarMod
SuRFR"""

# Since the text is small collocations are turned off and text is lower-cased
wc = WordCloud(collocations=False).generate(text.lower())

color_to_words = {
    # words below will be colored with a green single color function
    '#00ff00': ['beautiful', 'explicit', 'simple', 'sparse',
                'readability', 'rules', 'practicality',
                'explicitly', 'one', 'now', 'easy', 'obvious', 'better'],
    # will be colored with a red single color function
    'red': ['ugly', 'implicit', 'complex', 'complicated', 'nested',
            'dense', 'special', 'errors', 'silently', 'ambiguity',
            'guess', 'hard']
}

# Words that are not in any of the color_to_words values
# will be colored with a grey single color function
default_color = 'grey'

# Create a color function with single tone
# grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

# Create a color function with multiple tones
grouped_color_func = GroupedColorFunc(color_to_words, default_color)

# Apply our color function
wc.recolor(color_func=grouped_color_func)

# Plot
plt.figure()
plt.imshow(wc)
plt.axis("off")
plt.show()
