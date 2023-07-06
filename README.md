# POC Release Distribution Quality Gate
This is a poc to try out the possibilities of Azure functions and event grid. I followed this tutorial: https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-decorators to first create a HTTP triggered application and then changed it to an EventGrid trigger.

## Running it locally

* Setup the following depedencies:
    * An Azure account with an active subscription.
    * The Azure Functions Core Tools, version 4.0.4785 or a later version.
    * Python versions that are supported by Azure Functions. For more information, see How to install Python.
    * Visual Studio Code on one of the supported platforms.
    * The Python extension for Visual Studio Code.
    * The Azure Functions extension for Visual Studio Code, version 1.8.1 or later.
    * The Azurite V3 extension local storage emulator. While you can also use an actual Azure storage account, this article assumes you're using the Azurite emulator.
* Restart your VS Code
* Run `func init` in this directory to initialize the local configuration
* Make sure your local.settings.json looks like this:
    ```json
    {
    "IsEncrypted": false,
        "Values": {
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "AzureWebJobsStorage": "UseDevelopmentStorage=true",
            "AzureWebJobsFeatureFlags": "EnableWorkerIndexing"
        }
    }
    ```
* Use the `Azurite: Start` action in your VS Code (ctrl+p -> Azurite: Start)
* In the Azure tab in VS Code, right click "ValidateRelease" in "Workspace" and click "Execute Function now".

This should work and you should see the body of your event in the logs. If you do any changes to the code, they should reflect in the behavior of sending an event. Try it out!

## Setup on Azure

* Choose or create a subscription
* In this subscription:
    * Create an EventGrid Custom topic called "releases"
    * Setup the function:
        * Create a cloud function app called "poc-<your-name>-rdqc". This will bundle all the cloud functions for quality gate, reciding in this repository. (globally unique)
            * Do this with the VS Code extension! Doing it through the Azure Portal will cause issues like the storage account not being created.
            * Choose the advanced option to create a function app in VSCode. The other one doesn't allow you to configure the subscription where you're going to deploy this.
            * Setup the python 3.10 runtime stack in West Europe
        * In the Azure Portal, link the deployment to this repo in the deployment center of the function.
        * Set AzureWebJobsFeatureFlags in the function configuration on Azure to EnableWorkerIndexing (necessary since python configures functions inline with annotations).
    * Setup the integration between event grid and the function
        * Create an event grid subscription on the created topic, calling it "release-validations"
            * Use Cloud Event Schema V1.0
            * Topic Type: Event Grid Topic
            * Endpoint: ValidateRelease
    * That's it!

## Testing on Azure
After the Azure setup, you can now try out publishing events to the topic and see the results in the logs.$

* Open the Azure Cloud Shell
* Execute these commands:
```bash
export event='{
    "specversion" : "1.0",
    "type" : "com.example.someevent",
    "source" : "/mycontext",
    "subject": null,
    "id" : "C234-1234-1234",
    "time" : "2018-04-05T17:31:00Z",
    "comexampleextension1" : "value",
    "comexampleothervalue" : 5,
    "datacontenttype" : "application/json",
    "data" : {
        "appinfoA" : "abc",
        "appinfoB" : 123,
        "appinfoC" : true
    }
}'
resourceGroup=<your-subscription>
topicname=releases
endpoint=$(az eventgrid topic show --name $topicname -g $resourceGroup --query "endpoint" --output tsv)
key=$(az eventgrid topic key list --name $topicname -g $resourceGroup --query "key1" --output tsv)
curl -v -X POST -H "aeg-sas-key: $key" -H "content-type:application/cloudevents+json" -d "$event" $endpoint
```
* In Azure CLI you should see the call returning 200 OK.
* In the logs of the function, you should see something like this:
```
2023-07-06T14:40:23Z   [Information]   Executing 'Functions.ValidateRelease' (Reason='EventGrid trigger fired at 2023-07-06T14:40:22.5587945+00:00', Id=12040c9e-08c9-4378-8844-49c922a65869)
2023-07-06T14:40:23Z   [Verbose]   Sending invocation id: '12040c9e-08c9-4378-8844-49c922a65869
2023-07-06T14:40:23Z   [Verbose]   Posting invocation id:12040c9e-08c9-4378-8844-49c922a65869 on workerId:53ed56c1-8f4a-4bf7-9fe9-e536a6e44b79
2023-07-06T14:40:23Z   [Information]   Python EventGrid trigger processed an event
2023-07-06T14:40:23Z   [Information]   {'appinfoA': 'abc', 'appinfoB': 123, 'appinfoC': True}
2023-07-06T14:40:23Z   [Information]   Executed 'Functions.ValidateRelease' (Succeeded, Id=12040c9e-08c9-4378-8844-49c922a65869, Duration=50ms)
```
* It could take a couple of seconds until the logs show up.

If all went well, you're now master of your own event grid triggered python function!
