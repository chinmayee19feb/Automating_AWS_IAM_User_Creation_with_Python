# AWS IAM User Automation (Python)

Automates IAM user creation with secure passwords and S3 read-only access.

## Challenges Faced
- Understanding boto3 error handling for existing users
- Ensuring password complexity requirements were met
- Managing file permissions for credentials security
- Handling CSV file encoding and formatting

## Usage
1. Configure AWS CLI: `aws configure`
2. Create virtual env: `python3 -m venv .venv`
3. Activate env: `source .venv/bin/activate`
4. Install dependencies: `pip install boto3`
5. Run: `python create_iam_users.py`
6. Cleanup: `python cleanup_iam_users.py`

## File Format
**employees.csv:**
```csv
first_name,last_name,department
john,smith,engineering


## Improvement Suggestion
If I had more time, I would implement automated password rotation using AWS Secrets Manager. This would:
- Automatically rotate passwords every 90 days for enhanced security
- Store credentials securely in AWS Secrets Manager instead of local files
- Reduce manual maintenance and eliminate the risk of stale credentials
- Provide audit trail of all password changes