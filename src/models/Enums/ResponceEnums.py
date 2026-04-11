from enum import Enum
class result_signal(Enum):

    FILE_VALIDATING_SUCCESS = "File validated succeeded"
    FILE_TYPE_NOT_SUPPORTED = "File type is not supported"
    FILE_SIZE_EXCEED_LIMIT = "File size exceed limit"
    FILE_UPLOADED_SUCCESS = "File uploading succeeded"
    FILE_UPLOADED_FAILED = "File uploading was failed"
    PROCESSING_FAILED = "processing_failed"
    PROCESSING_SUCCESS = "processing_succeeded"