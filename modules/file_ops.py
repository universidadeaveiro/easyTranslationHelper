#!/usr/bin/python3

import re


def get_keys_in_file(fp, sep):
    k_list = []
    for line in fp:
        #print(line)
        if re.match(rf'^(.+){sep}.*$', line):
            k_list.append(re.match(rf'^(.+){sep}.*$', line).groups()[0])
    return k_list


def get_file_diffs(bf, af, b_enc, a_enc, b_sep, a_sep):
    with open(af, "r", encoding=b_enc) as aux_fp:
        with open(bf, "r", encoding=a_enc) as base_fp:
            diff_k_list = []
            base_k_list = get_keys_in_file(base_fp, b_sep)
            aux_k_list = get_keys_in_file(aux_fp, a_sep)

            for k in base_k_list:
                if not (k in aux_k_list):
                    diff_k_list.append(k)
    return diff_k_list


def check_file_for_key(filename, file_encoding, file_separator, search_key):
    with open(filename, 'r', encoding=file_encoding) as fp:
        for line in fp:
            m_aux = re.match(rf'^(.+){file_separator}(.*)$', line)
            if m_aux:
                m = m_aux.groups()
                if search_key == m[0]:
                    return m[1]
        return None
