# Build and deploy the ATM UI

## What the workflow does

`.github/workflows/publish-image.yml` builds the image on a GitHub-hosted
runner, publishes it to GHCR on pushes, then deploys that exact image to
Minikube from a self-hosted runner in WSL. Pull requests only build and do not
deploy. GHCR publishing uses the repository's `GITHUB_TOKEN`.

## Configure the WSL runner

1. In the GitHub repository, open **Settings → Actions → Runners → New
   self-hosted runner**. Choose Linux and follow GitHub's displayed setup
   instructions inside WSL.
2. Add the custom runner label `wsl-minikube` when configuring the runner (or
   add it later under the runner's settings). The workflow targets
   `self-hosted`, `linux`, and `wsl-minikube`.
3. Ensure `kubectl` is installed in WSL and its kubeconfig points to your
   Windows-hosted Minikube cluster. From the same WSL user that runs the
   Actions runner, verify:

   ```bash
   kubectl config current-context
   kubectl get nodes
   ```

   Both commands must work before the workflow can deploy. Minikube's API
   address and credentials must be reachable from WSL; a Windows kubeconfig
   that only refers to `localhost` or Windows-only certificate paths may need
   to be configured for WSL access. Do not expose the Kubernetes API publicly.
4. Keep the runner process running. For automatic deployment, configure it as
   a service using the instructions GitHub provides for the runner.

## Configure Minikube to pull the image

The GHCR package is private by default. Create a GitHub Personal Access Token
(classic) with `read:packages` permission. From PowerShell, create a pull
secret in the same Minikube cluster. Replace `GITHUB_USERNAME` and enter the
token when prompted:

```powershell
$env:GHCR_PAT = Read-Host "GHCR read:packages token"
kubectl create secret docker-registry ghcr-secret `
  --docker-server=ghcr.io `
  --docker-username=GITHUB_USERNAME `
  --docker-password="$env:GHCR_PAT" `
  --docker-email=unused@example.com
Remove-Item Env:GHCR_PAT
```

If `ghcr-secret` already exists, delete it before recreating it. The
`k8s/atm.yaml` manifest references this secret and the workflow replaces its
image placeholder with the newly published commit image before applying it.

## Deploy

Start Minikube on Windows, push this project to the repository's `main` or
`master` branch, and check **Actions** in GitHub. Once the image publish job
finishes, the WSL runner applies the Kubernetes manifest and waits for the
deployment rollout.

The UI is a frontend-only demo: its balance and transactions are kept in
browser memory and reset on refresh.
