from libs.exceptions import NotFoundRoot


class MeasurementNotFound(NotFoundRoot):
    pass

class BulkCreateError(BaseException):
    pass 
