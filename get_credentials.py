import boto3
from botocore.exceptions import NoCredentialsError

def main():
    try:
        session = boto3.Session()
        credentials = session.get_credentials()

        if credentials is None:
            raise NoCredentialsError()

        # Load actual values (resolve from temporary/refreshable creds)
        credentials = credentials.get_frozen_credentials()

        env_vars = {
            "AWS_ACCESS_KEY_ID": credentials.access_key,
            "AWS_SECRET_ACCESS_KEY": credentials.secret_key,
            "AWS_SESSION_TOKEN": credentials.token,  # Optional: if using temporary credentials
            "AWS_DEFAULT_REGION": session.region_name # fallback region,
            "AWS_BEDROCK_REGION": "us-west-2"  # fallback region
        }

        with open(".env", "w") as f:
            for key, value in env_vars.items():
                if value:  # Don't write empty values
                    f.write(f"{key}={value}\n")

        print(".env file created successfully.")
    except NoCredentialsError:
        print("No AWS credentials found. Please configure your AWS environment.")

if __name__ == '__main__':
    main()
