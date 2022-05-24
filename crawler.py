from icrawler.builtin import GoogleImageCrawler
from icrawler.builtin import BingImageCrawler
import os
import cv2
import argparse

# define path of text file in case no keywords are provided by user
file_path = "./keywords.txt"

# initiate list of keywords
keyword_list = []

# create argument parser
ap = argparse.ArgumentParser(description="crawler")
ap.add_argument("-n", "--max_number", required=True,
                help="Please declare max number of images you would like to search for.")
ap.add_argument("-e", "--engine", choices=["google", "bing"], default="bing",
                help="Please choose search engine (Google or Bing) you would like to perform your search with.")
ap.add_argument("-r", "--resize", choices=["yes", "no"], default="no",
                help="Please choose if all crawled pictures shall be resized.")
ap.add_argument("-k", "--keyword",
                help="Please provide descriptive keywords of the images you would like to search for separated by ','.")

# create dict for storing arguments entered by user
args = vars(ap.parse_args())

# create list of keywords either as defined by user or with keyword(s) from text file
if args["keyword"]:
    keyword_list = args["keyword"].split(",")
else:
    try:
        if os.path.getsize(file_path) > 0:
            with open(file_path, mode="r", encoding="utf_8") as f:
                keyword_list = list(f)
                for i in range(len(keyword_list)):
                    keyword_list[i] = keyword_list[i].replace('\n', '')
        # error handling: keyword file does exist but is empty
        else:
            print("Unfortunately 'keywords.txt' is currently empty, please fill with descriptive keywords for image search.")
    # error handling: keyword file does not exist or cannot be read
    except FileNotFoundError as e:
        print(f"{e} \n"
              "FileNotFoundError was successfully handled: "
              "Please include file 'keywords.txt' in directory or manually define keywords for image search next time.")

# create filters for image search
filters = dict(
    size="large",
    license="commercial,modify",
)


# initiate crawler for different search engine options and define storage
def get_crawler(args, directory):
    if args["engine"] == "google":
        crawler = GoogleImageCrawler(
            feeder_threads=1,
            parser_threads=2,
            downloader_threads=4,
            storage={"root_dir": directory}
        )
    elif args["engine"] == "bing":
        crawler = BingImageCrawler(
            feeder_threads=1,
            parser_threads=2,
            downloader_threads=4,
            storage={"root_dir": directory}
        )
    return crawler


# crawl chosen search engine for each keyword
for keyword in keyword_list:
    # directory of loaded images, create new directory if it does not exist yet
    directory = "icrawled/{0}".format(keyword)
    if not os.path.exists("icrawled"):
        os.makedirs("icrawled")
    crawler = get_crawler(args, directory)
    crawler.crawl(keyword=keyword, filters=filters, max_num=int(args["max_number"]), file_idx_offset=0)

    # user message: selected search engine
    message_e = "SEARCH ENGINE: " + args["engine"]
    print()
    print("#" * int(len(message_e)))
    print(message_e)
    print("#" * int(len(message_e)))

    # resize all crawled images (if desired by user)
    if args["resize"] == "yes":
        # define allowed filetypes to filter images in directory
        resize_file_types = ("jpg", "png")
        # if file is a picture
        for filename in os.listdir(directory):
            if filename.endswith(resize_file_types):
                print("resize {0}{1}".format(directory, filename))
                # read and resize image
                img = cv2.imread(directory + '/' + filename, cv2.IMREAD_COLOR)
                resized_img = cv2.resize(img, [1000, 1000])
                # write new picture
                cv2.imwrite(directory + '/' + filename, resized_img)

    # user message: number of downloaded images
    message_n = "** found and downloaded {0} image(s) in directory {1} **".format(len(os.listdir(directory)), directory)
    print()
    print(message_n)
    print("*" * int(len(message_n)))
