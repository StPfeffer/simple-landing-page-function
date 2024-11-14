import azure.functions as func
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route='http_trigger')
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON data", status_code=400)

    success = False

    if data:
        email = data['toMail']
        message = data['message']

        if not email or not message:
            return func.HttpResponse("Missing 'toMail' or 'message' in request", status_code=400)

        msg = Mail(
            from_email='mpfeffer@minha.fag.edu.br',
            to_emails=email,
            subject='Km Fácil',
            html_content=message
        )

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sg.send(msg)
            success = True
        except Exception as e:
            logging.error(f"Failed to send email: {str(e)}")
            success = False

    if success:
        return func.HttpResponse(f'Email sent to {email}', status_code = 200)
    else:
        return func.HttpResponse('Something went wrong', status_code=500)
