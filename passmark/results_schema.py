import pydantic
import datetime

from enum import Enum

class testname(Enum):
    CPU_INTEGER_MATH = "CPU_INTEGER_MATH"
    CPU_FLOATINGPOINT_MATH = "CPU_FLOATINGPOINT_MATH"
    CPU_PRIME = "CPU_PRIME"
    CPU_SORTING = "CPU_SORTING"
    CPU_ENCRYPTION = "CPU_ENCRYPTION"
    CPU_COMPRESSION = "CPU_COMPRESSION"
    CPU_SINGLETHREAD = "CPU_SINGLETHREAD"
    CPU_PHYSICS = "CPU_PHYSICS"
    CPU_MATRIX_MULT_SSE = "CPU_MATRIX_MULT_SSE"
    CPU_mm = "CPU_mm"
    CPU_sse = "CPU_sse"
    CPU_fma = "CPU_fma"
    CPU_avx = "CPU_avx"
    CPU_avx512 = "CPU_avx512"
    m_CPU_enc_SHA = "m_CPU_enc_SHA"
    m_CPU_enc_AES = "m_CPU_enc_AES"
    m_CPU_enc_ECDSA = "m_CPU_enc_ECDSA"
    ME_ALLOC_S = "ME_ALLOC_S"
    ME_READ_S = "ME_READ_S"
    ME_READ_L = "ME_READ_L"
    ME_WRITE = "ME_WRITE"
    ME_LARGE = "ME_LARGE"
    ME_LATENCY = "ME_LATENCY"
    ME_THREADED = "ME_THREADED"
    SUMM_CPU = "SUMM_CPU"
    SUMM_ME = "SUMM_ME"

class Passmark_Results(pydantic.BaseModel):
    Testname: testname
    Operations: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Start_Date: datetime.datetime
    End_Date: datetime.datetime
