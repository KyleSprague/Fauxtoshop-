'''
    This program contains functions to manipulate images.
    It contains the following methods in the class netpbm: __init__, readHeader, readPGMPixels,
    ReadPPMPixels, isPGM, getMagicNumber, getNumCols, getComment, getNumRows, getMaxLevel, getHeader,
    getPixels, writeImage, writeHeader, writePixels, changeBrightness, invert, rotate, flip, posterize,
    crop, toGrayscale, and glass. Details of each are provided in
    function comments below.

    Authors: Kyle Sprague (ksprague@bates.edu)

    Date Written: December 13 2021
'''

import random
import copy

#hello
class Netpbm:

    __slots__ = ('_header', '_pixels')


    def __init__(self, filename: str):

        '''
        Method that initializes an object of the Netpbm class along with the isntance variables
        used throughout the program.
        Args:
            self: argument used for all methods within a given class
            filename: str -- The filename of the image to be operated on using an object of
            the Netpbm class.
        Returns:
            Nothing. This method is nonfruitful.
        '''

        file_handle = open(filename,"r")
        self._header = self.readHeader(file_handle)
        if self._header[0] == "P2":
            self._pixels = self.readPGMPixels(file_handle)
        else: #if magic number is p2, pgm header; if its its p3, we use ppm header
            self._pixels = self.readPPMPixels(file_handle)
        file_handle.close()



    def readHeader(self, image_file: 'TextIO') -> list: #image file is the file handle here

        '''
        Method that reads the header information (lines 1-4) of a given PGM or PPM file using the file
        handle, then returns this information as part of a header list.
        Args:
            self: argument used for all methods within a given class
            image_file: 'TextIO' -- The filehandle for the given file that can be used for reading.
        Returns:
            A list called header contianing the header information for a file, including the magic number, a comment,
            the number of columns and rows, and the maximum level.
        '''

        #As a reminder: PGM files contain the following
            #line 1: P2: the magic magic_number (part of header info)
            #Line 2: Comment beginning with # (part of header info)
            #Line 3: Number of columns then rows (part of header info)
            #Line 4 Maximum gray level (part of header info)
            #Remainder of file: pixel payload with integer between 0 and max level (both inclusive)

            #Also: a note on filename vs. file handle. Above we are using the file handle, which
            #can be used in functions like readline and close, while the filename can not
            #In this situation, passing in the file handle enables us to track our work in the file.
            #readheader for a pgm file

        magic_number = image_file.readline().strip()
        comment = image_file.readline().strip()
        cols_rows = image_file.readline().strip()
        cols_rows_list = cols_rows.split()

        for i in range(len(cols_rows_list)):
            cols_rows_list[i] = int(cols_rows_list[i])

        max_level = int(image_file.readline().strip())
        header = [magic_number, comment, cols_rows_list, max_level]
        return header

    def readPGMPixels(self, image_file: 'TextIO') -> list:
        '''
        Method that reads the pixels information from a given PGM file using the file
        handle, then returns this information as part of a pixel list.
        Args:
            self: argument used for all methods within a given class
            image_file: 'TextIO' -- The filehandle for the given file that can be used for reading.
        Returns:
            A 1d list of integers called pixel_list containing the value of each pixel that comprises the image,
        '''
        line = image_file.readline() #read pixels for a pgm file
        pixel_list = []
        while line != '':
            line_list = line.strip().split()
            for i in range(len(line_list)):
                pixel_list.append(int(line_list[i]))
            line = image_file.readline()
        return pixel_list


    def readPPMPixels(self, image_file: 'TextIO') -> list:
        '''
        Method that reads the pixels information from a given PPM file using the file
        handle, then returns this information as part of a pixel list.
        Args:
            self: argument used for all methods within a given class
            image_file: 'TextIO' -- The filehandle for the given file that can be used for reading.
        Returns:
            A 3 element list of integers called pixel_list containing a list of red pixels,
            a list of green pixels, and a list of blue pixels.
        '''
        all_values_list = (image_file.read().strip().split())
        red_list = []
        green_list = []
        blue_list = []

        for i in range(0, len(all_values_list),3):
            red_list.append(int(all_values_list[i]))
        for i in range(1, len(all_values_list),3):
            green_list.append(int(all_values_list[i]))
        for i in range(2, len(all_values_list), 3):
            blue_list.append(int(all_values_list[i]))
        return [red_list,green_list,blue_list]


    def isPGM(self) -> bool:
        '''
        Method that determines the status of the file, whether PPM or PGM
        Args:
            self: argument used for all methods within a given class
        Returns:
            A boolean expression (True or False) indicating whether or not the magic number
            for the give file is P2 or P3
        '''
        magicNumber = self.getMagicNumber()
        if magicNumber == "P2":
            return True
        else:
            return False

    def getMagicNumber(self) -> str:
        '''
        Method that gets the magic number.
        Args:
            self: argument used for all methods within a given class
        Returns:
            The magic number at self._header[0] as a string
        '''
        return self._header[0]

    def getComment(self) -> str:
        '''
        Method that gets comment from the header.
        Args:
            self: argument used for all methods within a given class
        Returns:
            The comment at self._header[1] as a string
        '''
        return self._header[1]

    def getNumCols(self) -> int:
        '''
        Method that gets the number of columns from the header
        Args:
            self: argument used for all methods within a given class
        Returns:
            The number of columns at self._header[2][0] as an integer
        '''
        return self._header[2][0]

    def getNumRows(self) -> int:
        '''
        Method that gets the number of rows from the header
        Args:
            self: argument used for all methods within a given class
        Returns:
            The number of rows at self._header[2][1] as an integer
            '''
        return self._header[2][1]

    def getMaxLevel(self) -> int:
        return self._header[3]
        '''
        Method that gets the maximum pixel level for the image.
        Args:
            self: argument used for all methods within a given class
        Returns:
            The maximum pixel level at self._header[3] as an integer
        '''

    def getHeader(self) -> list:
        '''
        Method that returns the header for an image
        Args:
            self: argument used for all methods within a given class
        Returns:
            a copy of the header information from an image as a list
        '''
        return copy.deepcopy(self._header)

    def getPixels(self) -> list:
        '''
        Method that returns the pixels for an image
        Args:
            self: argument used for all methods within a given class
        Returns:
            a copy of the pixel information for either a PGM or PPM file as a list
        '''
        return copy.deepcopy(self._pixels)


    def writeImage(self, filename: str) -> None:
        '''
        Method that writes out the pixel and header content of a Netpbm object
        to another file.
        Args:
            self: argument used for all methods within a given class
            filename: str --the name of the file as a string
        Returns:
            Nothing. This method is nonfruitful
        '''
        output_file = open(filename, "w")
        self.writeHeader(output_file)
        self.writePixels(output_file)
        output_file.close()

    def writeHeader(self, image_file: 'TextIO') -> None:
        '''
        Method that writes out the header information using the
        filehandle from the fiven image and that is used by the
        writeImage method.
        Args:
            self: argument used for all methods within a given class
            image_file: TextIO -- the filehandle for a given file
        Returns:
            Nothing. This method is nonfruitful
        '''
        image_file.write((str(self._header[0])) + "\n")
        image_file.write((str(self._header[1])) + "\n")
        num_cols = (str(self._header[2][0]) + " ")
        num_rows = (str(self._header[2][1]) + "\n")
        image_file.write(str(num_cols))
        image_file.write(str(num_rows))
        image_file.write((str(self._header[3])) + "\n")

    def writePixels(self, image_file: 'TextIO') -> None:
        '''
        Method that writes out the pixel information using the
        filehandle from the fiven image and that is used by the
        writeImage method. The operation is altered for a 3-element
        list PPM file vs. a 1D list PGM file using an if statement.
        Args:
            self: argument used for all methods within a given class
            image_file: TextIO -- the filehandle for a given file
        Returns:
            Nothing. This method is nonfruitful
        '''
        if self.isPGM() == True:
            num_cols = self.getNumCols()
            num_rows = self.getNumRows()
            for i in range((num_cols) * (num_rows)):
                image_file.write((str(self._pixels[i])) + "\n")
        else:
            num_cols = self.getNumCols()
            num_rows = self.getNumRows()
            for i in range(num_cols*num_rows):
                for j in range(num_rows):
                    image_file.write((str(self._pixels[j][i])) + "\n")

    #new after working previous methods (up to B level specifications)


    def changeBrightness(self, amount: int) -> None:
        '''
        Method that changes the brightness of an image by modifying
        information containined in the self._pixels instance variable. The
        approach varies depending on whether Fauxtoshop is operating on a PGM
        file or PPM file and this change is illustrated via the use of an if
        else statement which relates a specific set of steps to a specific
        magic number.
        Args:
            self: argument used for all methods within a given class
            amount: int -- the integer value by which the brightness is to be altered
        Returns:
            Nothing. This method is nonfruitful
        '''
        max_level = self.getMaxLevel()
        if self.getMagicNumber() == "P2":
            for i in range (len(self._pixels)):
                max_value = self._pixels[i] + amount
                if max_value < 0:
                    max_value  = 0
                    self._pixels[i] = max_value
                if max_value > max_level:
                    self._pixels[i] = max_level
                else:
                    self._pixels[i] = max_value
        else:
            num_rows = self.getNumRows()
            num_cols = self.getNumCols()
            reds = self._pixels[0]
            greens = self._pixels[1]
            blues = self._pixels[2]

            for r in range(num_rows):
                for c in range(num_cols):
                    index = ((num_cols * r) + c)

                    reds[index] = reds[index] + amount
                    if (reds[index] + amount) < 0:
                        reds[index] = 0
                        self._pixels[0][index] = reds[index]
                    if (reds[index] + amount) > max_level:
                        reds[index] = max_level
                        self._pixels[0][index] = reds[index]
                    else:
                        self._pixels[0][index] = reds[index]

                    greens[index] = greens[index] + amount
                    if (greens[index] + amount) < 0:
                        greens[index] = 0
                        self._pixels[1][index] = greens[index]
                    if (greens[index] + amount) > max_level:
                        greens[index] = max_level
                        self._pixels[1][index] = greens[index]
                    else:
                        self._pixels[1][index] = greens[index]

                    blues[index] = blues[index] + amount
                    if (blues[index] + amount) < 0:
                        blues[index] = 0
                        self._pixels[2][index] = blues[index]
                    if (blues[index] + amount) > max_level:
                        blues[index] = max_level
                        self._pixels[2][index] = blues[index]
                    else:
                        self._pixels[2][index] = blues[index]


    def invert(self) -> None:
        '''
        Method that inverts an image by taking the maximum value for a given pixel
        and subtracting from that the actual value to get the inverse value. The
        approach varies depending on whether Fauxtoshop is operating on a PGM
        file or PPM file and this change is illustrated via the use of an if
        else statement which relates a specific set of steps to a specific
        magic number.
        Args:
            self: argument used for all methods within a given class

        Returns:
            Nothing. This method is nonfruitful
        '''
        magic_number = self.getMagicNumber()
        if magic_number == "P2":
            for i in range(len(self._pixels)):
                originalPixelValue = int(self._pixels[i])
                self._pixels[i] = 255 - originalPixelValue

        if magic_number == "P3":
            reds = self._pixels[0]
            blues = self._pixels[1]
            greens = self._pixels[2]
            num_cols = self.getNumCols()
            num_rows = self.getNumRows()

            for r in range (num_rows):
                for c in range (num_cols):
                     index = ((num_cols * r) + c)

                     original_value_reds = reds[index]
                     self._pixels[0][index] = 255 - original_value_reds

                     original_value_greens = greens[index]
                     self._pixels[1][index] = 255 - original_value_greens

                     original_value_blues = blues[index]
                     self._pixels[2][index] = 255 - original_value_blues

    def rotate(self, rotate_right: bool = True) -> None:
        '''
        Method that rotates the image to the right by 90 degrees or to the left by 90 degrees
        depending on the booleann given. It does this by stepping through
        the columns and rows in a specific manner, appending the pixels in
        that speciifc manner, then altering the number of rows and columns appropriately. The
        approach varies depending on whether Fauxtoshop is operating on a PGM
        file or PPM file and this change is illustrated via the use of an if
        else statement which relates a specific set of steps to a specific
        magic number.
        Args:
            self: argument used for all methods within a given class
            rotate_right: bool -- A boolean indicating whether the method is to perform
            rotate right or rotate left.
        Returns:
            Nothing. This method is nonfruitful
        '''
        if self._header[0] == "P2":
            num_cols = self.getNumCols()
            num_rows = self.getNumRows()
            pixel_list = []
            if rotate_right == True: #WORKING
                for c in range (0, num_cols, 1):
                    for r in range (num_rows-1, -1, -1):
                        index = ((num_cols*r)+c)
                        pixel_list.append(self._pixels[index])
                self._pixels = pixel_list
                change_variable = num_cols
                num_cols = num_rows
                num_rows = change_variable
                self._header[2][0] = num_cols
                self._header[2][1] = num_rows
            else:
                for c in range (num_cols-1, -1, -1):
                    for r in range (0, num_rows, 1):
                        index = ((num_cols*r)+c)
                        pixel_list.append(self._pixels[index])
                self._pixels = pixel_list
                change_variable = num_cols
                num_cols = num_rows
                num_rows = change_variable
                self._header[2][0] = num_cols
                self._header[2][1] = num_rows

        if self._header[0] == "P3":
            reds = self._pixels[0]
            greens = self._pixels[1]
            blues = self._pixels[2]
            reds_list = []
            blues_list = []
            greens_list = []
            num_cols = self.getNumCols()
            num_rows = self.getNumRows()
            pixel_list = [reds_list, greens_list, blues_list]
            if rotate_right == True: #WORKING
                for c in range (0, num_cols, 1):
                    for r in range (num_rows-1, -1, -1):
                        index = ((num_cols*r)+c)
                        reds_list.append(self._pixels[0][index])
                        greens_list.append(self._pixels[1][index])
                        blues_list.append(self._pixels[2][index])
                self._pixels = pixel_list
                change_variable = num_cols
                num_cols = num_rows
                num_rows = change_variable
                self._header[2][0] = num_cols
                self._header[2][1] = num_rows
            else:
                for c in range (num_cols-1, -1, -1):
                    for r in range (0, num_rows, 1):
                        index = ((num_cols*r)+c)
                        reds_list.append(self._pixels[0][index])
                        greens_list.append(self._pixels[1][index])
                        blues_list.append(self._pixels[2][index])
                self._pixels = pixel_list
                change_variable = num_cols
                num_cols = num_rows
                num_rows = change_variable
                self._header[2][0] = num_cols
                self._header[2][1] = num_rows

    def flip(self, vertical: bool = True) -> None:
        '''
        Method that flips the image horizontally or vertically depending on the boolean given
        depending on the booleann given. It does this by stepping through
        the columns and rows in a specific manner, then appending the pixels in
        that speciifc manner. The approach varies depending on whether Fauxtoshop is operating on a PGM
        file or PPM file and this change is illustrated via the use of an if
        else statement which relates a specific set of steps to a specific
        magic number.
        Args:
            self: argument used for all methods within a given class
            vertical: bool -- a boolean term indicating whether the image should be
            flipped horizontally or vertically
        Returns:
            Nothing. This method is nonfruitful
        '''
        if self.isPGM() == True:
            num_cols = self.getNumCols()
            num_rows = self.getNumRows()
            pixel_list = []
            if vertical == True:
                for r in range(num_rows-1, -1, -1):
                    for c in range (0, num_cols, 1):
                        index = ((num_cols*r)+c)
                        pixel_list.append(self._pixels[index])
                self._pixels = pixel_list
            else:
                for r in range(0, num_rows, 1):
                    for c in range (num_cols - 1, -1, -1):
                        index = ((num_cols*r)+c)
                        pixel_list.append(self._pixels[index])
                self._pixels = pixel_list

        if self.isPGM() == False:
            reds = self._pixels[0]
            greens = self._pixels[1]
            blues = self._pixels[2]
            reds_list = []
            blues_list = []
            greens_list = []
            pixel_list = [reds_list, greens_list, blues_list]
            num_cols = self.getNumCols()
            num_rows = self.getNumRows()
            if vertical == True:
                for r in range (num_rows-1, -1, -1):
                    for c in range(0, num_cols, 1):
                        index = ((num_cols*r)+c)
                        reds_list.append(self._pixels[0][index])
                        greens_list.append(self._pixels[1][index])
                        blues_list.append(self._pixels[2][index])
                self._pixels = pixel_list
            else:
                for r in range (0, num_rows, 1):
                    for c in range(num_cols-1, -1, -1):
                        index = ((num_cols*r)+c)
                        reds_list.append(self._pixels[0][index])
                        greens_list.append(self._pixels[1][index])
                        blues_list.append(self._pixels[2][index])
                self._pixels = pixel_list



