def raw(text): # text = Transaction One
    split_list = text.split() #----> list ['Transaction', 'One']
    src_word = ''
    for word in split_list:
        src_word += word.lower()
    return src_word

print(raw('Transaction For Parents')) 