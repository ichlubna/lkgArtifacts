import tempfile
import os
import basher

class Metrics:
    ssim = 0
    psnr = 0
    vmaf = 0
    vif = [0,0,0,0]

    def avgVif():
        return (sum(self.vif)/len(self.vif))

class Evaluator:
    tmpDir = ""
    ffmpegPath = "ffmpeg"

    def metrics(self, originalDir, distortedDir):
        m = Metrics()
        originalExtension = os.path.splitext(os.listdir(originalDir)[0])[1]
        distortedExtension = os.path.splitext(os.listdir(distortedDir)[0])[1]

        commandStart = self.ffmpegPath+" -i "+originalDir+"%04d"+originalExtension+" -i "+distortedDir+"%04d"+distortedExtension
        commandEnd = "-f null -"

        result = basher.run(commandStart+" -lavfi ssim "+commandEnd)
        m.ssim = result.stderr.partition("All:")[2]
        m.ssim = m.ssim.partition(" ")[0]

        result = basher.run(commandStart+" -lavfi psnr "+commandEnd)
        m.psnr = result.stderr.partition("average:")[2]
        m.psnr = m.psnr.partition(" min")[0]

        result = basher.run(commandStart+" -filter_complex libvmaf "+commandEnd)
        m.vmaf = result.stderr.partition("VMAF score: ")[2]
        m.vmaf = m.vmaf.partition("\n")[0]

        result = basher.run(commandStart+" -lavfi vif "+commandEnd)
        for i in range(0,4):
            m.vif[i] = result.stderr.partition("scale="+str(i)+" average:")[2]
            m.vif[i] = m.vif[i].partition(" min:")[0]
        return m

    def combineFrames(self, originalDir, outputDir):
        return

    def evaluate(self, originalDir, distortedDir):
        return

    def __init__(self):
        self.tmpDir = os.path.join(tempfile.mkdtemp(), '')

