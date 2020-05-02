from flask import Flask
from flask import render_template, redirect, request, url_for

from controller.StartController import StartController
from controller.MainController import MainController

app = Flask(__name__)
start_controller = StartController()
main_controller = MainController()


@app.route('/')
def start():
    serial_ports = start_controller.get_serial_ports()
    baudrates = start_controller.get_baudrates()
    return render_template("start.html", serial_ports=serial_ports, baudrates=baudrates)


@app.route('/start_test', methods=['POST'])
def start_test():
    serial_port = request.form.get('port')
    baudrate = request.form.get('baudrate')
    if serial_port and baudrate:
        main_controller.start_test(serial_port, baudrate)
        # TODO: else show the warning pop-up and do not redirect   ---flash in Flask
        return redirect(url_for('index'))


@app.route('/settings', methods=['POST'])
def settings():
    heartbeat_period = int(request.form.get('heartbeat_period'))
    ecc_period = int(request.form.get('ecc_period'))
    if heartbeat_period and ecc_period:
        main_controller.set_heartbeat_period(heartbeat_period)
        main_controller.set_ecc_period(ecc_period)
        return redirect(url_for('index'))
    # TODO: else show the warning pop-up and do not redirect   ---flash in Flask


@app.route('/index')
def index():
    return render_template("index.html", data_packets= main_controller.get_all_data(),
                           heartbeat_periods=main_controller.get_heartbeat_periods(),
                           ecc_check_periods=main_controller.get_ecc_check_periods()
                           )


@app.route('/reset', methods=['GET'])
def reset():
    main_controller.send_rest_request()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
