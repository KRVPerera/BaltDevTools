#
# author:  Sandaru Jayawardana
# author link: https://github.com/SandaruJayawardana
# modified by: KRV Perera
# original link: https://gist.github.com/SandaruJayawardana/6c91b947a418c75542ae73460f7492e0
# Remove duplicated labels and create the reorded output with adjesting the line length to 120.
#
# Input should be followed the standard Ballerina conformance test format and there should be a new line
# after the 'Labels:'.
#
# Ex:
# Input -
# Test-Case: output
# Description: Test field access expression with accessing existing fields when it belongs to JSON objects.
# Labels: DecimalNumber, DecimalNumber, json, list-constructor-expr, nil-literal, mapping-constructor-expr, HexIntLiteral, decimal,
#         string, float, FloatingPointSuffix, DecimalFloatingPointNumber, HexFloatingPointLiteral, boolean,
#         field-access-expr, readonly-type, array-type, DecimalNumber, DecimalNumber
#
# function init() {
#
# }
#
# Output -
# Test-Case: output
# Description: Test field access expression with accessing existing fields when it belongs to JSON objects.
# Labels: array-type, boolean, decimal, DecimalFloatingPointNumber, DecimalNumber, field-access-expr, float,
#         FloatingPointSuffix, HexFloatingPointLiteral, HexIntLiteral, json, list-constructor-expr,
#         mapping-constructor-expr, nil-literal, readonly-type, string
#
# function init() {
#
# }

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleExample')

lines = []
sub_line = []
INDENTATION_SIZE = len("Labels: ")


def updated_file_print(print_list):
    for i in print_list:
        print(i)


def update_label_list(label_list, new_label):
    fixed_list = new_label.replace(" ", '').split(",")
    for i in fixed_list:
        if i != '':
            label_list.append(i)


def re_order_labels(labels):
    labels = list(set(labels))  # Remove duplicates
    return sorted(labels, key=str.casefold)  # Rearrange in alphabetical order


def split_into_multiple_lines(labels):
    splitted_line = "Labels: "
    final_list = []
    char_count = INDENTATION_SIZE
    for i in labels[:-1]:
        char_count += len(i)
        if char_count >= 120:  # Consider the comma also
            final_list.append(splitted_line)
            splitted_line = " " * INDENTATION_SIZE
            char_count = INDENTATION_SIZE + len(i)
        splitted_line += i + ", "
        char_count += 2

    char_count += len(labels[-1])
    if char_count > 120:
        final_list.append(splitted_line)
        final_list.append(" " * INDENTATION_SIZE + labels[-1])
    else:
        splitted_line += labels[-1]
        final_list.append(splitted_line)
    return final_list


def label_sort():
    global sub_line
    global lines
    labels = []
    is_contd = False
    output_list = []
    for i in range(len(lines)):
        if is_contd:
            if sub_line[i] == [""]:
                is_contd = False
                #print("Final list", labels, "\n")
                labels = re_order_labels(labels)
                #print("re_order_labels", labels, "\n")
                resultant_list = split_into_multiple_lines(labels)
                #print("split_into_multiple_lines", resultant_list, "\n")
                for k in resultant_list:
                    output_list.append(k)
                output_list.append('')
                labels = []
                continue
            for j in sub_line[i]:
                update_label_list(labels, j)
            continue
        if sub_line[i][0] == "Labels:":
            is_contd = True
            for j in sub_line[i][1:]:
                update_label_list(labels, j)
            continue
        output_list.append(lines[i])
    #print("Output list ", output_list)
    return output_list


def sort_labels(file_ame):
    global sub_line
    global lines
    f = open(file_ame, "r")
    lines = f.read().split("\n")

    for i in lines:
        sub_line.append(list(i.split(" ")))
    output_list = label_sort()

    updated_file_print(output_list)