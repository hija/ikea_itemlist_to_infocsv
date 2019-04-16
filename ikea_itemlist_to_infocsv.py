import ikea_info_grabber
import argparse
import os
import sys
import re
import time
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates a csv with information about IKEA products for a list of IKEA product ids')
    parser.add_argument('inputfile', type=str, help='A newline separated file of product ids')
    parser.add_argument('--outputfile', type=str, default='products.csv', help='Output csv file in which the information shall be written. Will be overwritten if it exist')
    parser.add_argument('--delimiter', type=str, default=';', help='Delimiter for the csv file (defaults to German ;)')
    args = parser.parse_args()

    ## Try to open file
    if os.path.isfile(args.inputfile):

        # First we collect the information
        product_information = []
        with open(args.inputfile) as inputfile:
            for line in inputfile:
                if re.fullmatch('\d{3}\.\d{3}\.\d{2}', line.strip()):
                    print('[INFO] Found productid:', line.strip())
                    single_product_information = ikea_info_grabber.get_product_info(line.strip())
                    if len(single_product_information) > 1:
                        print('[INFO] Query for product', line.strip(), 'returned more than one product. Every product returned will be added. The number of rows in the csv file might be greater than the input file')
                    elif len(single_product_information) == 0:
                        print('[INFO] Query for product', line.strip(), 'returned no result. It will not be contained in the output csv.')
                    product_information.extend(single_product_information)
                    time.sleep(1) # Wait 1 second to not DoS IKEA's server

        # Then we write it into the csv
        if len(product_information) > 0:
            with open(args.outputfile, 'w', newline='') as csvfile:
                fieldnames = ['product_name', 'product_category', 'product_color', 'product_price', 'product_id', 'is_family_price', 'is_online_sellable']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=args.delimiter)
                writer.writeheader()
                writer.writerows(product_information)
        else:
            print('[INFO] No product information could be found. No output will be written.')
    else:
        print('[ERROR] The input file does not exist. Aborting', file=sys.stderr)
