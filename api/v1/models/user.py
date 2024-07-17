from pydantic import BaseModel, Field, ConfigDict, UUID4, EmailStr


class UserBase(BaseModel):
    username: str = Field(description="회원명")
    email: EmailStr


class UserCreate(UserBase):
    """
    password pattern 요구 사항
    1. 길이가 8자에서 20자 사이여야 함.
    2. 최소한 하나 이상의 알파벳 문자 (대소문자 포함)를 포함해야 함.
    3. 최소한 하나 이상의 숫자(0-9)를 포함해야 함.
    4. 최소한 하나 이상의 특수 문자(~!@#$%^&*()-_=+[{\]}\\|;:'",<.>/?)를 포함해야 함.
    """

    model_config = ConfigDict(regex_engine="python-re")

    password: str = Field(
        description="비밀번호",
        pattern=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[`~!@#$%^&*()-_=+[{\]}\\|;:\'\",<.>/?])[A-Za-z\d`~!@#$%^&*()-_=+[{\]}\\|;:\'\",<.>/?]{8,20}$",
    )


class User(UserBase):
    id: UUID4
