"""
Created on Mar 14, 2013

@author: Janne Pesonen
"""

import numpy

class IntegralImage(object):
    
    """
    Class for counting sum over a chosen rectangular area of a given matrix.
    """
    
    def sum_over_matrix(self, matrix):
        """
        First sums the horizontal and then the vertical rows of the matrix.
        
        Keyword arguments
        matrix    - - matrix to be summed over, type numpy.ndarray.  
        """
        sizex = 0
        sizey = 0
        try:
            sizex = matrix.shape[0]
            sizey = matrix.shape[1]
        except Exception:
            print "Matrix has to be 2-dimensional."
        self.integral_image = numpy.zeros((sizex, sizey))
        sum = 0
        """
        Block sums the horizontal rows of the matrix and adds the sums into
        the matrix.
        The resulting matrix is the same size as the original.
        """
        for i in range(sizex):
            for j in range(sizey):
                sum += matrix[i][j]
                self.integral_image[i][j] = sum
            sum = 0
        """
        Block sums the vertical rows of the matrix that was generated in the
        previous block.
        The resulting matrix is the same size as the original. 
        """
        for j in range(sizey):
            for i in range(sizex):
                sum += self.integral_image[i][j]
                self.integral_image[i][j] = sum
            sum = 0
        
    def sum_over_rectangular_area(self, top_left_corner, bottom_right_corner, matrix):
        """
        top_left_corner and bottom_right_corner are type tuple.
        Formula I(C)+I(A)-I(B)-I(D) is used to count the sum of the
        rectangular area.
        A is the top-left corner of the rectangle.
        B is the top-right corner of the rectangle.
        C is the bottom-right corner of the rectangle.
        D is the bottom-left corner of the rectangle.
                
        Keyword arguments:
        top_left_corner     - - top-left corner of the rectangle
        bottom_right_corner - - bottom-right corner of the rectangle
        matrix              - - matrix of type numpy.ndarray
        """
        """
        Blocks make sure that bottom-right corner of the rectangle isn't
        choosen out of bounds.
        """
        
        self.sum_over_matrix(matrix)
        
        if (bottom_right_corner[0] >= self.integral_image.shape[1]):
            return 'Rectangle out of bounds'
        if (bottom_right_corner[1] >= self.integral_image.shape[0]):
            return 'Rectangle out of bounds'
        A = self.integral_image[top_left_corner[1]-1][top_left_corner[0]-1]
        B = self.integral_image[top_left_corner[1]-1][bottom_right_corner[0]]
        C = self.integral_image[bottom_right_corner[1]][bottom_right_corner[0]]
        D = self.integral_image[bottom_right_corner[1]][top_left_corner[0]-1]
        rectangle_area_sum = 0
        """
        In case of the rectangle touching the left and top edge of the area.
        """
        if (top_left_corner[0] == 0 and top_left_corner[1] == 0):
            rectangle_area_sum = C
            return rectangle_area_sum
        """
        In case of the rectangle touching the left edge of the area.
        Block makes sure that x index isn't out of bounds when reducing the
        index by 1.
        """
        if (top_left_corner[0] == 0):
            rectangle_area_sum =  C - B
            return rectangle_area_sum
        """
        In case of the rectangle touching the top edge of the area.
        Block makes sure that y index isn't out of bounds when reducing the
        index by 1.
        """
        if (top_left_corner[1] == 0):
            rectangle_area_sum =  C - D
            return rectangle_area_sum
        rectangle_area_sum =  C + A - B - D
        return rectangle_area_sum
        