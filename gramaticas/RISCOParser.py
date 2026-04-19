# Generated from gramaticas/RISCO.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,58,467,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,1,0,5,0,58,8,0,10,0,12,0,61,9,0,1,0,1,0,5,0,65,8,0,10,
        0,12,0,68,9,0,5,0,70,8,0,10,0,12,0,73,9,0,1,0,1,0,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,3,1,86,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,
        1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,106,8,3,1,4,1,4,1,4,
        1,4,1,4,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,5,6,123,8,6,10,6,
        12,6,126,9,6,1,6,5,6,129,8,6,10,6,12,6,132,9,6,1,6,1,6,1,6,1,7,1,
        7,1,7,1,7,1,7,5,7,142,8,7,10,7,12,7,145,9,7,1,7,5,7,148,8,7,10,7,
        12,7,151,9,7,1,7,1,7,1,7,1,7,1,7,5,7,158,8,7,10,7,12,7,161,9,7,1,
        7,5,7,164,8,7,10,7,12,7,167,9,7,5,7,169,8,7,10,7,12,7,172,9,7,1,
        7,1,7,1,7,1,7,5,7,178,8,7,10,7,12,7,181,9,7,1,7,5,7,184,8,7,10,7,
        12,7,187,9,7,3,7,189,8,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,5,8,199,
        8,8,10,8,12,8,202,9,8,1,8,5,8,205,8,8,10,8,12,8,208,9,8,1,8,1,8,
        1,8,1,9,1,9,1,9,3,9,216,8,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,1,9,3,9,
        226,8,9,1,9,1,9,1,9,1,9,5,9,232,8,9,10,9,12,9,235,9,9,1,9,5,9,238,
        8,9,10,9,12,9,241,9,9,1,9,1,9,3,9,245,8,9,1,10,1,10,1,10,5,10,250,
        8,10,10,10,12,10,253,9,10,1,11,1,11,1,11,1,11,1,12,1,12,3,12,261,
        8,12,1,12,1,12,1,12,1,12,3,12,267,8,12,1,13,1,13,1,13,5,13,272,8,
        13,10,13,12,13,275,9,13,1,14,1,14,1,14,5,14,280,8,14,10,14,12,14,
        283,9,14,1,15,1,15,1,15,5,15,288,8,15,10,15,12,15,291,9,15,1,16,
        1,16,1,16,5,16,296,8,16,10,16,12,16,299,9,16,1,17,1,17,1,17,5,17,
        304,8,17,10,17,12,17,307,9,17,1,18,1,18,1,18,3,18,312,8,18,1,19,
        1,19,1,19,5,19,317,8,19,10,19,12,19,320,9,19,1,20,1,20,1,20,1,20,
        1,20,3,20,327,8,20,1,21,1,21,1,21,1,21,1,21,5,21,334,8,21,10,21,
        12,21,337,9,21,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,
        1,22,1,22,1,22,1,22,1,22,1,22,1,22,3,22,356,8,22,1,23,1,23,1,23,
        1,23,5,23,362,8,23,10,23,12,23,365,9,23,3,23,367,8,23,1,23,1,23,
        1,24,1,24,1,24,1,24,1,24,3,24,376,8,24,1,24,1,24,1,24,1,24,3,24,
        382,8,24,1,24,1,24,1,24,1,24,3,24,388,8,24,1,24,1,24,1,24,1,24,3,
        24,394,8,24,1,24,1,24,1,24,1,24,3,24,400,8,24,1,24,1,24,1,24,1,24,
        3,24,406,8,24,1,24,1,24,1,24,1,24,3,24,412,8,24,1,24,1,24,1,24,1,
        24,3,24,418,8,24,1,24,1,24,1,24,1,24,3,24,424,8,24,1,24,1,24,1,24,
        1,24,3,24,430,8,24,1,24,3,24,433,8,24,1,25,1,25,1,25,5,25,438,8,
        25,10,25,12,25,441,9,25,1,26,1,26,1,27,1,27,1,27,1,27,1,27,1,27,
        1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,1,27,
        1,27,3,27,465,8,27,1,27,0,0,28,0,2,4,6,8,10,12,14,16,18,20,22,24,
        26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,0,4,1,0,44,45,2,0,7,
        8,46,47,1,0,9,10,1,0,11,13,515,0,71,1,0,0,0,2,85,1,0,0,0,4,87,1,
        0,0,0,6,105,1,0,0,0,8,107,1,0,0,0,10,112,1,0,0,0,12,115,1,0,0,0,
        14,136,1,0,0,0,16,193,1,0,0,0,18,244,1,0,0,0,20,246,1,0,0,0,22,254,
        1,0,0,0,24,266,1,0,0,0,26,268,1,0,0,0,28,276,1,0,0,0,30,284,1,0,
        0,0,32,292,1,0,0,0,34,300,1,0,0,0,36,308,1,0,0,0,38,313,1,0,0,0,
        40,326,1,0,0,0,42,328,1,0,0,0,44,355,1,0,0,0,46,357,1,0,0,0,48,432,
        1,0,0,0,50,434,1,0,0,0,52,442,1,0,0,0,54,464,1,0,0,0,56,58,5,54,
        0,0,57,56,1,0,0,0,58,61,1,0,0,0,59,57,1,0,0,0,59,60,1,0,0,0,60,62,
        1,0,0,0,61,59,1,0,0,0,62,66,3,2,1,0,63,65,5,54,0,0,64,63,1,0,0,0,
        65,68,1,0,0,0,66,64,1,0,0,0,66,67,1,0,0,0,67,70,1,0,0,0,68,66,1,
        0,0,0,69,59,1,0,0,0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,
        74,1,0,0,0,73,71,1,0,0,0,74,75,5,0,0,1,75,1,1,0,0,0,76,86,3,6,3,
        0,77,86,3,8,4,0,78,86,3,10,5,0,79,86,3,12,6,0,80,86,3,4,2,0,81,86,
        3,14,7,0,82,86,3,16,8,0,83,86,3,18,9,0,84,86,3,22,11,0,85,76,1,0,
        0,0,85,77,1,0,0,0,85,78,1,0,0,0,85,79,1,0,0,0,85,80,1,0,0,0,85,81,
        1,0,0,0,85,82,1,0,0,0,85,83,1,0,0,0,85,84,1,0,0,0,86,3,1,0,0,0,87,
        88,5,24,0,0,88,89,5,1,0,0,89,90,3,24,12,0,90,91,5,2,0,0,91,92,5,
        54,0,0,92,5,1,0,0,0,93,94,5,22,0,0,94,95,5,53,0,0,95,96,5,3,0,0,
        96,97,3,24,12,0,97,98,5,54,0,0,98,106,1,0,0,0,99,100,5,23,0,0,100,
        101,5,53,0,0,101,102,5,3,0,0,102,103,3,24,12,0,103,104,5,54,0,0,
        104,106,1,0,0,0,105,93,1,0,0,0,105,99,1,0,0,0,106,7,1,0,0,0,107,
        108,5,53,0,0,108,109,5,3,0,0,109,110,3,24,12,0,110,111,5,54,0,0,
        111,9,1,0,0,0,112,113,3,24,12,0,113,114,5,54,0,0,114,11,1,0,0,0,
        115,116,5,19,0,0,116,117,5,53,0,0,117,118,5,20,0,0,118,119,3,24,
        12,0,119,120,5,4,0,0,120,130,5,54,0,0,121,123,5,54,0,0,122,121,1,
        0,0,0,123,126,1,0,0,0,124,122,1,0,0,0,124,125,1,0,0,0,125,127,1,
        0,0,0,126,124,1,0,0,0,127,129,3,2,1,0,128,124,1,0,0,0,129,132,1,
        0,0,0,130,128,1,0,0,0,130,131,1,0,0,0,131,133,1,0,0,0,132,130,1,
        0,0,0,133,134,5,21,0,0,134,135,5,54,0,0,135,13,1,0,0,0,136,137,5,
        25,0,0,137,138,3,24,12,0,138,139,5,4,0,0,139,149,5,54,0,0,140,142,
        5,54,0,0,141,140,1,0,0,0,142,145,1,0,0,0,143,141,1,0,0,0,143,144,
        1,0,0,0,144,146,1,0,0,0,145,143,1,0,0,0,146,148,3,2,1,0,147,143,
        1,0,0,0,148,151,1,0,0,0,149,147,1,0,0,0,149,150,1,0,0,0,150,170,
        1,0,0,0,151,149,1,0,0,0,152,153,5,26,0,0,153,154,3,24,12,0,154,155,
        5,4,0,0,155,165,5,54,0,0,156,158,5,54,0,0,157,156,1,0,0,0,158,161,
        1,0,0,0,159,157,1,0,0,0,159,160,1,0,0,0,160,162,1,0,0,0,161,159,
        1,0,0,0,162,164,3,2,1,0,163,159,1,0,0,0,164,167,1,0,0,0,165,163,
        1,0,0,0,165,166,1,0,0,0,166,169,1,0,0,0,167,165,1,0,0,0,168,152,
        1,0,0,0,169,172,1,0,0,0,170,168,1,0,0,0,170,171,1,0,0,0,171,188,
        1,0,0,0,172,170,1,0,0,0,173,174,5,27,0,0,174,175,5,4,0,0,175,185,
        5,54,0,0,176,178,5,54,0,0,177,176,1,0,0,0,178,181,1,0,0,0,179,177,
        1,0,0,0,179,180,1,0,0,0,180,182,1,0,0,0,181,179,1,0,0,0,182,184,
        3,2,1,0,183,179,1,0,0,0,184,187,1,0,0,0,185,183,1,0,0,0,185,186,
        1,0,0,0,186,189,1,0,0,0,187,185,1,0,0,0,188,173,1,0,0,0,188,189,
        1,0,0,0,189,190,1,0,0,0,190,191,5,21,0,0,191,192,5,54,0,0,192,15,
        1,0,0,0,193,194,5,28,0,0,194,195,3,24,12,0,195,196,5,4,0,0,196,206,
        5,54,0,0,197,199,5,54,0,0,198,197,1,0,0,0,199,202,1,0,0,0,200,198,
        1,0,0,0,200,201,1,0,0,0,201,203,1,0,0,0,202,200,1,0,0,0,203,205,
        3,2,1,0,204,200,1,0,0,0,205,208,1,0,0,0,206,204,1,0,0,0,206,207,
        1,0,0,0,207,209,1,0,0,0,208,206,1,0,0,0,209,210,5,21,0,0,210,211,
        5,54,0,0,211,17,1,0,0,0,212,213,5,53,0,0,213,215,5,1,0,0,214,216,
        3,20,10,0,215,214,1,0,0,0,215,216,1,0,0,0,216,217,1,0,0,0,217,218,
        5,2,0,0,218,219,5,5,0,0,219,220,3,24,12,0,220,221,5,54,0,0,221,245,
        1,0,0,0,222,223,5,53,0,0,223,225,5,1,0,0,224,226,3,20,10,0,225,224,
        1,0,0,0,225,226,1,0,0,0,226,227,1,0,0,0,227,228,5,2,0,0,228,229,
        5,5,0,0,229,239,5,54,0,0,230,232,5,54,0,0,231,230,1,0,0,0,232,235,
        1,0,0,0,233,231,1,0,0,0,233,234,1,0,0,0,234,236,1,0,0,0,235,233,
        1,0,0,0,236,238,3,2,1,0,237,233,1,0,0,0,238,241,1,0,0,0,239,237,
        1,0,0,0,239,240,1,0,0,0,240,242,1,0,0,0,241,239,1,0,0,0,242,243,
        5,21,0,0,243,245,5,54,0,0,244,212,1,0,0,0,244,222,1,0,0,0,245,19,
        1,0,0,0,246,251,5,53,0,0,247,248,5,6,0,0,248,250,5,53,0,0,249,247,
        1,0,0,0,250,253,1,0,0,0,251,249,1,0,0,0,251,252,1,0,0,0,252,21,1,
        0,0,0,253,251,1,0,0,0,254,255,5,29,0,0,255,256,3,24,12,0,256,257,
        5,54,0,0,257,23,1,0,0,0,258,260,5,1,0,0,259,261,3,20,10,0,260,259,
        1,0,0,0,260,261,1,0,0,0,261,262,1,0,0,0,262,263,5,2,0,0,263,264,
        5,5,0,0,264,267,3,24,12,0,265,267,3,26,13,0,266,258,1,0,0,0,266,
        265,1,0,0,0,267,25,1,0,0,0,268,273,3,28,14,0,269,270,5,43,0,0,270,
        272,3,28,14,0,271,269,1,0,0,0,272,275,1,0,0,0,273,271,1,0,0,0,273,
        274,1,0,0,0,274,27,1,0,0,0,275,273,1,0,0,0,276,281,3,30,15,0,277,
        278,5,42,0,0,278,280,3,30,15,0,279,277,1,0,0,0,280,283,1,0,0,0,281,
        279,1,0,0,0,281,282,1,0,0,0,282,29,1,0,0,0,283,281,1,0,0,0,284,289,
        3,32,16,0,285,286,7,0,0,0,286,288,3,32,16,0,287,285,1,0,0,0,288,
        291,1,0,0,0,289,287,1,0,0,0,289,290,1,0,0,0,290,31,1,0,0,0,291,289,
        1,0,0,0,292,297,3,34,17,0,293,294,7,1,0,0,294,296,3,34,17,0,295,
        293,1,0,0,0,296,299,1,0,0,0,297,295,1,0,0,0,297,298,1,0,0,0,298,
        33,1,0,0,0,299,297,1,0,0,0,300,305,3,36,18,0,301,302,7,2,0,0,302,
        304,3,36,18,0,303,301,1,0,0,0,304,307,1,0,0,0,305,303,1,0,0,0,305,
        306,1,0,0,0,306,35,1,0,0,0,307,305,1,0,0,0,308,311,3,38,19,0,309,
        310,5,20,0,0,310,312,3,38,19,0,311,309,1,0,0,0,311,312,1,0,0,0,312,
        37,1,0,0,0,313,318,3,40,20,0,314,315,7,3,0,0,315,317,3,40,20,0,316,
        314,1,0,0,0,317,320,1,0,0,0,318,316,1,0,0,0,318,319,1,0,0,0,319,
        39,1,0,0,0,320,318,1,0,0,0,321,327,3,42,21,0,322,323,3,42,21,0,323,
        324,5,14,0,0,324,325,3,40,20,0,325,327,1,0,0,0,326,321,1,0,0,0,326,
        322,1,0,0,0,327,41,1,0,0,0,328,335,3,44,22,0,329,330,5,15,0,0,330,
        331,3,24,12,0,331,332,5,16,0,0,332,334,1,0,0,0,333,329,1,0,0,0,334,
        337,1,0,0,0,335,333,1,0,0,0,335,336,1,0,0,0,336,43,1,0,0,0,337,335,
        1,0,0,0,338,356,5,48,0,0,339,356,5,49,0,0,340,356,5,50,0,0,341,356,
        5,51,0,0,342,356,5,52,0,0,343,356,3,46,23,0,344,356,3,48,24,0,345,
        356,3,54,27,0,346,356,5,53,0,0,347,348,5,1,0,0,348,349,3,24,12,0,
        349,350,5,2,0,0,350,356,1,0,0,0,351,352,5,10,0,0,352,356,3,44,22,
        0,353,354,5,17,0,0,354,356,3,44,22,0,355,338,1,0,0,0,355,339,1,0,
        0,0,355,340,1,0,0,0,355,341,1,0,0,0,355,342,1,0,0,0,355,343,1,0,
        0,0,355,344,1,0,0,0,355,345,1,0,0,0,355,346,1,0,0,0,355,347,1,0,
        0,0,355,351,1,0,0,0,355,353,1,0,0,0,356,45,1,0,0,0,357,366,5,15,
        0,0,358,363,3,24,12,0,359,360,5,6,0,0,360,362,3,24,12,0,361,359,
        1,0,0,0,362,365,1,0,0,0,363,361,1,0,0,0,363,364,1,0,0,0,364,367,
        1,0,0,0,365,363,1,0,0,0,366,358,1,0,0,0,366,367,1,0,0,0,367,368,
        1,0,0,0,368,369,5,16,0,0,369,47,1,0,0,0,370,371,5,53,0,0,371,372,
        5,18,0,0,372,373,5,53,0,0,373,375,5,1,0,0,374,376,3,50,25,0,375,
        374,1,0,0,0,375,376,1,0,0,0,376,377,1,0,0,0,377,433,5,2,0,0,378,
        379,5,53,0,0,379,381,5,1,0,0,380,382,3,50,25,0,381,380,1,0,0,0,381,
        382,1,0,0,0,382,383,1,0,0,0,383,433,5,2,0,0,384,385,5,30,0,0,385,
        387,5,1,0,0,386,388,3,50,25,0,387,386,1,0,0,0,387,388,1,0,0,0,388,
        389,1,0,0,0,389,433,5,2,0,0,390,391,5,31,0,0,391,393,5,1,0,0,392,
        394,3,50,25,0,393,392,1,0,0,0,393,394,1,0,0,0,394,395,1,0,0,0,395,
        433,5,2,0,0,396,397,5,32,0,0,397,399,5,1,0,0,398,400,3,50,25,0,399,
        398,1,0,0,0,399,400,1,0,0,0,400,401,1,0,0,0,401,433,5,2,0,0,402,
        403,5,33,0,0,403,405,5,1,0,0,404,406,3,50,25,0,405,404,1,0,0,0,405,
        406,1,0,0,0,406,407,1,0,0,0,407,433,5,2,0,0,408,409,5,34,0,0,409,
        411,5,1,0,0,410,412,3,50,25,0,411,410,1,0,0,0,411,412,1,0,0,0,412,
        413,1,0,0,0,413,433,5,2,0,0,414,415,5,35,0,0,415,417,5,1,0,0,416,
        418,3,50,25,0,417,416,1,0,0,0,417,418,1,0,0,0,418,419,1,0,0,0,419,
        433,5,2,0,0,420,421,5,36,0,0,421,423,5,1,0,0,422,424,3,50,25,0,423,
        422,1,0,0,0,423,424,1,0,0,0,424,425,1,0,0,0,425,433,5,2,0,0,426,
        427,5,37,0,0,427,429,5,1,0,0,428,430,3,50,25,0,429,428,1,0,0,0,429,
        430,1,0,0,0,430,431,1,0,0,0,431,433,5,2,0,0,432,370,1,0,0,0,432,
        378,1,0,0,0,432,384,1,0,0,0,432,390,1,0,0,0,432,396,1,0,0,0,432,
        402,1,0,0,0,432,408,1,0,0,0,432,414,1,0,0,0,432,420,1,0,0,0,432,
        426,1,0,0,0,433,49,1,0,0,0,434,439,3,52,26,0,435,436,5,6,0,0,436,
        438,3,52,26,0,437,435,1,0,0,0,438,441,1,0,0,0,439,437,1,0,0,0,439,
        440,1,0,0,0,440,51,1,0,0,0,441,439,1,0,0,0,442,443,3,24,12,0,443,
        53,1,0,0,0,444,445,5,38,0,0,445,446,5,1,0,0,446,447,3,24,12,0,447,
        448,5,2,0,0,448,465,1,0,0,0,449,450,5,39,0,0,450,451,5,1,0,0,451,
        452,3,24,12,0,452,453,5,2,0,0,453,465,1,0,0,0,454,455,5,40,0,0,455,
        456,5,1,0,0,456,457,3,24,12,0,457,458,5,2,0,0,458,465,1,0,0,0,459,
        460,5,41,0,0,460,461,5,1,0,0,461,462,3,24,12,0,462,463,5,2,0,0,463,
        465,1,0,0,0,464,444,1,0,0,0,464,449,1,0,0,0,464,454,1,0,0,0,464,
        459,1,0,0,0,465,55,1,0,0,0,50,59,66,71,85,105,124,130,143,149,159,
        165,170,179,185,188,200,206,215,225,233,239,244,251,260,266,273,
        281,289,297,305,311,318,326,335,355,363,366,375,381,387,393,399,
        405,411,417,423,429,432,439,464
    ]

