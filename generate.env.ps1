# generate-env.ps1

param (
    [string]$Profile = "default"
)

# Retrieve AWS credentials and region from the specified profile
$accessKey = aws configure get aws_access_key_id --profile $Profile
$secretKey = aws configure get aws_secret_access_key --profile $Profile
$region    = aws configure get region --profile $Profile
$sessionToken = aws configure get aws_session_token --profile $Profile  # Optional
$bedrockregion = "us-west-2"

# Create .env file content
$envContent = @"
AWS_ACCESS_KEY_ID=$accessKey
AWS_SECRET_ACCESS_KEY=$secretKey
AWS_SESSION_TOKEN=$sessionToken
AWS_DEFAULT_REGION=$region
AWS_BEDROCK_REGION=$bedrockregion
"@

# Write to .env file
$envContent | Out-File -Encoding ascii -FilePath ".env"
Write-Host ".env file created successfully for profile '$Profile'"