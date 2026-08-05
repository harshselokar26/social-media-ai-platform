from sqlalchemy import create_engine, text
from app.core.config import settings

def main():
    engine = create_engine(settings.DATABASE_URL, future=True)
    with engine.connect() as conn:
        print('columns=', conn.execute(text("SELECT data_type, udt_name FROM information_schema.columns WHERE table_name='organization_members' AND column_name='role';")).all())
        print('enum_exists=', conn.execute(text("SELECT EXISTS(SELECT 1 FROM pg_type WHERE typname='role');")).scalar())
        print('enum_labels=', conn.execute(text("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid=pg_type.oid WHERE pg_type.typname='role' ORDER BY enumsortorder; ")).all())
        print('constraint=', conn.execute(text("SELECT pg_get_constraintdef(c.oid) FROM pg_constraint c JOIN pg_class t ON c.conrelid=t.oid WHERE t.relname='organization_members' AND c.conname='organization_members_role_check';")).scalar())

if __name__ == '__main__':
    main()
