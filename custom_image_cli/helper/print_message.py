from .. import __version__


def print_validate_completion_message(validation_succeeded):
    print("-----------------------------------------------------------------")
    if validation_succeeded:
        print("Overall Custom Image Validation Succeeded.")
    else:
        print("Custom Image Validation Failed. Please see individual test results above for detailed information.")

    print("-----------------------------------------------------------------")


def print_pre_verification_text():
    print("Amazon EMR on EKS - Custom Image CLI")
    print("Version: %s" % __version__)
