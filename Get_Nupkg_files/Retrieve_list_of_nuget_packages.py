import io
from lxml import etree
import asyncio
import argparse
from urllib.request import urlretrieve


######################################################
# Constants
######################################################

PREFIX = "https://www.nuget.org/api/v2/package"

########################################################################
# Functions
########################################################################

def parse_args():
    parser=argparse.ArgumentParser(description="A script to download all the Nuget packages (.nupkg files) from a .csproj C# project")
    parser.add_argument("--csprojFile",
                        type=str,
                        help='C# project file to consider to download the Nuget packages, with particular versions')
    parser.add_argument("--outputDir",
                        type=str,
                        help='Output directory')
    args=parser.parse_args()
    return args

def get_npgk_urls(xml_tree: etree._ElementTree) -> list[str]:
    """
    Return the list of URLs where the .nupkg files can be downloaded,
    corresponding to the Nuget package reference and version extracted from
    the .csproj XML tree passed as argument

    Parameters:
    -----------
    xml_tree: etree._ElementTree
        the tree in input

    Returns:
    --------
    list of URLs to download .nupkg files
    """

    urls = []
    # Loop through the package references
    for s in xml_tree.xpath('//PackageReference'):
        version = s.attrib["Version"]
        include = s.attrib["Include"]
        print(f'URL is {PREFIX}/{include}/{version}')
        urls.append(f'{PREFIX}/{include}/{version}')
    return urls

async def retrieve_urls(urls: list[str], outputDir: str):
    for url in urls:
        splittedUrl = url.split('/')

        lastIndex = len(splittedUrl) - 1
        fileName = f'{outputDir}/{splittedUrl[lastIndex-1]}_{splittedUrl[lastIndex]}.nupkg'
        urlretrieve(url, fileName)

##########################################
# Example 
# python Retrieve_list_of_nuget_packages.py --csprojFile TestNugetSynaps2.csproj --outputDir ./bin
#########################################
async def main():
    # Retrieve args
    inputs=parse_args()

    csprojFile = inputs.csprojFile
    outputDir = inputs.outputDir

    print(f'CSProj File {csprojFile}')
    print(f'Output dir {outputDir}')

    tree = etree.parse(csprojFile)

    nugetDownloadUrls = get_npgk_urls(tree)

    await retrieve_urls(nugetDownloadUrls, outputDir)

asyncio.run(main())
