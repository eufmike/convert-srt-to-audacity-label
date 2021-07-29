#!/usr/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, sys
import pysrt
import argparse
import codecs
import tqdm
import re
import glob
import pandas as pd

def srt2txtexport(ipfilepath, opfilepath):
    subs = pysrt.open(ipfilepath, encoding='utf-8')
    with codecs.open(opfilepath, 'w', 'utf-8') as output:

        for s in subs:
            start = s.start.hours * 60 * 60 + s.start.minutes * 60 + s.start.seconds + s.start.milliseconds/1000.0
            end = s.end.hours * 60 * 60 + s.end.minutes * 60 + s.end.seconds + s.end.milliseconds/1000.0
            output.write( "%.6f\t%.6f\t%s\n" % (start,end,s.text.replace('\n',' \\\\ ') ) )

    print("%s wrote." % opfilepath)

    return
    
if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--input_file_path", help="input SRT file path")
    parser.add_argument('-d', "--input_directory", help="input srt folder")
    parser.add_argument('-nm', "--no_merge", action='store_true', help="create a merge txt file")
    args = parser.parse_args()

    if (args.input_file_path is None) and (args.input_directory is None):
        print('Error: Please define one SRT file or one folder includes SRT file(s).')
        sys.exit()
    elif(not args.input_file_path is None) and (not args.input_directory is None):
        print('Error: There can only be one SRT file path or one SRT folder.')
        sys.exit()

    elif(not args.input_file_path is None):
        if (not os.path.isfile(args.input_file_path)):
            print('Input SRT path does not exist, exiting'.format(args.input_file_path))
            sys.exit()
        else:
            opfilepath = re.sub('.srt', '-LABELS.txt', args.input_file_path)
            srt2txtexport(args.input_file_path, opfilepath)
    elif(not args.input_directory is None):
        if (not os.path.isdir(args.input_directory)):
            print('Input SRT path does not exist, exiting'.format(args.input_directory))
            sys.exit()
        else:
            srtfilelist = glob.glob(os.path.join(args.input_directory, '*.srt'))
            txtfilelist = [re.sub('.srt', '-LABELS.txt', ipfilepath) for ipfilepath in srtfilelist]

            for ipfile, opfile in zip(srtfilelist, txtfilelist):
                srt2txtexport(ipfile, opfile)
            
            if not args.no_merge:
                df_all = []
                for iptxt in txtfilelist:
                    df = pd.read_table(iptxt, header=None, names= ['start', 'end', 'content'], na_values='NaN')
                    iptxt_bsn = os.path.basename(iptxt)
                    df['name'] = re.sub('.cmn-hant-tw-LABELS.txt', '', iptxt_bsn)
                    df_all.append(df)

                df_all = pd.concat(df_all, axis=0)
                df_all = df_all[['name', 'start', 'end', 'content']]
                df_all = df_all.sort_values(by='start')

                df_all.to_csv(os.path.join(args.input_directory, 'merge.csv'), index=None)
                df_all.drop(['name'], axis = 1).to_csv(os.path.join(args.input_directory, 'merge.txt'), header=None, index=None, sep='\t', mode='a')
                print('Merge CSV and TXT files are exported.')

    