#for posterize, everything between 0 and the half goes into the half; everything from half to the one goes into the 1
#first chunki into 1, second into 2, third into 3, fourth into 4 (256/2)
#separate colors
#divide value by bin widths to get new value of pixel

    def posterize(self, num_levels: int) -> None:
        '''
        Method that reduces the value of each pixel for a given image. It does this by stepping through
        the given list of pixels and placing them in bins depending on the level of coloration a user in
        photoshop desires. Each bin corresponds to specific levels that the pixel can take on. A range
        of pixels with values that range widely are assorted into specific bins to reduce the number of values
        that they can take on. The approach varies depending on whether Fauxtoshop is operating on a PGM
        file or PPM file and this change is illustrated via the use of an if
        else statement which relates a specific set of steps to a specific
        magic number.
        Args:
            self: argument used for all methods within a given class
            num_leves: int -- an integer term indicating the number of levels the user wants
            the pixels in the image to be able to take on
        Returns:
            Nothing. This method is nonfruitful
        '''
        max_level = self.getMaxLevel()
        bin_width = (max_level + 1) / num_levels
        if self.isPGM() == True:
            for i in range (len(self._pixels)):
                binned = int(self._pixels[i] / bin_width)
                self._pixels[i] = binned
        else:
            reds = self._pixels[0]
            greens = self._pixels[1]
            blues = self._pixels[2]
            reds_list = []
            blues_list = []
            greens_list = []
            pixel_list = [reds_list, greens_list, blues_list]
            num_rows = self.getNumRows()
            num_cols = self.getNumCols()
            for r in range(num_rows):
                for c in range(num_cols):
                    index = ((num_cols * r) + c)
                    red_binned = int((self._pixels[0][index]) / bin_width)
                    blue_binned = int((self._pixels[1][index]) / bin_width)
                    green_binned = int((self._pixels[2][index]) / bin_width)
                    self._pixels[0][index] = red_binned
                    self._pixels[1][index] = blue_binned
                    self._pixels[2][index] = green_binned
        self._header[3] = (num_levels)

    def crop(self, upper_left_row: int, upper_left_column: int, \
    lower_right_row: int, lower_right_column: int) -> None:
        '''
        Method that crops the image by looping through the desired area and
        appending pixels to the self._pixels instance variable appropriately,
        then adjsuts the number of colums and rows accordingly so that the pixel
        number for the resulting image matches the number looped through.
        The approach varies depending on whether Fauxtoshop is operating on a PGM
        file or PPM file and this change is illustrated via the use of an if
        else statement which relates a specific set of steps to a specific
        magic number.
        Args:
            self: argument used for all methods within a given class
            upper_left_row: int -- the integer row position of where the crop starts
            upper_left_column: int -- the integer column position of where the crop starts
            lower_right_row: int -- the integer row positon of where the crop ends
            lower_right_column: int -- the integer column position of where the crop ends
        Returns:
            Nothing. This method is nonfruitful
        '''
        num_cols = self.getNumCols()
        num_rows = self.getNumRows()
        if self.isPGM() == True:
            pixel_list = []
            num_rows_final = (lower_right_row - upper_left_row)
            num_cols_final = (lower_right_column - upper_left_column)
            for r in range(upper_left_row, lower_right_row, 1):
                for c in range(upper_left_column, lower_right_column, 1):
                    index = ((num_cols * r) + c)
                    pixel_list.append(self._pixels[index])
            self._header[2][0] = num_cols_final
            self._header[2][1] = num_rows_final
            self._pixels = pixel_list
        else:
            reds = []
            blues = []
            greens = []
            num_rows_final = (lower_right_row - upper_left_row)
            num_cols_final = (lower_right_column - upper_left_column)
            for r in range(upper_left_row, lower_right_row, 1):
                for c in range(upper_left_column, lower_right_column, 1):
                    index = ((num_cols * r) + c)
                    reds.append(self._pixels[0][index])
                    blues.append(self._pixels[1][index])
                    greens.append(self._pixels[2][index])
            pixel_list = [reds,greens,blues]
            self._header[2][0] = num_cols_final
            self._header[2][1] = num_rows_final
            self._pixels = pixel_list

    def toGrayscale(self) -> None:
        '''
        Method that loops through a PPM image, altering each red, green, or blue
        pixel and changing it to a gray pixel, then appends the result to
        a 1D list to create a PGM by adjusting the magic number.
        Args:
            self: argument used for all methods within a given class
        Returns:
            Nothing. This method is nonfruitful
        '''
        num_cols = self.getNumCols()
        num_rows = self.getNumRows()
        reds = self._pixels[0]
        greens = self._pixels[1]
        blues = self._pixels[2]
        pixel_list = []
        for r in range(num_rows):
            for c in range(num_cols):
                index = ((num_cols * r) + c)
                gray_scale_pixel_at_index = int((0.2126*reds[index]) + (0.7152*blues[index]) + (0.0722*greens[index]))
                pixel_list.append(gray_scale_pixel_at_index)
        self._pixels = pixel_list
        self._header[0] = "P2"

    def glass (self, radius: int) -> None:
        '''
        Method that loops through a PPM image, altering each red, green, or blue
        pixels such that they become the values of the pixels in their immediate radius,
        thereby creating a washing out effect.
        Args:
            radius: an integer corresponding to the value by which the original pixel
        Returns:
            Nothing. This method is nonfruitful
        '''
        red_list = []
        blue_list = []
        green_list = []
        num_rows = self.getNumRows()
        num_cols = self.getNumCols()
        for r in range(num_rows):
            for c in range(num_cols):
                off_set_one = random.randint(-radius, radius)
                off_set_two = random.randint(-radius, radius)
                if off_set_one or off_set_two > num_rows:
                    r_and_off_set = (((r + off_set_one) + num_rows) % num_rows)
                    red_list.append(self._pixels[0][r_and_off_set])
                    green_list.append(self._pixels[1][r_and_off_set])
                    blue_list.append(self._pixels[2][r_and_off_set])
                if off_set_one or off_set_two > num_cols:
                    c_and_off_set = (((c + off_set_two) + num_cols) % num_cols)
                    red_list.append(self._pixels[0][c_and_off_set])
                    green_list.append(self._pixels[1][c_and_off_set])
                    blue_list.append(self._pixels[2][c_and_off_set])
                else:
                    red_list.append(self._pixels[0][([r] + off_set_one, [c] + off_set_two)])
                    green_list.append(self._pixels[1][([r] + off_set_one, [c] + off_set_two)])
                    blue_list.append(self._pixels[2][([r] + off_set_one, [c] + off_set_two)])
        pixel_list = [red_list, green_list, blue_list]
        self._pixels = pixel_list


