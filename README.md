# image_metadata_parser

The purpose of this repository is to get experience on image parsing. My goal is to be able to parse metadata and access pixel data by parsing an image binary.
I anticipate to support the following formats:
- PNG: List of chunks taken from [here](http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html). If there are more chunks you would like me to add, submit an issue or contact me at <johvnguyen@gmail.com>.
	- [x] IHDR Parser
	- [x] PLTE Parser
	- [x] IDAT Parser
	- [x] IEND Parser
	- [x] gAMA Parser
	- [x] IHDR Parser
	- [x] sRGB Parser
	- [x] tRNS Parser
	- [x] cHRM Parser
	- [x] iCCP Parser
	- [x] tEXt Parser
	- [x] zTXt Parser
	- [x] iTXt Parser
	- [x] bKGD Parser
	- [x] pHYs Parser
	- [x] sBIT Parser
	- [x] sPLT Parser
	- [x] hIST Parser
	- [x] tIME Parser

- JPG/JPEG
	- Much of my parser will be based on Yasoob Khalid's fantastic blog post on the [topic](https://yasoob.me/posts/understanding-and-writing-jpeg-decoder-in-python/#huffman-encoding). I credit any success in this parser to him and any bugs or errors found in here to myself. I will also be using the profile picture he used as an example for my testing.
- GIF?
- TIFF?


### TODO
- PNGParser bugs
	- ~~Write more PNG Chunk Parsers~~
	- Refactoring PNGParser's ChunkParsers
		- Define a format/schema that all chunk parsers will follow. Take the following into consideration:
			- Refacotring how we parse each chunk -- do we do it all at once, do we parse chunk values one at a time? Need to standardize
			- For ChunkParsers which use a keyword-value pair, I should refactor the data dictionary to contain 1 entry with all the keywords and a series of entries with the keyword for the key and the associated value for the value.
			- Refactor function names so that they are consistent and obvious throughout PNGParser
				- Functions which return a byte object should be prefixed with 'decode'
				- Functions which parse the image file pointer and sets associated variables should be prefixed with 'parse'
		- Refactor exceptions in some chunk parsers such as IHDR parser to use custom exception messages instead of generic ValueError. Ideally use both.
	- Find more png files to test with.
	- In PNGParser, write a function to take in all IDAT data and apply corresponding decompression algorithm to return raw image data.
	
	- Unit testing on faulty PNGs and see if error messages and logging can help catch the faults.
	- 
	
