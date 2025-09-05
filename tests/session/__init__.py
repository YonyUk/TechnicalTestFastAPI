class Session:
    _username: str = None # type: ignore
    _token: str = None # type: ignore

    @property
    def User(self) -> str:
        return self._username
    
    @property
    def Token(self) -> str:
        return self._token
    
    def authenticate(self,username:str,token:str) -> None:
        self._username = username
        self._token = token
    
    def logout(self) -> None:
        self._username = None # type: ignore
        self._token = None # type: ignore