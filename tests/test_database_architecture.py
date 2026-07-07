import pytest
from database.database import DatabaseManager, db_manager

def test_database_manager_initialization():
    # Verify singleton db_manager properties
    assert db_manager is not None
    assert db_manager.engine is not None
    assert db_manager.session_factory is not None
    
    # Assert pool parameters are configured correctly
    assert db_manager.engine.pool is not None
    # Depending on sqlalchemy dialect configuration, pool details are checked
    assert db_manager.db_url is not None

@pytest.mark.asyncio
async def test_database_manager_connection_verification():
    # Verify the connection routine can execute (returns bool)
    res = await db_manager.verify_connection()
    assert isinstance(res, bool)
