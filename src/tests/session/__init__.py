class Session:
    '''
    class to manage the user's session for the tests
    '''
    _username: str = None # type: ignore
    _token: str = None # type: ignore

    @property
    def User(self) -> str:
        '''
        username of the authenticated user
        '''
        return self._username
    
    @property
    def Token(self) -> str:
        '''
        authorization token of the authenticated user
        '''
        return self._token
    
    def authenticate(self,username:str,token:str) -> None:
        '''
        authenticate the given user
        '''
        self._username = username
        self._token = token
    
    def logout(self) -> None:
        '''
        logout the current authenticated user
        '''
        self._username = None # type: ignore
        self._token = None # type: ignore