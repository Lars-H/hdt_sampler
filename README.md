# HDT Sampler

Sample subgraphs from RDF Graphs stored as HDT Documents.


## Requirements

- Python Version 3.6.4 or higher
- [pyHDT](https://github.com/Callidon/pyHDT)
- [RDFLib](https://github.com/RDFLib/rdflib)

## Installation

- Install Python
- Follow instruction of pyHDT and RDFLib to install them
- Installation in a virtualenv is advised

## Usage

### Example:
```bash
python hdt_sampler.py -f myHDTFile.hdt -s 0.1 -m unweigthed
```

### CLI Arguments:
```bash
  -h, --help            show this help message and exit
  -f FILE, --file FILE  HDT File to be sampled from (required)
  -s SIZE, --size SIZE  Percentage of subjects to be sampled, range: [0,1]
                        (required)
  -n NUMBER, --number NUMBER
                        Number of samples to be created (default=1)
  -m {unweighted,weighted,hybrid}, --method {unweighted,weighted,hybrid}
                        Sampling method to be used (required: unweighted,
                        weigthed, hybrid)
  -r RATIO, --ratio RATIO
                        Ratio for hybrid sampling, range: [0,1] (default=0.5)
  -l {INFO,DEBUG,ERROR}, --logging {INFO,DEBUG,ERROR}
                        Set logging level (optional)
```


## Related Publication
```
Heling, Lars, Acosta, Maribel. 
"Estimating Characteristic Sets for RDF Dataset Profilesbased on Sampling." 
European Semantic Web Conference 2020.
```