class RISCOParser ( Parser ):

    grammarFileName = "RISCO.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'='", "':'", "'=>'", "','", 
                     "'>'", "'<'", "'+'", "'-'", "'*'", "'/'", "'%'", "'^'", 
                     "'['", "']'", "'!'", "'.'", "'for'", "'in'", "'end'", 
                     "'val'", "'var'", "'print'", "'if'", "'elif'", "'else'", 
                     "'while'", "'return'", "'long'", "'range'", "'map'", 
                     "'filter'", "'reduce'", "'unwrap'", "'free'", "'input'", 
                     "'num'", "'decimal'", "'texto'", "'bool'", "'&&'", 
                     "'||'", "'=='", "'!='", "'>='", "'<='", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'null'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "FOR", "IN", 
                      "END", "VAL", "VAR", "PRINT", "IF", "ELIF", "ELSE", 
                      "WHILE", "RETURN", "LONG_F", "RANGE_F", "MAP_F", "FILTER_F", 
                      "REDUCE_F", "UNWRAP_F", "FREE_F", "INPUT_F", "NUM_CAST", 
                      "DECIMAL_CAST", "TEXTO_CAST", "BOOL_CAST", "AND", 
                      "OR", "EQ", "NEQ", "GTE", "LTE", "NUMERO", "DECIMAL", 
                      "STRING", "BOOLEANO", "NULL", "IDENTIFICADOR", "NL", 
                      "WS", "COMENTARIO_LINEA", "COMENTARIO_BLOQUE", "COMENTARIO_DOC" ]

    RULE_programa = 0
    RULE_sentencia = 1
    RULE_print_stmt = 2
    RULE_declaracion_variable = 3
    RULE_asignacion = 4
    RULE_expresion_stmt = 5
    RULE_for_stmt = 6
    RULE_if_stmt = 7
    RULE_while_stmt = 8
    RULE_declaracion_funcion = 9
    RULE_lista_params = 10
    RULE_return_stmt = 11
    RULE_expresion = 12
    RULE_or_logico = 13
    RULE_and_logico = 14
    RULE_igualdad = 15
    RULE_relacional = 16
    RULE_suma = 17
    RULE_comparacion = 18
    RULE_termino = 19
    RULE_potencia = 20
    RULE_acceso = 21
    RULE_primario = 22
    RULE_lista = 23
    RULE_llamada_funcion = 24
    RULE_lista_args = 25
    RULE_argumento = 26
    RULE_casteo = 27

    ruleNames =  [ "programa", "sentencia", "print_stmt", "declaracion_variable", 
                   "asignacion", "expresion_stmt", "for_stmt", "if_stmt", 
                   "while_stmt", "declaracion_funcion", "lista_params", 
                   "return_stmt", "expresion", "or_logico", "and_logico", 
                   "igualdad", "relacional", "suma", "comparacion", "termino", 
                   "potencia", "acceso", "primario", "lista", "llamada_funcion", 
                   "lista_args", "argumento", "casteo" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    FOR=19
    IN=20
    END=21
    VAL=22
    VAR=23
    PRINT=24
    IF=25
    ELIF=26
    ELSE=27
    WHILE=28
    RETURN=29
    LONG_F=30
    RANGE_F=31
    MAP_F=32
    FILTER_F=33
    REDUCE_F=34
    UNWRAP_F=35
    FREE_F=36
    INPUT_F=37
    NUM_CAST=38
    DECIMAL_CAST=39
    TEXTO_CAST=40
    BOOL_CAST=41
    AND=42
    OR=43
    EQ=44
    NEQ=45
    GTE=46
    LTE=47
    NUMERO=48
    DECIMAL=49
    STRING=50
    BOOLEANO=51
    NULL=52
    IDENTIFICADOR=53
    NL=54
    WS=55
    COMENTARIO_LINEA=56
    COMENTARIO_BLOQUE=57
    COMENTARIO_DOC=58

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



        # Memoria para variables
        memoria = {}



    class ProgramaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(RISCOParser.EOF, 0)

        def sentencia(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.SentenciaContext)
            else:
                return self.getTypedRuleContext(RISCOParser.SentenciaContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.NL)
            else:
                return self.getToken(RISCOParser.NL, i)

        def getRuleIndex(self):
            return RISCOParser.RULE_programa

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrograma" ):
                return visitor.visitPrograma(self)
            else:
                return visitor.visitChildren(self)




    def programa(self):

        localctx = RISCOParser.ProgramaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_programa)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 71
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35751719883932674) != 0):
                self.state = 59
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==54:
                    self.state = 56
                    self.match(RISCOParser.NL)
                    self.state = 61
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 62
                self.sentencia()
                self.state = 66
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 63
                        self.match(RISCOParser.NL) 
                    self.state = 68
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

                self.state = 73
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 74
            self.match(RISCOParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SentenciaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaracion_variable(self):
            return self.getTypedRuleContext(RISCOParser.Declaracion_variableContext,0)


        def asignacion(self):
            return self.getTypedRuleContext(RISCOParser.AsignacionContext,0)


        def expresion_stmt(self):
            return self.getTypedRuleContext(RISCOParser.Expresion_stmtContext,0)


        def for_stmt(self):
            return self.getTypedRuleContext(RISCOParser.For_stmtContext,0)


        def print_stmt(self):
            return self.getTypedRuleContext(RISCOParser.Print_stmtContext,0)


        def if_stmt(self):
            return self.getTypedRuleContext(RISCOParser.If_stmtContext,0)


        def while_stmt(self):
            return self.getTypedRuleContext(RISCOParser.While_stmtContext,0)


        def declaracion_funcion(self):
            return self.getTypedRuleContext(RISCOParser.Declaracion_funcionContext,0)


        def return_stmt(self):
            return self.getTypedRuleContext(RISCOParser.Return_stmtContext,0)


        def getRuleIndex(self):
            return RISCOParser.RULE_sentencia

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSentencia" ):
                return visitor.visitSentencia(self)
            else:
                return visitor.visitChildren(self)




    def sentencia(self):

        localctx = RISCOParser.SentenciaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_sentencia)
        try:
            self.state = 85
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 76
                self.declaracion_variable()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.asignacion()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 78
                self.expresion_stmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 79
                self.for_stmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 80
                self.print_stmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 81
                self.if_stmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 82
                self.while_stmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 83
                self.declaracion_funcion()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 84
                self.return_stmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Print_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(RISCOParser.PRINT, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self):
            return self.getToken(RISCOParser.NL, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_print_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrint_stmt" ):
                return visitor.visitPrint_stmt(self)
            else:
                return visitor.visitChildren(self)




    def print_stmt(self):

        localctx = RISCOParser.Print_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_print_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.match(RISCOParser.PRINT)
            self.state = 88
            self.match(RISCOParser.T__0)
            self.state = 89
            self.expresion()
            self.state = 90
            self.match(RISCOParser.T__1)
            self.state = 91
            self.match(RISCOParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Declaracion_variableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VAL(self):
            return self.getToken(RISCOParser.VAL, 0)

        def IDENTIFICADOR(self):
            return self.getToken(RISCOParser.IDENTIFICADOR, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self):
            return self.getToken(RISCOParser.NL, 0)

        def VAR(self):
            return self.getToken(RISCOParser.VAR, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_declaracion_variable

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaracion_variable" ):
                return visitor.visitDeclaracion_variable(self)
            else:
                return visitor.visitChildren(self)




    def declaracion_variable(self):

        localctx = RISCOParser.Declaracion_variableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_declaracion_variable)
        try:
            self.state = 105
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 93
                self.match(RISCOParser.VAL)
                self.state = 94
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 95
                self.match(RISCOParser.T__2)
                self.state = 96
                self.expresion()
                self.state = 97
                self.match(RISCOParser.NL)
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 99
                self.match(RISCOParser.VAR)
                self.state = 100
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 101
                self.match(RISCOParser.T__2)
                self.state = 102
                self.expresion()
                self.state = 103
                self.match(RISCOParser.NL)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AsignacionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFICADOR(self):
            return self.getToken(RISCOParser.IDENTIFICADOR, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self):
            return self.getToken(RISCOParser.NL, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_asignacion

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAsignacion" ):
                return visitor.visitAsignacion(self)
            else:
                return visitor.visitChildren(self)




    def asignacion(self):

        localctx = RISCOParser.AsignacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_asignacion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            self.match(RISCOParser.IDENTIFICADOR)
            self.state = 108
            self.match(RISCOParser.T__2)
            self.state = 109
            self.expresion()
            self.state = 110
            self.match(RISCOParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expresion_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self):
            return self.getToken(RISCOParser.NL, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_expresion_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpresion_stmt" ):
                return visitor.visitExpresion_stmt(self)
            else:
                return visitor.visitChildren(self)




    def expresion_stmt(self):

        localctx = RISCOParser.Expresion_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_expresion_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.expresion()
            self.state = 113
            self.match(RISCOParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class For_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(RISCOParser.FOR, 0)

        def IDENTIFICADOR(self):
            return self.getToken(RISCOParser.IDENTIFICADOR, 0)

        def IN(self):
            return self.getToken(RISCOParser.IN, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.NL)
            else:
                return self.getToken(RISCOParser.NL, i)

        def END(self):
            return self.getToken(RISCOParser.END, 0)

        def sentencia(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.SentenciaContext)
            else:
                return self.getTypedRuleContext(RISCOParser.SentenciaContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_for_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFor_stmt" ):
                return visitor.visitFor_stmt(self)
            else:
                return visitor.visitChildren(self)




    def for_stmt(self):

        localctx = RISCOParser.For_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_for_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(RISCOParser.FOR)
            self.state = 116
            self.match(RISCOParser.IDENTIFICADOR)
            self.state = 117
            self.match(RISCOParser.IN)
            self.state = 118
            self.expresion()
            self.state = 119
            self.match(RISCOParser.T__3)
            self.state = 120
            self.match(RISCOParser.NL)
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35751719883932674) != 0):
                self.state = 124
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==54:
                    self.state = 121
                    self.match(RISCOParser.NL)
                    self.state = 126
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 127
                self.sentencia()
                self.state = 132
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 133
            self.match(RISCOParser.END)
            self.state = 134
            self.match(RISCOParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class If_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(RISCOParser.IF, 0)

        def expresion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.ExpresionContext)
            else:
                return self.getTypedRuleContext(RISCOParser.ExpresionContext,i)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.NL)
            else:
                return self.getToken(RISCOParser.NL, i)

        def END(self):
            return self.getToken(RISCOParser.END, 0)

        def sentencia(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.SentenciaContext)
            else:
                return self.getTypedRuleContext(RISCOParser.SentenciaContext,i)


        def ELIF(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.ELIF)
            else:
                return self.getToken(RISCOParser.ELIF, i)

        def ELSE(self):
            return self.getToken(RISCOParser.ELSE, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_if_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIf_stmt" ):
                return visitor.visitIf_stmt(self)
            else:
                return visitor.visitChildren(self)




    def if_stmt(self):

        localctx = RISCOParser.If_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_if_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.match(RISCOParser.IF)
            self.state = 137
            self.expresion()
            self.state = 138
            self.match(RISCOParser.T__3)
            self.state = 139
            self.match(RISCOParser.NL)
            self.state = 149
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35751719883932674) != 0):
                self.state = 143
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==54:
                    self.state = 140
                    self.match(RISCOParser.NL)
                    self.state = 145
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 146
                self.sentencia()
                self.state = 151
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 170
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 152
                self.match(RISCOParser.ELIF)
                self.state = 153
                self.expresion()
                self.state = 154
                self.match(RISCOParser.T__3)
                self.state = 155
                self.match(RISCOParser.NL)
                self.state = 165
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35751719883932674) != 0):
                    self.state = 159
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==54:
                        self.state = 156
                        self.match(RISCOParser.NL)
                        self.state = 161
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 162
                    self.sentencia()
                    self.state = 167
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 172
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 173
                self.match(RISCOParser.ELSE)
                self.state = 174
                self.match(RISCOParser.T__3)
                self.state = 175
                self.match(RISCOParser.NL)
                self.state = 185
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35751719883932674) != 0):
                    self.state = 179
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==54:
                        self.state = 176
                        self.match(RISCOParser.NL)
                        self.state = 181
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 182
                    self.sentencia()
                    self.state = 187
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 190
            self.match(RISCOParser.END)
            self.state = 191
            self.match(RISCOParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class While_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(RISCOParser.WHILE, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.NL)
            else:
                return self.getToken(RISCOParser.NL, i)

        def END(self):
            return self.getToken(RISCOParser.END, 0)

        def sentencia(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.SentenciaContext)
            else:
                return self.getTypedRuleContext(RISCOParser.SentenciaContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_while_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhile_stmt" ):
                return visitor.visitWhile_stmt(self)
            else:
                return visitor.visitChildren(self)




    def while_stmt(self):

        localctx = RISCOParser.While_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_while_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 193
            self.match(RISCOParser.WHILE)
            self.state = 194
            self.expresion()
            self.state = 195
            self.match(RISCOParser.T__3)
            self.state = 196
            self.match(RISCOParser.NL)
            self.state = 206
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35751719883932674) != 0):
                self.state = 200
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==54:
                    self.state = 197
                    self.match(RISCOParser.NL)
                    self.state = 202
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 203
                self.sentencia()
                self.state = 208
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 209
            self.match(RISCOParser.END)
            self.state = 210
            self.match(RISCOParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Declaracion_funcionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFICADOR(self):
            return self.getToken(RISCOParser.IDENTIFICADOR, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.NL)
            else:
                return self.getToken(RISCOParser.NL, i)

        def lista_params(self):
            return self.getTypedRuleContext(RISCOParser.Lista_paramsContext,0)


        def END(self):
            return self.getToken(RISCOParser.END, 0)

        def sentencia(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.SentenciaContext)
            else:
                return self.getTypedRuleContext(RISCOParser.SentenciaContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_declaracion_funcion

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaracion_funcion" ):
                return visitor.visitDeclaracion_funcion(self)
            else:
                return visitor.visitChildren(self)




    def declaracion_funcion(self):

        localctx = RISCOParser.Declaracion_funcionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_declaracion_funcion)
        self._la = 0 # Token type
        try:
            self.state = 244
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 212
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 213
                self.match(RISCOParser.T__0)
                self.state = 215
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==53:
                    self.state = 214
                    self.lista_params()


                self.state = 217
                self.match(RISCOParser.T__1)
                self.state = 218
                self.match(RISCOParser.T__4)
                self.state = 219
                self.expresion()
                self.state = 220
                self.match(RISCOParser.NL)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 222
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 223
                self.match(RISCOParser.T__0)
                self.state = 225
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==53:
                    self.state = 224
                    self.lista_params()


                self.state = 227
                self.match(RISCOParser.T__1)
                self.state = 228
                self.match(RISCOParser.T__4)
                self.state = 229
                self.match(RISCOParser.NL)
                self.state = 239
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35751719883932674) != 0):
                    self.state = 233
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    while _la==54:
                        self.state = 230
                        self.match(RISCOParser.NL)
                        self.state = 235
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)

                    self.state = 236
                    self.sentencia()
                    self.state = 241
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 242
                self.match(RISCOParser.END)
                self.state = 243
                self.match(RISCOParser.NL)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Lista_paramsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFICADOR(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.IDENTIFICADOR)
            else:
                return self.getToken(RISCOParser.IDENTIFICADOR, i)

        def getRuleIndex(self):
            return RISCOParser.RULE_lista_params

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLista_params" ):
                return visitor.visitLista_params(self)
            else:
                return visitor.visitChildren(self)




    def lista_params(self):

        localctx = RISCOParser.Lista_paramsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_lista_params)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 246
            self.match(RISCOParser.IDENTIFICADOR)
            self.state = 251
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 247
                self.match(RISCOParser.T__5)
                self.state = 248
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 253
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Return_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(RISCOParser.RETURN, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def NL(self):
            return self.getToken(RISCOParser.NL, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_return_stmt

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn_stmt" ):
                return visitor.visitReturn_stmt(self)
            else:
                return visitor.visitChildren(self)




    def return_stmt(self):

        localctx = RISCOParser.Return_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_return_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 254
            self.match(RISCOParser.RETURN)
            self.state = 255
            self.expresion()
            self.state = 256
            self.match(RISCOParser.NL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpresionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def lista_params(self):
            return self.getTypedRuleContext(RISCOParser.Lista_paramsContext,0)


        def or_logico(self):
            return self.getTypedRuleContext(RISCOParser.Or_logicoContext,0)


        def getRuleIndex(self):
            return RISCOParser.RULE_expresion

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpresion" ):
                return visitor.visitExpresion(self)
            else:
                return visitor.visitChildren(self)




    def expresion(self):

        localctx = RISCOParser.ExpresionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_expresion)
        self._la = 0 # Token type
        try:
            self.state = 266
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,24,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 258
                self.match(RISCOParser.T__0)
                self.state = 260
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==53:
                    self.state = 259
                    self.lista_params()


                self.state = 262
                self.match(RISCOParser.T__1)
                self.state = 263
                self.match(RISCOParser.T__4)
                self.state = 264
                self.expresion()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 265
                self.or_logico()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Or_logicoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def and_logico(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.And_logicoContext)
            else:
                return self.getTypedRuleContext(RISCOParser.And_logicoContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.OR)
            else:
                return self.getToken(RISCOParser.OR, i)

        def getRuleIndex(self):
            return RISCOParser.RULE_or_logico

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOr_logico" ):
                return visitor.visitOr_logico(self)
            else:
                return visitor.visitChildren(self)




    def or_logico(self):

        localctx = RISCOParser.Or_logicoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_or_logico)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 268
            self.and_logico()
            self.state = 273
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==43:
                self.state = 269
                self.match(RISCOParser.OR)
                self.state = 270
                self.and_logico()
                self.state = 275
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class And_logicoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def igualdad(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.IgualdadContext)
            else:
                return self.getTypedRuleContext(RISCOParser.IgualdadContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.AND)
            else:
                return self.getToken(RISCOParser.AND, i)

        def getRuleIndex(self):
            return RISCOParser.RULE_and_logico

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd_logico" ):
                return visitor.visitAnd_logico(self)
            else:
                return visitor.visitChildren(self)




    def and_logico(self):

        localctx = RISCOParser.And_logicoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_and_logico)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 276
            self.igualdad()
            self.state = 281
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42:
                self.state = 277
                self.match(RISCOParser.AND)
                self.state = 278
                self.igualdad()
                self.state = 283
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IgualdadContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relacional(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.RelacionalContext)
            else:
                return self.getTypedRuleContext(RISCOParser.RelacionalContext,i)


        def EQ(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.EQ)
            else:
                return self.getToken(RISCOParser.EQ, i)

        def NEQ(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.NEQ)
            else:
                return self.getToken(RISCOParser.NEQ, i)

        def getRuleIndex(self):
            return RISCOParser.RULE_igualdad

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIgualdad" ):
                return visitor.visitIgualdad(self)
            else:
                return visitor.visitChildren(self)




    def igualdad(self):

        localctx = RISCOParser.IgualdadContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_igualdad)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 284
            self.relacional()
            self.state = 289
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==44 or _la==45:
                self.state = 285
                _la = self._input.LA(1)
                if not(_la==44 or _la==45):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 286
                self.relacional()
                self.state = 291
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelacionalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def suma(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.SumaContext)
            else:
                return self.getTypedRuleContext(RISCOParser.SumaContext,i)


        def GTE(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.GTE)
            else:
                return self.getToken(RISCOParser.GTE, i)

        def LTE(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.LTE)
            else:
                return self.getToken(RISCOParser.LTE, i)

        def getRuleIndex(self):
            return RISCOParser.RULE_relacional

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelacional" ):
                return visitor.visitRelacional(self)
            else:
                return visitor.visitChildren(self)




    def relacional(self):

        localctx = RISCOParser.RelacionalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_relacional)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 292
            self.suma()
            self.state = 297
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 211106232533376) != 0):
                self.state = 293
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 211106232533376) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 294
                self.suma()
                self.state = 299
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SumaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def comparacion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.ComparacionContext)
            else:
                return self.getTypedRuleContext(RISCOParser.ComparacionContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_suma

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSuma" ):
                return visitor.visitSuma(self)
            else:
                return visitor.visitChildren(self)




    def suma(self):

        localctx = RISCOParser.SumaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_suma)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 300
            self.comparacion()
            self.state = 305
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==9 or _la==10:
                self.state = 301
                _la = self._input.LA(1)
                if not(_la==9 or _la==10):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 302
                self.comparacion()
                self.state = 307
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparacionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def termino(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.TerminoContext)
            else:
                return self.getTypedRuleContext(RISCOParser.TerminoContext,i)


        def IN(self):
            return self.getToken(RISCOParser.IN, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_comparacion

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparacion" ):
                return visitor.visitComparacion(self)
            else:
                return visitor.visitChildren(self)




    def comparacion(self):

        localctx = RISCOParser.ComparacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_comparacion)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 308
            self.termino()
            self.state = 311
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 309
                self.match(RISCOParser.IN)
                self.state = 310
                self.termino()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TerminoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def potencia(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.PotenciaContext)
            else:
                return self.getTypedRuleContext(RISCOParser.PotenciaContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_termino

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTermino" ):
                return visitor.visitTermino(self)
            else:
                return visitor.visitChildren(self)




    def termino(self):

        localctx = RISCOParser.TerminoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_termino)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 313
            self.potencia()
            self.state = 318
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 14336) != 0):
                self.state = 314
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 14336) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 315
                self.potencia()
                self.state = 320
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PotenciaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def acceso(self):
            return self.getTypedRuleContext(RISCOParser.AccesoContext,0)


        def potencia(self):
            return self.getTypedRuleContext(RISCOParser.PotenciaContext,0)


        def getRuleIndex(self):
            return RISCOParser.RULE_potencia

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPotencia" ):
                return visitor.visitPotencia(self)
            else:
                return visitor.visitChildren(self)




    def potencia(self):

        localctx = RISCOParser.PotenciaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_potencia)
        try:
            self.state = 326
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,32,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 321
                self.acceso()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 322
                self.acceso()
                self.state = 323
                self.match(RISCOParser.T__13)
                self.state = 324
                self.potencia()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AccesoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primario(self):
            return self.getTypedRuleContext(RISCOParser.PrimarioContext,0)


        def expresion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.ExpresionContext)
            else:
                return self.getTypedRuleContext(RISCOParser.ExpresionContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_acceso

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAcceso" ):
                return visitor.visitAcceso(self)
            else:
                return visitor.visitChildren(self)




    def acceso(self):

        localctx = RISCOParser.AccesoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_acceso)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 328
            self.primario()
            self.state = 335
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==15:
                self.state = 329
                self.match(RISCOParser.T__14)
                self.state = 330
                self.expresion()
                self.state = 331
                self.match(RISCOParser.T__15)
                self.state = 337
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimarioContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMERO(self):
            return self.getToken(RISCOParser.NUMERO, 0)

        def DECIMAL(self):
            return self.getToken(RISCOParser.DECIMAL, 0)

        def STRING(self):
            return self.getToken(RISCOParser.STRING, 0)

        def BOOLEANO(self):
            return self.getToken(RISCOParser.BOOLEANO, 0)

        def NULL(self):
            return self.getToken(RISCOParser.NULL, 0)

        def lista(self):
            return self.getTypedRuleContext(RISCOParser.ListaContext,0)


        def llamada_funcion(self):
            return self.getTypedRuleContext(RISCOParser.Llamada_funcionContext,0)


        def casteo(self):
            return self.getTypedRuleContext(RISCOParser.CasteoContext,0)


        def IDENTIFICADOR(self):
            return self.getToken(RISCOParser.IDENTIFICADOR, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def primario(self):
            return self.getTypedRuleContext(RISCOParser.PrimarioContext,0)


        def getRuleIndex(self):
            return RISCOParser.RULE_primario

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimario" ):
                return visitor.visitPrimario(self)
            else:
                return visitor.visitChildren(self)




    def primario(self):

        localctx = RISCOParser.PrimarioContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_primario)
        try:
            self.state = 355
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,34,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 338
                self.match(RISCOParser.NUMERO)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 339
                self.match(RISCOParser.DECIMAL)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 340
                self.match(RISCOParser.STRING)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 341
                self.match(RISCOParser.BOOLEANO)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 342
                self.match(RISCOParser.NULL)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 343
                self.lista()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 344
                self.llamada_funcion()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 345
                self.casteo()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 346
                self.match(RISCOParser.IDENTIFICADOR)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 347
                self.match(RISCOParser.T__0)
                self.state = 348
                self.expresion()
                self.state = 349
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 351
                self.match(RISCOParser.T__9)
                self.state = 352
                self.primario()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 353
                self.match(RISCOParser.T__16)
                self.state = 354
                self.primario()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.ExpresionContext)
            else:
                return self.getTypedRuleContext(RISCOParser.ExpresionContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_lista

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLista" ):
                return visitor.visitLista(self)
            else:
                return visitor.visitChildren(self)




    def lista(self):

        localctx = RISCOParser.ListaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_lista)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 357
            self.match(RISCOParser.T__14)
            self.state = 366
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                self.state = 358
                self.expresion()
                self.state = 363
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==6:
                    self.state = 359
                    self.match(RISCOParser.T__5)
                    self.state = 360
                    self.expresion()
                    self.state = 365
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 368
            self.match(RISCOParser.T__15)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Llamada_funcionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENTIFICADOR(self, i:int=None):
            if i is None:
                return self.getTokens(RISCOParser.IDENTIFICADOR)
            else:
                return self.getToken(RISCOParser.IDENTIFICADOR, i)

        def lista_args(self):
            return self.getTypedRuleContext(RISCOParser.Lista_argsContext,0)


        def LONG_F(self):
            return self.getToken(RISCOParser.LONG_F, 0)

        def RANGE_F(self):
            return self.getToken(RISCOParser.RANGE_F, 0)

        def MAP_F(self):
            return self.getToken(RISCOParser.MAP_F, 0)

        def FILTER_F(self):
            return self.getToken(RISCOParser.FILTER_F, 0)

        def REDUCE_F(self):
            return self.getToken(RISCOParser.REDUCE_F, 0)

        def UNWRAP_F(self):
            return self.getToken(RISCOParser.UNWRAP_F, 0)

        def FREE_F(self):
            return self.getToken(RISCOParser.FREE_F, 0)

        def INPUT_F(self):
            return self.getToken(RISCOParser.INPUT_F, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_llamada_funcion

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLlamada_funcion" ):
                return visitor.visitLlamada_funcion(self)
            else:
                return visitor.visitChildren(self)




    def llamada_funcion(self):

        localctx = RISCOParser.Llamada_funcionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_llamada_funcion)
        self._la = 0 # Token type
        try:
            self.state = 432
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 370
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 371
                self.match(RISCOParser.T__17)
                self.state = 372
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 373
                self.match(RISCOParser.T__0)
                self.state = 375
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 374
                    self.lista_args()


                self.state = 377
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 378
                self.match(RISCOParser.IDENTIFICADOR)
                self.state = 379
                self.match(RISCOParser.T__0)
                self.state = 381
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 380
                    self.lista_args()


                self.state = 383
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 384
                self.match(RISCOParser.LONG_F)
                self.state = 385
                self.match(RISCOParser.T__0)
                self.state = 387
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 386
                    self.lista_args()


                self.state = 389
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 390
                self.match(RISCOParser.RANGE_F)
                self.state = 391
                self.match(RISCOParser.T__0)
                self.state = 393
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 392
                    self.lista_args()


                self.state = 395
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 396
                self.match(RISCOParser.MAP_F)
                self.state = 397
                self.match(RISCOParser.T__0)
                self.state = 399
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 398
                    self.lista_args()


                self.state = 401
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 402
                self.match(RISCOParser.FILTER_F)
                self.state = 403
                self.match(RISCOParser.T__0)
                self.state = 405
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 404
                    self.lista_args()


                self.state = 407
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 408
                self.match(RISCOParser.REDUCE_F)
                self.state = 409
                self.match(RISCOParser.T__0)
                self.state = 411
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 410
                    self.lista_args()


                self.state = 413
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 414
                self.match(RISCOParser.UNWRAP_F)
                self.state = 415
                self.match(RISCOParser.T__0)
                self.state = 417
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 416
                    self.lista_args()


                self.state = 419
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 420
                self.match(RISCOParser.FREE_F)
                self.state = 421
                self.match(RISCOParser.T__0)
                self.state = 423
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 422
                    self.lista_args()


                self.state = 425
                self.match(RISCOParser.T__1)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 426
                self.match(RISCOParser.INPUT_F)
                self.state = 427
                self.match(RISCOParser.T__0)
                self.state = 429
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 17737320505705474) != 0):
                    self.state = 428
                    self.lista_args()


                self.state = 431
                self.match(RISCOParser.T__1)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Lista_argsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def argumento(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(RISCOParser.ArgumentoContext)
            else:
                return self.getTypedRuleContext(RISCOParser.ArgumentoContext,i)


        def getRuleIndex(self):
            return RISCOParser.RULE_lista_args

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLista_args" ):
                return visitor.visitLista_args(self)
            else:
                return visitor.visitChildren(self)




    def lista_args(self):

        localctx = RISCOParser.Lista_argsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_lista_args)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 434
            self.argumento()
            self.state = 439
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 435
                self.match(RISCOParser.T__5)
                self.state = 436
                self.argumento()
                self.state = 441
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgumentoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def getRuleIndex(self):
            return RISCOParser.RULE_argumento

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgumento" ):
                return visitor.visitArgumento(self)
            else:
                return visitor.visitChildren(self)




    def argumento(self):

        localctx = RISCOParser.ArgumentoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_argumento)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 442
            self.expresion()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CasteoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUM_CAST(self):
            return self.getToken(RISCOParser.NUM_CAST, 0)

        def expresion(self):
            return self.getTypedRuleContext(RISCOParser.ExpresionContext,0)


        def DECIMAL_CAST(self):
            return self.getToken(RISCOParser.DECIMAL_CAST, 0)

        def TEXTO_CAST(self):
            return self.getToken(RISCOParser.TEXTO_CAST, 0)

        def BOOL_CAST(self):
            return self.getToken(RISCOParser.BOOL_CAST, 0)

        def getRuleIndex(self):
            return RISCOParser.RULE_casteo

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCasteo" ):
                return visitor.visitCasteo(self)
            else:
                return visitor.visitChildren(self)




    def casteo(self):

        localctx = RISCOParser.CasteoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_casteo)
        try:
            self.state = 464
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [38]:
                self.enterOuterAlt(localctx, 1)
                self.state = 444
                self.match(RISCOParser.NUM_CAST)
                self.state = 445
                self.match(RISCOParser.T__0)
                self.state = 446
                self.expresion()
                self.state = 447
                self.match(RISCOParser.T__1)
                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 2)
                self.state = 449
                self.match(RISCOParser.DECIMAL_CAST)
                self.state = 450
                self.match(RISCOParser.T__0)
                self.state = 451
                self.expresion()
                self.state = 452
                self.match(RISCOParser.T__1)
                pass
            elif token in [40]:
                self.enterOuterAlt(localctx, 3)
                self.state = 454
                self.match(RISCOParser.TEXTO_CAST)
                self.state = 455
                self.match(RISCOParser.T__0)
                self.state = 456
                self.expresion()
                self.state = 457
                self.match(RISCOParser.T__1)
                pass
            elif token in [41]:
                self.enterOuterAlt(localctx, 4)
                self.state = 459
                self.match(RISCOParser.BOOL_CAST)
                self.state = 460
                self.match(RISCOParser.T__0)
                self.state = 461
                self.expresion()
                self.state = 462
                self.match(RISCOParser.T__1)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





