No problem! You can set it up directly through **Azure Portal**:

**Step 1: Create Service Principal in Azure Portal**

1. Go to **Azure Portal** → Search for **App registrations**
2. Click **New registration**
3. Fill in:
   - Name: `github-actions-sp`
   - Supported account types: `Accounts in this organizational directory only`
4. Click **Register**

**Step 2: Get the credentials**

On the App registration page, copy:
- **Application (client) ID** 181e8dae-da33-47d7-9567-927106355443
- **Directory (tenant) ID** 04fcb0b9-fe98-44e90a8d2-d402-4a64-ae50-0876d6df5768

Then go to **Certificates & secrets** → **New client secret**:
- Click **New client secret**
- Copy the **Value** 4e90a8d2-d402-4a64-ae50-0876d6df5768

**Step 3: Grant permissions**

1. Go to **Subscriptions** (search in portal)
2. Select your subscription
3. Click **Access control (IAM)** → **Add role assignment**
4. Role: `Contributor`
5. Assign to: Search and select your app name (`github-actions-sp`)
6. Click **Review + assign**

**Step 4: Create the JSON for GitHub**

Create this JSON manually and add to GitHub Secrets:

```json
{
  "clientId": "paste-your-application-id-here",
  "clientSecret": "paste-your-client-secret-here",
  "subscriptionId": "paste-your-subscription-id",
  "tenantId": "paste-your-directory-id"
}
```

**To find your Subscription ID:**
- Go to **Subscriptions** in Azure Portal
- Copy the **Subscription ID**

**Step 5: Add to GitHub**

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `AZURE_CREDENTIALS`
4. Paste the JSON

**Step 6: Find your resource details** (in Azure Portal):

- **Resource Group**: Go to **Resource groups** → copy the name
- **Container App Name**: Go to **Container Apps** → copy the name
- **ACR Name**: Go to **Container registries** → copy the name

Update these in your YAML:
```yaml
env:
  REGISTRY: your-acr-name.azurecr.io
  IMAGE_NAME: your-image-name
  RESOURCE_GROUP: your-resource-group-name
  CONTAINER_APP_NAME: your-container-app-name
```

That's it! Now GitHub has the credentials it needs. 👍

Perfect! Your app is already created! I can see **github-actions-sp** is ready. Now let's get the credentials:

**Step 1: Copy these credentials from the screen:**

From the "Essentials" section, copy:
- **Application (client) ID**: `181e8dae-d3d3-47d7-b567-92710635543` ← Copy this
- **Directory (tenant) ID**: `04fcb0b9-fe98-436d-8221-2fca9757add9` ← Copy this

**Step 2: Create Client Secret**

1. On the left sidebar, click **Manage** → **Certificates & secrets**
2. Click **+ New client secret**
3. Description: `GitHub Actions`
4. Expires: `12 months`
5. Click **Add**
6. **Immediately copy the Value** (the secret) ← This is important, you can only see it once!

**Step 3: Get Subscription ID**

1. Go to **Subscriptions** (search in portal)
2. Copy your **Subscription ID**

**Step 4: Create the JSON for GitHub**

Combine all values into this JSON:

```json
{
  "clientId": "181e8dae-d3d3-47d7-b567-92710635543",
  "clientSecret": "paste-the-secret-value-here",
  "subscriptionId": "paste-your-subscription-id-here",
  "tenantId": "04fcb0b9-fe98-436d-8221-2fca9757add9"
}
```

**Step 5: Add to GitHub**

1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `AZURE_CREDENTIALS`
4. Paste the JSON

Done! 🎉

Almost! You have the client secret created, but you need to **see the actual Value** to copy it.

The Value shown as `rAq***...` is masked. You need to click the **copy icon** next to it to get the full secret:

1. Click the **copy icon** (📋) next to the Value `rAq***...`
2. Paste it somewhere safe temporarily

Now you have:
- ✅ **clientId**: `181e8dae-d3d3-47d7-b567-92710635543`
- ✅ **clientSecret**: (the value you just copied)
- ✅ **tenantId**: `04fcb0b9-fe98-436d-8221-2fca9757add9`
- ⏳ **subscriptionId**: Still need this

**Get Subscription ID:**

1. Search for **"Subscriptions"** in Azure Portal
2. Click on your subscription
3. Copy the **Subscription ID**

**Then create the JSON:**

```json
{
  "clientId": "181e8dae-d3d3-47d7-b567-92710635543",
  "clientSecret": "paste-the-copied-secret-here",
  "subscriptionId": "paste-your-subscription-id-here",
  "tenantId": "04fcb0b9-fe98-436d-8221-2fca9757add9"
}
```

**Finally add to GitHub:**
1. GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Name: `AZURE_CREDENTIALS`
4. Paste the JSON

Then you're done! 🎉

I see - you're in the **Secrets and variables** page but don't see any secrets listed. You need to scroll down or look for the **Repository secrets** section.

**To add AZURE_CREDENTIALS:**

1. On this page, scroll down to find **"Repository secrets"** section
2. Click **"New repository secret"** button
3. Fill in:
   - **Name**: `AZURE_CREDENTIALS`
   - **Secret**: Paste your JSON:
   ```json
   {
     "clientId": "181e8dae-da33-47d7-9567-927106355443",
     "clientSecret": "your-actual-secret-value",
     "subscriptionId": "4504ddf2-f1c6-4eec-970d-f3eb1ea27330",
     "tenantId": "04fcb0b9-fe98-436d-8221-2fca9757add9"
   }
   ```
4. Click **Add secret**

**Important:** Make sure:
- ✅ The JSON is valid (no extra spaces/line breaks)
- ✅ All 4 fields are included
- ✅ Secret value is the actual client secret (not masked)

Once added, trigger your workflow again and it should work!

**Give IAM role FIRST** before pushing to GitHub.

Here's the order:

**Step 1: Assign IAM role to service principal** (do this NOW)

1. Go to **Azure Portal** → **Subscriptions**
2. Select your subscription
3. Click **Access control (IAM)** → **+ Add** → **Add role assignment**
4. **Role tab**: Select `Contributor` from **Privileged administrator roles**
5. Click **Next**
6. **Members tab**: 
   - Click **+ Select members**
   - Search for: `github-actions-sp`
   - Select it
   - Click **Review + assign**

**Step 2: Then push code to GitHub**

Once IAM role is assigned, push your code and trigger the workflow.

**Why this order?**
- The service principal needs permissions BEFORE it tries to authenticate
- If you push first, the workflow will fail because the app has no access to your Azure resources

So: **IAM role → GitHub push → Workflow runs successfully** ✅

Let me know once you've assigned the role!