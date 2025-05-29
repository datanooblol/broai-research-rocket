# This is a prototype-4

## Current:  
- update the project structure: backend, frontend
- update environment variables of each stack  

## Next:
- update stack from frontend streamlit to nextjs for better ux
- add saving to pdf functionality

## Tips:
```bash
# WARNING: This will delete your local changes!
git fetch origin
git reset --hard origin/main
```

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

```text
AWS_ACCESS_KEY_ID=access_key_id
AWS_SECRET_ACCESS_KEY=secret_key
AWS_SESSION_TOKEN=
AWS_DEFAULT_REGION=ap-southeast-1 # your choice
AWS_BEDROCK_REGION=us-west-2
```

```cmd
# if fetching huggingface failed due to low diskspace during start FastAPI
rm -rf ~/.cache/huggingface
```