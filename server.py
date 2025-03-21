from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# internal imports
import dbConnection  # Import database setup
from user_controllers import auth  # Import auth routes
from provider_controllers import telemetry, vm_crud
from cli_controllers import provider_get_requests, vms_get_request ,vms_post_request

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt with app

dbConnection.setupConnection()

@app.route('/')
def home():
    return "Hello, Welcome to the management server",200

# User Routes
app.add_url_rule('/register', 'register', auth.register, methods=['POST'])
app.add_url_rule('/login', 'login', auth.login, methods=['POST'])

# vm operations (provider)
app.add_url_rule('/requestvm','requesting-vm-creation',vm_crud.vm_creation,methods=['POST'])
app.add_url_rule('/vm/activate','activating-inactive-vm',vm_crud.activate_vm,methods=['POST'])
app.add_url_rule('/vm/deactivate','deactivating-active-vm',vm_crud.deactivate_vm,methods=['POST'])
# app.add_url_rule('/vm/delete','deleting-inactive-vm',vm_crud.delete_vm,methods=['POST'])

# provider server telemetry routes 
app.add_url_rule('/heartbeat','provider-heartbeat',telemetry.heartbeat,methods=['POST'])
app.add_url_rule('/<provider_id>/<path:subpath>', 'dynamic_proxy', telemetry.vm_telemetry, methods=['GET', 'POST', 'PUT', 'DELETE'])
# <path> (without subpath) captures only the first segzment after /vm/.

# CLI routes
app.add_url_rule('/cli/vms/<path:subpath>','cli_vms',vms_get_request.vmStatus,methods=['GET'])
app.add_url_rule('/cli/vms/launch','cli_launch_vm',vms_post_request.launchVm,methods=['POST'])
app.add_url_rule('/cli/providers/<path:subpath>','cli_providers',provider_get_requests.providers,methods=['GET'])

if __name__ == '__main__':
    try:
        app.run(debug=True,port=5000)
    except Exception as e:
        print(f"Error: {str(e)}")
