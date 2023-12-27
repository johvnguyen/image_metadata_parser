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
	- [ ] iCCP Parser
	- [ ] tEXt Parser
	- [ ] zTXt Parser
	- [ ] iTXt Parser
	- [ ] bKGD Parser
	- [x] pHYs Parser
	- [ ] sBIT Parser
	- [ ] sPLT Parser
	- [ ] hIST Parser
	- [ ] tIME Parser

- JPG/JPEG
- GIF?
- TIFF?


### TODO
- Write more PNG Chunk Parsers
- In PNGParser, write a function to take in all IDAT data and apply corresponding decompression algorithm to return raw image data.
- Refactor exceptions in some chunk parsers such as IHDR parser to use custom exception messages instead of generic ValueError. Ideally use both.
- Unit testing on faulty PNGs and see if error messages and logging can help catch the faults.
