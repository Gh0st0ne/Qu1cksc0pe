#!/usr/bin/env python3

# module checking
try:
    import os,sys,argparse,getpass
except:
    print("Missing modules detected!")
    sys.exit(1)
try:
    import puremagic as pr
except:
    print("Error: >puremagic< module not found.")
    sys.exit(1)

# Colors
red = '\u001b[91m'
cyan = '\u001b[96m'
white = '\u001b[0m'
green = '\u001b[92m'
yellow = '\u001b[93m'

# handling arguments
args = []

def scope():
    # Argument crating and parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",required=False,help="Select a suspicious file.")
    parser.add_argument("--windows",required=False,help="Analyze Windows files.",action="store_true")
    parser.add_argument("--linux",required=False,help="Analyze Linux files.",action="store_true")
    parser.add_argument("--vtFile",required=False,help="Scan your file with VirusTotal api.",action="store_true")
    parser.add_argument("--vtUrl",required=False,help="Scan your URL with VirusTotal api.",action="store_true")
    parser.add_argument("--metadata",required=False,help="Get exif/metadata information.",action="store_true")
    parser.add_argument("--url",required=False,help="Extract URLs from file.",action="store_true")
    parser.add_argument("--packer",required=False,help="Check if your file is packed with common packers.",action="store_true")
    parser.add_argument("--key_init",required=False,help="Enter your VirusTotal api key.",action="store_true")
    args = parser.parse_args()

    # Getting all strings from the file
    if args.file:
        command = "strings -a {} > temp.txt".format(args.file)
        os.system(command)
            
    # windows scan
    if args.windows:
        fileType = str(pr.magic_file(args.file))
        if "Windows" in fileType:
            command = "python3 winAnalyzer.py {}".format(args.file)
            os.system(command)
        else:
            print("{}[{}!{}]{} Please enter Windows files.".format(cyan,red,cyan,white))
            sys.exit(1)
        
    # linux scan
    if args.linux:
        fileType = str(pr.magic_file(args.file))
        if "ELF" in fileType:
            command = "readelf -a {} > elves.txt".format(args.file)
            os.system(command)
            command = "python3 elfAnalyzer.py {}".format(args.file)
            os.system(command)
        else:
            print("{}[{}!{}]{} Please enter ELF executable files.".format(cyan,red,cyan,white))
            sys.exit(1)
        
    # metadata
    if args.metadata:
        print("{}[{}+{}]{} Exif/Metadata information".format(cyan,red,cyan,white))
        command = "exiftool {}".format(args.file)
        print("+","-"*50,"+")
        os.system(command)
        print("+","-"*50,"+")

    # VT File scanner
    if args.vtFile:

        # if there is no key quit
        try:
            user = getpass.getuser()
            directory = "/home/{}/.apikey.txt".format(user)
            apik = open(directory, "r").read().split("\n")
        except:
            print("{}[{}!{}]{} Use --key_init to enter your key.".format(cyan,red,cyan,white))
            sys.exit(1)

        # if key is not valid quit
        if apik[0] == '' or apik[0] == None or len(apik[0]) != 64:
            print("{}[{}!{}]{} Please get your API key from -> {}https://www.virustotal.com/{}".format(cyan,red,cyan,white,green,white))
            sys.exit(1)
        else: 
            print("\n{}[{}+{}]{} VirusTotal Scan".format(cyan,red,cyan,white))
            print("+","-"*50,"+")
            command = "python3 VTwrapper.py {} --vtFile {}".format(apik[0],args.file)
            os.system(command)
            print("+","-"*50,"+")

    # VT URL scanner
    if args.vtUrl:

        # if there is no key quit
        try:
            user = getpass.getuser()
            directory = "/home/{}/.apikey.txt".format(user)
            apik = open(directory, "r").read().split("\n")
        except:
            print("{}[{}!{}]{} Use --key_init to enter your key.".format(cyan,red,cyan,white))
            sys.exit(1)

        # if key is not valid quit
        if apik[0] == '' or apik[0] == None or len(apik[0]) != 64:
            print("{}[{}!{}]{} Please get your API key from -> {}https://www.virustotal.com/{}".format(cyan,red,cyan,white,green,white))
            sys.exit(1)
        else:
            print("\n{}[{}+{}]{} VirusTotal Scan".format(cyan,red,cyan,white))
            print("+","-"*50,"+")
            command = "python3 VTwrapper.py {} --vtUrl".format(apik[0])
            os.system(command)
            print("+","-"*50,"+")

    # packer detection
    if args.packer:
        command = "python3 packerAnalyzer.py {}".format(args.file)
        os.system(command)
        
    # url extraction
    if args.url:
        command = "bash urlCatcher.sh {}".format(args.file)
        os.system(command)

    # entering VT API key
    if args.key_init:
        apikey = str(input("{}[{}+{}]{} Enter your VirusTotal API key: ".format(cyan,red,cyan,white)))
        user = getpass.getuser()
        command = "echo '{}' > /home/{}/.apikey.txt".format(apikey,user)
        os.system(command)
        print("{}[{}+{}]{} Your VirusTotal API key saved.".format(cyan,red,cyan,white))

# Exectuion area
os.system("bash .startUp.sh")
try:
    scope()
    os.system("rm -rf temp.txt elves.txt")
except:
    os.system("rm -rf temp.txt elves.txt")
