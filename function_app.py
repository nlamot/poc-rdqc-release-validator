import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="ValidateRelease")
@app.event_grid_trigger(arg_name="azeventgrid")
def ValidateRelease(azeventgrid: func.EventGridEvent):
    logging.info('Python EventGrid trigger processed an event')
    logging.info(azeventgrid.get_json())
    logging.info("Zalmtoastje")
