from enum import Enum
from .config import Config

config = Config()

class TableNames(str, Enum):
    SCHEDULES = config.dynamodb.schedules_table
    APPLIES = config.dynamodb.schedules_applies
    

class IndexNames:
    SCHEUDULE_GSI = 'ScheduleIndex'
    SCHEDULE_JOB_POSTING_GSI = 'ScheduleJobPostingIndex'

DB_CONSTANTS = {
    'batch_size': 25,
    'max_retries': 3,
    'timeout': 30,
}