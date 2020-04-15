from flask import Flask
from flask import render_template, redirect, request, url_for

from controller.Start_controller import StartController
from controller.MainController import MainController

app = Flask(__name__)
start_controller = StartController()
main_controller = MainController()

@app.route('/')
def start():
    serial_ports = start_controller.get_serial_ports()
    baudrates = start_controller.get_baudrates()
    return render_template("start.html", serial_ports=serial_ports, baudrates=baudrates)

@app.route('/', methods=['POST'])
def start_post():
    serial_port = request.form.get('port')
    baudrate = request.form.get('baudrate')
    if serial_port and baudrate:
        return redirect(url_for('index', serial_port=serial_port, baudrate=baudrate))
    # TODO: else show the warning thingy


@app.route('/index', methods=['GET'])
def index():
    serial_port = request.args.get('serial_port')
    baudrate = request.args.get('baudrate')
    main_controller.start_test(serial_port, baudrate)
    return render_template("index.html")



if __name__ == '__main__':
    app.run()
