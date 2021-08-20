import argparse
import sys
from custom_image_cli import __version__


# Parses command line arguments and assigns values to global variables
class ArgsParser(argparse.ArgumentParser):
    def error(self, msg):
        sys.stderr.write('Error: %s \n' % msg)
        self.print_help()
        sys.exit(2)


def parse_commandline_arguments(args=None):
    if args is None:
        args = sys.argv[1:]

    main_parser = ArgsParser(prog="emr-on-eks-custom-image",
                             formatter_class=argparse.RawTextHelpFormatter)
    main_parser.add_argument('--version', action='version',
                             version='Amazon EMR on EKS Custom Image CLI '
                                     '\nVersion: {version}'.format(version=__version__))
    subparsers = main_parser.add_subparsers(dest="command")

    validate_image_parser = parse_validate_image(subparsers)
    main_parser_args = main_parser.parse_args(args)

    return main_parser_args


def parse_validate_image(subparsers):
    validate_image_parser = subparsers.add_parser(name="validate-image",
                                                  formatter_class=argparse.RawTextHelpFormatter)
    validate_image_parser.add_argument('--version', action='version',
                                       version='%(prog)s \nVersion: {version}'.format(version=__version__))
    validate_image_parser.add_argument("-i", "--local-image-uri",
                                       help="specifies the name of image uri",
                                       required=True)
    validate_image_parser.add_argument("-r", "--release-name",
                                       help="specifies the release name of the image. e.g. emr-5.32.0",
                                       required=True)
    validate_image_parser.add_argument("-t", "--image-type",
                                       help="specifies the image runtime type. e.g. spark \ndefault runtime type is "
                                            "spark")
    return validate_image_parser
