#!/usr/bin/python3

import argparse
import re
import datetime as dt
import modules.file_ops as file_ops
import modules.time_ops as time_ops


# PARSE INPUT ARGUMENTS
parser = argparse.ArgumentParser(description='Compose/update properties file based on a base file and an auxiliary file.')
parser.add_argument('base_file', type=str, help='source file used as the base for comparison/composition')
parser.add_argument('aux_file', type=str, help='file used to complement base file')
parser.add_argument('-o', '--out_file', type=str, help='custom file containing result from comparison/composition tasks. Defaults to a file named "out.properties" being created in current directory')#, default='./out.properties')
parser.add_argument('-benc', '--base_file_encoding', type=str, help='base file encoding to use in file operations (read/write). Defaults to "utf-8".', default='utf-8', choices=['utf-8', 'latin-1'])
parser.add_argument('-aenc', '--aux_file_encoding', type=str, help='aux file encoding to use in file operations (read/write). Defaults to "utf-8".', default='utf-8', choices=['utf-8', 'latin-1'])
parser.add_argument('-bfs', '--base_file_separator', type=str, help="select cutomized character(s) to separate keys and values in base file (defaults to '=')", default='=')
parser.add_argument('-afs', '--aux_file_separator', type=str, help="select cutomized character(s) to separate keys and values in aux file(defaults to '=')", default='=')
parser.add_argument('-ofs', '--out_file_separator', type=str, help="select cutomized character(s) to separate keys and values in out file (defaults to base file separator)")
exc_group = parser.add_mutually_exclusive_group()
exc_group.add_argument('-c', '--compose', action='store_true', help='merge data from aux file into base file. Returns data from base file with the values from base file entries replaced with the corresponding data from aux file (DEFAULT)')
exc_group.add_argument('-d', '--diff', action='store_true', help='return count and list of keys present in base file that are missing in aux file')
exc_group2 = parser.add_mutually_exclusive_group()
exc_group2.add_argument('-l', '--line', type=int, help='start properties file processing starting on a specific line')
exc_group2.add_argument('-k', '--key', type=str, help='start properties file processing starting on a specific key')
args = parser.parse_args()

start_time = dt.datetime.now()

if not args.out_file_separator:
    o_sep = args.base_file_separator
else:
    o_sep = args.out_file_separator

#print(f'SEPARATOR: {args.separator}')

if args.out_file:
    o_file = args.out_file
else:
    o_file = './out.properties'
#print(o_file)

if args.diff:
    diff_k_list = file_ops.get_file_diffs(args.base_file, args.aux_file, args.base_file_encoding, args.aux_file_encoding, args.base_file_separator, args.aux_file_separator)

    if len(diff_k_list) > 0:
        if args.out_file:
            with open(o_file, "w", encoding='UTF-8') as out_fp:
                for k in diff_k_list:
                    out_fp.write(f'{k}\n')
        else:
            print(f'--> Found {len(diff_k_list)} keys from base file that do not exist in aux file:')
            for k in diff_k_list:
                print(f'{k}')
    else:
        print(f'--> Base file and Aux file have the same keys!')

    time_ops.print_elapsed_time(start_time)
    exit(0)

if args.line:
    #print(f'LINE ARG DETECTED! VALUE: {args.line}')
    line_count = 0
    with open(args.base_file, "r", encoding=args.base_file_encoding) as base_fp:
        for l in base_fp:
            line_count += 1
    #print(f'FILE LINE COUNT: {line_count}')

    if args.line <= line_count:
        with open(args.base_file, "r", encoding=args.base_file_encoding) as base_fp:
            c = 1
            with open(o_file, "w", encoding='UTF-8') as out_fp:
                for line in base_fp:
                    m_found = False
                    if c >= args.line:
                        # GET KEY AND VALUE IN LINE
                        m_base = re.match(rf'^(.+){args.base_file_separator}(.*)$', line)
                        #print(m_base)
                        if m_base:
                            #print(m_base.groups())
                            # CHECK IF KEY EXISTS IN AUX FILE
                            m_found = file_ops.check_file_for_key(args.aux_file, args.aux_file_encoding,
                                                                  args.aux_file_separator, m_base.groups()[0])
                            if m_found and (len(m_found) > 0):
                                out_fp.write(f"{m_base.groups()[0]}{o_sep}{m_found}\n")
                                print(f"-->> {m_base.groups()[0]}: Match found in aux file! Value updated!")
                            else:
                                out_fp.write(f"{m_base.groups()[0]}{o_sep}{m_base.groups()[1]}\n")
                                print(f"-->> {m_base.groups()[0]}: NO match found in aux file! Keeping data from base file!")
                        else:
                            #print("Unable to get key/value from base properties file!!! Empty line?")
                            out_fp.write(line)
                    c += 1
        time_ops.print_elapsed_time(start_time)
        exit(0)
    else:
        print(f"--> ERROR! Value for '--line' argument ({args.line}) exceeds number of lines available in base file ({line_count})")
        time_ops.print_elapsed_time(start_time)
        exit(1)

