from StringIO import StringIO

if __name__ == '__main__':
    # read dev file
    dev_file = open('dev', 'r')
    lines = dev_file.read().splitlines()
    dev_file.close()

    # create new file of dev without the tags
    text = StringIO()
    for line in lines:
        pairs = line.split(' ')

        word, tag = pairs[0].rsplit('/', 1)
        text.write(word)

        for pair in pairs[1:]:
            word, tag = pair.rsplit('/', 1)
            text.write(' ' + word)
        text.write('\n')

    # write to the new file
    output_file = open('dev_test', 'w')
    output_file.write(text.getvalue())
    output_file.close()
