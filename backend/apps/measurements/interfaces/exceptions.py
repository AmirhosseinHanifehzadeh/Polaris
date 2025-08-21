from libs.exceptions import NotFoundRoot, BadRequestRoot


class MeasurementNotFound(NotFoundRoot):
    pass

class BulkCreateError(BadRequestRoot):
    pass 
