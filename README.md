# ThriveBase - Modern Budgeting Application

ThriveBase is a modern budgeting application designed for freelancers, gig workers, and anyone with variable income. It provides flexible budgeting tools that adapt to your unique pay schedule.

## Features

- 🔐 Secure authentication with email/password and Google sign-in
- 🏦 Multi-bank account integration via Plaid
  - Connect multiple bank accounts
  - Real-time balance tracking
  - Secure token storage with encryption
  - Institution information tracking
- 📊 Transaction tracking and categorization
- 💰 Variable income handling
- 📱 Responsive design for all devices
- ♿ Accessibility-first approach

## Tech Stack

### Frontend
- Vue 3 with Composition API
- Vue Router for navigation
- Pinia for state management
- Vite for development and building
- Modern CSS with custom properties

### Backend
- FastAPI for the REST API
- SuperTokens for authentication
- Plaid for bank integration
- Baserow for data storage
- Fernet symmetric encryption for sensitive data

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python 3.8+
- Poetry (Python dependency management)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/thrivebase.git
cd thrivebase
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
cd backend
poetry install
```

4. Create environment files:
```bash
cp .env.example .env
```

5. Generate encryption key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

6. Set up your environment variables in `.env`:
```env
# FastAPI Settings
API_V1_STR=/api/v1
PROJECT_NAME=ThriveBase
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Plaid Settings
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
PLAID_ENV=sandbox

# Supertokens Settings
SUPERTOKENS_CONNECTION_URI=your_supertokens_connection_uri
SUPERTOKENS_API_KEY=your_supertokens_api_key
SUPERTOKENS_APP_NAME=ThriveBase
SUPERTOKENS_API_DOMAIN=http://localhost:8000
SUPERTOKENS_WEBSITE_DOMAIN=http://localhost:5173

# Baserow Settings
BASEROW_API_TOKEN=your_baserow_token
BASEROW_API_URL=your_baserow_url
BASEROW_TRANSACTIONS_TABLE_ID=your_transactions_table_id
BASEROW_ACCOUNTS_TABLE_ID=your_accounts_table_id
BASEROW_TOKENS_TABLE_ID=your_tokens_table_id

# Security Settings
ENCRYPTION_KEY=your_generated_encryption_key
```

### Development

1. Start the frontend development server:
```bash
npm run dev
```

2. Start the backend server:
```bash
cd backend
poetry run uvicorn app.main:app --reload
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
thrivebase/
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── config/
│   │   ├── router/
│   │   ├── views/
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── api_v1/
│   │   │       └── endpoints/
│   │   │           ├── baserow.py
│   │   │           └── plaid.py
│   │   ├── core/
│   │   │   └── security.py
│   │   ├── models/
│   │   │   ├── account.py
│   │   │   └── token.py
│   │   ├── schemas/
│   │   ├── services/
│   │   │   └── token_service.py
│   │   └── main.py
│   └── pyproject.toml
└── README.md
```

## Development Guidelines

### Code Style

- Follow Vue.js Style Guide
- Use ESLint and Prettier for code formatting
- Write meaningful commit messages
- Document complex functions and components

### Git Workflow

1. Create a new branch for each feature/fix
2. Write descriptive commit messages
3. Submit pull requests for review
4. Squash commits before merging

### Testing

Run the test suites:

```bash
# Frontend tests
npm run test:unit

# Backend tests
cd backend
poetry run pytest
```

## Deployment

1. Build the frontend:
```bash
npm run build
```

2. Start the production server:
```bash
cd backend
poetry run uvicorn app.main:app
```

## Security Considerations

### Token Storage
- All Plaid access tokens are encrypted using Fernet symmetric encryption
- Encryption keys are managed through environment variables
- No plaintext sensitive data is stored in the database
- Token status tracking for security auditing
- Automatic token revocation on account disconnection

### Multi-Bank Support
- Secure storage of multiple bank connections
- Institution-level information tracking
- Real-time balance updates
- Proper cleanup of sensitive data on disconnection

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Plaid](https://plaid.com/) for banking integration
- [SuperTokens](https://supertokens.com/) for authentication
- [Baserow](https://baserow.io/) for database management
- [cryptography](https://cryptography.io/) for secure token encryption
