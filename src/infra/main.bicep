param location string = resourceGroup().location
param keyVaultName string = 'amlwsmlokeyvault7251ed5b'
 
@description('Reference an existing Key Vault')
resource kv 'Microsoft.KeyVault/vaults@2023-02-01' existing = {
  name: keyVaultName
}
 
@description('Create an App Service Plan with a Basic SKU')
resource exampleAppServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: 'mlflow-ASP'
  location: location
  kind: 'Linux'
  properties: {
    reserved: true
  }
  sku: {
    tier: 'Basic'
    name: 'B1'
  }
}
 
@description('Create the App Service with a system-assigned identity')
resource exampleAppService 'Microsoft.Web/sites@2022-09-01' = {
  name: 'mlops-skaroti-appservice' // must be globally unique
  location: location
  kind: 'linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: exampleAppServicePlan.id
    reserved: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
    }
  }
}
 
@description('Configure the App Service with the Key Vault secrets')
resource exampleAppServiceConfig 'Microsoft.Web/sites/config@2022-09-01' = {
  name: 'web'
  parent: exampleAppService
  properties: {
    appSettings: [
      {
        name: 'API_KEY'
        value: '@Microsoft.KeyVault(SecretUri=https://${kv.name}.vault.azure.net/secrets/apiKey/)'
      }
      {
        name: 'AZURE_ML_ENDPOINT_URL'
        value: '@Microsoft.KeyVault(SecretUri=https://${kv.name}.vault.azure.net/secrets/endpointUrl/)'
      }
      {
        name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
        value: '1'
      }
    ]
  }
}
 
@description('This is the built-in Key Vault Secrets User role. See https://docs.microsoft.com/azure/role-based-access-control/built-in-roles')
resource keyVaultSecretsUser 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '4633458b-17de-408a-b874-0445c86b69e6'
}
 
@description('Assign the Key Vault Secrets User role to the App Service')
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(kv.id, exampleAppService.id)
  properties: {
    principalId: exampleAppService.identity.principalId
    roleDefinitionId: keyVaultSecretsUser.id
    principalType: 'ServicePrincipal'
  }
  scope: kv
}
