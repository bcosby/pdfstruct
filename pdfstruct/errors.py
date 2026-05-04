class PDFError(Exception):
    pass


class PDFSyntaxError(PDFError):
    pass


class PDFXRefError(PDFError):
    pass


class PDFStreamError(PDFError):
    pass


class PDFUnsupportedFeature(PDFError):
    pass


class PDFEncryptionError(PDFError):
    pass
