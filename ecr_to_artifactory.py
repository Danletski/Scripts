import boto3
import docker

# AWS ECR configuration
aws_region = 'us-east-1'
aws_profile = 'aws-profile'
ecr_registry_id = 'ecr-registry'

# JFrog Artifactory configuration
artifactory_url = 'URL
artifactory_repo = 'REPO'

#Docker client
docker_client = docker.from_env()

#ECR client
client = boto3.client('ecr')
response = client.describe_repositories()
repositories = response['repositories']

# List to track skipped repositories
skipped_repos = []

for repo in repositories:
    repo_name = repo['repositoryName']
    try:
        image_tag = 'TAG'
        # falback_tag = 'latest'
        image_uri = f'{ecr_registry_id}/{repo_name}:{image_tag}'
        docker_client.images.pull(image_uri)
        print(image_uri)
        
        # Tag the image for JFrog Artifactory
        artifactory_image_uri = f'{artifactory_url}/{artifactory_repo}/{repo_name}:{image_tag}'
        docker_client.images.get(image_uri).tag(artifactory_image_uri)
        print(f'{image_uri} Tagged as {artifactory_image_uri}')
        
        # Push the image to JFrog Artifactory
        docker_client.images.push(artifactory_image_uri)
        print(f'Pushed image {repo_name}:{image_tag} to artifactory')

    except docker.errors.NotFound:
        # Image with tag 'x' not found, skip to the next repository
        skipped_repos.append(repo_name)
        continue

# Print the list of skipped repositories
print("Skipped Repositories:")
for skipped_repo in skipped_repos:
    print(skipped_repo)
