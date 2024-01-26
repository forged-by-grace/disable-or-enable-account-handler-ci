from dataclasses_avroschema.pydantic import AvroBaseModel
from pydantic import Field

class AccountID(AvroBaseModel):
    id: str = Field(description='Id to id an account.')

class Disable_Enable_Account(AccountID):
    disabled: bool = Field(description="Flag used to enable or disable an account.")

