import os
import cv2

class Artifactor:

    def gaussianNoise(image ,self):
        return

    def generate(inputDir, outputPath, self):
        effects = [ gaussianNoise ]
        for effect in effects:
            effectPath = outputPath+"/"+effect.__name__
            if not os.path.exists(effectPath):
                os.makedirs(effectPath)

        inputFrameNames = sorted(os.listdir(inputDir))
        for fileName in inputFrameNames:
            image = cv2.imread(inputDir+fileName)
            for effect in effects:
                effect(image, outputPath+"/"+effect.__name__+"/"+fileName)
