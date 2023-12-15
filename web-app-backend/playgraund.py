# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 21:57:47 2023

@author: timka
"""
import os
from pylint import epylint as lint
import tempfile
from multiprocessing import Pool, cpu_count
from pylint_errors import pylint_dict_final

def is_os_linux():
    if os.name == "nt":
        return False
    return True

def format_errors(pylint_text):
    """Format errors into parsable nested dictionary

    :param pylint_text: original pylint output
    :return: dictionary of errors as:
        {
            {
                "type":_type,
                "code":...,
                "error": ...,
                "message": ...,
                "line": ...,
                "error_info": ...,
            }
            ...
        }
    """
    errors_list = pylint_text.splitlines(True)

    # If there is not an error, return nothing
    if "--------------------------------------------------------------------" in errors_list[1] and \
            "Your code has been rated at" in errors_list[2] and "module" not in errors_list[0]:
        return None

    errors_list.pop(0)

    pylint_list = []
    for error in errors_list:
        pylint_list.append(process_error(error))
    # count = 0
    # for error in errors_list:
    #     pylint_dict[count]=process_error(error)
    #     count +=1
    return [error for error in pylint_list if error!=None]

def evaluate_pylint(text):
    """Create temp files for pylint parsing on user code

    :param text: user code
    :return: dictionary of pylint errors:
        {
            {
                "type":_type,
                "code":...,
                "error": ...,
                "message": ...,
                "line": ...,
                "error_info": ...,
            }
            ...
        }
    """
    # Open temp file for specific session.
    # IF it doesn't exist (aka the key doesn't exist), create one
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        for t in text:
            temp.write(t.encode("utf-8"))
        temp.flush()

    try:
        ARGS = " -r n --disable=R,C"
        (pylint_stdout, pylint_stderr) = lint.py_run(
            temp.name + ARGS, return_std=True)
    except Exception as e:
        raise Exception(e)

    if pylint_stderr.getvalue():
        raise Exception("Issue with pylint configuration")

    return format_errors(pylint_stdout.getvalue())

def process_error(error):
    """Formats error message into dictionary

        :param error: pylint error full text
        :return: dictionary of error as:
            { 
                "type":_type,
                "code":...,
                "error": ...,
                "message": ...,
                "line": ...,
                "error_info": ...,
            }
    """
    # Return None if not an error or warning
    if error == " " or error is None:
        return None
    if error.find("Your code has been rated at") > -1:
        return None

    list_words = error.split()
    if len(list_words) < 3:
        return None

    # Detect OS
    line_num = None
    if is_os_linux():
        try:
            line_num = error.split(":")[1]
        except Exception as e:
            print(os.name + " not compatible: " + e)
    else:
        line_num = error.split(":")[2]

    # list_words.pop(0)
    error_yet, message_yet, first_time = False, False, True
    i, length = 0, len(list_words)
    # error_code=None
    while i < length:
        word = list_words[i]
        if (word == "error" or word == "warning") and first_time:
            error_yet = True
            first_time = False
            i += 1
            continue
        if error_yet:
            error_code = word[1:-1]
            error_string = list_words[i + 1][:-1]
            i = i + 3
            error_yet = False
            message_yet = True
            continue
        if message_yet:
            full_message = ' '.join(list_words[i:length - 1])
            break
        i += 1
    try:
     error_info = pylint_dict_final[error_code]
    except:
     error_info = 'undefine error'
    _type = ''
    if 'E' in error_code:
        _type ='error'
    elif 'W' in error_code:
        _type = 'warning'
    else:
        _type = 'undefine'

    return {
        "type":_type,
        "code": error_code,
        "error": error_string,
        "message": full_message,
        "line": line_num,
        "error_info": error_info,
    }