def main():

        #Tests to see if brightness is working on 4x4 4x5 and 5x4 grayscale images

        image = Netpbm("images/pgm/sample4x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.changeBrightness(5)
        image.writeImage("images/pgm/sample_bright1.pgm")
        print("-"*100) #for the terminal!

        image = Netpbm("images/pgm/sample4x5.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.changeBrightness(5)
        image.writeImage("images/pgm/sample_bright2.pgm")
        print("-"*100) #for the terminal!

        image = Netpbm("images/pgm/sample5x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.changeBrightness(5)
        image.writeImage("images/pgm/sample_bright3.pgm")
        print("="*100) #for the terminal!

        #Tests to see if invert is working on 4x4 4x5 and 5x4 grayscale images

        image = Netpbm("images/pgm/sample4x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.invert()
        image.writeImage("images/pgm/sample_invert1.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample4x5.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.invert()
        image.writeImage("images/pgm/sample_invert2.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample5x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.invert()
        image.writeImage("images/pgm/sample_invert3.pgm")
        print("="*100)

        #Tests to see if rotate is working on 4x4 4x5 and 5x4 grayscale images

        image = Netpbm("images/pgm/sample4x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.rotate(True)
        image.writeImage("images/pgm/sample_rotate1.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample4x5.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.rotate(False)
        image.writeImage("images/pgm/sample_rotate2.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample5x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.rotate(True)
        image.writeImage("images/pgm/sample_rotate3.pgm")
        print("="*100)

        #Tests to see if flip is working on 4x4 4x5 and 5x4 grayscale images

        image = Netpbm("images/pgm/sample4x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.flip(True)
        image.writeImage("images/pgm/sample_flip1.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample4x5.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.flip(True)
        image.writeImage("images/pgm/sample_flip2.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample5x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.flip(False)
        image.writeImage("images/pgm/sample_flip3.pgm")
        print("="*100)

        #Tests to see if posterize is working on 4x4 4x5 and 5x4 grayscale images

        image = Netpbm("images/pgm/sample4x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.posterize(2)
        image.writeImage("images/pgm/sample_posterize1.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample4x5.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.posterize(2)
        image.writeImage("images/pgm/sample_posterize2.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample5x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.posterize(2)
        image.writeImage("images/pgm/sample_posterize3.pgm")
        print("="*100)

        #Tests to see if crop is working on 4x4 4x5 and 5x4 grayscale images

        image = Netpbm("images/pgm/sample4x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.crop(0,0,3,3)
        image.writeImage("images/pgm/sample_crop1.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample4x5.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.crop(0,0,2,2)
        image.writeImage("images/pgm/sample_crop2.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample5x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.crop(0,0,1,1)
        image.writeImage("images/pgm/sample_crop3.pgm")
        print("="*100)

        #Tests to see if toGrayscale is working on 4x4 4x5 and 5x4 grayscale images
        '''
        image = Netpbm("images/pgm/sample4x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.toGrayscale()
        image.writeImage("images/pgm/sample_crop.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample4x5.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.toGrayscale()
        image.writeImage("images/pgm/sample_crop.pgm")
        print("-"*100)

        image = Netpbm("images/pgm/sample5x4.pgm")
        print(f"Magic #: {image.getMagicNumber()}")
        print(f"Dimensions: {image.getNumRows()} X {image.getNumCols()}")
        print(f"Header: {image.getHeader()}")
        print(f"Pixels: {image.getPixels()}")
        image.toGrayscale()
        image.writeImage("images/pgm/sample_crop.pgm")
        print("="*100)
        '''
        #Tests to see if toGrayscale is working on 4x4 4x5 and 5x4 grayscale images

if __name__ == "__main__": # won’t call Netpbm’s main when running Fauxtoshop

    main()



#our given object for the above functions is given by the photoshop program; the methods
# are then able to use that opject to get specific data.
