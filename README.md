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
	- [ ] iTXt Parser
	- [x] bKGD Parser
	- [x] pHYs Parser
	- [x] sBIT Parser
	- [ ] sPLT Parser
	- [ ] hIST Parser
	- [ ] tIME Parser

- JPG/JPEG
- GIF?
- TIFF?


### TODO
- PNGParser bugs
	- Write more PNG Chunk Parsers
	- In PNGParser, write a function to take in all IDAT data and apply corresponding decompression algorithm to return raw image data.
	- Refactor exceptions in some chunk parsers such as IHDR parser to use custom exception messages instead of generic ValueError. Ideally use both.
	- Unit testing on faulty PNGs and see if error messages and logging can help catch the faults.
	- Refacotring how we parse each chunk -- do we do it all at once, do we parse chunk values one at a time? Need to standardize
	- For ChunkParsers which use a keyword-value pair, I should refactor the data dictionary to contain 1 entry with all the keywords and a series of entries with the keyword for the key and the associated value for the value.
	- Refactor function names so that they are consistent and obvious throughout PNGParser
		- Functions which return a byte object should be prefixed with 'decode'
		- Functions which parse the image file pointer and sets associated variables should be prefixed with 'parse'
