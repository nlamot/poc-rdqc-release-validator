# POC RDQC Release Validator
This is a poc to try out the possibilities of Azure functions and event grid. I followed this tutorial: https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-decorators to first create a HTTP triggered application and then changed it to an EventGrid trigger.

More information to be added.

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