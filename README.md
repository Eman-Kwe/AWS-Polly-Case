# 🎙️ AWS Polly Text-to-Speech Pipeline

> Automatically convert course text into MP3 audio using Amazon Polly, S3, and GitHub Actions — no servers required.

[![Beta Workflow](https://img.shields.io/badge/workflow-beta-blue?logo=github-actions)](/.github/workflows/on_pull_request.yml)
[![Prod Workflow](https://img.shields.io/badge/workflow-prod-green?logo=github-actions)](/.github/workflows/on_merge.yml)
[![AWS Polly](https://img.shields.io/badge/AWS-Polly%20%7C%20S3-FF9900?logo=amazon-aws)](https://aws.amazon.com/polly)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

---

## What This Project Does

This project builds a fully automated, serverless text-to-speech pipeline for **Pixel Learning Co.**, a digital-first education startup focused on accessibility.

You write text, commit it to GitHub, and the pipeline automatically converts it into a high-quality `.mp3` audio file using Amazon Polly and stores it in S3.

- Pull request → generates `polly-audio/beta.mp3`
- Merge to main → generates `polly-audio/prod.mp3`

---

## Project Structure

```
AWS-Polly-Case/
├── .github/
│   └── workflows/
│       ├── on_pull_request.yml    # Beta workflow — triggers on PR
│       └── on_merge.yml           # Prod workflow — triggers on merge
├── src/
│   └── advanced/
│       ├── lambda_handler.py      # Lambda function (Advanced level)
│       └── requirements.txt       # Lambda dependencies
├── .gitignore
├── LICENSE
├── README.md
├── speech.txt                     # Course text input
└── synthesize.py                  # Core Polly + S3 script
```

---

## Prerequisites

- AWS account (free tier is enough)
- GitHub account
- Python 3.11 or higher
- AWS CLI installed locally
- Basic Git knowledge

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Eman-Kwe/AWS-Polly-Case.git
cd AWS-Polly-Case
```

### 2. Create your S3 bucket

1. Go to [AWS S3 Console](https://s3.console.aws.amazon.com/s3)
2. Click **Create bucket**
3. Name it something unique, for example `pixel-learning-tts-yourname`
4. Choose your region and leave all defaults
5. Click **Create bucket**

### 3. Create an IAM user

1. Go to [IAM Console](https://console.aws.amazon.com/iam)
2. Click **Users** → **Create user**
3. Name it `github-actions-polly`
4. Attach these policies:
   - `AmazonPollyFullAccess`
   - `AmazonS3FullAccess`
5. Go to **Security credentials** → **Create access key**
6. Choose **Application running outside AWS**
7. Download the CSV file

### 4. Add GitHub Secrets

Go to your repo → **Settings** → **Secrets and variables** → **Actions** and add:

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | From your CSV file |
| `AWS_SECRET_ACCESS_KEY` | From your CSV file |
| `AWS_REGION` | Your region, e.g. `us-east-1` |
| `S3_BUCKET_NAME` | Your bucket name |

---

## How to Use

### Modify the course content

Open `speech.txt` and replace the text with your own content:

```
Welcome to Pixel Learning Co. This module covers accessible course design.
Audio versions of all lessons are generated automatically.
```

### Trigger the beta workflow

```bash
git checkout -b feature/your-branch-name
git add .
git commit -m "update course content"
git push origin feature/your-branch-name
```

Open a pull request on GitHub. The beta workflow runs automatically.

### Trigger the prod workflow

Merge the pull request. The prod workflow runs automatically and uploads the final audio to S3.

### Verify the audio files

```bash
aws s3 ls s3://your-bucket-name/polly-audio/
```

You should see:
```
polly-audio/beta.mp3
polly-audio/prod.mp3
```

---

## How the Scripts Work

### `synthesize.py`

Reads `speech.txt`, calls Amazon Polly's neural voice engine, saves the audio as an MP3, and uploads it to S3.

```python
# Key environment variables used
AWS_REGION        # AWS region for Polly client
S3_BUCKET_NAME    # Target S3 bucket
ENVIRONMENT       # beta or prod — controls S3 key path
```

### `on_pull_request.yml`

Runs on every pull request targeting `main`. Installs dependencies, configures AWS credentials from secrets, and runs `synthesize.py` with `ENVIRONMENT=beta`.

### `on_merge.yml`

Runs on every push to `main`. Same setup as the PR workflow but uses `ENVIRONMENT=prod` to upload the production audio file.

---

## Credential Security

| Practice | Why |
|---|---|
| Store keys in GitHub Secrets | Encrypted, never visible in logs |
| Dedicated IAM user | Easy to revoke if compromised |
| No hardcoded values | Keys committed to Git are considered compromised |
| Environment variables only | Injected at runtime, not stored in code |

---

## Troubleshooting

**Signature mismatch error**
Your `AWS_SECRET_ACCESS_KEY` was copied incorrectly. Go to GitHub Secrets, click the secret, and paste the value fresh from your CSV file. Then re-run the workflow.

**NoSuchBucket error**
The bucket name in `S3_BUCKET_NAME` does not match an existing bucket. Run `aws s3 ls` to confirm the exact name.

**Workflow does not trigger**
Check that your workflow files are inside `.github/workflows/` and not directly inside `.github/`.

**AccessDeniedException from Polly**
The IAM user is missing `AmazonPollyFullAccess`. Go to IAM and attach the policy to `github-actions-polly`.

---

## Roadmap

- [x] Foundational — Direct CI/CD with Polly and S3
- [ ] Advanced — Lambda functions with API Gateway endpoints
- [ ] Complex — Infrastructure-as-Code with Terraform

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: your change"`
4. Push and open a pull request

---

## License

MIT License. See [LICENSE](./LICENSE) for details.

---

*Built for Pixel Learning Co. — making course content accessible through automated audio generation.*
