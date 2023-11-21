# Install DVC
sudo wget \
       https://dvc.org/deb/dvc.list \
       -O /etc/apt/sources.list.d/dvc.list
wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor > packages.iterative.gpg
sudo install -o root -g root -m 644 packages.iterative.gpg /etc/apt/trusted.gpg.d/
rm -f packages.iterative.gpg
sudo apt update
sudo apt install dvc

# Configure DVC
TOKEN=$(curl -X PUT 'http://169.254.169.254/latest/api/token' -H 'X-aws-ec2-metadata-token-ttl-seconds: 21600')
response=$(curl -H 'X-aws-ec2-metadata-token: $TOKEN' -s http://169.254.169.254/latest/meta-data/iam/security-credentials/SkillsTracker-DVCReadS3)
dvc remote modify --local s3 access_key_id '$(echo '$response' | jq -r '.AccessKeyId')'
dvc remote modify --local s3 secret_access_key '$(echo '$response' | jq -r '.SecretAccessKey')'
dvc remote modify --local s3 session_token '$(echo '$response' | jq -r '.Token')'
dvc pull --recursive
