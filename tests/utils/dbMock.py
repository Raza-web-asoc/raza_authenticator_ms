async def mock_get_db():
    class DummyDB:
        async def commit(self): pass
        async def refresh(self, obj): pass
    return DummyDB()
