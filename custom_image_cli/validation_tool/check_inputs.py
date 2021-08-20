import sys


def check_version(version, release_name, log):
    if not version:
        log.error("No matching image with %s \'%s\' : FAIL" % ('ReleaseName', release_name))
        sys.exit(2)


def check_image(image, image_type, log):
    if not image:
        log.error("No matching image with %s \'%s\' : FAIL" % ('Imagetype', image_type))
        sys.exit(2)


