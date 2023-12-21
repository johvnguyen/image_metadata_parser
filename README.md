# image_metadata_parser

The purpose of this repository is to get experience on image parsing. My goal is to be able to parse metadata and access pixel data by parsing an image binary.
I anticipate to support the following formats:
- PNG: List of chunks taken from [here](http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html). If there are more chunks you would like me to add, submit an issue or contact me at <johvnguyen@gmail.com>.
	- [x] IHDR Parser
	- [ ] PLTE Parser
	- [ ] IDAT Parser
	- [ ] IEND Parser
	- [x] gAMA Parser
	- [x] IHDR Parser
	- [x] sRGB Parser
	- [ ] tRNS Parser
	- [ ] cHRM Parser
	- [ ] iCCP Parser
	- [ ] tEXt Parser
	- [ ] zTXt Parser
	- [ ] iTXt Parser
	- [ ] bKGD Parser
	- [ ] pHYs Parser
	- [ ] sBIT Parser
	- [ ] sPLT Parser
	- [ ] hIST Parser
	- [ ] tIME Parser

- JPG/JPEG
- GIF?
- TIFF?


### TODO
- Write more PNG Chunk Parsers
