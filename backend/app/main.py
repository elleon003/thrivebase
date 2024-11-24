from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
import supertokens_python as supertokens
from supertokens_python.recipe import emailpassword, session, thirdpartyemailpassword
from supertokens_python.recipe.thirdparty.provider import GoogleProvider
from supertokens_python.framework.fastapi import get_middleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("PROJECT_NAME", "ThriveBase"),
    openapi_url=f"{os.getenv('API_V1_STR', '/api/v1')}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=eval(os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:5173"]')),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure SuperTokens
supertokens.init(
    app_info=supertokens.InputAppInfo(
        app_name=os.getenv("SUPERTOKENS_APP_NAME"),
        api_domain=os.getenv("SUPERTOKENS_API_DOMAIN"),
        website_domain=os.getenv("SUPERTOKENS_WEBSITE_DOMAIN"),
    ),
    supertokens_config=supertokens.ConnectionConfig(
        connection_uri=os.getenv("SUPERTOKENS_CONNECTION_URI"),
        api_key=os.getenv("SUPERTOKENS_API_KEY")
    ),
    framework='fastapi',
    recipe_list=[
        thirdpartyemailpassword.init(
            providers=[
                GoogleProvider(
                    client_id=os.getenv("GOOGLE_CLIENT_ID"),
                    client_secret=os.getenv("GOOGLE_CLIENT_SECRET")
                )
            ]
        ),
        session.init()
    ]
)

# Add SuperTokens middleware
app.add_middleware(get_middleware())

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse({"status": "healthy"})

# Include routers
from app.api.api_v1.api import api_router
app.include_router(api_router, prefix=os.getenv("API_V1_STR", "/api/v1"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
