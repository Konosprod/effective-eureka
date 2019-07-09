import sys
import argparse
import os

def Extract(infile, outputdir):
    filein = open(infile, "rb")

    if not outputdir.endswith("/"):
        outputdir += "/"

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    filein.seek(0x04, 0)
    
    starting_offset = int.from_bytes(filein.read(0x04), "little")
    header_size = int.from_bytes(filein.read(0x04), "little")
    starting_table = 0x111
    entry_size = 0x28

    file_number = int(header_size / entry_size)

    print("Starting at : 0x{:08X}".format(starting_offset))
    print("Header size : 0x{:08X}".format(header_size))
    print(str(file_number) + " files")
    print("----------------------------------------")
    sys.stdout.flush()
    filein.seek(starting_table, 0)

    for i in range(0, file_number):
        filename = filein.read(0x20)
        file_offset = int.from_bytes(filein.read(0x04), "little") + starting_offset
        file_size = int.from_bytes(filein.read(0x04), "little")
        print("".join( chr(x) for x in bytearray(filename)))
        print("Offset : 0x{:08X}".format(file_offset))
        print("Size : 0x{:08X}".format(file_size))
        print("----------------------------")

        fileout = open(outputdir + "".join( chr(x) for x in bytearray(filename)).rstrip('\0'), "wb")
        pos = filein.tell()
        filein.seek(file_offset, 0)

        while file_size > 0:
            if file_size >= 1024:
                data = filein.read(1024)
            else:
                data = filein.read(file_size)

            fileout.write(data)
            file_size -= (1024 if (file_size >= 1024) else file_size)

        fileout.close()

        filein.seek(pos, 0)

        sys.stdout.flush()


    filein.close()

    return
    
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-x", "--extract", help="Extract AOS", action="store_true")
parser.add_argument("input", help="Input file in case of -x or input directory in case of -c")
parser.add_argument("output", help="Output directory in case of -x or output file in case of -c")

args = parser.parse_args()

if args.extract:
    Extract(args.input, args.output)

