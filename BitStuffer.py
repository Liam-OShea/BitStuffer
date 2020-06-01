# File: BitStuffer.py
# Author: Liam O'Shea B00613041
# Description: This program reads text input from a file, converts to binary ascii representation and creates
# a stuffed binary string. The binary string is then unstuffed and converted back to text. The text is saved to
# a file.

def getBinary(inputString):
    binary = []
    for char in inputString:
        # Get binary form of ascii, returns String with value
        char = bin(ord(char))
        # Remove 0b
        char = char[2:]
        # Make each character 8 bits (some are 7)
        while len(char) != 8:
            char = "0" + char
        binary.append(char)
    return binary


def stringFromList(inputList):
    string = ""
    string = string.join(inputList)
    return string


def bitStuffer(inputString):
    stuffedBinaryString = ""
    oneCount = 0

    for digit in inputString:
        stuffedBinaryString += digit
        if int(digit) == 1:
            oneCount += 1
        else:
            oneCount = 0
        if oneCount == 5:
            stuffedBinaryString += "0"
            oneCount = 0

    # Append flags
    stuffedBinaryString = "01111110" + stuffedBinaryString + "01111110"
    return stuffedBinaryString


def deStuffer(inputString):
    # Remove 8 bit flags
    inputString = inputString[8:len(inputString) - 8]

    destuffedBinaryString = ""
    oneCount = 0
    i = 0
    while i < len(inputString):

        if int(inputString[i]) == 1:
            oneCount += 1
        elif oneCount == 5:
            i += 1
        else:
            oneCount = 0

        destuffedBinaryString += inputString[i]
        if oneCount == 5:
            i += 1
            oneCount = 0
        i += 1
    return destuffedBinaryString


def getMessage(inputString):
    ascii_ = []
    letters = []
    msg = ""
    # Convert to list of bytes
    while inputString:
        ascii_.append(inputString[:8])
        inputString = inputString[8:]
    for char in ascii_:
        letters.append(chr(int(char, 2)))
    return msg.join(letters)


# This function reads a text file, converts it to binary, and stuffs the binary stream.
def getBitStream(file):
    lines = file.readlines()
    message = ""
    message = message.join(lines)
    binary = getBinary(message)
    binaryString = stringFromList(binary)
    stuffedString = bitStuffer(binaryString)
    return stuffedString


# This function takes a bitstream and converts it back to text.
def stuffedBitstreamToText(bitstream):
    destuffedString = deStuffer(bitstream)
    reconverted = getMessage(destuffedString)
    return reconverted


file = open("text.txt", "r")

bitstream = getBitStream(file)
text = stuffedBitstreamToText(bitstream)
print("Stuffed Bitstream: ", bitstream)

# Write stuffed bitstream to file
bs = open("StuffedBitstream.txt", "w+")
bs.write(bitstream)
bs.close()

print("\nBitstream converted back to text:\n-----------------------------\n", text)
# Write reconverted message to file
reconvertedText = open("ReconvertedToText.txt", "w+")
reconvertedText.write(text)
reconvertedText.close()

print("\nOther bit stuffing examples:")
tests = ["1011111011111111100", "11111", "111001101101111110"]
for test in tests:
    print("Unstuffed:\t", test)
    print("Stuffed:\t", bitStuffer(test))
    print("Destuffed:\t", deStuffer(bitStuffer(test)))
