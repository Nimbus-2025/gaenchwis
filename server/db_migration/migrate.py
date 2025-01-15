import argparse
from migrations.manager import MigrationManager
from dotenv import load_dotenv

load_dotenv()

def run_migration(action: str):
    manager = MigrationManager()
    
    if action == 'up':
        print("Recreating all tables with updated schemas...")
        manager.recreate_tables()
        print("Migration completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DynamoDB Migration Tool')
    parser.add_argument('action', choices=['up'],
                    help='Migration action to perform')
    
    args = parser.parse_args()
    run_migration(args.action)