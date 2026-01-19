# LLM-Based Input Validator

A Python-based data validation script that uses an LLM (OpenAI GPT-4o-mini) to validate user profiles against high-level constraints.

[cite_start]This project strictly follows the requirement to use the LLM as the **sole validator** without external validation libraries (like regex or logic helpers)[cite: 4, 39, 40].

## Project Structure
- `validate_user.py`: Main script containing the LLM validation logic.
- `promptfooconfig.yaml`: Configuration for automated evaluations.
- `tests/`: JSON files used for testing specific edge cases.
- `.env`: API credentials (not included in repo).

## Prerequisites
- [cite_start]Python 3.10+ [cite: 125]
- Node.js (for running Promptfoo evals)

## Setup Instructions

1. **Clone the repository and enter the directory:**
   ```bash
   git clone <repo-url>
   cd llm-validator

2. **Create and activate a virtual environment:**
   ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

3. **Install Python dependencies:**
   ```bash
   pip install openai pydantic python-dotenv
   
4. **Set up Environment Variables: Rename .env.example to .env and add your OpenAI API key:**
   ```Plaintext
   OPENAI_API_KEY=sk-proj-...

## Usage
- Run the script by providing a JSON file path as an argument:
  ```bash
  python validate_user.py tests/valid.json

## Example Input (tests/valid.json):
   {
  "name": "Aarav Patel",
  "email": "aarav.patel@gmail.com",
  "age": 24,
  "country": "IN",
  "phone": "+919876543210"
  }

## Example Output:
   
   {
  "is_valid": true,
  "errors": [],
  "warnings": []
  }

## Running Evaluations
   This project uses Promptfoo to ensure the LLM strictly adheres to the schema and logic rules. The evaluation suite tests valid inputs, invalid inputs (errors), and edge cases (warnings).

1. **Initialize Promptfoo (if not installed):**
   ```bash
   npx promptfoo@latest init

2. **Run the Evaluation Suite:**
   ```bash
   npx promptfoo@latest eval

3. **View the Results: To see a visual matrix of the test results:**
   ```bash
   npx promptfoo@latest view

**Author**
   Name: Sudhanshu Dave
   Email: sudhanshu.22211610@viit.ac.in