if args.key:
    #print(f'KEY ARG DETECTED! VALUE: {args.key}')
    with open(args.base_file, "r", encoding=args.base_file_encoding) as base_fp:
        base_k_list = file_ops.get_keys_in_file(base_fp, args.base_file_separator)

    if args.key in base_k_list:
        with open(args.base_file, "r", encoding=args.base_file_encoding) as base_fp:
                with open(o_file, "w", encoding='UTF-8') as out_fp:
                    proceed = False
                    m_found = False
                    for line in base_fp:
                        # GET KEY AND VALUE IN LINE
                        m_base = re.match(rf'^(.+){args.base_file_separator}(.*)$', line)
                        #print(m_base)

                        if m_base:  # Account for empty lines which do not match a typical line and will not have populated groups
                            if (m_base.groups()[0] == args.key) and not proceed:
                                proceed = True
                                #print("PROCEED FROM NOW ON!!")

                            if proceed:
                                # CHECK IF KEY EXISTS IN AUX FILE
                                m_found = file_ops.check_file_for_key(args.aux_file, args.aux_file_encoding,
                                                                      args.aux_file_separator, m_base.groups()[0])

                                if m_found and (len(m_found) > 0):
                                    out_fp.write(f"{m_base.groups()[0]}{o_sep}{m_found}\n")
                                    print(f"-->> {m_base.groups()[0]}: Match found in aux file! Value updated!")
                                else:
                                    out_fp.write(f"{m_base.groups()[0]}{o_sep}{m_base.groups()[1]}\n")
                                    print(f"-->> {m_base.groups()[0]}: NO match found in aux file! Keeping data from base file!")
                            #else:
                                #    print("DO NOTHING")
                        else:
                            if proceed:
                                #print("Unable to get key/value from base properties file!!! Empty line?")
                                out_fp.write(line)
                            #else:
                            #    print("DO NOTHING")
        time_ops.print_elapsed_time(start_time)
        exit(0)
    else:
        print(f"--> ERROR! Value for '--key' argument ({args.key}) does not exist in base file")
        time_ops.print_elapsed_time(start_time)
        exit(1)


with open(args.base_file, "r", encoding=args.base_file_encoding) as base_fp:
    with open(o_file, "w", encoding='UTF-8') as out_fp:
        for line in base_fp:
            # GET KEY AND VALUE IN LINE
            m_base = re.match(rf'^(.+){args.base_file_separator}(.*)$', line)
            #print(m_base)
            if m_base:
                #print(m_base.groups())
                # CHECK IF KEY EXISTS IN AUX FILE
                m_found = file_ops.check_file_for_key(args.aux_file, args.aux_file_encoding,
                                                      args.aux_file_separator, m_base.groups()[0])

                if m_found and (len(m_found) > 0):
                    out_fp.write(f"{m_base.groups()[0]}{o_sep}{m_found}\n")
                    print(f"-->> {m_base.groups()[0]}: Match found in aux file! Value updated!")
                else:
                    out_fp.write(f"{m_base.groups()[0]}{o_sep}{m_base.groups()[1]}\n")
                    print(f"-->> {m_base.groups()[0]}: NO match found in aux file! Keeping data from base file!")
            else:
                #print("Unable to get key/value from base properties file!!! Empty line?")
                out_fp.write(line)

#print_status()
time_ops.print_elapsed_time(start_time)
exit(0)
