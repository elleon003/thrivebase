# Baserow Table Structures

This document outlines the required fields for each table in the Baserow database.

## Accounts Table

Table Name: Accounts
Table ID Environment Variable: BASEROW_ACCOUNTS_TABLE_ID

Fields:
- id (Number, Auto-increment) - Primary key
- plaid_account_id (Text) - Unique identifier from Plaid
- plaid_item_id (Text) - Reference to the Plaid item
- name (Text) - Account name from institution
- official_name (Text, Optional) - Official account name
- type (Text) - Account type (checking, savings, etc.)
- subtype (Text, Optional) - Account subtype
- balance_current (Decimal Number) - Current balance
- balance_available (Decimal Number, Optional) - Available balance
- iso_currency_code (Text) - Currency code (e.g., USD)
- user_id (Text) - Reference to the user
- last_updated (Date Time) - Last balance update timestamp

## Transactions Table

Table Name: Transactions
Table ID Environment Variable: BASEROW_TRANSACTIONS_TABLE_ID

Fields:
- id (Number, Auto-increment) - Primary key
- user_id (Text) - Reference to the user
- account_id (Text) - Reference to the Plaid account
- amount (Decimal Number) - Transaction amount
- date (Date) - Transaction date
- description (Text) - Transaction description
- category (Text) - Transaction category
- created_at (Date Time, Auto) - Record creation timestamp

## Tokens Table

Table Name: Plaid Tokens
Table ID Environment Variable: BASEROW_TOKENS_TABLE_ID

Fields:
- id (Number, Auto-increment) - Primary key
- plaid_item_id (Text) - Unique identifier for Plaid connection
- encrypted_access_token (Text) - Encrypted Plaid access token
- user_id (Text) - Reference to the user
- institution_id (Text, Optional) - Plaid institution identifier
- institution_name (Text, Optional) - Institution name
- status (Text) - Token status (active, revoked, error)
- created_at (Date Time, Auto) - Record creation timestamp
- last_updated (Date Time) - Last status update timestamp

## Notes

1. Security Considerations:
   - The encrypted_access_token field stores Fernet-encrypted Plaid access tokens
   - No plaintext sensitive data should be stored
   - The encryption key is managed through environment variables

2. Relationships:
   - Accounts and Transactions are linked through account_id
   - Accounts and Tokens are linked through plaid_item_id
   - All tables include user_id for data isolation

3. Indexing Recommendations:
   - user_id should be indexed on all tables
   - plaid_item_id should be indexed on Accounts and Tokens tables
   - account_id should be indexed on Transactions table

4. Data Types:
   - Use appropriate precision for decimal numbers (balances and amounts)
   - Ensure date fields include timezone information
   - Text fields should have appropriate length limits

5. Setup Instructions:
   1. Create each table in Baserow
   2. Configure the fields as specified above
   3. Add the table IDs to your environment variables
   4. Test the connections using the API endpoints
