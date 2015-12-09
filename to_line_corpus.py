import sys
import bz2
from optparse import OptionParser
from docs import config
from lib.tokenizer import text_to_sentences

def build_opt_parser():
    usage = "usage: %prog [options] <filename> [, <filename>, ...]"
    parser = OptionParser(usage=usage)

    parser.add_option("-o", "--out-file", dest="out_file",
                      default=config.default_line_out_file,
                      help="The file to which the output will be written"
    )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments(parser):
    (options, args) = parser.parse_args()
    
    if len(args) < 1:
        parser.print_help()
        exit()

    return options, args

def main():
    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)

    with bz2.BZ2File(options.out_file, 'w') as line_corpus:
        for fname in args:
            with open(fname, "r") as f:
                fcontents = f.read()
                sentences = text_to_sentences(fcontents)
                for sentence in sentences:
                    line_corpus.write('{0}\n'.format(sentence))

if __name__ == "__main__":
    main()
