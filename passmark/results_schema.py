import pydantic
import datetime
class Passmark_Results(pydantic.BaseModel):
    Testname: str
    Operations: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Start_Date: datetime.datetime
    End_Date: datetime.datetime
