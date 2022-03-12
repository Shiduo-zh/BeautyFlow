import cv2
import numpy as np

class wrinkle_merge():
    def __init__(self):
        self.texture=0

    def Merge(face, wrinkle, faceRect):
        rendererRect = CGRect(x: 0, y: 0, width: face.size.width, height: face.size.height)
        renderer = UIGraphicsImageRenderer(bounds: rendererRect)
        outputImage = renderer.image { ctx in
            UIColor.white.set()
            ctx.fill(rendererRect)
            face.draw(in: rendererRect, blendMode: .normal, alpha: 1)
            // 柔光混合
            wrinkle.draw(in: faceRect, blendMode: .softLight, alpha: 1)
        }
        return outputImage
