import sys
import os
import compressor as cmp
import artifactor as art

class Convertor:
    inputDir = ""
    outputDir = ""
    inputFrameNames = []

    def __init__(self):
        if len(sys.argv) > 2:
            raise Exception("Need at least two arguments: input (containing LKG frames) and output directory")
        self.inputDir = sys.argv[1]
        self.outputDir = sys.argv[2]

    def generateArtifacts(self):
        Artifactor artifactor();
        artifactor.generate(self.inputDir, self.outputDir);

    def encodeDecode(self):
        Compressor compressor();

c = Convertor()
try:
    c.run()
except Exception as e:
    print(e)
    print(traceback.format_exc())
