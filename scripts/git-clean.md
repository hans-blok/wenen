# Create orphan branch (without history)
git checkout --orphan version-0.1

# Add all files
git add .

# Commit everything
git commit -m "version 0.1"

# Tag the commit
git tag -a v0.1 -m "Release version 0.1"

# Replace main branch
git branch -D main
git branch -m main

# Force push
git push origin main --force
git push origin v0.1