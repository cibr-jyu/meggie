'''
Created on Mar 14, 2013

@author: jaolpeso
'''

import numpy



class IntegralImage():
    
    def sumOverMatrix(self, matrix):
        """
        Matrix is type numpy.ndarray
        """
        
        sizex = 0
        sizey = 0
        
        try:
            sizex = matrix.shape[0]
            sizey = matrix.shape[1]
        except Exception:
            pass
        

        self.integral_image = numpy.zeros((sizex, sizey))
        sum = 0
        temp = 0
        
        for i in range(sizex):
            for j in range(sizey):
                sum += matrix[i][j]
                self.integral_image[i][j] = sum
            sum = 0
        
        for j in range(sizey):
            for i in range(sizex):
                sum += self.integral_image[i][j]
                self.integral_image[i][j] = sum
            sum = 0
        
        
    def sumOverRectangularArea(self, top_left_corner, bottom_right_corner):
        """
        top_left_corner and bottom_right_corner are type tuple
        Formula I(C)+I(A)-I(B)-I(D) is used to count the sum of the rectangular area.
        A is the t
                
        Keyword arguments:
        top_left_corner - - top-left corner of the rectangle
        bottom_right_corner - - bottom-right corner of the rectangle
        """
                
        """
        Blocks make sure that bottom-right corner of the rectangle isn't choosen out of bounds.
        """
        if (bottom_right_corner[0] >= self.integral_image.shape[1]):
            return 'Rectangle out of bounds'
        if (bottom_right_corner[1] >= self.integral_image.shape[0]):
            return 'Rectangle out of bounds'
        
        rectangle_area_sum = 0
        """
        In case of the rectangle touching the left and top edge of the area.
        """
        if (top_left_corner[0] == 0 and top_left_corner[1] == 0):
            rectangle_area_sum = self.integral_image[bottom_right_corner[1]][bottom_right_corner[0]]
            return rectangle_area_sum
        """
        In case of the rectangle touching the left edge of the area.
        Block makes sure that x index isn't out of bounds when reducing the index by 1.
        """
        if (top_left_corner[0] == 0):
            rectangle_area_sum =  self.integral_image[bottom_right_corner[1]][bottom_right_corner[0]] - self.integral_image[top_left_corner[1]-1][bottom_right_corner[0]]
            return rectangle_area_sum
        """
        In case of the rectangle touching the top edge of the area.
        Block makes sure that y index isn't out of bounds when reducing the index by 1.
        """
        if (top_left_corner[1] == 0):
            rectangle_area_sum =  self.integral_image[bottom_right_corner[1]][bottom_right_corner[0]] - self.integral_image[bottom_right_corner[1]][top_left_corner[0]-1]
            return rectangle_area_sum
        rectangle_area_sum =  self.integral_image[bottom_right_corner[1]][bottom_right_corner[0]] + self.integral_image[top_left_corner[1]-1][top_left_corner[0]-1] - self.integral_image[top_left_corner[1]-1][bottom_right_corner[0]] - self.integral_image[bottom_right_corner[1]][top_left_corner[0]-1]
        return rectangle_area_sum
        """
        try:
            
            rectangle_area_sum =  self.integral_image[down_right_corner[0]][down_right_corner[1]]
            + self.integral_image[up_left_corner[0]-1][up_left_corner[1]-1]
            - self.integral_image[down_right_corner[0]][up_left_corner[1]-1]
            - self.integral_image[up_left_corner[0]-1][down_right_corner[1]]
            
            
            
            
            
            for i in range(sizex):
                for j in range(sizey):
                    sum += self.integral_image[i][j]
                    
                    
        
        except Exception:
            return
        """
                
        