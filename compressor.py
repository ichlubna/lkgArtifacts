import shutil
import tempfile
import os
import cv2
import basher

class Compressor:
    #VVC implementation from: https://github.com/fraunhoferhhi
    encoderPath = "./vvc/vvenc/bin/release-static/vvencapp"
    decoderPath = "./vvc/vvdec/bin/release-static/vvdecapp"
    ffmpegPath = "ffmpeg"
    pixFmt = "420"
    tmpDir = ""

    def toYUV (self, inputDir, outputFile):
        extension = os.path.splitext(os.listdir(inputDir)[0])[1]
        if os.path.splitext(outputFile)[1] != ".yuv":
            raise Exception("YUV file must have .yuv extension!")
        basher.run(self.ffmpegPath+" -i "+inputDir+"/%04d"+extension+" -pix_fmt yuv"+self.pixFmt+"p "+outputFile)

    def compress(self, inputDir, outputDir, qp):
        resolution = cv2.imread(inputDir+"/"+os.listdir(inputDir)[0]).shape
        resolutionString = str(resolution[1])+"x"+str(resolution[0])
        yuvFile = self.tmpDir+"/"+resolutionString+".yuv"
        self.toYUV(inputDir, yuvFile)
        outputFilePath = outputDir+"/"+resolutionString+".266"
        basher.run(self.encoderPath+" -i "+yuvFile+" -s "+resolutionString+" -c yuv"+self.pixFmt+" -q "+str(qp)+" -o "+outputFilePath)
        os.remove(yuvFile)
        return outputFilePath

    def decompress(self, inputFile, outputDir):
        yuvFile = self.tmpDir+"/video.yuv"
        resolution = os.path.splitext(os.path.basename(inputFile))[0]
        #.partition("x")
        basher.run(self.decoderPath+" -b "+inputFile+" -o "+yuvFile)
        basher.run(self.ffmpegPath+" -s "+resolution+" -pix_fmt yuv"+self.pixFmt+"p -i "+yuvFile+" -pix_fmt yuv"+self.pixFmt+"p -s:v "+resolution+" "+outputDir+"/%04d.png")
        os.remove(yuvFile)

    def process(self, inputDir, outputDir):
        videoPath = self.compress(inputDir, self.tmpDir, 32)
        self.decompress(videoPath, outputDir)

    def __init__(self):
        self.tmpDir = os.path.join(tempfile.mkdtemp(), '')

    def __del__(self):
        shutil.rmtree(self.tmpDir)
        return

c = Compressor()
c.process("./data", "./test")
