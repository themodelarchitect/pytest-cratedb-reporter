import pytest
import sqlalchemy as sa
from pprint import pp
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

def get_key_id():
    return str(uuid.uuid4())

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(String, primary_key=True, default=get_key_id)
    nodeid = Column(String)
    outcome = Column(String)
    message = Column(String)
    backtrace = Column(String)
    duration = Column(Integer)
    timestamp = Column(DateTime)
    passed = Column(Boolean)
    failed = Column(Boolean)

def pytest_addoption(parser):
    group = parser.getgroup('cratedb')
    group.addoption(
        '--cratedb-url',
        action='store',
        help='CrateDB connection URL (e.g., crate://localhost:4200)',
    )

def pytest_configure(config):
    cratedb_url = config.getoption('--cratedb-url')
    if cratedb_url:
        config.cratedb_engine = sa.create_engine(cratedb_url)
        try:
            Base.metadata.create_all(config.cratedb_engine)
        except Exception as e:
            print(f"Error creating tables: {e}")  # Add error handling
            raise  # Re-raise the exception to stop pytest
        config.cratedb_session = sessionmaker(bind=config.cratedb_engine)()
    else:
        config.cratedb_engine = None
        config.cratedb_session = None

def pytest_unconfigure(config):
    if hasattr(config, 'cratedb_session') and config.cratedb_session:
        config.cratedb_session.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if hasattr(item.config, 'cratedb_session') and item.config.cratedb_session:
        # Extract test message and backtrace
        message = None
        backtrace = None
        if report.longrepr:
            if hasattr(report.longrepr, 'reprcrash'):
                # For assertion failures, get the clean error message
                message = report.longrepr.reprcrash.message
                backtrace = str(report.longrepr)
            elif isinstance(report.longrepr, (str, Exception)):
                # For other errors (like raised exceptions), get the error message
                message = str(report.longrepr).split('\n')[0]  # First line is usually the error
                backtrace = str(report.longrepr)
            else:
                # Fallback: use the full repr as both message and backtrace
                message = str(report.longrepr)
                backtrace = str(report.longrepr)

        test_result = TestResult(
            nodeid=report.nodeid,
            outcome=report.outcome,
            message=message or "",
            backtrace=backtrace or "",
            duration=int(report.duration * 1000), #store in milliseconds
            timestamp=datetime.now(),
            passed=report.outcome == 'passed',
            failed=report.outcome == 'failed',
        )
        item.config.cratedb_session.add(test_result)
        item.config.cratedb_session.commit()