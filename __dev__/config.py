
from core.database.sessions import engine
from core.database.db_models import Base
from modules.users.users_models import User
from modules.agents.agents_models import Agent
from sqlalchemy import text

Base.metadata.create_all(bind=engine)
print("✅ Tables created.")

# with engine.connect() as conn:
#     conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS email_hash TEXT NOT NULL;"))
#     conn.commit()





# from dotenv import load_dotenv
# load_dotenv()
# from core.services.webtoken_service import WebTokenService

# verToken = WebTokenService().generate_token({
#     "user_id": "675d2559-fa47-402d-8c16-e5b6e2b88acf"
# }, "356d")

# print(verToken)