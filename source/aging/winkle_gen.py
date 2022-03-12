import cv2
import numpy as np

class ImageMesh():
   def __init__(self,vd,hd):
        self.verticalDivisions = vd
        self.horizontalDivisions = hd
        self.indexArrSize = 2 * self.verticalDivisions * (self.horizontalDivisions + 1)
        self.vertexIndices=np.zeros(self.indexArrSize)
        #Opengl
        self.verticesArr=np.zeros(2*self.indexArrSize)
        self.textureCoordsArr=np.zeros(2*self.indexArrSize)
        self.texture=None
        
        self.image_width=0.0
        self.image_height= 0.0
        
        self.numVertices= (self.verticalDivisions+1)*(self.horizontalDivisions+1)
        self.xy=np.zeros(2*self.numVertices).reshape((2,self.numVertices))
        self.xy=np.zeros(2*self.numVertices).reshape((2,self.numVertices))
    
    def init_param(self): 
        self.init()
       
        var count = 0
        for i in 0..<verticalDivisions {
            for j in 0...horizontalDivisions {
                vertexIndices![count] = (i + 1) * (horizontalDivisions + 1) + j; count += 1
                vertexIndices![count] = i * (horizontalDivisions + 1) + j; count += 1
            }
        }
        let xIncrease = 1.0 / Float(horizontalDivisions)
        let yIncrease = 1.0 / Float(verticalDivisions)
        count = 0
        for i in 0..<verticalDivisions {
            for j in 0...horizontalDivisions {
                let currX = Float(j) * xIncrease;
                let currY = 1 - Float(i) * yIncrease;
                textureCoordsArr![count] = currX; count += 1
                textureCoordsArr![count] = currY - yIncrease; count += 1
                textureCoordsArr![count] = currX; count += 1
                textureCoordsArr![count] = currY; count += 1
            }
        }
    
