# csec731scraper
CSEC-731 Web Scraper Project

## Assumptions
 - External references listed in HTTP Response headers do not qualify
 - Assignment desires ALL **EXTERNAL REFERENCES** hence filtering by attributes accepting URIs is insufficient...  The code provides these relevant attributes regardless
 - Collects references located in scripts


 ## URI Accepting Attributes
 - action
 - archive
 - background
 - cite
 - classid
 - codebase
 - data
 - formaction
 - href
 - icon
 - itemtype
 - longdesc
 - manifest
 - poster
 - profile
 - src
 - srcset
 - usemap
 - xmlns

## Install
    # Clone the repository
    git clone https://github.com/spk3077/csec731scraper

    # Install dependencies
    pip install -r requirements.txt


## Running

    # Enter cloned directory
    cd csec731scraper

    # Run 
    python3 scraper.py https://www.rit.edu/
